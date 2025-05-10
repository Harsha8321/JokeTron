import os
import requests
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ollama API endpoint for Gemma 3
API_URL = "http://localhost:11434/api/generate"

# Headers for API requests
headers = {
    "Content-Type": "application/json"
}

def generate_gemma_response(user_message, user=None):
    """
    Generate either a joke or a conversation response based on user input using Gemma 3
    
    Args:
        user_message (str): The user's message
        user (User): User object containing profile information
        
    Returns:
        str: Generated response from Gemma 3
    """
    # Get user profile if available
    user_data = {}
    if user:
        user_data = {
            'humor_style': user.humor_style,
            'age': user.age,
            'region': user.region,
            'language': user.language
        }
    
    # Detect if the message is asking for a joke
    joke_keywords = ['joke', 'funny', 'laugh', 'comedy', 'humor', 'tell me a joke']
    is_joke_request = any(keyword in user_message.lower() for keyword in joke_keywords)
    
    # Create system prompt based on whether it's a joke request or conversation
    if is_joke_request:
        system_prompt = f"""You are JokeTron, a comedy AI specializing in jokes. 
        Generate a joke that matches:
        - Humor style: {user_data.get('humor_style', 'general')}
        - Age appropriate for: {user_data.get('age', 'adult')}
        - Regional relevance: {user_data.get('region', 'global')}
        Keep it concise and clever. Do NOT mention or refer to the user's profile information in your response. 
        Do NOT preface your joke with any description of what kind of joke it is.
        Just tell the joke directly and concisely."""
    else:
        system_prompt = f"""You are JokeTron, a friendly AI assistant with a good sense of humor.
        You respond to normal conversation in a light, friendly way with occasional humor.
        Your responses should be conversational but brief (1-3 sentences).
        Add a touch of humor when appropriate without forcing jokes."""
    
    # Format as a prompt for Ollama with Gemma 3
    prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"
    
    # Payload format for Ollama API
    payload = {
        "model": "gemma3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 150
        }
    }
    
    try:
        # Send request to Ollama API
        # Note: No API key is needed for Ollama as it runs locally
        response = requests.post(API_URL, headers=headers, json=payload)
        
        logger.info(f"Ollama API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Extract the response from Ollama's JSON format
            response_data = response.json()
            assistant_response = response_data.get("response", "")
            return assistant_response.strip()
        else:
            logger.error(f"Ollama API Error: {response.text}")
            return fallback_response(is_joke_request, user_data)
    except Exception as e:
        logger.error(f"Error with Ollama API: {str(e)}")
        return fallback_response(is_joke_request, user_data)

def fallback_response(is_joke_request, user_data=None):
    """
    Provide a fallback response when the API fails
    
    Args:
        is_joke_request (bool): Whether the user requested a joke
        user_data (dict): User profile data
        
    Returns:
        str: A fallback response
    """
    if is_joke_request:
        return get_fallback_joke(user_data)
    else:
        return "I'm here to chat! Feel free to ask me for a joke anytime."

def get_fallback_joke(user_data=None):
    """
    Get a fallback joke based on user preferences
    
    Args:
        user_data (dict): User profile data
        
    Returns:
        str: A joke from the appropriate category
    """
    # Get user humor style if available
    humor_style = "general"
    if user_data and user_data.get('humor_style'):
        humor_style = user_data.get('humor_style').lower()
    
    # Jokes by category
    pun_jokes = [
        "I used to be a baker, but I couldn't make enough dough.",
        "What do you call a fake noodle? An impasta!",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "Why don't scientists trust atoms? Because they make up everything!",
    ]
    
    dark_jokes = [
        "Light travels faster than sound. That's why some people appear bright until they speak.",
        "I have a stepladder because my real ladder left when I was a kid.",
        "My wife told me to stop impersonating a flamingo. I had to put my foot down.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    ]
    
    sarcastic_jokes = [
        "I'm not lazy, I'm just on energy-saving mode.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Common sense is like deodorant. The people who need it most never use it.",
        "I don't have a short attention span, I just... oh look, a butterfly!",
    ]
    
    general_jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
        "Why don't eggs tell jokes? They'd crack each other up.",
    ]
    
    # Select appropriate joke category
    if "pun" in humor_style:
        jokes = pun_jokes
    elif "dark" in humor_style:
        jokes = dark_jokes
    elif "sarcastic" in humor_style:
        jokes = sarcastic_jokes
    else:
        jokes = general_jokes
        
    return f"Here's a joke for you: {random.choice(jokes)}"