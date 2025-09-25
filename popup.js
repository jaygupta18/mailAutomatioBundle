// Popup script for Gmail AI Assistant
const SERVER_URL = 'http://localhost:5000';

// DOM elements
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const processButton = document.getElementById('processButton');
const settingsButton = document.getElementById('settingsButton');
const processedCount = document.getElementById('processedCount');
const successRate = document.getElementById('successRate');

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
    await checkServerStatus();
    loadStats();
    setupEventListeners();
});

// Check if the AI server is running
async function checkServerStatus() {
    try {
        const response = await fetch(`${SERVER_URL}/health`);
        if (response.ok) {
            statusDot.classList.remove('offline');
            statusText.textContent = 'Server Online';
        } else {
            throw new Error('Server not responding');
        }
    } catch (error) {
        statusDot.classList.add('offline');
        statusText.textContent = 'Server Offline';
        processButton.disabled = true;
        processButton.textContent = '❌ Server Not Available';
    }
}

// Load statistics from storage
function loadStats() {
    chrome.storage.local.get(['processedCount', 'successCount'], (result) => {
        const total = result.processedCount || 0;
        const success = result.successCount || 0;
        const rate = total > 0 ? Math.round((success / total) * 100) : 0;
        
        processedCount.textContent = total;
        successRate.textContent = `${rate}%`;
    });
}

// Setup event listeners
function setupEventListeners() {
    processButton.addEventListener('click', handleProcessEmails);
    settingsButton.addEventListener('click', handleSettings);
}

// Handle process emails button click
async function handleProcessEmails() {
    if (processButton.disabled) return;
    
    processButton.disabled = true;
    processButton.textContent = '⏳ Processing...';
    
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
            // Update statistics
            updateStats(data.processed_count, true);
            
            // Show success message
            processButton.textContent = '✅ Success!';
            setTimeout(() => {
                processButton.textContent = '🚀 Process Emails Now';
                processButton.disabled = false;
            }, 2000);
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    } catch (error) {
        console.error('Error processing emails:', error);
        
        // Update statistics (count as failed)
        updateStats(0, false);
        
        processButton.textContent = '❌ Error';
        setTimeout(() => {
            processButton.textContent = '🚀 Process Emails Now';
            processButton.disabled = false;
        }, 2000);
    }
}

// Handle settings button click
function handleSettings() {
    // Open settings page or show settings modal
    chrome.tabs.create({
        url: chrome.runtime.getURL('settings.html')
    });
}

// Update statistics
function updateStats(processed, success) {
    chrome.storage.local.get(['processedCount', 'successCount'], (result) => {
        const newProcessed = (result.processedCount || 0) + processed;
        const newSuccess = (result.successCount || 0) + (success ? processed : 0);
        
        chrome.storage.local.set({
            processedCount: newProcessed,
            successCount: newSuccess
        }, () => {
            loadStats();
        });
    });
}

// Check server status periodically
setInterval(checkServerStatus, 30000); // Check every 30 seconds 