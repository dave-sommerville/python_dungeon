from game_engine import GameEngine
from locations.dungeon import Dungeon
from game_states import GameState

engine = GameEngine()
dungeon = Dungeon()

print("=== Dungeon Crawler Started ===")

while dungeon.state != GameState.GAME_OVER:
    # 1. Describe the world
    print("\n------------------------")
    print(dungeon.player.current_chamber.describe_chamber())

    # 2. Show menu
    options = GameEngine.get_current_menu(dungeon)
    print("\nWhat do you do?")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    # 3. Get input
    try:
        choice = int(input("> ")) - 1
        action = options[choice]
    except (ValueError, IndexError):
        print("Invalid selection.")
        continue

    # 4. Resolve action
    engine.resolve_action(dungeon, action)


