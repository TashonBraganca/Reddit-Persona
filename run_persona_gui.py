import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv
from reddit_scraper import init_reddit_api, get_user_content
from persona_generator import generate_persona
from utils import save_persona_to_file

# Helper to run the persona generation pipeline
def run_persona(username, status_callback):
    load_dotenv()
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, OPENAI_API_KEY]):
        status_callback("Error: Missing one or more environment variables. Check your .env file.")
        return

    try:
        status_callback(f"Initializing Reddit API...")
        reddit = init_reddit_api(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT)
        if not reddit:
            status_callback("Failed to initialize Reddit API.")
            return
        status_callback(f"Fetching content for u/{username}...")
        comments, posts = get_user_content(reddit, username, limit=200)
        if not comments and not posts:
            status_callback(f"No public comments or posts found for u/{username}.")
            return
        all_user_content = []
        for comment in comments:
            all_user_content.append({"type": "comment", "text": comment["text"], "url": comment["url"]})
        for post in posts:
            text_content = post["text"] if post["text"] else post["title"]
            all_user_content.append({"type": "post", "text": text_content, "url": post["url"], "title": post["title"]})
        status_callback("Generating persona using OpenAI API...")
        persona_content = generate_persona(OPENAI_API_KEY, all_user_content, username)
        if persona_content:
            save_persona_to_file(username, persona_content)
            status_callback(f"Persona generation complete! Saved as {username}_persona.txt")
        else:
            status_callback("Persona generation failed or returned empty.")
    except Exception as e:
        status_callback(f"An error occurred: {e}")

# GUI setup
def main():
    root = tk.Tk()
    root.title("Reddit Persona Generator")
    root.geometry("400x200")

    tk.Label(root, text="Enter Reddit Username:").pack(pady=10)
    username_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=username_var, width=30)
    entry.pack(pady=5)
    entry.focus()

    status_var = tk.StringVar()
    status_label = tk.Label(root, textvariable=status_var, wraplength=380, fg="blue")
    status_label.pack(pady=10)

    def on_generate():
        username = username_var.get().strip()
        if not username:
            messagebox.showerror("Input Error", "Please enter a Reddit username.")
            return
        status_var.set("")
        root.update()
        def update_status(msg):
            status_var.set(msg)
            root.update()
        run_persona(username, update_status)

    tk.Button(root, text="Generate Persona", command=on_generate).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main() 