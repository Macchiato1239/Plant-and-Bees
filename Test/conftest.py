from types import SimpleNamespace
import sys
import types
import pytest


# Some Python installations ship tkinter.py without the optional _tkinter
# extension. The game only needs Tk constructors at startup, so provide
# placeholders for unit tests that use FakeCanvas and FakeWindow instead.
try:
    import tkinter  # noqa: F401
except ModuleNotFoundError:
    tkinter_stub = types.ModuleType("tkinter")
    tkinter_stub.TclError = type("TclError", (Exception,), {})
    tkinter_stub.Tk = lambda: None
    tkinter_stub.Canvas = lambda *args, **kwargs: None
    sys.modules["tkinter"] = tkinter_stub


class FakeCanvas:
    '''Small in-memory stand-in for the Tk canvas API used by the game.'''

    def __init__(self):
        self.items = {}
        self.next_id = 1
        self.bindings = {}
        self.after_calls = []

    def _create(self, kind, coords, options):
        item_id = self.next_id
        self.next_id += 1
        self.items[item_id] = {"kind": kind, "coords": tuple(coords), **options}
        return item_id

    def create_rectangle(self, *coords, **options):
        return self._create("rectangle", coords, options)

    def create_oval(self, *coords, **options):
        return self._create("oval", coords, options)

    def create_text(self, *coords, **options):
        return self._create("text", coords, options)

    def coords(self, item_id, *coords):
        if coords:
            self.items[item_id]["coords"] = tuple(coords)
        return self.items[item_id]["coords"]

    def itemconfig(self, item_id, **options):
        self.items[item_id].update(options)

    itemconfigure = itemconfig

    def move(self, item_id, dx, dy):
        coords = self.items[item_id]["coords"]
        self.items[item_id]["coords"] = tuple(
            value + (dx if index % 2 == 0 else dy)
            for index, value in enumerate(coords)
        )

    def delete(self, item_id):
        self.items.pop(item_id, None)

    def find_all(self):
        return tuple(self.items)

    def tag_raise(self, item_id):
        return item_id

    def pack(self):
        self.packed = True

    def bind(self, sequence, callback, add=None):
        binding_id = f"binding-{len(self.bindings) + 1}"
        self.bindings[(sequence, binding_id)] = callback
        return binding_id

    def unbind(self, sequence, binding_id=None):
        self.bindings.pop((sequence, binding_id), None)


class FakeWidget:
    def __init__(self):
        self.bindings = {}
        self.after_calls = []
        self.cancelled = []
        self.destroyed = False

    def bind(self, sequence, callback, add=None):
        binding_id = f"binding-{len(self.bindings) + 1}"
        self.bindings[(sequence, binding_id)] = callback
        return binding_id

    def unbind(self, sequence, binding_id=None):
        self.bindings.pop((sequence, binding_id), None)

    def after(self, milliseconds, callback):
        self.after_calls.append((milliseconds, callback))
        return f"after-{len(self.after_calls)}"

    def after_cancel(self, after_id):
        self.cancelled.append(after_id)

    def destroy(self):
        self.destroyed = True

    def mainloop(self):
        return None

    def geometry(self, value):
        self.geometry_value = value


class FakeWindow:
    def __init__(self):
        self.window = FakeWidget()
        self.canva = FakeCanvas()
        self.window_width = 1000
        self.window_height = 700
        self.running = True

    def create_window(self):
        self.window.geometry(f"{self.window_width}x{self.window_height}")


@pytest.fixture
def canvas():
    return FakeCanvas()


@pytest.fixture
def window():
    return FakeWindow()


@pytest.fixture
def event():
    return lambda x=0, y=0, **values: SimpleNamespace(x=x, y=y, **values)
