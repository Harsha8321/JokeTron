import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
    # Default system message for joke generation
    system_message = """You are JokeTron, an AI comedy assistant specializing in generating jokes and humor.
    Your primary goal is to make the user laugh with clever, original jokes and comedy.
    Keep responses concise and focused on humor.
    Adapt your comedy style based on the user's profile and their message.
    If asked a question, try to answer in a humorous way while being helpful.
    Avoid any inappropriate, offensive, or adult content."""
    
    # Build the messages for the API call
    messages = [{"role": "system", "content": system_message}]
    
    # Add user profile context if available
    if user_data:
        profile_prompt = f"""User profile information:
        - Age: {user_data.get('age', 'Unknown')}
        - Region: {user_data.get('region', 'Unknown')}
        - Preferred humor style: {user_data.get('humor_style', 'General')}
        - Language: {user_data.get('language', 'English')}
        
        Please adapt your humor style to match these preferences."""
        
        messages.append({"role": "user", "content": profile_prompt})
        messages.append({"role": "assistant", "content": "I'll personalize jokes based on your profile!"})
    
    # Add conversation history if available
    if previous_jokes and len(previous_jokes) > 0:
        # Limit to last 5 jokes to keep context size manageable
        recent_jokes = previous_jokes[-5:]
        
        for joke in recent_jokes:
            if joke.get('reaction'):
                reaction_note = f"User reaction: {joke.get('reaction')}"
                messages.append({"role": "assistant", "content": joke.get('content')})
                messages.append({"role": "user", "content": reaction_note})
    
    # Add the user's new message
    if user_message:
        messages.append({"role": "user", "content": user_message})
    else:
        messages.append({"role": "user", "content": "Tell me a joke that would make me laugh."})
    
    try:
        # Make the API call to generate the joke
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=300,
            temperature=0.8,  # A bit of randomness for creative jokes
        )
        
        # Extract and return the joke text
        joke_text = response.choices[0].message.content.strip()
        return joke_text
        
    except Exception as e:
        error_message = str(e)
        print(f"Error generating joke: {error_message}")
        
        # Check for specific error types
        if "insufficient_quota" in error_message or "exceeded your current quota" in error_message:
            return "🛑 OpenAI API Quota Exceeded: The API key has run out of credits. Please check your OpenAI account billing details to continue using AI-generated jokes."
        elif "rate limit" in error_message.lower() or "429" in error_message:
            return "⏱️ Rate limit reached. The AI is taking a quick break. Please try again in a moment!"
        else:
            # Provide a personalized fallback joke based on user preferences
            import random
            
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
                "I was going to tell a dead baby joke. But I decided to abort.",
                "I have a stepladder because my real ladder left when I was a kid.",
                "My wife told me to stop impersonating a flamingo. I had to put my foot down.",
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
                
            return f"Here's a joke while my AI brain reboots: {random.choice(jokes)}"