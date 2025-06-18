# JokeTron - MacOS Installation Guide

JokeTron is an AI-powered joke generator and chat application that uses Gemma 3 on Ollama for personalized humor.

## Installation Instructions

### Step 1: Clone or download this repository
Download and extract the JokeTron zip file to your preferred location.

### Step 2: Set up Python virtual environment
Open Terminal and navigate to the extracted JokeTron folder:

```bash
cd path/to/joketron
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama and the Gemma 3 model

First, install Ollama which will host the AI model locally:

```bash
# For Mac with curl installed (most systems)
curl -fsSL https://ollama.com/install.sh | sh

# If that doesn't work, visit https://ollama.com/download and download the macOS installer
```

After installing Ollama, pull the Gemma 3 model:

```bash
ollama pull gemma3
```

Note: The Gemma 3 model is approximately 4GB, so this download may take some time depending on your internet connection.

Start the Ollama service:

```bash
# This will run Ollama in the background
ollama serve &
```

### Step 5: Initialize the database

```bash
python init_db.py
```

### Step 6: Run the application

```bash
python run.py
```

The application will be available at [http://127.0.0.1:8080](http://127.0.0.1:8080) in your web browser.

## Usage Instructions

1. Create an account by clicking "Sign Up"
2. Complete your profile with preferences to get personalized jokes
3. Chat with JokeTron - ask for jokes or just have a conversation
4. Use the message input at the bottom to send messages
5. You can clear your chat history using the "Clear" button

## Troubleshooting

- **Flask errors**: Make sure your virtual environment is activated and all dependencies are installed.
- **Database errors**: Check that the `instance` folder exists and contains the SQLite database file.
- **AI Generation errors**: Ensure Ollama is running with `ollama serve` and the Gemma 3 model is downloaded.

