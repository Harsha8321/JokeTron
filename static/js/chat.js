// Chat functionality and joke interaction

document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.querySelector('.chat-container');
    const messageForm = document.getElementById('message-form');
    const userMessageInput = document.getElementById('user-message');
    const clearChatButton = document.getElementById('clear-chat');
    
    // Load previous jokes/messages
    loadPreviousJokes();
    
    // Set up clear chat button
    if (clearChatButton) {
        clearChatButton.addEventListener('click', function() {
            clearChat();
        });
    }
    
    // Set up message form submission
    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const message = userMessageInput.value.trim();
            if (message) {
                // Add user message to chat
                addUserMessageToChat(message);
                
                // Send message to server
                sendMessage(message);
                
                // Clear input field
                userMessageInput.value = '';
            }
        });
    }
    
    // Load previous jokes from the server
    function loadPreviousJokes() {
        fetch('/api/get-jokes')
            .then(response => response.json())
            .then(data => {
                if (data.jokes && data.jokes.length > 0) {
                    // First, clear any existing messages to avoid duplicates
                    const existingMessages = document.querySelectorAll('.chat-container > div');
                    existingMessages.forEach(msg => msg.remove());
                    
                    // Add messages in the correct order and with proper formatting
                    data.jokes.forEach(msg => {
                        if (msg.is_user) {
                            // This is a user message
                            addUserMessageToChat(msg.content);
                        } else {
                            // This is an AI/joke message
                            addJokeToChat(msg.content, msg.id, msg.reaction);
                        }
                    });
                    
                    // Scroll to bottom of chat
                    scrollToBottom();
                } else {
                    // Show welcome message if no jokes
                    const welcomeMsg = "Welcome to JokeTron! I'm your personal comedy assistant. Ask me anything or request a joke tailored to your preferences!";
                    addSystemMessageToChat(welcomeMsg);
                }
            })
            .catch(error => {
                console.error('Error loading messages:', error);
                addSystemMessageToChat("Couldn't load your previous messages. Please try refreshing the page.");
            });
    }
    
    // Send a message to the server
    function sendMessage(message) {
        // Show typing indicator
        showTypingIndicator();
        
        // Call API to send message
        fetch('/api/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            // Hide typing indicator
            hideTypingIndicator();
            
            if (data.success) {
                // Add AI response to chat
                addJokeToChat(data.ai_response.content, data.ai_response.id);
            } else {
                throw new Error(data.error || 'Unknown error');
            }
            
            // Scroll to bottom of chat
            scrollToBottom();
        })
        .catch(error => {
            console.error('Error sending message:', error);
            hideTypingIndicator();
            addSystemMessageToChat("Sorry, I couldn't process your message. Please try again.");
        });
    }
    
    // Add user message to chat
    function addUserMessageToChat(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'user-message mb-3 fade-in';
        
        // Format message with line breaks
        const formattedMessage = message.replace(/\n/g, '<br>');
        
        // Get the current username from the page
        const username = document.getElementById('current-username-data')?.getAttribute('data-username') || 'You';
        
        // Create message content
        messageElement.innerHTML = `
            <div class="flex items-start justify-end max-w-4xl mx-auto">
                <div class="message-content">
                    <div class="bg-indigo-600 rounded-lg shadow ml-auto">
                        <p class="text-white">${formattedMessage}</p>
                    </div>
                </div>
                <div class="flex-shrink-0 ml-4">
                    <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold">
                        ${username.charAt(0).toUpperCase()}
                    </div>
                </div>
            </div>
        `;
        
        // Add to chat container
        chatContainer.appendChild(messageElement);
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Add joke/AI response to chat container
    function addJokeToChat(jokeText, jokeId, existingReaction = null) {
        const jokeElement = document.createElement('div');
        jokeElement.className = 'joke-container mb-3 fade-in';
        jokeElement.dataset.jokeId = jokeId;
        
        // Format joke text with line breaks
        const formattedJoke = jokeText.replace(/\n/g, '<br>');
        
        // Create joke content
        jokeElement.innerHTML = `
            <div class="flex items-start max-w-4xl mx-auto">
                <div class="flex-shrink-0 mr-4">
                    <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                        JT
                    </div>
                </div>
                <div class="message-content">
                    <div class="bg-gray-800 rounded-lg shadow">
                        <p class="text-white">${formattedJoke}</p>
                    </div>
                    <div class="reaction-btns mt-2 flex space-x-3">
                        <button class="reaction ${existingReaction === 'funny' ? 'selected' : ''}" data-reaction="funny" title="Funny">
                            <span class="text-xl">😂</span>
                        </button>
                        <button class="reaction ${existingReaction === 'neutral' ? 'selected' : ''}" data-reaction="neutral" title="Neutral">
                            <span class="text-xl">😐</span>
                        </button>
                        <button class="reaction ${existingReaction === 'boring' ? 'selected' : ''}" data-reaction="boring" title="Boring">
                            <span class="text-xl">😴</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add to chat container
        chatContainer.appendChild(jokeElement);
        
        // Add event listeners to reaction buttons
        const reactionBtns = jokeElement.querySelectorAll('.reaction');
        reactionBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const reaction = this.dataset.reaction;
                
                // Remove selected class from all buttons
                reactionBtns.forEach(b => b.classList.remove('bg-gray-700', 'selected'));
                
                // Add selected class to clicked button
                this.classList.add('bg-gray-700', 'selected');
                
                // Send reaction to server
                rateJoke(jokeId, reaction);
            });
        });
        
        // If there's an existing reaction, mark it as selected
        if (existingReaction) {
            const selectedBtn = jokeElement.querySelector(`.reaction[data-reaction="${existingReaction}"]`);
            if (selectedBtn) {
                selectedBtn.classList.add('bg-gray-700', 'selected');
            }
        }
    }
    
    // Add system message to chat
    function addSystemMessageToChat(message) {
        const msgElement = document.createElement('div');
        msgElement.className = 'system-message mb-3 fade-in';
        
        msgElement.innerHTML = `
            <div class="flex justify-center">
                <div class="bg-gray-700 rounded-lg px-4 py-2 text-sm text-gray-300">
                    ${message}
                </div>
            </div>
        `;
        
        chatContainer.appendChild(msgElement);
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator mb-3 fade-in';
        indicator.id = 'typing-indicator';
        
        // Random funny thinking messages
        const thinkingMessages = [
            "Thinking of something funny...",
            "Searching for the perfect joke...",
            "Brewing comedy gold...",
            "Consulting my joke database...",
            "Channeling my inner comedian...",
            "Finding humor in chaos...",
            "Polishing a punchline...",
            "Loading laugh.exe...",
            "Warming up the joke engine...",
            "Calculating optimal humor ratio..."
        ];
        
        // Select a random message
        const randomMessage = thinkingMessages[Math.floor(Math.random() * thinkingMessages.length)];
        
        indicator.innerHTML = `
            <div class="flex items-start max-w-4xl mx-auto">
                <div class="flex-shrink-0 mr-4">
                    <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                        JT
                    </div>
                </div>
                <div class="message-content">
                    <div class="bg-gray-800 rounded-lg shadow py-3 px-4">
                        <div class="typing-indicator">
                            <div class="bubble">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            <div class="thinking-text text-xs text-gray-400 ml-2 mt-1">${randomMessage}</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        chatContainer.appendChild(indicator);
        scrollToBottom();
        
        // Change the thinking message every few seconds for additional fun
        if (window.typingMessageInterval) {
            clearInterval(window.typingMessageInterval);
        }
        
        window.typingMessageInterval = setInterval(() => {
            const thinkingText = document.querySelector('.thinking-text');
            if (thinkingText) {
                const newMessage = thinkingMessages[Math.floor(Math.random() * thinkingMessages.length)];
                thinkingText.textContent = newMessage;
            } else {
                clearInterval(window.typingMessageInterval);
            }
        }, 3000);
    }
    
    // Hide typing indicator
    function hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
        
        // Clear the interval for changing messages
        if (window.typingMessageInterval) {
            clearInterval(window.typingMessageInterval);
            window.typingMessageInterval = null;
        }
    }
    
    // Send joke rating to server
    function rateJoke(jokeId, reaction) {
        fetch('/api/rate-joke', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                joke_id: jokeId,
                reaction: reaction
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Error rating joke:', data.error);
            }
        })
        .catch(error => {
            console.error('Error rating joke:', error);
        });
    }
    
    // Scroll to bottom of chat container
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Clear chat function
    function clearChat() {
        // Remove all messages from the chat container
        while (chatContainer.firstChild) {
            chatContainer.removeChild(chatContainer.firstChild);
        }
        
        // Show welcome message
        const welcomeMsg = "Chat cleared! I'm ready for a fresh conversation. What can I do for you today?";
        addSystemMessageToChat(welcomeMsg);
        
        // Clear jokes from the database by making a POST request to the server
        fetch('/api/clear-jokes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Error clearing jokes:', data.error);
                addSystemMessageToChat("There was an error clearing your conversation history.");
            }
        })
        .catch(error => {
            console.error('Error clearing jokes:', error);
        });
    }
});
