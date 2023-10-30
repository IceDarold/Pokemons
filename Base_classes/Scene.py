import pygame
from pygame import Surface
from pygame.event import Event
from pygame.time import Clock
import time

from Pokemons.Base_classes.game_data import GameData
from Pokemons.Base_classes.game_object import GameObject
from Pokemons.UI.base_ui.UI import UI


class Scene:
    def __init__(self, name: str, game_data: GameData, ui_surface: Surface = None,
                 fill_screen_color: tuple[int, int, int] = (255, 255, 255)):
        self.name = name
        self.running = False
        self.game_data = game_data
        self.ui = UI(ui_surface if ui_surface else self.game_data.screen)
        self.clock: Clock = game_data.clock
        self.fill_screen_color = fill_screen_color
        self.FPS = game_data.FPS

    @staticmethod
    def start_decorator(start_function):
        def return_start(self):
            print("START DECOR")
            self.running = True
            start_function(self)
            self.main_loop()

        return return_start

    def add_game_object(self, game_object: GameObject | list):
        if isinstance(game_object, GameObject):
            GameObject.all_objects.append(game_object)
        elif isinstance(game_object, list):
            for i in range(len(game_object)):
                if isinstance(game_object[i], GameObject):
                    GameObject.all_objects.append(game_object[i])
                else:
                    print(f"{game_object[i]} - не GameObject")
        else:
            print(f"{game_object} - не GameObject!")

    @start_decorator
    def start(self):
        pass

    @staticmethod
    def end_decorator(end_game_function):
        def end_decorator(self):
            self.running = False
            end_game_function(self)

        return end_decorator

    @end_decorator
    def end_game(self):
        """
        Вызывается когда пользователь нажимает на крестик
        :return:
        """
        pass

    @staticmethod
    def event_decorator(event_function):
        def return_func(self):
            for e in pygame.event.get():
                self.ui.update_UI(e)
                event_function(self, e)
                if e.type == pygame.QUIT:
                    print("QUIT")
                    self.end_game()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down(e)
                elif e.type == pygame.MOUSEMOTION:
                    self.mouse_motion(e)
                if e.type == pygame.KEYUP:
                    self.any_key_pressed(e)
        return return_func

    @event_decorator
    def events(self, e):
        pass

    def mouse_button_down(self, e: Event):
        """
        Вызывается когда пользователь нажимает мышью
        :param e: экземпляр класса события, в котором храниться вся информация о действии пользователя
        :return:
        """
        pass

    def mouse_motion(self, e: Event):
        """
        Вызывается когда пользователь двигает мышь
        :param e: экземпляр класса события, в котором храниться вся информация о действии пользователя
        :return:
        """
        pass

    @staticmethod
    def main_loop_decorator(main_loop):
        """
        Вызывается каждый кадр
        :param main_loop:
        :return:
        """

        def main_loop_return(self):
            while self.running:
                start_time = time.time()
                self.events()
                main_loop(self)
                # Рендеринг
                self.game_data.screen.fill(self.fill_screen_color)
                for i in GameObject.all_objects:
                    try:
                        i.draw(self.game_data.screen)
                    except KeyError:
                        print(f"У {i} нет метода draw")
                        # print("Вы добавили в список объектов для отрисовки объект без метода Draw!")
                    i.update()
                # После отрисовки всего, переворачиваем экран
                self.ui.draw_UI(self.game_data.screen)
                pygame.display.flip()
                self.clock.tick(self.FPS)


        return main_loop_return

    @main_loop_decorator
    def main_loop(self):
        pass

    def any_key_pressed(self, e: Event):
        pass

    @staticmethod
    def find_scene(scene_name: str):
        pass
