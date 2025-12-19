let currentMenu = [];
let currentState = null; // server-reported game state (e.g. 'INVENTORY_MANAGEMENT')
let isEventMenu = false; // true when the server is showing an active event menu (use/discard/back)

async function sendAction(overrideAction) {
    const inputEl = document.getElementById('player-input');
    let action = typeof overrideAction === 'string' ? overrideAction : inputEl.value;
    inputEl.value = ''; // Clear input

    // If user typed a number, map to menu (1-based displayed)
    const numericMatch = action.trim().match(/^\d+$/);
    if (numericMatch) {
        const idx = parseInt(action.trim(), 10) - 1;
        if (currentMenu && idx >= 0 && idx < currentMenu.length) {
            // If the currently displayed menu is an event menu (use/discard/back)
            // we should send the option string (e.g. "use"). If it's the
            // inventory-selection state, send the numeric index directly so the
            // engine can open the item event.
            if (isEventMenu) {
                action = currentMenu[idx];
            } else if (currentState === 'INVENTORY_MANAGEMENT') {
                action = String(idx);
            } else {
                action = currentMenu[idx];
            }
        }
    }
    try {
        const response = await fetch('/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action })
        });

        if (!response.ok) throw new Error('Server error: ' + response.status);

        var data = await response.json();
    } catch (err) {
        document.getElementById('error-panel').innerText = String(err);
        return;
    }

    // 1. Update Logs (Append to the stream)
    const logPanel = document.getElementById('log-panel');
    (data.logs || []).forEach(msg => {
        logPanel.innerHTML += `<p>> ${msg}</p>`;
    });
    logPanel.scrollTop = logPanel.scrollHeight; // Auto-scroll

    // 2. Update Menu (render numbered clickable list)
    currentMenu = data.menu || [];
    currentState = data.state || null;
    isEventMenu = data.event || false;
    const ol = document.getElementById('options-list');
    ol.innerHTML = '';
    currentMenu.forEach((opt, i) => {
        const li = document.createElement('li');
        li.style.cursor = 'pointer';
        li.dataset.index = i;
        li.innerText = `${i + 1}: ${opt}`;
        // Event menus expect option strings; inventory state expects numeric index selection
        if (isEventMenu) {
            li.addEventListener('click', () => sendAction(opt));
        } else if (currentState === 'INVENTORY_MANAGEMENT') {
            li.addEventListener('click', () => sendAction(String(i)));
        } else {
            li.addEventListener('click', () => sendAction(opt));
        }
        ol.appendChild(li);
    });

    // 3. Update Errors
    document.getElementById('error-panel').innerText = data.error || "";
}

// Initialize UI on load by requesting a describe action to populate menu/logs
window.addEventListener('DOMContentLoaded', () => {
    // Try to get initial state; ignore errors
    (async () => {
        try {
            // Reset server-side state on load so the page shows the initial game
            const resp = await fetch('/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            if (!resp.ok) return;
            const initData = await resp.json();
            const logPanel = document.getElementById('log-panel');
            logPanel.innerHTML = '';
            (initData.logs || []).forEach(m => logPanel.innerHTML += `<p>> ${m}</p>`);
            // populate currentMenu and render
            currentMenu = initData.menu || [];
            currentState = initData.state || null;
            isEventMenu = initData.event || false;
            const ol = document.getElementById('options-list');
            ol.innerHTML = '';
            currentMenu.forEach((opt, i) => {
                const li = document.createElement('li');
                li.style.cursor = 'pointer';
                li.style.marginBottom = '4px';
                li.dataset.index = i;
                li.innerText = `${i + 1}: ${opt}`;
                if (isEventMenu) {
                    li.addEventListener('click', () => sendAction(opt));
                } else if (currentState === 'INVENTORY_MANAGEMENT') {
                    li.addEventListener('click', () => sendAction(String(i)));
                } else {
                    li.addEventListener('click', () => sendAction(opt));
                }
                ol.appendChild(li);
            });
            // focus input
            document.getElementById('player-input').focus();
        } catch (e) {
            // silently fail — backend may be offline
        }
    })();
    // Enter key submits the input
    const inputEl = document.getElementById('player-input');
    inputEl.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            sendAction();
        }
    });
});