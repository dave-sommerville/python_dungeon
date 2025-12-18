async function sendAction() {
    const inputEl = document.getElementById('player-input');
    const action = inputEl.value;
    inputEl.value = ''; // Clear input

    const response = await fetch('/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    });

    const data = await response.json();

    // 1. Update Logs (Append to the stream)
    const logPanel = document.getElementById('log-panel');
    data.logs.forEach(msg => {
        logPanel.innerHTML += `<p>> ${msg}</p>`;
    });
    logPanel.scrollTop = logPanel.scrollHeight; // Auto-scroll

    // 2. Update Menu
    document.getElementById('options-list').innerText = data.menu.join(", ");

    // 3. Update Errors
    document.getElementById('error-panel').innerText = data.error || "";
}