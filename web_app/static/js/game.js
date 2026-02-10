import {
  select, 
  listen, 
  create, 
} from './utils.js';
let door = [
    "      ______",
    "   ,-' ;  ! `-.",
    "  / :  !  :  . \\",
    " |_ ;   __:  ;  |",
    " )| .  :)(.  !  |",
    " |\"    (##)  _  |",
    " |  :  ;`'  (_) (",
    " |  :  :  .     |",
    " )_ !  ,  ;  ;  |",
    " || .  .  :  :  |",
    " |\" .  |  :  .  |",
    " |mt-2_;----.___|"
];
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

async function sendAction(overrideAction) {
    let raw = overrideAction ?? inputEl.value.trim();
    inputEl.value = '';

    let action = raw;

    // Numeric shortcut → menu index
    if (/^\d+$/.test(raw)) {
        const idx = parseInt(raw, 10) - 1;
        if (currentMenu[idx]) {
            action = currentMenu[idx].id;
        } else {
            errorPanel.innerText = "Invalid menu selection";
            return;
        }
    }

    try {
        const response = await fetch('/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
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
            
            // Type the text and scroll as we go
            await typeText(p, msg);
            window.scrollTo(0, document.body.scrollHeight);
        }
    }
    
    ol.innerHTML = '';
    currentMenu.forEach((opt, i) => {
        const li = create('li');
        li.className = 'menu-item';
        li.style.cursor = 'pointer';
        li.innerText = `${i + 1}: ${opt.label}`;
        li.onclick = () => sendAction(opt.id);
        ol.appendChild(li);
    });

    errorPanel.innerText = data.error || "";
    inputEl.focus();
    // Final scroll to ensure menu is visible
    window.scrollTo(0, document.body.scrollHeight);
}


// Initial Load
listen('DOMContentLoaded', window, () => {
    (async () => {
    for (let i = 0; i < door.length; i++) {
        const p = create('p');
        p.textContent = '> '; 
        logPanel.appendChild(p);
        await typeText(p, door[i]);
    }
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