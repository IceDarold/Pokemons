import dataclasses

from pygame import Surface
from pygame.time import Clock

from Pokemons.Base_classes.Camera import Camera
from Pokemons.online.client import Client
from Pokemons.online.server import Server


@dataclasses.dataclass
class GameData:
    FPS: int
    screen: Surface
    clock: Clock
    resolution: tuple[int, int]
    full_screen: bool
    server: Server
    client: Client
