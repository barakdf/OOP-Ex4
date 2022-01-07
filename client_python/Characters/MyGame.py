import json

from client_python.Characters import Pokemon, Agent
from client_python.Characters.Agent import agent
from client_python.Characters.Pokemon import pokemon


numOfAgents = 0

class MyGame:
    def __init__(self):
        self.pokemon_list = []
        self.agent_list = []

    def add_pokemon(self, pokemon: Pokemon):
        self.pokemon_list.append(pokemon)
        #self.pokemon_list.sort(key=pokemon.value, reverse=True)

    def add_agent(self, agent: Agent):
        self.agent_list.append(agent)

    def update_list(self, p_json: str, a_json: str):
        global numOfAgents
        """Add Pokemon from JSON"""
        p_dic = json.loads(p_json)

        for i in p_dic["Pokemons"]:

            pok = pokemon(value=i["Pokemon"]["value"], edge_type=i["Pokemon"]["type"],
                          pos=i["Pokemon"]["pos"].split(","))


            self.add_pokemon(pok)
            print(pok.repr())

        """Add Agent from JSON"""


        agent_dic = json.loads(a_json)

        for a in agent_dic["Agents"]:
            t_agent = agent(id=a["Agent"]["id"], value=a["Agent"]["value"], src=a["Agent"]["src"], dest=a["Agent"]["dest"], speed=a["Agent"]["speed"], pos=a["Agent"]["pos"].split(","))
            self.add_agent(t_agent)
            print(t_agent.repr())




    def numAgents(self, info: str) -> int:
        return int(json.loads(info)["GameServer"]["agents"])
