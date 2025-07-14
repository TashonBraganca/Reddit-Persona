import os
import sys
import re
from dotenv import load_dotenv

# Import modules from the same project structure
from reddit_scraper import init_reddit_api, get_user_content
from persona_generator import generate_persona
from utils import save_persona_to_file

def get_username_from_url(url: str) -> str | None:
    """
    Extracts the Reddit username from a given user profile URL.

    Args:
        url (str): The Reddit user profile URL.

    Returns:
        str | None: The extracted username or None if not found/invalid URL.
    """
    match = re.search(r"reddit\.com/user/([^/]+)", url)
    if match:
        return match.group(1)
    return None

def main():
    """
    Main function to orchestrate the Reddit user persona generation process.
    """
    # 1. Load environment variables
    load_dotenv()
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Check if all required environment variables are set
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, OPENAI_API_KEY]):
        print("Error: Missing one or more environment variables.")
        print("Please ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, and OPENAI_API_KEY are set in your .env file.")
        sys.exit(1)

    # 2. Parse command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python main.py <reddit_user_profile_url>")
        print("Example: python main.py https://www.reddit.com/user/kojied/")
        sys.exit(1)

    user_url = sys.argv[1]
    username = get_username_from_url(user_url)

    if not username:
        print(f"Error: Invalid Reddit user profile URL format: {user_url}")
        print("Please provide a URL like 'https://www.reddit.com/user/username/'")
        sys.exit(1)

    print(f"Starting persona generation for Reddit user: u/{username}")

    try:
        # 3. Initialize Reddit API
        reddit = init_reddit_api(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT)
        if not reddit:
            print("Failed to initialize Reddit API. Exiting.")
            sys.exit(1)

        # 4. Fetch user comments and posts
        comments, posts = get_user_content(reddit, username, limit=200) # Fetch more content for better persona

        if not comments and not posts:
            print(f"No public comments or posts found for u/{username}. Cannot generate persona.")
            sys.exit(0)

        # 5. Prepare content for LLM
        # Combine and preprocess text, ensuring URLs are kept for citations
        all_user_content = []
        for comment in comments:
            # Preprocessing here is minimal to retain original text for LLM context
            all_user_content.append({"type": "comment", "text": comment["text"], "url": comment["url"]})
        for post in posts:
            # Use selftext if available, otherwise title
            text_content = post["text"] if post["text"] else post["title"]
            all_user_content.append({"type": "post", "text": text_content, "url": post["url"], "title": post["title"]})

        # 6. Generate the user persona
        print("Generating user persona using OpenAI API...")
        persona_content = generate_persona(OPENAI_API_KEY, all_user_content, username)
        
        if persona_content:
            # 7. Save the generated persona to a text file
            save_persona_to_file(username, persona_content)
            print(f"\nPersona generation complete for u/{username}.")
        else:
            print(f"Persona generation failed or returned empty for u/{username}.")

    except Exception as e:
        print(f"\nAn unhandled error occurred during the process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
