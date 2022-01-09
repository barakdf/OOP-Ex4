import json
import math

import numpy as np

from client_python.Characters import Pokemon, Agent
from client_python.Characters.Agent import agent
from client_python.Characters.Pokemon import pokemon
from client_python.src.DiGraph import DiGraph
from client_python.src.GraphAlgo import GraphAlgo
from client_python.src.Node import Node

numOfAgents = 0
EPS = 0.1


class MyGame:
    def __init__(self, graph: DiGraph):
        self.pokemon_list = []
        self.agent_list = []
        self.graph = graph
        self.deployed = False
        self.graphAlgo = GraphAlgo(self.graph)
        self.nodeList = {}
        for i in range(self.graph.v_size()):
            self.nodeList[i] = False

    def add_pokemon(self, pokemon: Pokemon):
        self.pokemon_list.append(pokemon)
        self.pokemon_list.sort()

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
            print("value------------->", pok.value)

            """ find the edge of each pokemon"""
            pokemon_pos = (float(pok.pos[0]), float(pok.pos[1]), float(pok.pos[2]))
            edge_pos = self.find_edge(pokPos=pokemon_pos, type=pok.edge_type)
            pok.p_src, pok.p_dest = edge_pos[0], edge_pos[1]
            # print("Pokemon val: ", pok.value, "POS: ", pok.p_src, pok.p_dest)

            self.add_pokemon(pok)

        # print(self.pokemon_list.__repr__())

        """Add Agent from JSON"""

        agent_dic = json.loads(a_json)
        self.agent_list.clear()

        for a in agent_dic["Agents"]:
            t_agent = agent(id=a["Agent"]["id"], value=a["Agent"]["value"], src=a["Agent"]["src"],
                            dest=a["Agent"]["dest"], speed=a["Agent"]["speed"], pos=a["Agent"]["pos"].split(","),
                            targets=self.nodeList)
            self.add_agent(t_agent)

        self.Call_Of_Duty()

    def Call_Of_Duty(self):
        if self.agent_list.__len__() == 1:
            self.one_man_war(self.agent_list[0], self.pokemon_list)
        else:
            for p in range(self.pokemon_list.__len__()):
                pok: pokemon = self.pokemon_list[p]
                if not pok.taken:
                    self.allocate(self.agent_list, pok)

    def one_man_war(self, ag: agent, pok_list: list):
        path: list = []
        for p in pok_list:
            pok: pokemon = p
            pok.taken = True
            ag.targets[pok.p_src] = True
            path.append(pok.p_src)
        final_path = self.graphAlgo.TSP(path)[0]
        if ag.src == final_path[0]:
            for a in range(1, final_path.__len__()):
                ag.explore.append(final_path[a])
        else:
            if self.deployed:
                ag.explore.pop(0)
            shortest = self.graphAlgo.shortest_path(ag.src, final_path[0])[1]
            for i in range(shortest.__len__() - 1):
                ag.explore.append(shortest[i])
            for t in final_path:
                ag.explore.append(t)
        for p in pok_list:
            if p.p_src == final_path[final_path.__len__() - 1]:
                ag.explore.append(p.p_dest)
                break
        # print("PATHHHHHHHHHHHHHHH: ", final_path)

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
                if ag.weight + shortest[0] < minVal and shortest[0] != -1:
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
            # print("PATHHHHHHHHHHHHHHH: ", path)
            currAgent.explore.pop()
            for i in range(0, path.__len__()):
                currAgent.explore.append(path[i])
            currAgent.explore.append(pok.p_dest)
        pok.taken = True

    def is_on_the_way(self, pokSrc: int, pokDest: int, explore: list) -> tuple:
        temp = 0

        for e in explore:
            if 0 < e < explore.__len__() - 1:
                temp += self.graph.edges_out[e][e + 1]  # weight
            if e < explore.__len__() - 1:
                if explore[e] == pokSrc and explore[e + 1] == pokDest:
                    return True, temp
        return False, -1

    def deploy_agents(self) -> bool:
        for a in range(len(self.agent_list)):
            ag: agent = self.agent_list[a]
            for p in range(len(self.pokemon_list)):
                curr_pok: pokemon = self.pokemon_list[p]
                if not curr_pok.taken:
                    ag.src = curr_pok.p_src
                    curr_pok.taken = True
                    if ag.explore[0] != curr_pok.p_src:
                        ag.explore[0] = curr_pok.p_src
                    ag.explore.append(curr_pok.p_dest)
        self.deployed = True

        return True

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

    def attack(self, ag: agent) -> bool:
        for i in range(ag.pokemon_radar[ag.src].__len__()):
            pok_pos = ag.pokemon_radar[ag.src][i].pos
            if math.dist(ag.get_pos(), (float(pok_pos[0]), float(pok_pos[1]), float(pok_pos[2]))) < EPS:
                return True

        return False

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()
