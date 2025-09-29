document.getElementById('addTextBtn').addEventListener('click', async () => {
    const text = document.getElementById('inputText').value;
    try {
        await fetch('http://localhost:8000/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
    } catch (error) {
        console.error('Error sending request:', error);
    }
});

document.getElementById('askBtn').addEventListener('click', async () => {
    const text = document.getElementById('queryInput').value;
    try {
        const response = await fetch(`http://localhost:8000/ask?text=${encodeURIComponent(text)}`, {
            method: 'GET'
        });
        const result = await response.text();
        console.log('Server response:', result);
    } catch (error) {
        console.error('Error sending request:', error);
    }
});
