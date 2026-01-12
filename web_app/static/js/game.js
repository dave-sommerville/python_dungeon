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
const actionForm = select('#action-form'); // Target the form

function typeText(element, text, speed = 5) {
    const str = String(text || "");
    return new Promise((resolve) => {
        if (str.length === 0) return resolve();
        let i = 0;
        const interval = setInterval(() => {
            if (i < str.length) {
                element.textContent += str[i];
                i++;
            }
            if (i >= str.length) {
                clearInterval(interval);
                resolve();
            }    
        }, speed);
    });
}
function getActionValue(index) {
    const opt = currentMenu[index];
    const subMenuCommands = ["use", "discard", "back", "cancel"];
    if (subMenuCommands.includes(opt.toLowerCase())) {
        return opt;
    }
    if (currentState === 'INVENTORY_MANAGEMENT') {
        return String(index);
    }
    return opt;
}
async function sendAction(overrideAction) {
    let action = typeof overrideAction === 'string' ? overrideAction : inputEl.value;
    inputEl.value = '';
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
        await updateUI(data);
    } catch (err) {
        errorPanel.innerText = String(err);
    }
}
async function updateUI(data) {
    currentMenu = data.menu || [];
    currentState = data.state || null;
    isEventMenu = data.event || false;
    if (data.logs) {
        for (const msg of data.logs) {
            const p = create('p');
            p.textContent = '> '; 
            logPanel.appendChild(p);
            await typeText(p, msg);
        }
    }
    ol.innerHTML = '';
    currentMenu.forEach((opt, i) => {
        const li = create('li');
        li.className = 'menu-item';
        li.style.cursor = 'pointer';
        li.innerText = `${i + 1}: ${opt}`;
        li.onclick = () => sendAction(getActionValue(i));
        ol.appendChild(li);
    });

    errorPanel.innerText = data.error || "";
    inputEl.focus();
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
            await updateUI(initData);
        } catch (e) {
            console.error("Initialization failed", e);
        }
    })();

    listen('submit', actionForm, (ev) => {
        ev.preventDefault(); 
        sendAction();
    });
});