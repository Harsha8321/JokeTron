import json
import os
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import OpenAI library if available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not installed. Using fallback responses only.")

# Fallback jokes by category
FALLBACK_JOKES = {
    "dark": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "I have a joke about unemployed people, but it doesn't work.",
        "What's the difference between a well-dressed man on a bicycle and a poorly dressed man on a tricycle? Attire."
    ],
    "pun": [
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Did you hear about the guy who invented the knock-knock joke? He won the 'no-bell' prize.",
        "I used to be a baker, but I couldn't make enough dough.",
        "How do you organize a space party? You planet."
    ],
    "sarcastic": [
        "I'm not arguing, I'm just explaining why I'm right.",
        "I'm not saying I'm Batman. I'm just saying no one has ever seen me and Batman in the same room.",
        "I'm not lazy, I'm just on energy-saving mode.",
        "I don't always have patience, but when I do, it lasts about 5 seconds."
    ],
    "general": [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a fake noodle? An impasta!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "What's the best time to go to the dentist? Tooth hurty!"
    ]
}

def generate_joke(user_data=None, previous_jokes=None, user_message=None):
    """
    Generate a joke using OpenAI's API based on user data and conversation context.
    
    Args:
        user_data (dict): User profile data like age, region, and humor style
        previous_jokes (list): List of previous jokes and their reactions
        user_message (str): The user's most recent message
        
    Returns:
        str: The generated joke or conversational response
    """
    try:
        if not OPENAI_AVAILABLE or not os.environ.get("OPENAI_API_KEY"):
            # If OpenAI is not available, use fallback jokes
            return get_fallback_joke(user_data)
        
        # Initialize OpenAI client
        openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Format user data for context
        user_profile = ""
        if user_data:
            user_profile = f"""
            User profile information:
            - Age: {user_data.get('age', 'Not specified')}
            - Region: {user_data.get('region', 'Not specified')}
            - Preferred humor style: {user_data.get('humor_style', 'Not specified')}
            - Language: {user_data.get('language', 'English')}
            
            Please adapt your humor style to match these preferences.
            """
        
        # Format previous jokes for context
        joke_history = ""
        if previous_jokes and len(previous_jokes) > 0:
            joke_history = "Recent conversation history:\n"
            for i, joke in enumerate(previous_jokes[:5]):  # Limit to 5 most recent jokes
                reaction = joke.get('reaction', 'No reaction')
                joke_history += f"Joke {i+1}: {joke.get('content')}\nUser reaction: {reaction}\n\n"
        
        # Format user message
        message_context = f"User says: {user_message}" if user_message else "User has requested a joke."
        
        # Create the complete prompt
        messages = [
            {
                "role": "system", 
                "content": "You are JokeTron, an AI comedy assistant specializing in generating jokes and humor.\n"
                           "Your primary goal is to make the user laugh with clever, original jokes and comedy.\n"
                           "Keep responses concise and focused on humor.\n"
                           "Adapt your comedy style based on the user's profile and their message.\n"
                           "If asked a question, try to answer in a humorous way while being helpful.\n"
                           "Avoid any inappropriate, offensive, or adult content."
            },
            {
                "role": "user",
                "content": user_profile
            },
            {
                "role": "assistant",
                "content": "I'll personalize jokes based on your profile!"
            },
            {
                "role": "user",
                "content": message_context
            }
        ]
        
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
            messages=messages,
            max_tokens=300,
            temperature=0.8,
        )
        
        # Extract the response text
        joke_text = response.choices[0].message.content
        return joke_text
    
    except Exception as e:
        logging.error(f"Error generating joke: {str(e)}")
        return get_fallback_joke(user_data)

def get_fallback_joke(user_data=None):
    """Return a fallback joke when OpenAI API is unavailable."""
    humor_style = user_data.get('humor_style', 'general').lower() if user_data else 'general'
    
    # Map user's humor style to available categories
    if 'dark' in humor_style or 'black' in humor_style:
        category = 'dark'
    elif 'pun' in humor_style or 'word' in humor_style:
        category = 'pun'
    elif 'sarcas' in humor_style or 'ironic' in humor_style or 'dry' in humor_style:
        category = 'sarcastic'
    else:
        category = 'general'
    
    # Get jokes for the category
    jokes = FALLBACK_JOKES.get(category, FALLBACK_JOKES['general'])
    
    # Return a random joke from the category
    return random.choice(jokes)