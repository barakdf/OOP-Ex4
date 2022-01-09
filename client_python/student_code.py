import pygame

from client import Client
from client_python.Characters.MyGame import MyGame
from src.DiGraph import *
from src.GraphAlgo import GraphAlgo

if __name__ == '__main__':
    # default port
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'

    client = Client()
    client.start_connection(HOST, PORT)

    """ INIT GRAPH """

    graph_json = client.get_graph()
    graph = DiGraph()
    graph_algo = GraphAlgo(graph)

    # load the json string into grape Object
    graph_algo.load_from_json(graph_json)

    GameManager = MyGame(graph=graph_algo.get_graph(), client=client)

    pok_str = client.get_pokemons()

    GameManager.update_list(p_json=pok_str)

    FONT = pygame.font.SysFont('Arial', 20, bold=True)

    graph_algo.plot_graph(client=client, game=GameManager)
