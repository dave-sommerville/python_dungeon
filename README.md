# Python Dungeon

Small dungeon-crawler project with a Flask API and a CLI runner.

Quick setup

- Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# or .venv\Scripts\activate.bat for cmd.exe
```

- Install dependencies from the package folder:

```bash
python -m pip install -r requirements.txt
```

Run the web server (default)

```bash
cd python_dungeon\python_dungeon
python run.py
```

The Flask app listens on http://127.0.0.1:5000 and exposes an endpoint:

- `POST /action` — JSON body: `{ "action": "describe" }`

Example request (PowerShell):

```powershell
$body = @{ action = 'describe' } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:5000/action -Method Post -Body $body -ContentType 'application/json'
```

Run the CLI loop

```powershell
cd python_dungeon\python_dungeon
set PYDUNGEON_MODE=cli
python run.py
```

Notes

- Development server: the Flask server runs in debug mode — do not use it in production.
- If you hit import errors, ensure you run Python from the `python_dungeon\python_dungeon` folder so package-relative imports resolve correctly.
- Code is in `game_engine` and `web_app` directories; `run.py` chooses between web and cli modes.

If you want, tell me which additional docs or example flows you'd like added.
