import random
import time
import pygame

from Pokemons.Base_classes.Scene import Scene
from Pokemons.Base_classes.game_data import GameData
from Pokemons.Base_classes.transform import Transform
from Pokemons.Scenes.bad_scene import WL
from Pokemons.UI.base_ui.button import Button
from Pokemons.UI.base_ui.text import Text
from Pokemons.main_files import colors


class BagScene(Scene):
    def __init__(self, name: str, game_data: GameData, fill_screen_color: tuple[int, int, int] = colors.RED):
        super().__init__(name, game_data, fill_screen_color=fill_screen_color)
        self.flag = False
        self.wait_time = 5
        self.start_time = -1

    @Scene.start_decorator
    def start(self):
        self.game_data.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.game_data.resolution = pygame.display.get_window_size()
        self.begin()

    def begin(self):
        self.ui.UI_elements.clear()
        text = Text("Произошел баг... Пж не снижайте оценку(а лучше напишите о баге в тг @IceDarold)",
                    colors.WHITE,
                    Transform(position=(self.game_data.resolution[0] // 2, 50, 0)),
                    300, 25)
        exit_button = Button(colors.BLACK,
                             Transform(position=(
                                 self.game_data.resolution[0] // 2, self.game_data.resolution[1] - 150, 0)),
                             500, 100, 50,
                             Text("Закончить путь Алфея...", colors.WHITE, Transform(), 0, 0), self.end_game)
        dont_press = Button(colors.BLACK,
                            Transform(position=(
                                self.game_data.resolution[0] // 2, self.game_data.resolution[1] - 300, 0)),
                            600, 200, 50,
                            Text("НЕ НАЖИМАЙ СЮДА! УБЬЕТ", colors.WHITE, Transform(), 0, 0), self.sure)
        self.ui.add_new_UI_element([text, exit_button, dont_press])

    def exit_func(self):
        print("УМЕР")
        # WL.start()

    def sure(self):
        print("SURRRE")
        self.ui.UI_elements.clear()
        text = Text("Уверен? Это не шутки...",
                    colors.WHITE,
                    Transform(position=(self.game_data.resolution[0] // 2, 50, 0)),
                    300, 25, font="calibri")
        yes = Button(colors.BLACK,
                     Transform(position=(
                         self.game_data.resolution[0] // 2, self.game_data.resolution[1] - 50, 0)),
                     300, 100, 50,
                     Text("Да", colors.WHITE, Transform(), 0, 0), self.next_stage)
        exit_button = Button(colors.BLACK,
                             Transform(position=(
                                 self.game_data.resolution[0] // 2, self.game_data.resolution[1] - 150, 0)),
                             300, 100, 50,
                             Text("Все, мне страшно, возвращаюсь на базу", colors.WHITE, Transform(), 0, 0), self.begin)
        self.ui.add_new_UI_element([exit_button, text, yes])
        print("YLGE", self.ui.UI_elements)

    def change_flag(self):
        self.flag = True

    def next_stage(self):
        pass

    @Scene.main_loop_decorator
    def main_loop(self):
        pass
        # if self.flag and self.start_time == -1:
        #     self.start_time = time.time()
        # if self.flag:
        #     self.fill_screen_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # if self.flag and time.time() - self.start_time > self.wait_time:
        #     self.end_game()
        #     self.exit_func()
        # else:
        #     self.fill_screen_color = colors.RED
        # self.flag = not self.flag
