import re

def preprocess_text(text: str) -> str:
    """
    Preprocesses the input text by:
    - Converting to lowercase.
    - Removing URLs.
    - Removing non-alphanumeric characters (keeping spaces).
    - Handling multiple spaces.
    """
    if not isinstance(text, str):
        return "" # Ensure text is a string

    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-z0-9\s]', '', text)          # Remove non-alphanumeric except spaces
    text = re.sub(r'\s+', ' ', text).strip()         # Replace multiple spaces with single, then strip
    return text

def save_persona_to_file(username: str, persona_content: str):
    """
    Saves the generated user persona to a text file.

    Args:
        username (str): The Reddit username, used for the filename.
        persona_content (str): The complete user persona string.
    """
    filename = f"{username}_persona.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(persona_content)
        print(f"Successfully saved user persona to {filename}")
    except IOError as e:
        print(f"Error saving persona to file {filename}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving file: {e}")

if __name__ == "__main__":
    # Example usage for testing utils.py
    test_text = "Hello, this is a test! Visit https://example.com and check out my profile: @user123. Multiple   spaces here."
    processed = preprocess_text(test_text)
    print(f"Original: {test_text}")
    print(f"Processed: {processed}")

    test_persona = "### User Persona: testuser\n\nInterests: Gaming (Citations: https://reddit.com/r/gaming/comments/123)"
    save_persona_to_file("testuser", test_persona)
