# Reddit User Persona Generator

This project generates a user persona for a given Reddit user by scraping their public posts and comments and analyzing them using the OpenAI API.

## Features

- Scrapes Reddit user's top posts and comments.
- Generates a detailed user persona (Demographics, Behavior & Habits, Frustrations, Goals & Needs, Motivations, Personality Traits, Online Behavior, Quote).
- Provides citations (links to original Reddit content) for every persona characteristic.
- Outputs the persona to a text file.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TashonBraganca/Reddit-Persona.git
   cd Reddit-Persona
   ```

2. **Create a Python Virtual Environment (recommended):**
   ```bash
   python3 -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Credentials:**

   - **Reddit API:**
     1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps).
     2. Click "create an app...".
     3. Choose "script" for the type.
     4. Fill in a name (e.g., "PersonaGenerator"), description, and `redirect uri` (e.g., `http://localhost:8080`).
     5. After creation, you will see your `client_id` (under "personal use script") and `client_secret`.
     6. For `user_agent`, use a unique and descriptive string like `RedditPersonaGenerator/1.0 (by /u/your_reddit_username)`.

   - **OpenAI API:**
     1. Go to the [OpenAI API Keys page](https://platform.openai.com/account/api-keys) to generate an API key.

   - **Create `.env` file:**
     Create a file named `.env` in the root directory and add your credentials:
     ```
     REDDIT_CLIENT_ID="YOUR_REDDIT_CLIENT_ID"
     REDDIT_CLIENT_SECRET="YOUR_REDDIT_CLIENT_SECRET"
     REDDIT_USER_AGENT="YOUR_UNIQUE_USER_AGENT_STRING"
     OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
     ```
     **Important:** Do not share your `.env` file or commit it to version control.

## Usage

To run the script, execute `main.py` with the Reddit user profile URL as an argument:

```bash
python main.py https://www.reddit.com/user/kojied/
```

The generated user persona will be saved in a text file named `[username]_persona.txt` in the project root directory.

### GUI Version

You can also use a simple graphical interface:

```bash
python run_persona_gui.py
```

- This will open a window where you can enter a Reddit username.
- The script will generate the persona and display status updates.
- The output file will be saved in the same way as the command-line version.

## Error Handling

- The script includes error handling for API calls and file operations.
- If you encounter issues, ensure your API keys are correctly configured and you have an active internet connection.

## Disclaimer

This tool is for educational and personal use only. Please respect Reddit's API terms of service and user privacy. The generated persona is an inference based on public data and may not be entirely accurate.

