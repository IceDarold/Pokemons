from pygame import Vector2

from Pokemons.Base_classes.base_functions import check_collision_in_group
from Pokemons.Base_classes.transform import Transform
from Pokemons.main_files.Pokemon import Pokemon
from Pokemons.UI.base_ui.UI import UI
from Pokemons.UI.base_ui.image import Image


def draw_check_frame(position: Vector2 | tuple[int, int], pokemons: list[Pokemon | Image], ui: UI, frame_image: Image):
    """
    Рисует пунктирную рамку вокруг объекта из списка pokemons, на который сейчас наведена мышь
    :param position: позиция мыши
    :param pokemons: список объектов, вокруг которых рамка может быть нарисована
    :param ui: объект UI в рамках которого будет рисоваться рамка
    :param frame_image: объект изображения рамки
    :return: nothing
    """
    ui.remove_UI_element("frame_image")
    collision = check_collision_in_group(position, pokemons)
    if collision:
        print("COLLISION")
        frame_image.change_position(Vector2(collision.rect.center[0], collision.rect.center[1]))
        frame_image.change_pixel_size(Vector2(collision.rect.width, collision.rect.height))
        if not ui.contain_element(frame_image):
            print('ADD')
            ui.add_new_UI_element(frame_image)


def choice_team(player_team: list[Pokemon], first_pokemon_position: Vector2, pokemons_in_row: int,
                pixel_size: tuple[int, int] | Vector2) -> (dict[Image, Pokemon], Vector2):
    """
    Настраивает размещение покемонов в окошке выбора покемонов для боя
    :param pixel_size: размер изображений в пикселях
    :param player_team: список покемонов, среди которых нужно выбирать команду для боя
    :param first_pokemon_position: позиция покемона в левом верхнем углу меню для выбора
    :param pokemons_in_row: количество покемонов в строчке
    :return: Group, состоящую из покемонов с настроенной позицией и размер всего размещения
    """
    if len(player_team) == 0:
        print("player team пустой!")
        return
    index = 0
    image_list: dict[Image, Pokemon] = {}
    last_position: Vector2 = first_pokemon_position.copy()
    for pokemon in player_team:
        if index % pokemons_in_row == 0 and index != 0:
            height_list = []
            for pokemon_height in list(image_list.keys()):
                print("PH", pokemon_height.rect.height)
                height_list.append(pixel_size[1])
            last_position.x = first_pokemon_position.x
            last_position.y += max(height_list)
        last_position += Vector2(image_list[list(image_list.keys())[0]].rect.width // 2 if index % pokemons_in_row != 0 else 0,
                                 0)
        last_position += Vector2(pixel_size[0], 0)
        print("CP", last_position)
        image = Image(transform=Transform(position=last_position),
                      image=pokemon.get_img(),
                      pixel_size=pixel_size,
                      name="pokemon image",
                      )
        #        pokemon.vx = pokemon.vy = 0
        image_list[image] = pokemon
        index += 1
    last_right_sprite = image_list[list(image_list.keys())[-1]] if len(image_list.keys()) <= pokemons_in_row else image_list[list(image_list.keys())[pokemons_in_row - 1]]
    # Берем края всей композиции спрайтов и вычитаем их, получая общий размер композиции
    size = Vector2((last_right_sprite.rect.center[0] + last_right_sprite.rect.width / 2) -
                   (first_pokemon_position.x - image_list[list(image_list.keys())[0]].rect.width / 2),
                   (player_team[-1].rect.center[1] + player_team[-1].rect.height / 2) -
                   (player_team[0].rect.center[1] - player_team[0].rect.width / 2))
    center = size / 2 + player_team[0].rect.center
    print("CHOICE_TEAM", image_list[list(image_list.keys())[0]].rect.center, center)
    return image_list, size, center
