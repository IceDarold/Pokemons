from pygame import Surface

from Pokemons.Base_classes.transform import Transform
from Pokemon import Pokemon


class WaterPokemon(Pokemon):
    def __init__(self, name, transform: Transform, image: Surface, atk: int = None, df: int = None):
        super().__init__(name, transform=transform, atk=atk, df=df, image=image)

    def attack(self, aim: Pokemon):
        if isinstance(aim, FirePokemon):
            aim.damage(self.get_atk() * 3 - aim.get_def())
        else:
            super().attack(aim)


class FirePokemon(Pokemon):
    def __init__(self, name, transform: Transform, image: Surface, atk: int = None, df: int = None):
        super().__init__(name, transform=transform, image=image, atk=atk, df=df)


class GrassPokemon(Pokemon):
    def __init__(self, name, transform: Transform, image: Surface, atk: int = None, df: int = None):
        super().__init__(name, transform=transform, image=image, atk=atk, df=df)

    def attack(self, aim: Pokemon):
        if isinstance(aim, FirePokemon):
            aim.damage(self.get_atk() - aim.get_def() / 2)
        else:
            super().attack(aim)


class ElectricPokemon(Pokemon):
    def __init__(self, name, transform: Transform, image: Surface, atk: int = None, df: int = None):
        super().__init__(name, transform=transform, image=image, atk=atk, df=df)

    def attack(self, aim: Pokemon):
        if isinstance(aim, WaterPokemon):
            aim.damage(self.get_atk())
        else:
            super().attack(aim)
