"""Launcher for python_dungeon project.

Usage:
  - default: runs the web app (`FLASK` mode) using Flask
  - set environment variable `PYDUNGEON_MODE=cli` to run the CLI loop
"""

import os


def run_web():
	from web_app.app import app
	app.run(debug=True)


def run_cli():
	# importing game_engine.main runs the CLI loop
	import game_engine.main


if __name__ == "__main__":
	mode = os.getenv("PYDUNGEON_MODE", "web").lower()
	if mode == "cli":
		run_cli()
	else:
		run_web()
