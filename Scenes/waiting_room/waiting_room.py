import time

from pygame import Vector3

from Pokemons.Base_classes.Scene import Scene
from Pokemons.Base_classes.game_data import GameData
from Pokemons.Base_classes.scene_manager import SceneManager
from Pokemons.Base_classes.transform import Transform
from Pokemons.UI.base_ui.button import Button
from Pokemons.UI.base_ui.text import Text
from Pokemons.main_files import colors
from Pokemons.online import online_config
from Pokemons.online.server import Server


class WaitingRoomScene(Scene):
    def __init__(self, name: str, game_data: GameData, fill_screen_color: tuple[int, int, int] = colors.WHEAT):
        super().__init__(name, game_data, fill_screen_color=fill_screen_color)
        self.max_players = online_config.max_players
        self.total_connected_text: Text = None
        self._last_min_loop_time_update = 0
        self._last_number_of_player = 0

    def draw_players(self):
        top_position = Vector3(150, 150, 0)
        distance_y = 100
        players_text = []
        players = self.get_users()
        for player_index in range(len(players)):
            players_text.append(Text(
                players[player_index], colors.WHITE,
                Transform(position=top_position + Vector3(0, distance_y * player_index, 0)), 300, 20))
        self.ui.add_new_UI_element(players_text)
        self._last_number_of_player = len(players)

    def get_users(self) -> list[str]:
        return list(self.game_data.server.connect_users.keys()) if online_config.is_server else self.game_data.client.get_players()

    @Scene.start_decorator
    def start(self):
        self.draw_players()
        self.total_connected_text: Text = Text(
            "", colors.WHITE,
            Transform(position=(150, 100, 0)),
            300, 25)
        if online_config.is_server:
            print("UPDATE")
            self.total_connected_text.text = \
                f"Игроков в комнате {len(self.game_data.server.connect_users)}/{self.max_players}"
            self.ui.add_new_UI_element(Text(
                "Host", colors.WHITE,
                Transform(position=(50, 20, 0)),
                300, 50))
        else:
            self.total_connected_text.text = \
                f"Игроков в комнате {len(self.game_data.client.get_players())}/{self.max_players}"

        title: Text = Text("Waiting room", colors.WHITE,
                           Transform(position=(self.game_data.resolution[0] // 2, 50, 0)),
                           300, 70)
        ip_text = Text(Server.get_ip(), colors.WHITE,
                       Transform(position=(self.game_data.resolution[0] // 2 + 200, 100, 0)),
                       300, 40)
        start_button: Button = Button(colors.DARK_ORCHID,
                                      Transform(position=(
                                          self.game_data.resolution[0] - 200, self.game_data.resolution[1] - 50, 0)),
                                      300, 100, 50,
                                      Text("Начать игру", colors.WHITE, Transform(), 0, 0), self.start_game)
        number_of_ready: Text = Text(f"0/{len(self.get_users())}", colors.WHITE,
                                     Transform(position=(self.game_data.resolution[0] - 200,
                                                         self.game_data.resolution[1] - 100, 0)),
                                     70, 40)

        self.ui.add_new_UI_element([title, start_button, self.total_connected_text, ip_text, number_of_ready])

    def start_game(self):
        if online_config.is_server:
            items = self.game_data.server.connect_users.items()
        else:
            items = self.game_data.client.get_ready().items()
        for user, is_ready in items:
            if user == Server.get_ip():
                if online_config.is_server:
                    self.game_data.server.connect_users[user] = not is_ready
                else:
                    self.game_data.client.change_readiness(user, not is_ready)
        if not (False in self.game_data.server.connect_users.values()):
            SceneManager.load_new_scene("hunting_scene")

    @Scene.main_loop_decorator
    def main_loop(self):
        if time.time() - self._last_min_loop_time_update > 1:
            self._last_min_loop_time_update = time.time()
            current_number_of_players = len(self.game_data.server.connect_users) if online_config.is_server \
                else len(self.game_data.client.get_players())
            players = self.get_users()
            top_position = Vector3(150, 150, 0)
            distance_y = 100
            for i in range(current_number_of_players - self._last_number_of_player):
                self.ui.add_new_UI_element(Text(
                    players[current_number_of_players - self._last_number_of_player + i], colors.WHITE,
                    Transform(position=(top_position + Vector3(0, distance_y * (current_number_of_players -
                                                                                self._last_number_of_player + i), 0))),
                    300, 25))
            self._last_number_of_player = current_number_of_players
            self.total_connected_text.text = f"Игроков в комнате {current_number_of_players}/{self.max_players}"
