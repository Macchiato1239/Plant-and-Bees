from types import SimpleNamespace
import pytest

from Base.build import Base, Path, Spawn
from Manager.buildings import Buildings
from Base.button import Button
from Base.debuff import EffectType
from Base.enemy import Enemy, Enemy_Info
from Base.hotbar import Slot
from Base.entity import Entity
from Base.module_tower import (
    DebuffStats,
    DebuffTower,
    DpsStats,
    DpsTower,
    Farm,
    IncomeStats,
    TowerInfo,
)
from Base.projectile import Projectile
from Base.rect import Rect
from dictionary import Ebook, Tbook
from dictionary import Dictionary, Tower_Dictionary


def test_rect_geometry_mutation_and_drawing(canvas):
    rect = Rect(canvas, 10, 20, 30, 40, "red", "blue", 2)
    assert (rect.cord_x, rect.cord_y) == (25, 40)
    assert rect.cord_overlap_check(15, 25)
    assert not rect.cord_overlap_check(10, 20)
    rect.x1 = 12.5
    rect.y1 = 25
    rect.width = 35
    rect.height = 45
    rect.fill = "green"
    rect.change_color("purple")
    rect.change_color(3)
    assert rect.fill == "purple"
    assert (rect.x1, rect.y1, rect.width, rect.height) == (12.5, 25, 35, 45)
    rect.delete()
    assert rect.rect_id not in canvas.items


def test_entity_properties_and_delete(canvas):
    rect = Rect(canvas, 0, 0, 10, 10)
    item = Entity(rect)
    assert item.rect is rect
    item.cord_x = 20
    item.cord_y = 30.5
    item.cord_x = "invalid"
    item.rect = object()
    assert (item.cord_x, item.cord_y, item.rect) == (25, 35.5, rect)
    replacement = Rect(canvas, 5, 5, 4, 4)
    item.rect = replacement
    assert item.rect is replacement
    item.delete()
    assert replacement.rect_id not in canvas.items


def test_button_and_slot_text_and_tower_assignment(canvas):
    button = Button(canvas, 50, 60, 100, 40, "Go", fill="orange", border_width=3)
    assert button.rect.x1 == 0
    assert canvas.items[button.text]["text"] == "Go"
    button.text = "Ready"
    assert canvas.items[button.text]["text"] == "Ready"
    slot = Slot(canvas, 100, 100, 80, 50)
    assert isinstance(slot, Button)
    assert canvas.items[slot.text]["state"] == "normal"
    assert canvas.items[slot.text]["text"] == "None"
    slot.tower = 1
    assert slot.tower == 1
    assert canvas.items[slot.text]["text"] == Tbook.get(1).name
    slot.tower = None
    assert canvas.items[slot.text]["text"] == "None"


def test_spawn_base_path_and_buildings(canvas):
    spawn = Spawn(canvas, 100, 200)
    base = Base(canvas, 50, 300, 200)
    assert (spawn.rect.cord_x, spawn.rect.cord_y) == (100, 200)
    assert base.health == 50
    base.health = -5
    assert base.health == 0
    base.health = 2.5
    assert base.health == 0
    path = Path(canvas, 10, 30, 110, 80)
    assert (path.start_x, path.start_y, path.end_x, path.end_y) == (10, 30, 110, 80)
    assert path.rect.x1 == -15
    buildings = Buildings(canvas, 100)
    assert len(buildings.paths) == len(buildings.path_points) - 1
    assert buildings.map_length == sum(
        abs(b[0] - a[0]) + abs(b[1] - a[1])
        for a, b in zip(buildings.path_points, buildings.path_points[1:])
    )


def test_enemy_info_and_enemy_movement_and_health(canvas):
    info = Enemy_Info("Bee", 12, 10, "yellow", 8, 6)
    assert (info.name, info.health, info.speed, info.color, info.width, info.height) == (
        "Bee", 12, 10, "yellow", 8, 6
    )
    enemy = Enemy(canvas, "Bee", 0, 0, 10, 10, 12, 10, "yellow")
    assert enemy.name == "Bee"
    assert enemy.health == 12
    assert enemy.reward == 12
    assert enemy.initial_health == 12
    assert enemy.move(canvas, 20, 0, 1) is False
    assert enemy.rect.cord_x == 15
    assert enemy.distance_covered == 10
    assert enemy.move(canvas, 20, 0, 1) is True
    assert enemy.move(canvas, 20, 20, 0.5) is False
    assert enemy.rect.cord_y == 5
    enemy.health = 0
    assert enemy.health == 0


@pytest.mark.parametrize("property_name,value", [
    ("freeze", 2.0), ("freeze_level", 5), ("burn", 1.5),
    ("burn_damage", 3), ("progress", 2),
    ("distance_covered", 12.5), ("speed", 4.0), ("color", "blue"),
])
def test_enemy_mutable_stats(canvas, property_name, value):
    enemy = Enemy(canvas, "Bee", 0, 0, 10, 10, 12, 10, "yellow")
    setattr(enemy, property_name, value)
    expected = min(4, value) if property_name == "freeze_level" else value
    assert getattr(enemy, property_name) == expected


def test_enemy_buff_debuff_and_invalid_setters(canvas):
    enemy = Enemy(canvas, "Bee", 0, 0, 10, 10, 12, 10, "yellow")
    enemy.buff = ["shield"]
    enemy.debuff = [EffectType.FROZEN]
    assert enemy.buff == ["shield"]
    assert enemy.debuff == [EffectType.FROZEN]
    enemy.burn = "invalid"
    enemy.distance_covered = "invalid"
    enemy.health = 1.5
    enemy.speed = "invalid"
    assert enemy.burn == 0
    assert enemy.distance_covered == 0
    assert enemy.health == 12
    assert enemy.speed == 10


def test_enemy_freeze_and_stun_restore_speed(canvas):
    enemy = Enemy(canvas, "Bee", 0, 0, 10, 10, 12, 10, "yellow")
    enemy.freeze = 0.5
    enemy.freeze_level = 2
    enemy.process_debuff(0.25)
    assert enemy.speed == 6
    assert enemy.freeze == 0.25
    enemy.process_debuff(0.25)
    assert enemy.speed == 10
    enemy.freeze = 1
    enemy.freeze_level = 4
    enemy.process_debuff(0)
    enemy.process_debuff(0.1)
    assert enemy.speed == 0
    enemy.process_debuff(0.6)
    assert enemy.speed == 10


def test_enemy_burn_damage_and_full_freeze_stun(canvas):
    enemy = Enemy(canvas, "Bee", 0, 0, 10, 10, 12, 10, "yellow")
    enemy.burn = 2
    enemy.burn_damage = 3
    enemy.burn_tick = 0.5
    enemy.process_debuff(0.6)
    assert enemy.health == 9
    assert enemy.burn == pytest.approx(1.4)
    enemy.freeze = 1
    enemy.freeze_level = 4
    enemy.process_debuff(0.1)
    assert enemy.stun == pytest.approx(0.5)
    assert enemy.freeze_level == 0
    assert enemy.freeze == 0


def test_projectile_reaches_target_and_destroy(canvas):
    projectile = Projectile(canvas, (0, 0), (10, 0), speed=10)
    assert not projectile.update(0.5)
    assert canvas.coords(1) == (1, -4, 9, 4)
    assert projectile.update(0.5)
    projectile.destroy()
    assert 1 not in canvas.items


def test_projectile_zero_distance(canvas):
    projectile = Projectile(canvas, (2, 3), (2, 3))
    assert projectile.update(0)
    projectile.destroy()


def test_tower_models_and_dictionary_summoning(canvas, monkeypatch):
    info = TowerInfo("test", 10, "red", 50, 5, DpsStats(4, 1))
    tower = DpsTower(info, Rect(canvas, 0, 0, 10, 10))
    assert tower.wave_income == 0
    assert (tower.name, tower.size, tower.cost, tower.color, tower.act_range) == (
        "test", 5, 10, "red", 50
    )
    tower.last_act = 0
    assert tower.last_act == 0
    monkeypatch.setattr("Base.module_tower.time.monotonic", lambda: 0.25)
    assert not tower.cooldown_check()
    monkeypatch.setattr("Base.module_tower.time.monotonic", lambda: 2)
    assert tower.cooldown_check()
    assert tower.last_act == 2
    assert tower.fire_rate == 1
    monkeypatch.setattr("Base.module_tower.time.time", lambda: 2)
    tower.last_act = 0
    assert tower.act() == 4
    assert tower.act() is None
    tower.fire_rate = 0.1
    tower.fire_rate = 0
    tower.damage = 8
    tower.damage = 2.5
    assert tower.damage == 8
    tower.cost = 20
    assert tower.cost == 20
    tower.cost = -1
    assert tower.cost == 20
    tower.act_range = 25.5
    assert tower.act_range == 25.5

    debuff_info = TowerInfo(
        "freeze", 12, "blue", 60, 5, DpsStats(2, 0),
        DebuffStats(EffectType.FROZEN, 1, 2),
    )
    debuff = DebuffTower(debuff_info, Rect(canvas, 0, 0, 10, 10))
    assert debuff.type is EffectType.FROZEN
    debuff.magnitude = 2.5
    debuff.duration = 3
    debuff.magnitude = "invalid"
    debuff.duration = None
    assert debuff.magnitude == 2.5 and debuff.duration == 3
    assert debuff.debuff.magnitude == 2.5 and debuff.debuff.duration == 3
    debuff.fire_rate = 1
    debuff.last_act = 2
    assert debuff.act() is None
    frozen_enemy = SimpleNamespace(freeze=0, freeze_level=0)
    debuff.debuff.apply_to(frozen_enemy)
    assert frozen_enemy.freeze == 3 and frozen_enemy.freeze_level == 2.5

    burn_effect = DebuffStats(EffectType.BURN, 4, 2)
    burned_enemy = SimpleNamespace(burn=0, burn_damage=0)
    burn_effect.apply_to(burned_enemy)
    assert burned_enemy.burn == 2 and burned_enemy.burn_damage == 4

    farm_info = TowerInfo("farm", 8, "yellow", 0, 5, income=IncomeStats(100))
    farm = Farm(farm_info, Rect(canvas, 0, 0, 10, 10))
    farm.income = 125
    farm.income = 2.5
    assert farm.income == 125 and farm.wave_income == 125 and farm.act() is None
    from Base.module_tower import Tower
    assert Tower.act(tower) is None
    assert Tbook.summon_tower(1, Rect(canvas, 0, 0, 10, 10)).name == "soldier"
    assert Tbook.summon_tower(2, Rect(canvas, 0, 0, 10, 10)).name == "freezer"
    assert Tbook.summon_tower(4, Rect(canvas, 0, 0, 10, 10)).name == "farm"


def test_dictionary_lookup_and_tower_configuration_errors(canvas, monkeypatch):
    with pytest.raises(KeyError, match="Unknown tower ID: 9999"):
        Tbook.get(9999)
    with pytest.raises(KeyError, match="Unknown tower ID"):
        Tbook.summon_tower(9999, Rect(canvas, 0, 0, 10, 10))
    with pytest.raises(TypeError, match="hashable"):
        Ebook.get([])
    with pytest.raises(ValueError, match="Unsupported tower type"):
        Tbook.add("unknown", 999, "bad", 1, "red", 1, 1)

    monkeypatch.setitem(Tbook.dictionary, 998, ["dps", object()])
    with pytest.raises(AttributeError, match="missing stats"):
        Tbook.summon_tower(998, Rect(canvas, 0, 0, 10, 10))
    monkeypatch.setitem(Tbook.dictionary, 997, ["unknown", None])
    with pytest.raises(ValueError, match="unsupported type"):
        Tbook.summon_tower(997, Rect(canvas, 0, 0, 10, 10))

    with pytest.raises(TypeError):
        Dictionary.get(Ebook, [])
