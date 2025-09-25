// Background script for Gmail AI Assistant
const SERVER_URL = 'http://localhost:5000';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'processEmails') {
        processEmails().then(sendResponse);
        return true; 
    }
});

async function processEmails() {
    try {
        const response = await fetch(`${SERVER_URL}/process-emails`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'process_emails'
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