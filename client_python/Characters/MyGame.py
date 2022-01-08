import json
import math

import numpy

from client_python.Characters import Pokemon, Agent
from client_python.Characters.Agent import agent
from client_python.Characters.Pokemon import pokemon
import numpy as np

from client_python.src.DiGraph import DiGraph
from client_python.src.Node import Node

numOfAgents = 0
EPS = 0.01


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

            # edge_pos = self.find_edge(pokPos=pok.pos, type=pok.edge_type)
            # pok.p_src, pok.p_dest = edge_pos[0], edge_pos[1]
            # print("Pokemon val: ", pok.value, "POS: ", pok.p_src, pok.p_dest)

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

    def find_edge(self, pokPos: tuple, type: int) -> tuple:
        min_dist = math.inf
        curr_pos = ()
        for i in self.graph.get_all_v():
            src: Node = self.graph.get_all_v().get(i)
            for j in self.graph.all_out_edges_of_node(src.id):
                dest: Node = self.graph.get_all_v().get(j)
                # print(src.id, "-->", dest.id)

                if type < 0:
                    if src.id > dest.id and self.is_on(pokPos, src.pos, dest.pos) < min_dist:
                        min_dist = self.is_on(pokPos, src.pos, dest.pos)
                        curr_pos = (src.id, dest.id)
                else:
                    if src.id < dest.id and self.is_on(pokPos, src.pos, dest.pos) < min_dist:
                        min_dist = self.is_on(pokPos, src.pos, dest.pos)
                        curr_pos = (src.id, dest.id)
        # print(min_dist)
        return curr_pos



    def is_on(self, pokPos: tuple, srcPos: tuple, destPos: tuple) -> float:
        src_x_y = (srcPos[0], srcPos[1])
        dest_x_y = (destPos[0], destPos[1])
        dis = math.dist(src_x_y, dest_x_y)

        pokDist = math.dist(srcPos, pokPos) + math.dist(pokPos, destPos)

        return math.fabs(dis - pokDist)

# #:[{"Pokemon":{"value":5.0,"type":-1,"pos":"35.197656770719604,32.10191878639921,0.0"}}]}
# if __name__ == '__main__':
#     a = (5.20319591121872, 32.1031462, 0.0)
#     b = (35.19597880064568, 32.10154696638656, 0.0)
#
#     c = (35.197656770719604, 32.10191878639921, 0.0)
#
#     pok = pokemon(5, -1, c)
#
#
