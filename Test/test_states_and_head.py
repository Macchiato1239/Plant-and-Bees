from types import SimpleNamespace

import pytest
from conftest import FakeCanvas, FakeWidget

import Head.game as game_module
import Head.module_window as window_module
from Head.game import Game
from Head.module_window import Window
from Head.states import GameState, State
from Manager.collision import CollisionManager
from States.gameflow import GameFlow
from States.gameover import GameOverState
from States.lose import LostState
from States.menu import MenuState
from States.pause import PausedState
from States.victory import VictoryState


@pytest.mark.parametrize("state", list(State))
def test_state_enum_has_distinct_members(state):
    assert state in State


def test_window_creation_and_validated_properties(monkeypatch):
    fake_root = FakeWidget()
    fake_canvas = FakeCanvas()
    monkeypatch.setattr(window_module.tk, "Tk", lambda: fake_root)
    monkeypatch.setattr(window_module.tk, "Canvas", lambda *a, **k: fake_canvas)
    window = Window()
    assert window.window is fake_root
    assert window.canva is fake_canvas
    assert window.window_width == 1000 and window.window_height == 700
    window.window_width = 1200
    window.window_height = 800
    window.bg_color = "pink"
    window.running = False
    window.window_width = "invalid"
    window.window_height = 3.5
    window.bg_color = 10
    window.running = 1
    window.create_window()
    assert fake_root.geometry_value == "1200x800"
    assert fake_canvas.packed
    assert window.bg_color == "pink" and not window.running


def test_menu_state_lifecycle_actions_and_difficulty(window, event):
    menu = MenuState(window)
    menu.enter()
    assert len(menu._MenuState__collision.interactive) == 3
    assert menu.handle_click(event(500, 220)) == "play"
    assert menu.handle_click(event(500, 310)) == "difficulty"
    menu.cycle_difficulty()
    assert menu.difficulty == 2
    assert window.canva.items[menu._MenuState__difficulty_button.text]["text"] == "Difficulty: Hard"
    for _ in range(2):
        menu.cycle_difficulty()
    assert menu.difficulty == 1
    assert menu.handle_click(event(500, 400)) == "quit"
    menu.exit()
    assert menu._MenuState__collision.interactive == []
    assert menu.handle_click(event(20, 20)) is None


@pytest.mark.parametrize("state_cls,title", [
    (LostState, "Game Over"), (VictoryState, "Victory!"),
])
def test_terminal_state_actions_and_visibility(window, event, state_cls, title):
    state = state_cls(window)
    state.enter()
    assert state.handle_click(event(500, 350)) == "menu"
    assert state.handle_click(event(500, 415)) == "restart"
    assert state.handle_click(event(20, 20)) is None
    state._GameOverState__collision.interactive.append(
        SimpleNamespace(rect=SimpleNamespace(x1=0, y1=0, width=10, height=10))
    )
    assert state.handle_click(event(5, 5)) is None
    state.exit()
    assert state._GameOverState__collision.interactive == []
    assert window.canva.items[state._GameOverState__title]["text"] == title


def test_pause_state_resume_menu_restart(window, event):
    pause = PausedState(window)
    pause.enter()
    assert pause.handle_click(event(500, 315)) == "resume"
    assert pause.handle_click(event(500, 375)) == "menu"
    assert pause.handle_click(event(500, 435)) == "restart"
    pause.exit()


def test_gameflow_initialization_loop_and_gameplay_clicks(window, monkeypatch, event):
    class FakeEnemies:
        game_info = [[[]]]
        active_enemies = []
        completed_waves = 0
        display_wave = "Wave 1/1"
        next_wave_countdown = ""
        base_damage = 0
        is_complete = False

        def __init__(self, *args):
            pass

        def update(self, delta_time, canvas):
            return 0

    monkeypatch.setattr("States.gameflow.EnemyManager", FakeEnemies)
    outcomes = []
    game = GameFlow(window, 1, outcomes.append)
    assert not game._GameFlow__towers.active_towers
    game.create_game_loop()
    assert len(game._GameFlow__hotbar.hotbar) == 5
    assert window.window.after_calls
    game.handle_click(event(115, 635))
    assert game._GameFlow__towers.current_tower == 1
    game.handle_click(event(700, 200))
    assert len(game._GameFlow__towers.active_towers) == 1
    game.handle_click(event(500, 200))
    game.handle_click(event(115, 635))
    game.handle_key(SimpleNamespace(keysym="q"))
    game.handle_key(SimpleNamespace(keysym="x"))
    assert game._GameFlow__towers.current_tower is None
    game.update_range_display(event(10, 10))
    game.exit()
    game.handle_click(event(115, 635))
    assert game._GameFlow__towers.current_tower is None
    game.cleanup()
    assert game._GameFlow__disposed
    assert not window.canva.items
    game.cleanup()
    game.create_game_loop()
    game.game_loop()


def test_gameflow_lifecycle_edge_paths(window, monkeypatch):
    import tkinter as tk

    class FakeEnemies:
        game_info = [[]]
        active_enemies = []
        completed_waves = 1
        display_wave = "Wave 1/1"
        next_wave_countdown = ""
        base_damage = 0
        is_complete = False

        def __init__(self, *args):
            pass

        def update(self, delta_time, canvas):
            return 0

    monkeypatch.setattr("States.gameflow.EnemyManager", FakeEnemies)
    outcomes = []
    game = GameFlow(window, 1, outcomes.append)
    game.enter()
    from dictionary import Tbook
    from Base.rect import Rect
    game._GameFlow__towers.active_towers.append(
        Tbook.summon_tower(4, Rect(window.canva, 700, 100, 10, 10))
    )
    game.game_loop()
    assert game._GameFlow__money == 850
    assert window.window.after_calls

    def raise_tcl_error(after_id):
        raise tk.TclError(after_id)

    monkeypatch.setattr(window.window, "after_cancel", raise_tcl_error)
    game.cleanup()
    assert game._GameFlow__disposed

    stopped_window = type(window)()
    stopped = GameFlow(stopped_window, 1, outcomes.append)
    stopped_window.running = False
    stopped.game_loop()
    assert stopped_window.window.destroyed


def test_gameflow_game_loop_returns_on_terminal_condition(window, monkeypatch):
    class FakeEnemies:
        game_info = [[]]
        active_enemies = []
        completed_waves = 0
        display_wave = "Wave 1/1"
        next_wave_countdown = ""
        base_damage = 0
        is_complete = False

        def __init__(self, *args):
            pass

        def update(self, delta_time, canvas):
            return 0

    monkeypatch.setattr("States.gameflow.EnemyManager", FakeEnemies)
    outcomes = []
    game = GameFlow(window, 1, outcomes.append)
    game._GameFlow__base_health = 0
    game.game_loop()
    assert outcomes == [State.LOST]
    assert window.window.after_calls == []


def test_gameflow_victory_and_lose_conditions(window, monkeypatch):
    class FakeEnemies:
        game_info = [[]]
        active_enemies = []
        completed_waves = 0
        display_wave = "Wave 1/1"
        next_wave_countdown = ""
        base_damage = 0
        is_complete = False

        def __init__(self, *args):
            pass

        def update(self, delta_time, canvas):
            return 0

    monkeypatch.setattr("States.gameflow.EnemyManager", FakeEnemies)
    outcomes = []
    game = GameFlow(window, 1, outcomes.append)
    game._GameFlow__base_health = 0
    assert game.game_over_check()
    assert outcomes == [State.LOST]
    game._GameFlow__base_health = 100
    game._GameFlow__enemies.is_complete = True
    assert game.game_over_check()
    assert outcomes[-1] == State.VICTORY


def test_game_state_router_menu_finish_restart_and_return(window, monkeypatch, event):
    # Construct the real Game against fake Tk-backed objects.
    monkeypatch.setattr(game_module, "Window", lambda: window)

    class FakeFlow:
        def __init__(self, window_obj, difficulty, finish):
            self.finish = finish
            self.entered = False
            self.cleaned = False
            self.clicks = []

        def create_game_loop(self):
            pass

        def handle_click(self, event):
            self.clicks.append(event)

        def enter(self):
            self.entered = True

        def exit(self):
            self.entered = False

        def cleanup(self):
            self.cleaned = True

    monkeypatch.setattr(game_module, "GameFlow", FakeFlow)
    game = Game()
    game.start()
    game.click_manager(event(500, 310))
    game.click_manager(event(500, 310))
    game.click_manager(event(500, 220))
    assert game._Game__state is State.PLAYING
    old_game = game._Game__game
    game.click_manager(event(100, 100))
    assert len(old_game.clicks) == 1
    game.finish_game(State.VICTORY)
    assert game._Game__state is State.VICTORY
    game.click_manager(event(500, 415))
    assert old_game.cleaned
    assert game._Game__state is State.PLAYING
    game.finish_game(State.LOST)
    game.click_manager(event(500, 350))
    assert game._Game__state is State.MENU
    assert game._Game__game is None
    game.finish_game(State.VICTORY)
    game._Game__state = None
    assert game.click_manager(event(20, 20)) is None
    game._Game__state = State.MENU
    game.click_manager(event(500, 400))
    assert window.window.destroyed


def test_game_pause_toggle_and_quit(window, monkeypatch, event):
    monkeypatch.setattr(game_module, "Window", lambda: window)
    game = Game()
    game._Game__state = State.PLAYING

    class CurrentGame:
        def __init__(self):
            self.exited = 0
            self.entered = 0

        def exit(self):
            self.exited += 1

        def enter(self):
            self.entered += 1

    current = CurrentGame()
    game._Game__game = current
    game.toggle_pause(SimpleNamespace(keysym="r"))
    assert game._Game__state is State.PAUSED and current.exited == 1
    game.toggle_pause(SimpleNamespace(keysym="r"))
    assert game._Game__state is State.PLAYING and current.entered == 1
    game.toggle_pause(SimpleNamespace(keysym="escape"))
    assert game._Game__state is State.PLAYING
    game.toggle_pause(SimpleNamespace(keysym="r"))
    game.click_manager(event(500, 315))
    assert game._Game__state is State.PLAYING and current.entered == 2
    game.quit(SimpleNamespace(keysym="s"))
    assert window.window.destroyed
    game.quit(SimpleNamespace(keysym="a"))


def test_abstract_base_methods_are_defined_as_noops(window):
    class ConcreteState(GameState):
        def enter(self):
            return "entered"

        def exit(self):
            return "exited"

        def handle_click(self, event):
            return event

    instance = ConcreteState(window)
    assert instance.window is window
    assert GameState.enter(instance) is None
    assert GameState.exit(instance) is None
    assert GameState.handle_click(instance, None) is None

    from dictionary import Dictionary
    assert Dictionary.add() is None
