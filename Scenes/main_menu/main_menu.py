from threading import Thread

from pygame import Vector2
from pygame.event import Event

from Pokemons.UI.base_ui.button import Button
from Pokemons.main_files import colors
from Pokemons.Base_classes.Scene import Scene
from Pokemons.Base_classes.game_data import GameData
from Pokemons.Base_classes.scene_manager import SceneManager
from Pokemons.Base_classes.transform import Transform
from Pokemons.UI.base_ui.text import Text
from Pokemons.lexicon_ru.main_menu_lexicon_ru import MAIN_MENU_LEXICON_RU
from Pokemons.online import online_config


class MainMenuScene(Scene):
    def __init__(self, name: str, game_data: GameData):
        super().__init__(name, game_data, fill_screen_color=colors.WHEAT)

    def any_key_pressed(self, e: Event):
        self.ui.UI_elements.clear()
        server_transform = Transform(position=Vector2(self.game_data.resolution[0] // 2 - 200, 300))
        server_button = Button(colors.DARK_ORCHID,
                               server_transform, 300, 100, 50,
                               Text("Обычный", colors.WHITE, server_transform, 60, 40),
                               lambda: SceneManager.load_new_scene("hunting_scene"))
        client_transform = Transform(position=Vector2(self.game_data.resolution[0] // 2 + 200, 300))
        client_button = Button(colors.DARK_ORCHID,
                               client_transform, 300, 100, 50,
                               Text("Онлайн", colors.WHITE, client_transform, 60, 40), self.online)
        choose_text = Text("Выберите режим", colors.WHITE,
                           Transform(position=(self.game_data.resolution[0] // 2, 100, 0)),
                           300, 70)

        self.ui.add_new_UI_element([server_button, client_button, choose_text])

    def online(self):
        self.ui.UI_elements.clear()
        print(self.ui.UI_elements)
        server_transform = Transform(position=Vector2(self.game_data.resolution[0] // 2 - 200, 300))
        server_button = Button(colors.DARK_ORCHID,
                               server_transform, 300, 100, 50,
                               Text("Сервер", colors.WHITE, server_transform, 60, 40), self.server)
        client_transform = Transform(position=Vector2(self.game_data.resolution[0] // 2 + 200, 300))
        client_button = Button(colors.DARK_ORCHID,
                               client_transform, 300, 100, 50,
                               Text("Клиент", colors.WHITE, client_transform, 60, 40), self.client)
        choose_text = Text("Выберите роль", colors.WHITE,
                           Transform(position=(self.game_data.resolution[0] // 2, 100, 0)),
                           300, 100)

        self.ui.add_new_UI_element([server_button, client_button, choose_text])

    def server(self):
        # print("SERVER")
        # server = self.game_data.server
        online_config.is_server = True
        server_thread = Thread(target=self.game_data.server.connect)
        # load_thread = Thread(target=SceneManager.load_new_scene, args=("waiting_room",), kwargs={"role": "Server"}, )
        server_thread.start()
        SceneManager.load_new_scene("waiting_room")
        # load_thread.start()

    def client(self):
        print("CLIENT")
        self.game_data.client.connect()
        SceneManager.load_new_scene("waiting_room")

    @Scene.start_decorator
    def start(self):
        # SceneManager.load_new_scene("hunting_scene")
        text = Text(
            text=MAIN_MENU_LEXICON_RU["start"],
            text_color=colors.DARK_GOLDENROD,
            transform=Transform(
                position=Vector2(self.game_data.screen.get_width() // 2,
                                 self.game_data.screen.get_height() // 2)),
            width=700,
            height=50,
            font="../fonts/JosefinSans-VariableFont_wght.ttf")
        self.ui.add_new_UI_element(text)
