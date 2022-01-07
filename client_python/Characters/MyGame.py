import json

from client_python.Characters import Pokemon, Agent
from client_python.Characters.Agent import agent
from client_python.Characters.Pokemon import pokemon


class MyGame:
    def __init__(self):
        self.pokemon_list = []
        self.agent_list = []

    def add_pokemon(self, pokemon: Pokemon):
        self.pokemon_list.append(pokemon)
        self.pokemon_list.sort(key=pokemon.value, reverse=True)

    def add_agent(self, agent: Agent):
        self.agent_list.append(agent)

    def update_list(self, p_json: str, a_json: str):

        """Add Pokemon from JSON"""
        p_dic = json.loads(p_json)

        for n in p_dic["Pokemons"]:
            p = n["pos"].split(",")
            pos = (p[0], p[1], p[2])
            pok = pokemon(value=n["value"], edge_type=n["type"], pos=pos)
            self.add_pokemon(pok)

        """Add Agent from JSON"""
        agent_dic = json.loads(a_json)

        for a in agent_dic["Agents"]:
            p = a["pos"].split(",")
            pos = (p[0], p[1], p[2])
            t_agent = agent(id=a["id"], value=a["value"], src=a["src"], dest=a["dest"], speed=a["speed"], pos=pos)
            self.add_agent(t_agent)

    def numAgents(self, info: str):
        return int(json.loads(info)["GameServer"]["agents"])
