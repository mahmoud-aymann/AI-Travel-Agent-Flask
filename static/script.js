// JavaScript for AI Travel Agent

// Example queries
const exampleQueries = {
    beach: `I want to visit Goa for 5 days in December.
My budget is 30,000 INR.
Get current weather for Goa.
Find hotels under 3,000 INR per night.
I want to know about beaches, water sports, and nightlife.
Calculate exact costs including food (500 INR per day).
Show me travel videos about Goa.`,
    
    international: `I want to visit Thailand for 4 days.
My budget is 800 USD.
Convert all costs to Indian Rupees.
Get current weather for Bangkok.
Find budget hotels under 30 USD per night.
Include street food and restaurant costs.
Show temple entry fees and transportation costs.
Calculate total trip cost in both USD and INR.`
};

// Chat history storage
let chatHistory = [];

// DOM elements
const exampleSelect = document.getElementById('exampleSelect');
const queryInput = document.getElementById('queryInput');
const submitBtn = document.getElementById('submitBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const responseArea = document.getElementById('responseArea');
const responseContent = document.getElementById('responseContent');
const errorArea = document.getElementById('errorArea');
const errorMessage = document.getElementById('errorMessage');
const chatHistoryDiv = document.getElementById('chatHistory');
const historyContent = document.getElementById('historyContent');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Example query selection
    exampleSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        if (selectedValue !== 'custom' && exampleQueries[selectedValue]) {
            queryInput.value = exampleQueries[selectedValue];
        } else if (selectedValue === 'custom') {
            queryInput.value = '';
        }
    });

    // Submit button click
    submitBtn.addEventListener('click', handleSubmit);

    // Enter key in textarea
    queryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            handleSubmit();
        }
    });

    // Load chat history from session storage
    loadChatHistory();
});

// Handle form submission
async function handleSubmit() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('Please enter your travel query!');
        return;
    }

    // Show loading state
    setLoadingState(true);
    hideError();
    hideResponse();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            showResponse(data.response);
            
            // Add to chat history
            addToHistory(query, data.response);
        } else {
            // Error
            showError(data.error || 'An error occurred while processing your request.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        setLoadingState(false);
    }
}

// Set loading state
function setLoadingState(loading) {
    if (loading) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Planning...';
        loadingSpinner.style.display = 'block';
    } else {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-rocket"></i> Plan My Trip';
        loadingSpinner.style.display = 'none';
    }
}

// Show response
function showResponse(response) {
    responseContent.textContent = response;
    responseArea.style.display = 'block';
    responseArea.scrollIntoView({ behavior: 'smooth' });
}

// Hide response
function hideResponse() {
    responseArea.style.display = 'none';
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorArea.style.display = 'block';
    errorArea.scrollIntoView({ behavior: 'smooth' });
}

// Hide error
function hideError() {
    errorArea.style.display = 'none';
}

// Add to chat history
function addToHistory(query, response) {
    const historyItem = {
        query: query,
        response: response,
        timestamp: new Date().toLocaleString()
    };
    
    chatHistory.unshift(historyItem);
    
    // Keep only last 10 items
    if (chatHistory.length > 10) {
        chatHistory = chatHistory.slice(0, 10);
    }
    
    // Save to session storage
    sessionStorage.setItem('travelAgentHistory', JSON.stringify(chatHistory));
    
    // Update UI
    updateChatHistory();
}

// Load chat history from session storage
function loadChatHistory() {
    const saved = sessionStorage.getItem('travelAgentHistory');
    if (saved) {
        try {
            chatHistory = JSON.parse(saved);
            updateChatHistory();
        } catch (e) {
            console.error('Error loading chat history:', e);
        }
    }
}

// Update chat history UI
function updateChatHistory() {
    if (chatHistory.length === 0) {
        chatHistoryDiv.style.display = 'none';
        return;
    }
    
    chatHistoryDiv.style.display = 'block';
    
    historyContent.innerHTML = chatHistory.map((item, index) => `
        <div class="history-item">
            <div class="history-query">
                <strong>Query ${chatHistory.length - index}:</strong> ${item.query}
                <small class="text-muted d-block">${item.timestamp}</small>
            </div>
            <div class="history-response">${item.response}</div>
        </div>
    `).join('');
}

// Clear chat history
function clearHistory() {
    chatHistory = [];
    sessionStorage.removeItem('travelAgentHistory');
    updateChatHistory();
}

// Add clear history button if there's history
function addClearHistoryButton() {
    if (chatHistory.length > 0 && !document.getElementById('clearHistoryBtn')) {
        const clearBtn = document.createElement('button');
        clearBtn.id = 'clearHistoryBtn';
        clearBtn.className = 'btn btn-outline-danger btn-sm mt-2';
        clearBtn.innerHTML = '<i class="fas fa-trash"></i> Clear History';
        clearBtn.onclick = clearHistory;
        
        const cardHeader = chatHistoryDiv.querySelector('.card-header');
        cardHeader.appendChild(clearBtn);
    }
}

// Initialize clear history button
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(addClearHistoryButton, 1000);
});

// Auto-resize textarea
queryInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});

// Add some utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show a temporary success message
        const btn = event.target;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        btn.classList.add('btn-success');
        btn.classList.remove('btn-outline-secondary');
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-outline-secondary');
        }, 2000);
    });
}

// Add copy buttons to responses
function addCopyButtons() {
    const responses = document.querySelectorAll('.response-content, .history-response');
    responses.forEach(response => {
        if (!response.querySelector('.copy-btn')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn btn-outline-secondary btn-sm copy-btn';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            copyBtn.style.float = 'right';
            copyBtn.style.marginTop = '10px';
            copyBtn.onclick = () => copyToClipboard(response.textContent);
            response.appendChild(copyBtn);
        }
    });
}

// Add copy buttons when content is loaded
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            addCopyButtons();
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
