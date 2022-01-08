"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import json
import threading
from types import SimpleNamespace

import pygame
from pygame import *

from client_python.Characters.MyGame import MyGame
from src.DiGraph import DiGraph
from client import Client
from src.GraphAlgo import GraphAlgo
from src.DiGraph import *

# init pygame

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

# screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)







""" INIT GRAPH """



graph_json = client.get_graph()
graph = DiGraph()
graph_algo = GraphAlgo(graph)


# load the json string into grape Object
graph_algo.load_from_json(graph_json)


GameManager = MyGame(graph=graph_algo.get_graph())


"""add agent """
for i in range(GameManager.numAgents(client.get_info())):
    id = str(i)
    client.add_agent("{\"id\":" + id + "}")



pok_str = client.get_pokemons()
agent_str = client.get_agents()


GameManager.update_list(p_json=pok_str, a_json=agent_str)




FONT = pygame.font.SysFont('Arial', 20, bold=True)


GameManager.deploy_agents()
graph_algo.plot_graph(client=client, game=GameManager)






# # this commnad starts the server - the game is running now
# client.start()
#
# """
# The code below should be improved significantly:
# The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
# """
#
#     # refresh rate
#     clock.tick(60)
#
#
# # game over:
