class MouseHandler:
    '''Translate input events into game actions.'''
    def __init__(self, game_flow):
        self.__game_flow = game_flow

    def on_key_press(self, event):
        self.__game_flow.handle_key(event)

    def interact_with_ui(self, event):
        self.__game_flow.handle_click(event)

    def track_display_range(self, event):
        self.__game_flow.update_range_display(event)
