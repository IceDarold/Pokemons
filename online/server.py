import socket
from Pokemons.Base_classes.maze_data import MazeData


class Server:
    class ServerCommands:
        get_seed = "get seed"
        get_players = "get players"
        get_readiness = "get ready"
        change_readiness = "change_readiness"

    def __init__(self, maze_data: MazeData):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #ip игрока и готов ли он к игре
        self.connect_users: dict[str, bool] = {Server.get_ip(): False}
        self.maze_data = maze_data

    @staticmethod
    def get_ip():
        host_name = socket.gethostname()
        return socket.gethostbyname(host_name)

    def connect(self):
        try:
            print(Server.get_ip())
            self.server.bind(("localhost", 2282))
        except socket.error as e:
            print("ERROR", str(e))
        self.server.listen(10)

        while True:
            connection, addr = self.server.accept()
            with connection:
                print(f"client {addr}, {connection} connection!")
                self.connect_users.append(addr)
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    data_str = str(data, "utf-8")
                    print("C->S", data_str)
                    if data_str == Server.ServerCommands.get_seed:
                        resp = str(self.maze_data.seed)
                    elif data_str == Server.ServerCommands.get_players:
                        result = ""
                        for player, is_ready in self.connect_users.items():
                            result += f"{player}|"
                        resp = result[:-1]
                    elif data_str == Server.ServerCommands.get_readiness:
                        result = ""
                        for player, is_ready in self.connect_users:
                            result += f"{player}:{is_ready}|"
                        resp = result[:-1]
                    elif data_str.startswith(Server.ServerCommands.change_readiness):
                        v_list = data_str.split("|")[1].split(":")
                        self.connect_users[v_list[0]] = True if v_list[1] == "True" else False
                        resp = "Change successful"
                    else:
                        resp = "Can't understand"
                    print("S->C", resp)
                    connection.sendall(resp.encode("utf-8"))
            connection.close()

    def __del__(self):
        self.server.close()

