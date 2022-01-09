import json
import math
from random import random

import numpy as np

from client_python.Characters import Pokemon, Agent
from client_python.Characters.Agent import agent
from client_python.Characters.Pokemon import pokemon
from client_python.src.DiGraph import DiGraph
from client_python.src.GraphAlgo import GraphAlgo
from client_python.src.Node import Node

EPS = 0.1


class MyGame:
    def __init__(self, graph: DiGraph, client):
        self.pokemon_list = []
        self.agent_list = []
        self.graph = graph
        self.deployed = False
        self.graphAlgo = GraphAlgo(self.graph)
        self.nodeList = {}
        self.center_point = self.graphAlgo.centerPoint()[0]

        for i in range(self.graph.v_size()):
            self.nodeList[i] = False
        self.client = client
        self.num_Of_Agents = self.numAgents(self.client.get_info())

    def add_pokemon(self, pokemon: Pokemon):
        self.pokemon_list.append(pokemon)
        self.pokemon_list.sort()

    def add_agent(self, agent: Agent):
        self.agent_list.append(agent)

    def update_list(self, p_json: str):
        global numOfAgents
        """Add Pokemon from JSON"""
        p_dic = json.loads(p_json)
        self.pokemon_list.clear()

        for i in p_dic["Pokemons"]:
            pok = pokemon(value=i["Pokemon"]["value"], edge_type=i["Pokemon"]["type"],
                          pos=i["Pokemon"]["pos"].split(","))

            """ find the edge of each pokemon"""
            pokemon_pos = (float(pok.pos[0]), float(pok.pos[1]), float(pok.pos[2]))
            edge_pos = self.find_edge(pokPos=pokemon_pos, type=pok.edge_type)
            pok.p_src, pok.p_dest = edge_pos[0], edge_pos[1]
            if not self.deployed and self.num_Of_Agents > 0:
                self.client.add_agent("{\"id\":" + str(pok.p_src) + "}")
                self.num_Of_Agents -= 1
            self.deployed = True

            self.add_pokemon(pok)

        while self.num_Of_Agents > 0:
            self.client.add_agent("{\"id\":" + str(self.center_point) + "}")
            self.num_Of_Agents -= 1
        """Add Agent from JSON"""
        a_json: str = self.client.get_agents()
        agent_dic = json.loads(a_json)
        self.agent_list.clear()
        for a in agent_dic["Agents"]:
            t_agent = agent(id=a["Agent"]["id"], value=a["Agent"]["value"], src=a["Agent"]["src"],
                            dest=a["Agent"]["dest"], speed=a["Agent"]["speed"], pos=a["Agent"]["pos"].split(","),
                            targets=self.nodeList)
            self.add_agent(t_agent)

        self.Call_Of_Duty()

    def Call_Of_Duty(self):
        for p in range(self.pokemon_list.__len__()):
            pok: pokemon = self.pokemon_list[p]
            if not pok.taken:
                self.allocate(self.agent_list, pok)
        for a in self.agent_list:
            ag: agent = a
            if ag.explore.__len__() == 1:
                path = self.graphAlgo.shortest_path(ag.src, self.center_point)
                curr_path = path[1]

                if path[0] != -1:
                    for i in range(1, curr_path.__len__()):
                        ag.explore.append(curr_path[i])

    def allocate(self, listAgent: list, pok: pokemon):
        currAgent = None
        path = []
        on_the_way = False
        minVal = math.inf
        for a in range(listAgent.__len__()):
            ag: agent = listAgent[a]
            tup = self.is_on_the_way(pok.p_src, pok.p_dest, ag.explore)
            if tup[0]:
                if tup[1] < minVal:
                    minVal = tup[1]
                    currAgent = ag
                    on_the_way = True

            else:
                shortest: tuple = self.graphAlgo.shortest_path(ag.explore[ag.explore.__len__() - 1], pok.p_src)
                if (ag.weight + shortest[0]) / ag.speed < minVal and shortest[0] != -1:
                    minVal = ag.weight + shortest[0]
                    currAgent = ag
                    on_the_way = False
                    path = shortest[1]

        currAgent.targets[pok.p_src] = True
        if currAgent.pokemon_radar.__contains__(pok.p_src):
            currAgent.pokemon_radar[pok.p_src].append(pok)
        else:
            currAgent.pokemon_radar[pok.p_src] = []
            currAgent.pokemon_radar[pok.p_src].append(pok)

        if not on_the_way:
            currAgent.weight += minVal
            currAgent.explore.pop()
            for i in range(0, path.__len__()):
                currAgent.explore.append(path[i])
            currAgent.explore.append(pok.p_dest)
        pok.taken = True

    def is_on_the_way(self, pokSrc: int, pokDest: int, explore: list) -> tuple:
        temp = 0

        for e in range(explore.__len__()):
            if 0 < e < explore.__len__() - 1:
                temp += self.graphAlgo.get_graph().all_out_edges_of_node(explore[e])[explore[e + 1]]  # weight
            if e < explore.__len__() - 1:
                if explore[e] == pokSrc and explore[e + 1] == pokDest:
                    return True, temp
        return False, -1

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

                if type < 0:
                    if src.id > dest.id and self.is_on(pokPos, src.pos, dest.pos) < min_dist:
                        min_dist = self.is_on(pokPos, src.pos, dest.pos)
                        curr_pos = (src.id, dest.id)
                else:
                    if src.id < dest.id and self.is_on(pokPos, src.pos, dest.pos) < min_dist:
                        min_dist = self.is_on(pokPos, src.pos, dest.pos)
                        curr_pos = (src.id, dest.id)
        return curr_pos

    def is_on(self, pokPos: tuple, srcPos: tuple, destPos: tuple) -> float:
        src_x_y = (srcPos[0], srcPos[1])
        dest_x_y = (destPos[0], destPos[1])
        dis = math.dist(src_x_y, dest_x_y)

        pokDist = math.dist(srcPos, pokPos) + math.dist(pokPos, destPos)

        return math.fabs(dis - pokDist)

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()
