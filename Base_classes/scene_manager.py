from Pokemons.Base_classes.Scene import Scene
from Pokemons.Base_classes.game_object import GameObject


class SceneManager:
    _current_scene: Scene = None
    _scenes_list: list[Scene] = []

    @staticmethod
    def load_new_scene(scene: Scene | str):
        if isinstance(scene, str):
            for scene_i in SceneManager._scenes_list:
                if scene_i.name == scene:
                    scene = scene_i
                    break
            else:
                print(f"Сцены с названием {scene} нет!")
                return
        if SceneManager._current_scene:
            SceneManager._current_scene.end_game()
        SceneManager._current_scene = scene
        print('START')
        GameObject.all_objects.clear()
        scene.start()

    @staticmethod
    def add_scenes(scenes: list[Scene]):
        for scene in scenes:
            SceneManager._scenes_list.append(scene)

