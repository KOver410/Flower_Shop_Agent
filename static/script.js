// JavaScript cho Flower Chatbot - Chat functionality

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const submitButton = chatForm.querySelector('button[type="submit"]');

    // Xử lý form submit
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;

        // Disable input while processing
        userInput.disabled = true;
        submitButton.disabled = true;
        
        // Hiển thị tin nhắn user
        addMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Hiển thị typing indicator
        showTypingIndicator();
        
        try {
            // Gửi request đến server
            const formData = new FormData();
            formData.append('message', message);
            
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            hideTypingIndicator();
            
            // Hiển thị response từ bot
            addMessage(data.response, 'bot');
            
        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage('Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau.', 'bot');
        } finally {
            // Re-enable input
            userInput.disabled = false;
            submitButton.disabled = false;
            userInput.focus();
        }
    });

    // Function để thêm tin nhắn
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Xử lý HTML trong response (cho lists, links, etc.)
        if (sender === 'bot' && text.includes('<')) {
            contentDiv.innerHTML = text;
        } else {
            contentDiv.textContent = text;
        }
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Auto scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Hiển thị typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typing-indicator';
        
        const indicatorDiv = document.createElement('div');
        indicatorDiv.className = 'typing-indicator';
        indicatorDiv.innerHTML = '<span></span><span></span><span></span>';
        
        typingDiv.appendChild(indicatorDiv);
        chatMessages.appendChild(typingDiv);
        
        // Auto scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Ẩn typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Auto focus vào input khi tải trang
    userInput.focus();

    // Enter key để gửi tin nhắn
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
});
