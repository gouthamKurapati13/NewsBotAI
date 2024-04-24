document.querySelector('#user-query').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        sendMessage(); 
    }
});

function addBotMessageLoader() {
    const botMessage = `
    <div class="flex items-start bot-loading">
        <img src="/static/Images/NewsBot Icon.jpg" alt="NewsBot Icon" class="message-icon mr-2">
        <div class="bot-message rounded-lg p-3 max-w-xs">
            <span class="spinner"></span>
        </div>
    </div>
    `
    chatMessages.insertAdjacentHTML('beforeend', botMessage);
}

function addBotMessage(message) {
    window.scrollBy(0, 100);
    const chatMessages = document.getElementById('chat-messages');
    const botMessage = `
        <div class="flex items-start">
            <img src="/static/Images/NewsBot Icon.jpg" alt="NewsBot Icon" class="message-icon mr-2">
            <div class="bot-message rounded-lg p-3 max-w-xs">
                <p>${message}</p>
            </div>
        </div>`;
    chatMessages.insertAdjacentHTML('beforeend', botMessage);
}

function addUserMessage(message) {
    window.scrollBy(0, 100);
    document.getElementById('user-query').value = '';
    const chatMessages = document.getElementById('chat-messages');
    const userMessage = `
        <div class="flex items-start justify-end">
            <div class="user-message rounded-lg p-3 max-w-xs">
                <p>${message}</p>
            </div>
            <img src="/static/Images/User Icon.jpg" alt="User Icon" class="message-icon ml-2">
        </div>`;
    chatMessages.insertAdjacentHTML('beforeend', userMessage);
}

async function sendQuery(query) {
    addUserMessage(query);
    fetch('/answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: query })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.answer);
        if (Array.isArray(data.answer) && data.answer.length > 0) {
            data.answer.forEach(answer => {
                addBotMessage("<b>" + answer['title'] + "</b>" + "<br\>" +answer['body']);
            });
        }
        else {
            addBotMessage(data.answer);
        }
    })
    .catch(error => console.error('Error:', error));
}

async function sendMessage() {
    const userQuery = document.getElementById('user-query').value.trim();
    if (userQuery !== '') {
        const mssg = userQuery.replace('CATEGORY : ','').replace('TOPIC : ', '').trim();
        addUserMessage(mssg);
        try {
            const rawResponse = await fetch('/answer', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'question': userQuery }),
            });

            const response = await rawResponse.json();
            console.log(response.answer);
            if (Array.isArray(response.answer) && response.answer.length > 0) {
                response.answer.forEach(answer => {
                    addBotMessage("<b>" + answer['title'] + "</b>" + "<br\>" +answer['body']);
                });
            }
            else {
                addBotMessage(response.answer);
            }
        } catch (err) {
            console.log(err);
        }
    }
}

function categoryQuery() {
    addUserMessage("Category");
    addBotMessage("Please specify the category you want to know about");
    const queryfield = document.getElementById('user-query');
    queryfield.value = "CATEGORY : ";
    queryfield.focus();
}

function topicQuery() {
    addUserMessage("Topic");
    addBotMessage("Please specify the specific topic you want to know about");
    const queryfield = document.getElementById('user-query');
    queryfield.value = "TOPIC : ";
    queryfield.focus();
}

function discussQuery() {
    addUserMessage("Discuss");
    addBotMessage("Yeah sure. You can ask questions about any news I have shared with you so far.");
    const queryfield = document.getElementById('user-query');
    queryfield.focus();
}