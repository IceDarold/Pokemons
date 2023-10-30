import socket
from typing import Type, Any

import Pokemons.online.online_config as online_config
from Pokemons.Base_classes.maze_data import MazeData


class Client:
    def __init__(self, maze_data: MazeData):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.maze_data = maze_data

    def connect(self):
        try:
            self.client.connect(("localhost", 2282))
        except socket.error as e:
            print(e)
    def change_readiness(self, key, value):
        self.send_data(f"change_readiness|{str(key)}:{str(value)}")
        return self.get_response()
    def get_seed(self) -> int:
        """
        Возвращает сид для лабиринта
        :return:
        """
        self.send_data("get seed")
        return int(self.get_response())

    def get_players(self) -> list[str]:
        """
        Возвращает всех игроков в комнате
        :return:
        """
        self.send_data("get players")
        players_str: str = self.get_response()
        return players_str.split("|")
    def get_ready(self):
        self.send_data("get ready")
        players_str: str = self.get_response()
        return_dict = {}
        for pair in players_str.split("|"):
            v_list = pair.split(":")
            return_dict[v_list[0]] = v_list[1]
        return return_dict

    def send_data(self, data: str):
        self.client.sendall(data.encode("utf-8"))

    def get_response(self) -> str:
        while True:
            resp = self.client.recv(1024)
            return str(resp, "utf-8")
