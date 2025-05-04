// Handle profile form submission and validation

document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profile-form');
    
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const age = document.getElementById('age').value;
            const region = document.getElementById('region').value;
            const humorStyle = document.getElementById('humor-style').value;
            const language = document.getElementById('language').value;
            
            // Validate inputs
            if (!age || !region || !humorStyle || !language) {
                showProfileAlert('Please fill in all fields', 'error');
                return;
            }
            
            // Validate age is a number between 13 and 120
            if (isNaN(age) || age < 13 || age > 120) {
                showProfileAlert('Please enter a valid age between 13 and 120', 'error');
                return;
            }
            
            // Submit the form
            this.submit();
        });
    }
    
    // Update humor style description when selection changes
    const humorStyleSelect = document.getElementById('humor-style');
    const humorDescription = document.getElementById('humor-description');
    
    if (humorStyleSelect && humorDescription) {
        const descriptions = {
            'Puns': 'Wordplay and double meanings that make you groan and laugh at the same time',
            'Observational': 'Witty observations about everyday life situations',
            'Dark': 'Humor that deals with taboo subjects in a provocative way',
            'Sarcastic': 'Ironic remarks and dry wit that point out life\'s absurdities',
            'Absurdist': 'Illogical and nonsensical humor that defies conventional expectations'
        };
        
        humorStyleSelect.addEventListener('change', function() {
            const description = descriptions[this.value] || '';
            humorDescription.textContent = description;
            humorDescription.classList.remove('hidden');
        });
        
        // Trigger on initial load
        if (humorStyleSelect.value) {
            const description = descriptions[humorStyleSelect.value] || '';
            humorDescription.textContent = description;
            humorDescription.classList.remove('hidden');
        }
    }
    
    // Display alert message
    function showProfileAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = type === 'error' 
            ? 'mb-4 p-4 rounded bg-red-100 border border-red-400 text-red-700'
            : 'mb-4 p-4 rounded bg-green-100 border border-green-400 text-green-700';
        alertDiv.textContent = message;
        
        const form = document.querySelector('form');
        form.parentNode.insertBefore(alertDiv, form);
        
        // Remove alert after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
});
