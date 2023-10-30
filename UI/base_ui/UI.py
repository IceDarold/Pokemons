from pygame import Rect, Surface
from pygame.event import Event

from Pokemons.Base_classes.transform import Transform


class UIElement:
    def __init__(self, transform: Transform, layer: int = 0, name: str = "new element"):
        self._transform = transform
        self.layer = layer
        self.name = name

    def get_transform(self) -> Transform:
        return self._transform.copy()

    def draw(self, surface: Surface):
        pass

    def update(self, event: Event):
        """
        Вызывается для проверки различных условий взаимодействия с UI, по типу нажатия на кнопку
        :param event: экземпляр класса pygame.event.Event.
        :return:
        """
        pass


class UI:
    def __init__(self, surface: Surface, elements: list[UIElement | Rect] = None):
        if not elements:
            self.UI_elements = []
        else:
            self.UI_elements: list[UIElement | Rect] = elements
        self.surface = surface
        self.layers_list: [[int, UIElement]] = []
        pass

    def add_new_UI_element(self, element: UIElement | list[UIElement]):
        if isinstance(element, list):
            for el in element:
                if isinstance(el, UIElement):
                    self.UI_elements.append(el)
                else:
                    print(f"{el} - не UI!")
        else:
            self.UI_elements.append(element)
            self.layers_list.append([element.layer, element])

    def contain_element(self, element: UIElement):
        return element in self.UI_elements

    def remove_UI_element(self, element: str | UIElement):
        if isinstance(element, UIElement):
            self.UI_elements.remove(element)
            return
        new_ui_elements = self.UI_elements.copy()
        for ui_element in self.UI_elements:
            if ui_element.name == element:
                new_ui_elements.remove(ui_element)
        self.UI_elements = new_ui_elements.copy()

    def draw_UI(self, surface: Surface):
        if len(self.UI_elements) != len(self.layers_list):
            self.layers_list = [[el.layer, el] for el in self.UI_elements]
        self.layers_list.sort(key=lambda el: el[0])
        # print(self.layers_list)
        for element in self.layers_list:
            element[1].draw(surface)

    def update_UI(self, event: Event) -> None:
        for element in self.UI_elements:
            element.update(event)

    def get_ui_elements(self) -> list[UIElement]:
        return self.UI_elements.copy()

# def a():
#     print("a")
#
# def b():
#     print("b")
# c = a
# c += b
# c()
