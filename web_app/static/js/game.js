import {
  select, 
  listen, 
  create, 
} from './utils.js';

let currentMenu = [];
let currentState = null;
let isEventMenu = false;
const errorPanel = select('#error-panel');
const logPanel = select('#log-panel');
const ol = select('#options-list');
const inputEl = select('#player-input');

function getActionValue(index) {
    const opt = currentMenu[index];
    const subMenuCommands = ["use", "discard", "back", "cancel"];
    // Typed command guard function
    if (subMenuCommands.includes(opt.toLowerCase())) {
        return opt;
    }
    // Tracking state from backend to determine whether to use the index or name
    if (currentState === 'INVENTORY_MANAGEMENT') {
        return String(index);
    }
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
        errorPanel.innerText = String(err);
    }
}

function updateUI(data) {
    // Update State
    currentMenu = data.menu || [];
    currentState = data.state || null;
    isEventMenu = data.event || false;
    // Update Logs
    if (data.logs) {
        for (const msg of data.logs) {
            logPanel.innerHTML += `<p>> ${msg}</p>`;
            logPanel.scrollTop = logPanel.scrollHeight;
        }
    }
    // Update Menu Rendering
    ol.innerHTML = '';
    currentMenu.forEach((opt, i) => {
        const li = create('li');
        li.className = 'menu-item'; // Use classes for styling
        li.style.cursor = 'pointer';
        li.innerText = `${i + 1}: ${opt}`;
        
        // Use the same logic as keyboard input for consistency
        li.onclick = () => sendAction(getActionValue(i));
        ol.appendChild(li);
    });

    errorPanel.innerText = data.error || "";
}

// Initial Load
listen('DOMContentLoaded', window, () => {
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

    listen('keydown', inputEl, (ev) => {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            sendAction();
        }
    });
});