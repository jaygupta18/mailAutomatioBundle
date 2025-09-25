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
        // Load settings from Chrome storage
        const settings = await new Promise((resolve) => {
            chrome.storage.local.get(['maxEmails', 'replyStyle', 'customPrompt'], (result) => {
                resolve(result);
            });
        });
        
        // Send message to background script with settings
        const response = await chrome.runtime.sendMessage({
            action: 'processEmails',
            settings: settings
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


function injectButton() {
    // Look for Gmail's top right area - multiple possible selectors
    const topRightSelectors = [
        // Gmail's header area
        '.gb_Ac', // Main header
        '.gb_jc', // Toolbar area
        '.gb_ec', // Another header variant
        '[role="banner"]', // Banner role
        '.gb_Ka', // Header container
        '.gb_La', // Header wrapper
        // Look for the area near the profile picture/settings
        '.gb_Na', // Profile area
        '.gb_Oa', // Settings area
        '.gb_Pa', // Account area
        // Fallback to body if specific areas not found
        'body'
    ];
    
    let targetArea = null;
    for (const selector of topRightSelectors) {
        targetArea = document.querySelector(selector);
        if (targetArea) {
            console.log('Found target area:', selector);
            break;
        }
    }
    
    if (targetArea && !aiButton) {
        createAIButton();
        
        // Position the button in the top right
        aiButton.style.position = 'fixed';
        aiButton.style.top = '20px';
        aiButton.style.right = '20px';
        aiButton.style.zIndex = '9999';
        
        // Add to body for better positioning
        document.body.appendChild(aiButton);
        
        console.log('AI Assistant button injected successfully');
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
    
    // Initial injection attempts with delays
    setTimeout(injectButton, 1000);
    setTimeout(injectButton, 3000);
    setTimeout(injectButton, 5000);
    setTimeout(injectButton, 8000);
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