let currentMenu = [];
let currentState = null;
let isEventMenu = false;
const inputEl = document.getElementById('player-input');

// Helper to determine if we should send an index or a string
function getActionValue(index) {
    const opt = currentMenu[index];
    const subMenuCommands = ["use", "discard", "back", "cancel"];
    
    // 1. If it's a specific navigation command, always send the string
    if (subMenuCommands.includes(opt.toLowerCase())) {
        return opt;
    }

    // 2. If we are in inventory selection, the server usually wants the index
    if (currentState === 'INVENTORY_MANAGEMENT') {
        return String(index);
    }

    // 3. Default to sending the string (for Combat, Movement, etc.)
    return opt;
}

async function sendAction(overrideAction) {
    let action = typeof overrideAction === 'string' ? overrideAction : inputEl.value;
    inputEl.value = '';

    // Handle numeric keyboard input
    const numericMatch = action.trim().match(/^\d+$/);
    if (numericMatch) {
        const idx = parseInt(action.trim(), 10) - 1;
        if (currentMenu && idx >= 0 && idx < currentMenu.length) {
            action = getActionValue(idx);
        }
    }

    try {
        const response = await fetch('/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action })
        });

        if (!response.ok) throw new Error('Server error: ' + response.status);
        const data = await response.json();
        updateUI(data);
    } catch (err) {
        document.getElementById('error-panel').innerText = String(err);
    }
}

function updateUI(data) {
    // Update State
    currentMenu = data.menu || [];
    currentState = data.state || null;
    isEventMenu = data.event || false;

    // Update Logs
    const logPanel = document.getElementById('log-panel');
    if (data.logs) {
        data.logs.forEach(msg => {
            logPanel.innerHTML += `<p>> ${msg}</p>`;
        });
        logPanel.scrollTop = logPanel.scrollHeight;
    }

    // Update Menu Rendering
    const ol = document.getElementById('options-list');
    ol.innerHTML = '';
    currentMenu.forEach((opt, i) => {
        const li = document.createElement('li');
        li.className = 'menu-item'; // Use classes for styling
        li.style.cursor = 'pointer';
        li.innerText = `${i + 1}: ${opt}`;
        
        // Use the same logic as keyboard input for consistency
        li.onclick = () => sendAction(getActionValue(i));
        
        ol.appendChild(li);
    });

    document.getElementById('error-panel').innerText = data.error || "";
}

// Initial Load
window.addEventListener('DOMContentLoaded', () => {
    (async () => {
        try {
            const resp = await fetch('/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            const initData = await resp.json();
            updateUI(initData);
            inputEl.focus();
        } catch (e) {
            console.error("Initialization failed", e);
        }
    })();

    inputEl.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            sendAction();
        }
    });
});