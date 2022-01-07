import json

import numpy

from client_python.Characters import Pokemon, Agent
from client_python.Characters.Agent import agent
from client_python.Characters.Pokemon import pokemon
import numpy as np

from client_python.src.DiGraph import DiGraph
from client_python.src.Node import Node

numOfAgents = 0
EPS = 0.0001


class MyGame:
    def __init__(self, graph: DiGraph):
        self.pokemon_list = []
        self.agent_list = []
        self.graph = graph

    def add_pokemon(self, pokemon: Pokemon):
        self.pokemon_list.append(pokemon)
        # self.pokemon_list.sort(key=pokemon.value, reverse=True)

    def add_agent(self, agent: Agent):
        self.agent_list.append(agent)

    def update_list(self, p_json: str, a_json: str):
        global numOfAgents
        """Add Pokemon from JSON"""
        p_dic = json.loads(p_json)
        self.pokemon_list.clear()

        for i in p_dic["Pokemons"]:
            pok = pokemon(value=i["Pokemon"]["value"], edge_type=i["Pokemon"]["type"],
                          pos=i["Pokemon"]["pos"].split(","))

            self.add_pokemon(pok)

        """Add Agent from JSON"""

        agent_dic = json.loads(a_json)
        self.agent_list.clear()

        for a in agent_dic["Agents"]:
            t_agent = agent(id=a["Agent"]["id"], value=a["Agent"]["value"], src=a["Agent"]["src"],
                            dest=a["Agent"]["dest"], speed=a["Agent"]["speed"], pos=a["Agent"]["pos"].split(","))
            self.add_agent(t_agent)

    def numAgents(self, info: str) -> int:
        return int(json.loads(info)["GameServer"]["agents"])

    def dist(self, x, y):
        a = np.array(x)
        b = np.array(y)
        return np.sqrt(np.sum((a - b) ** 2))

    # def find_edge(self, pokPos: tuple, type: int):
    #
    #
    #
    #     for i in self.graph.get_all_v():
    #         curr: Node = self.graph.get_all_v().get(i)
    #
    #         for j in self.graph.all_out_edges_of_node(curr.id):
    #
    #             if type < 0:

    def is_on(self, pokPos: tuple, srcPos: tuple, destPos: tuple) -> bool:
        dist = self.dist(srcPos, destPos)
        pokDist = self.dist(srcPos, pokPos) + self.dist(pokPos, destPos)
        return dist > pokDist - EPS

    