/**
 * Main JavaScript file for OTP Authentication System
 */

document.addEventListener('DOMContentLoaded', function() {
    // Phone number validation helper
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            const value = e.target.value;
            
            // Basic visual feedback for '+' prefix
            if (value && !value.startsWith('+')) {
                input.classList.add('input-error');
                showInlineError(input, "Phone number must start with '+'");
            } else {
                input.classList.remove('input-error');
                removeInlineError(input);
            }
        });
    });

    function showInlineError(element, message) {
        let errorSpan = element.parentNode.querySelector('.inline-error');
        if (!errorSpan) {
            errorSpan = document.createElement('span');
            errorSpan.className = 'inline-error';
            element.parentNode.appendChild(errorSpan);
        }
        errorSpan.textContent = message;
        errorSpan.style.color = 'var(--error)';
        errorSpan.style.fontSize = '0.75rem';
        errorSpan.style.marginTop = '4px';
        errorSpan.style.display = 'block';
    }

    function removeInlineError(element) {
        const errorSpan = element.parentNode.querySelector('.inline-error');
        if (errorSpan) {
            errorSpan.remove();
        }
    }
});
