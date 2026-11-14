try:
    from Head.game import Game
except ModuleNotFoundError as error:
    module_name = error.name or "unknown module"
    raise SystemExit(
        f"Cannot start the game because {module_name!r} could not be imported. "
        "Check that project packages are named consistently and Tkinter is installed."
    ) from error

gameplay=Game()

gameplay.start()
