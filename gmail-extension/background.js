// Background script for Gmail AI Assistant
let SERVER_URL = 'http://localhost:5000'; // Will be updated from settings

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'processEmails') {
        processEmails(request.settings).then(sendResponse);
        return true; 
    }
});

// Load settings from Chrome storage
async function loadSettings() {
    return new Promise((resolve) => {
        chrome.storage.local.get(['serverUrl', 'maxEmails', 'replyStyle', 'customPrompt'], (result) => {
            if (result.serverUrl) {
                SERVER_URL = result.serverUrl;
            }
            resolve(result);
        });
    });
}

async function processEmails(settings = null) {
    try {
        // Load settings if not provided
        if (!settings) {
            settings = await loadSettings();
        }
        
        const response = await fetch(`${SERVER_URL}/process-emails`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'process_emails',
                settings: {
                    maxEmails: settings.maxEmails || '10',
                    replyStyle: settings.replyStyle || 'professional',
                    customPrompt: settings.customPrompt || ''
                }
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.success) {
            return {
                success: true,
                message: data.message,
                processed_count: data.processed_count
            };
        } else {
            return {
                success: false,
                error: data.error || 'Unknown error occurred'
            };
        }
    } catch (error) {
        console.error('Error processing emails:', error);
        return {
            success: false,
            error: error.message || 'Failed to connect to AI service'
        };
    }
}

// Check server status on extension startup
chrome.runtime.onStartup.addListener(async () => {
    try {
        const response = await fetch(`${SERVER_URL}/health`);
        if (response.ok) {
            console.log('AI server is running');
        }
    } catch (error) {
        console.warn('AI server is not running:', error.message);
    }
});

chrome.runtime.onInstalled.addListener(async () => {
    try {
        const response = await fetch(`${SERVER_URL}/health`);
        if (response.ok) {
            console.log('AI server is running');
        }
    } catch (error) {
        console.warn('AI server is not running:', error.message);
    }
}); 