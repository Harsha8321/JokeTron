// Main application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Toggle between dark and light mode
    const themeToggle = document.getElementById('theme-toggle');
    
    if (themeToggle) {
        // Check for saved theme preference or use default dark theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        setTheme(savedTheme);
        
        themeToggle.addEventListener('change', function() {
            const theme = this.checked ? 'dark' : 'light';
            setTheme(theme);
            localStorage.setItem('theme', theme);
        });
    }
    
    // Set light or dark theme
    function setTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
            if (themeToggle) themeToggle.checked = true;
        } else {
            document.documentElement.classList.remove('dark');
            if (themeToggle) themeToggle.checked = false;
        }
    }
    
    // Mobile navigation toggle
    const navToggle = document.getElementById('nav-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (navToggle && mobileMenu) {
        navToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Flash message handling
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(message) {
        // Add close button functionality
        const closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.remove();
            });
        }
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            message.classList.add('opacity-0');
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Settings panel toggle
    const settingsToggle = document.getElementById('settings-toggle');
    const settingsPanel = document.getElementById('settings-panel');
    const closeSettings = document.getElementById('close-settings');
    
    if (settingsToggle && settingsPanel) {
        settingsToggle.addEventListener('click', function() {
            settingsPanel.classList.toggle('translate-x-full');
            settingsPanel.classList.toggle('translate-x-0');
        });
        
        if (closeSettings) {
            closeSettings.addEventListener('click', function() {
                settingsPanel.classList.remove('translate-x-0');
                settingsPanel.classList.add('translate-x-full');
            });
        }
        
        // Close settings panel when clicking outside
        document.addEventListener('click', function(event) {
            if (!settingsPanel.contains(event.target) && event.target !== settingsToggle) {
                settingsPanel.classList.remove('translate-x-0');
                settingsPanel.classList.add('translate-x-full');
            }
        });
    }
});
