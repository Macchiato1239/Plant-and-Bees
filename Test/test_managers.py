from types import SimpleNamespace

import pytest

from Base.build import Spawn
from Base.enemy import Enemy
from Base.rect import Rect
from Manager.collision import CollisionManager
from Manager.difficulty import Difficulty, diff, make_wave
from Manager.display import Display
from Manager.enemymanager import EnemyManager
from Manager.hotbarmanager import HotBarManager
from Manager.mouseevent import MouseHandler
from Manager.towermanager import TowerManager


def test_collision_hit_testing_and_distances(canvas):
    collision = CollisionManager()
    rect = Rect(canvas, 10, 20, 30, 40)
    collision.taken.append(rect)
    assert collision.compare_cord_rect(15, 25, collision.taken)
    assert not collision.compare_cord_rect(10, 20, collision.taken)
    assert collision.dist_cord_cord(rect, Rect(canvas, 40, 60, 0, 0)) == pytest.approx(25)
    item = SimpleNamespace(rect=rect)
    collision.interactive.append(item)
    assert collision.interactive_at(15, 25) is item
    assert collision.interactive_at(100, 100) is None
    assert collision.range_enemy_tower(
        SimpleNamespace(rect=rect), SimpleNamespace(rect=rect, act_range=0)
    )
    assert not collision.range_enemy_tower(
        SimpleNamespace(rect=rect),
        SimpleNamespace(rect=Rect(canvas, 100, 100, 2, 2), act_range=1),
    )


def test_difficulty_storage_and_wave_builder():
    store = Difficulty()
    store.add("custom", [[1, 0]])
    assert store.get("custom") == [[1, 0]]
    with pytest.raises(KeyError):
        store.get("missing")
    assert make_wave((1, 2, 0.5), (2, 1, 0.8)) == [[1, 0.5], [1, 0.5], [2, 0]]
    assert make_wave() == []
    assert len(diff.get("normal")) < len(diff.get("hard")) < len(diff.get("insane"))


def test_hotbar_slots_equipping_and_colors(canvas, monkeypatch):
    from dictionary import Tbook

    monkeypatch.setitem(Tbook.dictionary, 5, Tbook.dictionary[1])
    monkeypatch.setitem(Tbook.dictionary, 6, Tbook.dictionary[1])
    collision = CollisionManager()
    hotbar = HotBarManager(canvas, collision)
    hotbar.create_slots()
    assert len(hotbar.hotbar) == 5
    assert len(collision.interactive) == 5
    assert hotbar.hotbar[0].tower is None
    hotbar.equip_tower("bad")
    hotbar.equip_tower(1)
    hotbar.equip_tower(2)
    assert hotbar.hotbar[0].tower == 1
    assert hotbar.hotbar[1].tower == 2
    assert hotbar.contains(hotbar.hotbar[0])
    hotbar.update_colors()
    assert hotbar.hotbar[0].rect.fill == "#bd7e1a"
    assert hotbar.hotbar[4].rect.fill == "black"
    hotbar.equip_tower(3)
    hotbar.equip_tower(4)
    hotbar.equip_tower(5)
    hotbar.equip_tower(6)
    assert hotbar.equipped_towers == [2, 3, 4, 5, 6]
    assert hotbar.hotbar[0].tower == 2
    hotbar.create_slots()
    assert len(collision.interactive) == 5


def test_display_text_and_range_visibility(canvas):
    display = Display(canvas, 100, 20, 3)
    assert canvas.items[display.money_display]["text"] == "Cash: 100"
    assert canvas.items[display.health_display]["text"] == "Health: 20"
    display.money_display = 75
    display.health_display = 10
    display.wave_display = "Wave 2/3"
    display.next_wave_display = "Next wave in: 2s"
    assert canvas.items[display.money_display]["text"] == "Cash: 75"
    assert canvas.items[display.health_display]["text"] == "Health: 10"
    assert canvas.items[display.wave_display]["text"] == "Wave 2/3"
    assert canvas.items[display.next_wave_display]["text"] == "Next wave in: 2s"
    display.show_range(10, 20, None)
    assert canvas.items[display.range_circle]["state"] == "hidden"
    display.show_range(10, 20, __import__("dictionary").Tbook.get(1))
    assert canvas.items[display.range_circle]["coords"] == (-190, -180, 210, 220)
    assert canvas.items[display.space_taken_rect]["state"] == "normal"


def test_mouse_handler_forwards_events():
    calls = []

    class Target:
        def handle_key(self, event):
            calls.append(("key", event))

        def handle_click(self, event):
            calls.append(("click", event))

        def update_range_display(self, event):
            calls.append(("motion", event))

    handler = MouseHandler(Target())
    event = object()
    handler.on_key_press(event)
    handler.interact_with_ui(event)
    handler.track_display_range(event)
    assert calls == [("key", event), ("click", event), ("motion", event)]


@pytest.fixture
def tower_setup(canvas):
    collision = CollisionManager()
    manager = TowerManager(canvas, collision)
    return manager, collision


def test_tower_selection_placement_validation_and_deletion(tower_setup):
    manager, collision = tower_setup
    assert manager.selected_tower_info is None
    assert manager.place_tower(100, 100, 1000) == (False, 1000)
    manager.select_tower_card(1)
    manager.cancel_selection()
    manager.select_tower_card(9999)
    assert manager.current_tower is None
    with pytest.raises(TypeError, match="numeric"):
        manager.place_tower("x", 100, 1000)
    manager.select_tower_card(1)
    assert manager.selected_tower_info.name == "soldier"
    manager.investigate_tower(SimpleNamespace(x=100, y=100))
    assert manager.place_tower(100, 100, 10) == (False, 10)
    assert manager.current_tower is None
    manager.select_tower_card(1)
    collision.taken.append(Rect(manager._TowerManager__canvas, 70, 70, 60, 60))
    assert manager.place_tower(100, 100, 1000) == (False, 1000)
    manager.cancel_selection()
    collision.taken.clear()
    manager.select_tower_card(1)
    placed, remaining = manager.place_tower(100, 100, 1000)
    assert placed and remaining == 750
    tower = manager.active_towers[0]
    assert tower.rect in collision.taken
    manager.investigate_tower(SimpleNamespace(x=100, y=100))
    manager.delete_tower()
    assert manager.active_towers == []
    assert tower.rect not in collision.taken
    manager.delete_tower()


def test_tower_manager_farm_income_and_projectile_debuff(tower_setup, monkeypatch, canvas):
    manager, collision = tower_setup
    manager.select_tower_card(4)
    assert manager.place_tower(100, 100, 1000) == (True, 800)
    assert manager.farm_income_per_wave == 100
    manager.select_tower_card(2)
    assert manager.place_tower(200, 100, 1000)[0]
    enemy = Enemy(canva=manager._TowerManager__canvas, name="target", x1=190, y1=90,
                  width=20, height=20, health=50, speed=1, color="green")
    enemy.distance_covered = 3
    monkeypatch.setattr("Base.module_tower.time.time", lambda: 10)
    collision.range_enemy_tower = lambda target, tower: True
    manager.update([enemy], collision, 0.1)
    assert enemy.health == 45
    assert enemy.freeze == 0.4
    assert enemy.freeze_level == 1
    assert len(manager._TowerManager__projectiles) == 1
    manager.update([], collision, 1)
    assert manager._TowerManager__projectiles == []


def test_tower_manager_max_count_and_target_sorter(tower_setup):
    manager, _ = tower_setup
    manager._TowerManager__max_active_towers = 0
    manager.select_tower_card(1)
    assert manager.place_tower(100, 100, 1000) == (False, 1000)
    assert TowerManager._TowerManager__enemy_sorter([]) == 0
    first = SimpleNamespace(distance_covered=1)
    second = SimpleNamespace(distance_covered=5)
    assert TowerManager._TowerManager__enemy_sorter([first, second]) is second


def test_tower_manager_ignores_support_towers_and_out_of_range_targets(tower_setup):
    from Base.module_tower import Tower, TowerInfo

    manager, collision = tower_setup

    class SupportTower(Tower):
        def act(self):
            return None

    support = SupportTower(TowerInfo("support", 1, "white", 1, 2),
                           Rect(manager._TowerManager__canvas, 0, 0, 10, 10))
    manager.active_towers.append(support)
    manager.update([], collision, 0)

    manager.select_tower_card(1)
    assert manager.place_tower(100, 100, 1000)[0]
    shooter = manager.active_towers[-1]
    shooter.act = lambda: 5
    manager.update([], collision, 0)
    assert manager._TowerManager__projectiles == []


def test_enemy_manager_wave_spawn_rewards_break_and_completion(canvas, monkeypatch, event):
    monkeypatch.setattr(diff, "get", lambda key: [
        [[1, 0]], [[2, 0]],
    ])
    spawn = Spawn(canvas, 0, 0)
    manager = EnemyManager(canvas, 1, spawn, [(0, 0), (100, 0)])
    assert manager.display_wave == "Wave 1/2"
    assert manager.next_wave_countdown == ""
    assert manager.update(0, canvas) == 0
    assert len(manager.active_enemies) == 1
    reward = manager.active_enemies[0].reward
    manager.active_enemies[0].health = 0
    assert manager.update(0, canvas) == reward
    assert manager.completed_waves == 1
    assert manager.next_wave_countdown == "Next wave in: 3s"
    manager.update(1.2, canvas)
    assert manager.next_wave_countdown == "Next wave in: 2s"
    manager.update(1.8, canvas)
    assert len(manager.active_enemies) == 1
    manager.active_enemies[0].health = 0
    manager.update(0, canvas)
    assert manager.is_complete
    assert manager.completed_waves == 2
    assert manager.display_wave == "Wave 2/2"


def test_enemy_manager_base_damage_branch(canvas, monkeypatch):
    monkeypatch.setattr(diff, "get", lambda key: [[ [1, 0] ]])
    spawn = Spawn(canvas, 0, 0)
    manager = EnemyManager(canvas, 1, spawn, [(0, 0), (10, 0)])
    enemy = manager.spawn(__import__("dictionary").Ebook.get(1))
    manager._EnemyManager__time_til_next_spawn = 100
    enemy.progress = 1
    enemy.rect.x1 = 10 - enemy.rect.width / 2
    manager.update(0, canvas)
    assert manager.base_damage == 6
    assert enemy not in manager.active_enemies


@pytest.mark.parametrize("level,key", [(1, "normal"), (2, "hard"), (3, "insane")])
def test_enemy_manager_difficulty_accessors(canvas, level, key):
    manager = EnemyManager(canvas, level, Spawn(canvas, 0, 0), [(0, 0)])
    assert manager.game_info == diff.get(key)
    manager.base_damage = 5
    assert manager.base_damage == 5
    manager.base_damage = "invalid"
    assert manager.base_damage == 5


def test_enemy_manager_spawns_multiple_enemies_in_wave(canvas, monkeypatch):
    monkeypatch.setattr(diff, "get", lambda key: [[[1, 0.5], [2, 0]]])
    manager = EnemyManager(canvas, 1, Spawn(canvas, 0, 0), [(0, 0), (100, 0)])
    manager.update(0, canvas)
    assert len(manager.active_enemies) == 1
    manager.update(0.25, canvas)
    assert len(manager.active_enemies) == 1
    manager.update(0.25, canvas)
    assert len(manager.active_enemies) == 2
    rewards = sum(enemy.reward for enemy in manager.active_enemies)
    for enemy in manager.active_enemies:
        enemy.health = 0
    assert manager.update(0, canvas) == rewards
    assert manager.is_complete


def test_enemy_manager_rejects_bad_difficulty_and_delta(canvas):
    spawn = Spawn(canvas, 0, 0)
    with pytest.raises(TypeError, match="difficulty_level"):
        EnemyManager(canvas, "hard", spawn, [(0, 0)])
    with pytest.raises(ValueError, match=r"1 \(normal\)"):
        EnemyManager(canvas, 9, spawn, [(0, 0)])
    manager = EnemyManager(canvas, 1, spawn, [(0, 0)])
    with pytest.raises(TypeError, match="delta_time"):
        manager.update("fast", canvas)
    with pytest.raises(ValueError, match="negative"):
        manager.update(-1, canvas)


def test_enemy_manager_reports_malformed_wave_enemy_and_path_data(canvas, monkeypatch):
    spawn = Spawn(canvas, 0, 0)

    monkeypatch.setattr(diff, "get", lambda key: [[[1]]])
    malformed_wave = EnemyManager(canvas, 1, spawn, [(0, 0)])
    with pytest.raises(ValueError, match="wave entry"):
        malformed_wave.update(0, canvas)

    monkeypatch.setattr(diff, "get", lambda key: [[[999, 0]]])
    unknown_enemy = EnemyManager(canvas, 1, spawn, [(0, 0)])
    with pytest.raises(KeyError, match="Enemy_Dictionary"):
        unknown_enemy.update(0, canvas)

    monkeypatch.setattr(diff, "get", lambda key: [[ [[], 0] ]])
    invalid_enemy_key = EnemyManager(canvas, 1, spawn, [(0, 0)])
    with pytest.raises(TypeError, match="hashable"):
        invalid_enemy_key.update(0, canvas)

    monkeypatch.setattr(diff, "get", lambda key: [[[1, 0]]])
    bad_index = EnemyManager(canvas, 1, spawn, [(0, 0)])
    bad_index._EnemyManager__wave_progress = 2
    with pytest.raises(IndexError, match="Wave data"):
        bad_index.update(0, canvas)

    bad_path = EnemyManager(canvas, 1, spawn, [(0, 0)])
    bad_path._EnemyManager__game_progress = -1
    bad_path.active_enemies.append(SimpleNamespace(
        progress=5, health=10, process_debuff=lambda dt: None
    ))
    with pytest.raises(IndexError, match="path progress"):
        bad_path.update(0, canvas)

    malformed_path = EnemyManager(canvas, 1, spawn, [(0,)])
    malformed_path._EnemyManager__game_progress = -1
    malformed_path.active_enemies.append(SimpleNamespace(
        progress=0, health=10, process_debuff=lambda dt: None
    ))
    with pytest.raises(ValueError, match="path point"):
        malformed_path.update(0, canvas)

    with pytest.raises(AttributeError, match="enemy_info"):
        bad_path.spawn(object())

