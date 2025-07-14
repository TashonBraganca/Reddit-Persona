from openai import OpenAI
from openai import APIError
from typing import List, Dict

def generate_persona(openai_api_key: str, user_content: List[Dict], username: str) -> str:
    """
    Generates a user persona based on provided user content using the Google Gemini API.

    Args:
        gemini_api_key (str): Your Google Gemini API key.
        user_content (List[Dict]): A list of dictionaries, where each dict represents
                                   a comment or post with 'text' and 'url' keys.
        username (str): The Reddit username for the persona title.

    Returns:
        str: The generated user persona in Markdown format.

    Raises:
        ValueError: If the Gemini API key is missing or invalid.
        generation_types.BlockedPromptException: If the prompt is blocked by safety filters.
        Exception: For any other unexpected errors.
    """
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please configure it in your .env file.")

    client = OpenAI(api_key=openai_api_key)

    # Prepare user content for the LLM, ensuring URLs are embedded with text
    combined_text_for_llm = ""
    for item in user_content:
        content_type = item.get("type", "unknown").capitalize()
        content_text = item.get("text", "")
        content_url = item.get("url", "")
        content_title = item.get("title", "") # For posts, selftext might be empty, use title

        # Use title if selftext is empty for posts
        if content_type == "Post" and not content_text and content_title:
            content_text = content_title

        if content_text: # Only add if there's actual text content
            combined_text_for_llm += f"- {content_type}: \"{content_text.strip()}\" ({content_url})\n"
    
    if not combined_text_for_llm.strip():
        return f"### User Persona: {username}\n\nNo sufficient public content found to generate a persona."

    llm_prompt = f"""
You are an AI assistant specialized in creating detailed user personas from text data.
Your task is to analyze the provided Reddit user content (posts and comments) and construct a comprehensive user persona.

**Instructions:**
- Only include information that can be directly inferred from the provided user content. If a category cannot be filled, state concisely: "Not enough information."
- For every inferred detail, you MUST provide a direct citation (URL) to the supporting Reddit post or comment.
- Use bullet points for all lists. Be concise and factual.
- Strictly follow the output format below:

---
### User Persona: {username}

**Demographics:**
* Age: [Inferred Age or Age Range] (Citation: [Link])
* Gender: [Inferred Gender] (Citation: [Link])
* Location: [Inferred Location] (Citation: [Link])
* Occupation/Status: [Inferred Occupation/Status] (Citation: [Link])
* Archetype: [Inferred Archetype] (Citation: [Link])

**Behavior & Habits:**
- [Habit 1] (Citation: [Link])
- [Habit 2] (Citation: [Link])
- ...

**Frustrations:**
- [Frustration 1] (Citation: [Link])
- [Frustration 2] (Citation: [Link])
- ...

**Goals & Needs:**
- [Goal or Need 1] (Citation: [Link])
- [Goal or Need 2] (Citation: [Link])
- ...

**Motivations:**
- [Motivation 1] (Citation: [Link])
- [Motivation 2] (Citation: [Link])
- ...

**Personality Traits:**
- [Trait 1] (Citation: [Link])
- [Trait 2] (Citation: [Link])
- ...

**Online Behavior:**
* Frequency of Posting/Commenting: [Inferred Frequency] (Citation: [Link])
* Subreddits Engaged In: [List of Subreddits, comma-separated] (Citation: [Link])
* Tone of Communication: [Description] (Citation: [Link])

**Quote:**
"[A representative quote from their content]" (Citation: [Link])
---

**User Content to Analyze:**
{combined_text_for_llm}
"""
    try:
        print("Sending content to OpenAI API for persona generation...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # or "gpt-4o" if preferred and available
            messages=[
                {"role": "system", "content": "You are an AI assistant specialized in creating detailed user personas from text data."},
                {"role": "user", "content": llm_prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        if response.choices[0].message.content:
            print("Persona generated successfully by OpenAI API.")
            return response.choices[0].message.content
        else:
            print("OpenAI API returned an empty response.")
            return f"### User Persona: {username}\n\nCould not generate persona: OpenAI API returned empty response."

    except APIError as e:
        print(f"OpenAI API Error: {e}")
        return f"### User Persona: {username}\n\nPersona generation failed due to OpenAI API error: {e}"

if __name__ == "__main__":
    # This block is for testing purposes only.
    # Replace with your actual (or dummy) GEMINI_API_KEY for local testing.
    # For a real run, this would come from environment variables.
    DUMMY_OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE" # Replace with a real key for testing

    print("--- Testing persona_generator.py ---")
    sample_content = [
        {"type": "comment", "text": "I really enjoy playing Elden Ring in my free time. It's a masterpiece!", "url": "https://reddit.com/r/Eldenring/comments/123"},
        {"type": "post", "title": "Looking for recommendations for sci-fi books.", "text": "Just finished Dune and loved it. Any suggestions for similar epic space operas?", "url": "https://reddit.com/r/scifi/comments/456"},
        {"type": "comment", "text": "Work has been pretty stressful lately, especially with all the deadlines.", "url": "https://reddit.com/r/jobs/comments/789"},
        {"type": "comment", "text": "Always trying to learn new things, currently diving into Python.", "url": "https://reddit.com/r/learnprogramming/comments/012"}
    ]
    
    if DUMMY_OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        print("WARNING: OpenAI API key not set. Persona generation will not work without a valid key.")
        print("Please replace 'YOUR_OPENAI_API_KEY_HERE' with your actual API key for testing.")
    else:
        try:
            generated_persona = generate_persona(DUMMY_OPENAI_API_KEY, sample_content, "sample_user")
            print("\n--- Generated Persona ---")
            print(generated_persona)
        except Exception as e:
            print(f"Test failed: {e}")
    print("--- Finished testing persona_generator.py ---")