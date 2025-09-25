// Content script for Gmail AI Assistant
let aiButton = null;
let isProcessing = false;

// Function to create the AI button
function createAIButton() {
    if (aiButton) return; // Button already exists
    
    aiButton = document.createElement('div');
    aiButton.className = 'gmail-ai-button';
    aiButton.innerHTML = `
        <div class="ai-button-content">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <span>AI Assistant</span>
        </div>
    `;
    
    aiButton.addEventListener('click', handleAIClick);
    
    // Add loading state
    aiButton.addEventListener('mouseenter', () => {
        if (!isProcessing) {
            aiButton.style.transform = 'scale(1.05)';
        }
    });
    
    aiButton.addEventListener('mouseleave', () => {
        if (!isProcessing) {
            aiButton.style.transform = 'scale(1)';
        }
    });
}

// Function to handle AI button click
async function handleAIClick() {
    if (isProcessing) return;
    
    isProcessing = true;
    aiButton.classList.add('processing');
    aiButton.querySelector('.ai-button-content span').textContent = 'Processing...';
    
    try {
        // Send message to background script
        const response = await chrome.runtime.sendMessage({
            action: 'processEmails'
        });
        
        if (response.success) {
            showNotification('Emails processed successfully!', 'success');
        } else {
            showNotification('Error processing emails: ' + response.error, 'error');
        } 
    } catch (error) {
        showNotification('Failed to connect to AI service', 'error');
        console.error('Error:', error);
    } finally {
        isProcessing = false;
        aiButton.classList.remove('processing');
        aiButton.querySelector('.ai-button-content span').textContent = 'AI Assistant';
    }
}

// Function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `gmail-ai-notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Function to inject the button into Gmail
function injectButton() {
    // Look for Gmail's toolbar area
    const toolbarSelectors = [
        '.gb_jc', // Gmail's main toolbar
        '[role="toolbar"]',
        '.gb_Ac',
        '.gb_ec'
    ];
    
    let toolbar = null;
    for (const selector of toolbarSelectors) {
        toolbar = document.querySelector(selector);
        if (toolbar) break;
    }
    
    if (toolbar && !aiButton) {
        createAIButton();
        toolbar.appendChild(aiButton);
    }
}

// Observer to watch for DOM changes
const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
        if (mutation.type === 'childList') {
            injectButton();
        }
    }
});

// Start observing when the page loads
function startObserving() {
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Initial injection attempt
    setTimeout(injectButton, 1000);
    setTimeout(injectButton, 3000);
    setTimeout(injectButton, 5000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startObserving);
} else {
    startObserving();
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getStatus') {
        sendResponse({ isProcessing });
    }
}); 
