document.addEventListener('DOMContentLoaded', () => {
    const chat = document.getElementById('chat');
    const threads = document.getElementById('threads');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const newThreadBtn = document.getElementById('newThreadBtn');

    console.log(newThreadBtn)

    var lastThread;
    var last_threadId;

    newThreadBtn.addEventListener('click', () => {
        createThread().then(lastThread => {
            console.log(lastThread);
            fetchThreads();
        });
    });

    // Fetch previous threads
    function fetchThreads() {
        fetch('/threads')
            .then(response => response.json())
            .then(data => {
                threads.innerHTML = ''; // Clear the threads list before appending new ones
                data.forEach(thread => {
                    const li = document.createElement('li');
                    li.textContent = thread.title;
                    li.addEventListener('click', () => loadThread(thread.id));
                    console.log(thread.id);
                    threads.appendChild(li);
                });
            });
    }

    function fetchStartThreads() {
        fetch('/start_threads')
            .then(response => response.json())
            .then(data => {
                threads.innerHTML = ''; // Clear the threads list before appending new ones
                data.forEach(thread => {
                    const li = document.createElement('li');
                    li.textContent = thread.title;
                    li.addEventListener('click', () => loadThread(thread.id));
                    threads.appendChild(li);
                });
            });
    }

    fetchStartThreads();

    function addCurrentMessage(sender, message, threadId) {
        console.log(threadId);
        const lines = message.split('\n');
        const messageDiv = document.createElement('div');
        if (sender === 'assistant' && threadId === last_threadId) {
            messageDiv.className = 'aimessage';
            for (let line of lines) {
                const lineDiv = document.createElement('div');
                lineDiv.textContent = line;
                messageDiv.appendChild(lineDiv);
            }
            chat.appendChild(messageDiv);
            chat.scrollTop = chat.scrollHeight;
        }
    }

    // Send message
    sendBtn.addEventListener('click', () => {
        const message = userInput.value;
        if (message.trim() !== '') {
            addMessage('User', message);
            sendBtn.disabled = true;
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, threadId: last_threadId })
            })
            .then(response => response.json())
            .then(data => {
                addCurrentMessage('assistant', data.response, data.threadId);
                sendBtn.disabled = false;
            })
            .catch(error => {
                console.error('Error:', error);
                // Enable the send button in case of error
                sendBtn.disabled = false;
            });
            userInput.value = '';
        }
    });

    // function addMessage(sender, message) {
    //     const messageDiv = document.createElement('div');
    //     messageDiv.textContent = `${sender}: ${message}`;
    //     if (sender === 'AI') {
    //         messageDiv.className = 'aimessage';
    //     }
    //     else {
    //         messageDiv.className = 'usermessage';
    //     }
    //     chat.appendChild(messageDiv);
    //     chat.scrollTop = chat.scrollHeight;
    // }

    function addMessage(sender, message) {
        const lines = message.split('\n');
        const messageDiv = document.createElement('div');
        if (sender === 'assistant') {
            messageDiv.className = 'aimessage';
        }
        else {
            messageDiv.className = 'usermessage';
        }
        for (let line of lines) {
            const lineDiv = document.createElement('div');
            lineDiv.textContent = line;
            messageDiv.appendChild(lineDiv);
        }
        chat.appendChild(messageDiv);
        chat.scrollTop = chat.scrollHeight;
    }

    function loadThread(threadId) {
        chat.innerHTML = '';
        last_threadId = threadId;
        fetch(`/threads/${threadId}`)
            .then(response => response.json())
            .then(data => {
                data.messages.forEach(msg => {
                    addMessage(msg.sender, msg.content);
                });
            });
    }

    
    async function createThread() {
        const response = await fetch(`/add_thread`);
        const data = await response.json();
        lastThread = data;
        last_threadId = lastThread.id;
        return lastThread.id;
    }
});
