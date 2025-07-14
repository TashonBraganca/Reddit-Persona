import praw
from typing import List, Dict, Tuple

def init_reddit_api(client_id: str, client_secret: str, user_agent: str) -> praw.Reddit:
    """
    Initializes and returns a praw.Reddit instance for interacting with the Reddit API.

    Args:
        client_id (str): Your Reddit API client ID.
        client_secret (str): Your Reddit API client secret.
        user_agent (str): A unique string identifying your application (e.g., "UserPersonaGenerator/1.0").

    Returns:
        praw.Reddit: An initialized PRAW Reddit instance.

    Raises:
        praw.exceptions.ClientException: If PRAW initialization fails due to invalid credentials.
        Exception: For other unexpected errors during initialization.
    """
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        # Test connection by trying to fetch a user (this doesn't require auth for public data)
        # reddit.user.me() # This would require user login, which is not needed for public scraping
        print("Reddit API initialized successfully.")
        return reddit
    except praw.exceptions.ClientException as e:
        print(f"Error initializing Reddit API (PRAW Client Exception): {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during Reddit API initialization: {e}")
        raise

def get_user_content(reddit: praw.Reddit, username: str, limit: int = 100) -> Tuple[List[Dict], List[Dict]]:
    """
    Fetches a Reddit user's top comments and submissions (posts).

    Args:
        reddit (praw.Reddit): An initialized PRAW Reddit instance.
        username (str): The Reddit username to scrape.
        limit (int): The maximum number of top comments and posts to fetch.

    Returns:
        Tuple[List[Dict], List[Dict]]: A tuple containing two lists:
            - comments (List[Dict]): List of dictionaries, each representing a comment.
              Format: {"type": "comment", "text": comment_body, "url": permalink, "score": score}
            - posts (List[Dict]): List of dictionaries, each representing a post.
              Format: {"type": "post", "title": post_title, "text": post_selftext, "url": permalink, "score": score}

    Raises:
        praw.exceptions.NotFound: If the user does not exist.
        praw.exceptions.RedditorBlocked: If the redditor has blocked your application.
        praw.exceptions.ClientException: For other PRAW-related client errors.
        Exception: For any other unexpected errors during content fetching.
    """
    comments = []
    posts = []

    try:
        user = reddit.redditor(username)

        print(f"Fetching top {limit} comments for u/{username}...")
        for comment in user.comments.top(limit=limit):
            comments.append({
                "type": "comment",
                "text": comment.body,
                "url": f"https://reddit.com{comment.permalink}", # Full URL
                "score": comment.score
            })
            # Add a small delay to respect rate limits if fetching many items
            # time.sleep(0.1)

        print(f"Fetching top {limit} posts for u/{username}...")
        for submission in user.submissions.top(limit=limit):
            posts.append({
                "type": "post",
                "title": submission.title,
                "text": submission.selftext, # selftext can be empty for link posts
                "url": f"https://reddit.com{submission.permalink}", # Full URL
                "score": submission.score
            })
            # Add a small delay to respect rate limits if fetching many items
            # time.sleep(0.1)

        print(f"Fetched {len(comments)} comments and {len(posts)} posts for u/{username}.")
        return comments, posts

    except praw.exceptions.ClientException as e:
        print(f"Error fetching content (PRAW Client Exception): {e}")
        return [], []
    except Exception as e:
        print(f"An unexpected error occurred while fetching Reddit content: {e}")
        return [], []

if __name__ == "__main__":
    # This block is for testing purposes only.
    # Replace with your actual (or dummy) credentials for local testing.
    # For a real run, these would come from environment variables.
    DUMMY_CLIENT_ID = "dummy_client_id"
    DUMMY_CLIENT_SECRET = "dummy_client_secret"
    DUMMY_USER_AGENT = "LocalTestScript/1.0"

    print("--- Testing reddit_scraper.py ---")
    try:
        # This will likely fail without real credentials, but demonstrates the flow
        reddit_instance = init_reddit_api(DUMMY_CLIENT_ID, DUMMY_CLIENT_SECRET, DUMMY_USER_AGENT)
        
        # Use a known public user for testing if you have real credentials
        # For dummy credentials, this will likely raise an error handled above.
        comments, posts = get_user_content(reddit_instance, "spez", limit=5)
        print("\n--- Sample Fetched Content (first 2 items) ---")
        if comments:
            print("Comments:", comments[:2])
        if posts:
            print("Posts:", posts[:2])

    except Exception as e:
        print(f"Test failed: {e}")
    print("--- Finished testing reddit_scraper ---")

