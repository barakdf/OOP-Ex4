import sys
import time

import pygame
# from GraphAlgo import *
from pygame import gfxdraw

# from client_python.src.GraphAlgo import *
from client_python.Characters.MyGame import *
from client_python.client import Client
from client_python.src import Node

prev = 0
EPS = 0.1
first = True
start = 0
pygame.font.init()
FONT = pygame.font.SysFont("Ariel", 20, bold=True)
BUTTON_FONT = pygame.font.SysFont("Ariel", 30)
SAVE_LOAD_FONT = pygame.font.SysFont("Ariel", 40)
CONSOLE_FONT = pygame.font.SysFont("Helvetica", 30, bold=True)

screen = pygame.display.set_mode((1600, 800), flags=pygame.RESIZABLE)
SCREEN_TOPLEFT = screen.get_rect().topleft
SCREEN_BUTTON_R = screen.get_width() / 5
RADIUS = 10
clock = pygame.time.Clock()

""" BackGround Picture """
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, screen.get_size())
        self.rect = self.image.get_rect()
        screen.get_size()


# this algorithm is not mine. https://stackoverflow.com/questions/13053061/circle-line-intersection-points
# algorithm to find the intersection point of segment and circle.
def node_line_inter(pointA, pointB, pointC, radius):
    ans = []

    ba_x = pointB[0] - pointA[0]
    ba_y = pointB[1] - pointA[1]

    ca_x = pointC[0] - pointA[0]
    ca_y = pointC[1] - pointA[1]

    a = (ba_x * ba_x) + (ba_y * ba_y)
    bBy2 = (ba_x * ca_x) + (ba_y * ca_y)
    c = (ca_x * ca_x) + (ca_y * ca_y) - (radius * radius)

    pBy2 = bBy2 / a
    q = c / a

    disc = (pBy2 * pBy2) - q
    if disc < 0:
        return None

    tmp_sqrt = math.sqrt(disc)
    abScalingF_1 = -pBy2 + tmp_sqrt
    abScalingF_2 = -pBy2 - tmp_sqrt

    p1 = (pointA[0] - (ba_x * abScalingF_1), pointA[1] - (ba_y * abScalingF_1))
    ans.append(p1)
    if disc == 0:
        return ans

    p2 = (pointA[0] - (ba_x * abScalingF_2), pointA[1] - (ba_y * abScalingF_2))
    ans.append(p2)
    return ans


class Button:
    def __init__(self, rect: pygame.Rect, color, text, func=None):
        self.rect = rect
        self.color = color
        self.text = text
        self.func = func
        self.is_clicked = False

    def press(self):
        self.is_clicked = not self.is_clicked

class Console:
    def __init__(self):
        self.func = ""
        self.src = ""
        self.dest = ""
        self.con_text = "Catch 'em All"


console = Console()

"""------------------> START SCALE METHODS"""


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


min_x = min_y = max_x = max_y = 0


def min_max(graph=None):
    global min_x, min_y, max_x, max_y
    try:
        min_x = min(list(graph.get_all_v().values()), key=lambda n: n.pos[0]).pos[0]
        min_y = min(list(graph.get_all_v().values()), key=lambda n: n.pos[1]).pos[1]
        max_x = max(list(graph.get_all_v().values()), key=lambda n: n.pos[0]).pos[0]
        max_y = max(list(graph.get_all_v().values()), key=lambda n: n.pos[1]).pos[1]
    except:
        TypeError


moves = ""
catches = ""
time_left = ""

""" --------------------------------------------> GUI <--------------------------------------------------------"""


class GUI:
    def __init__(self, graph_, client: Client, game):
        self.graph = graph_
        self.game = game
        self.client = client
        self.client.start()
        self.display(graph=self.graph)

    def update_info(self):
        global moves, catches, time_left

        dic = json.loads(self.client.get_info())

        i = dic["GameServer"]
        moves = i["moves"]
        catches = i["grade"]
        time_left = str(int(self.client.time_to_end()) / 1000)

    def update_game(self):
        pok_str = self.client.get_pokemons()
        self.game.update_list(p_json=pok_str)

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, screen.get_width() - 50, min_x, max_x)
        if y:
            return scale(data, 50, screen.get_height() - 50, min_y, max_y)

    """------------------> END SCALE METHODS <------------------"""

    """------------------> START Draw Methods <-----------------"""

    def arrow(self, start, end, d, h, color):
        dx = float(end[0] - start[0])
        dy = float(end[1] - start[1])
        D = float(math.sqrt(dx * dx + dy * dy))
        xm = float(D - d)
        xn = float(xm)
        ym = float(h)
        yn = -h
        sin = dy / D
        cos = dx / D
        x = xm * cos - ym * sin + start[0]
        ym = xm * sin + ym * cos + start[1]
        xm = x
        x = xn * cos - yn * sin + start[0]
        yn = xn * sin + yn * cos + start[1]
        xn = x
        points = [(end[0], end[1]), (int(xm), int(ym)), (int(xn), int(yn))]

        pygame.draw.aalines(screen, color, True, (start, end), 7)

    """ -------------------------> DRAW <----------------------------"""

    def draw(self, graph, node_display=-1):
        SCREEN_BUTTON_R = screen.get_width() / 4
        """scaling buttons size"""
        moves_button.rect = pygame.Rect(SCREEN_TOPLEFT, (SCREEN_BUTTON_R, 40))
        time_button.rect = pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R, 0), (SCREEN_BUTTON_R, 40))
        catches_button.rect = pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R * 2, 0), (SCREEN_BUTTON_R, 40))
        stop_button.rect = pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R * 3, 0), (SCREEN_BUTTON_R, 40))

        """draw menu"""
        CLICK_col = (177, 177, 177)
        DEAFULT_col = (222, 223, 219)
        STOP_col = (50, 50, 50)
        if moves_button.is_clicked:
            pygame.draw.rect(screen, CLICK_col, moves_button.rect)
        else:
            pygame.draw.rect(screen, DEAFULT_col, moves_button.rect)
        if time_button.is_clicked:
            pygame.draw.rect(screen, CLICK_col, time_button.rect)
        else:
            pygame.draw.rect(screen, DEAFULT_col, time_button.rect)
        if catches_button.is_clicked:
            pygame.draw.rect(screen, CLICK_col, catches_button.rect)
        else:
            pygame.draw.rect(screen, DEAFULT_col, catches_button.rect)
        if stop_button.is_clicked:
            pygame.draw.rect(screen, (177, 177, 177), stop_button.rect)
        else:
            pygame.draw.rect(screen, STOP_col, stop_button.rect)

        pygame.draw.rect(screen, (0, 0, 0), ((0, screen.get_height() - 40), screen.get_rect().bottomright), 3)
        pygame.draw.rect(screen, moves_button.color, moves_button.rect, 3)
        pygame.draw.rect(screen, time_button.color, time_button.rect, 3)
        pygame.draw.rect(screen, catches_button.color, catches_button.rect, 3)
        pygame.draw.rect(screen, stop_button.color, stop_button.rect, 3)

        console_text = CONSOLE_FONT.render(console.con_text, True, (204, 0, 0))
        screen.blit(console_text, (screen.get_rect().right/2.3, screen.get_height() - 40))

        """Moves button box draw"""
        move_text = f"{moves_button.text}{moves}"
        center_but_text = BUTTON_FONT.render(move_text, True, (0, 0, 0))
        screen.blit(center_but_text, (moves_button.rect.topleft[0] + 10, moves_button.rect.topleft[1] + 10))

        """Time Left box draw"""
        if float(time_left) < 10:
            time_button_text = BUTTON_FONT.render(time_button.text + time_left, True, (242, 5, 5))
        else:
            time_button_text = BUTTON_FONT.render(time_button.text + time_left, True, (0, 0, 0))
        screen.blit(time_button_text, (time_button.rect.topleft[0] + 7, time_button.rect.topleft[1] + 10))

        """Catches button box draw"""
        catch_text = f"{catches_button.text}{catches}"
        catch_button_text = BUTTON_FONT.render(catch_text, True, (0, 0, 0))
        screen.blit(catch_button_text,
                    (catches_button.rect.topleft[0] + 10, catches_button.rect.topleft[1] + 10))

        """STOP button box draw"""
        load_button_text = SAVE_LOAD_FONT.render(stop_button.text, True, (253, 196, 0))
        screen.blit(load_button_text,
                    (stop_button.rect.topleft[0] + SCREEN_BUTTON_R / 4 + 40, stop_button.rect.topleft[1] + 7))

        for src in graph.get_all_v().values():
            global RADIUS
            node: Node = src
            x = None
            y = None

            try:
                x = self.my_scale(data=node.pos[0], x=True)
                y = self.my_scale(data=node.pos[1], y=True)
            except:
                TypeError
            src_text = FONT.render(str(node.id), True, (0, 0, 0))
            rect = src_text.get_rect(center=(x, y))

            node_radius = RADIUS
            if x is not None and y is not None:

                gfxdraw.aacircle(screen, int(x), int(y), node_radius, (0, 0, 0))

                gfxdraw.aacircle(screen, int(x), int(y), node_radius - 1, (250, 204, 58))
                gfxdraw.filled_circle(screen, int(x), int(y), node_radius - 1, (250, 204, 58))

                screen.blit(src_text, rect)
                try:
                    for dest in graph.all_out_edges_of_node(node.id):

                        dest: Node = graph.get_all_v()[dest]
                        dest_x = self.my_scale(data=dest.pos[0], x=True)
                        dest_y = self.my_scale(data=dest.pos[1], y=True)

                        src_arrow = ()
                        dest_arrow = ()

                        collition_dest = node_line_inter((x, y), (dest_x, dest_y), (dest_x, dest_y), node_radius)

                        for i in range(collition_dest.__len__() - 1):
                            if math.dist((x, y), collition_dest[i]) < math.dist((x, y), collition_dest[i + 1]):
                                dest_arrow = collition_dest[i]
                            else:
                                dest_arrow = collition_dest[i + 1]

                        collition_src = node_line_inter((dest_x, dest_y), (x, y), (x, y), node_radius)

                        for i in range(collition_src.__len__() - 1):
                            if math.dist((dest_x, dest_y), collition_src[i]) <= math.dist((dest_x, dest_y),
                                                                                          collition_src[i + 1]):
                                src_arrow = collition_src[i]
                            else:
                                src_arrow = collition_src[i + 1]

                        self.arrow(src_arrow, dest_arrow, 17, 7, color=(54, 54, 54))
                except TypeError:
                    pass

        # draw agents
        for a in range(self.game.agent_list.__len__()):
            ag: agent = self.game.agent_list[a]

            x = self.my_scale(data=float(self.game.agent_list[a].pos[0]), x=True)
            y = self.my_scale(data=float(self.game.agent_list[a].pos[1]), y=True)
            pos = (int(x) - 15, int(y) - 15)

            if self.game.agent_list[a].attack_mode:
                agent_image = pygame.image.load("../data/BackgroundPics/gaming.png")
                agent_image = pygame.transform.scale(agent_image, (40, 40))
                screen.blit(agent_image, pos)
            else:
                # draw agent
                agent_image = pygame.image.load("../data/BackgroundPics/pokeball.png")
                agent_image = pygame.transform.scale(agent_image, (25, 25))
                screen.blit(agent_image, pos)


        # draw pokemon
        for p in range(self.game.pokemon_list.__len__()):
            x = self.my_scale(data=float(self.game.pokemon_list[p].pos[0]), x=True)
            y = self.my_scale(data=float(self.game.pokemon_list[p].pos[1]), y=True)
            pos = (int(x) - 15, int(y) - 15)

            if self.game.pokemon_list[p].value <= 5.0:


                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/rattata.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (35, 35))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 6:


                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/bullbasaur.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (35, 35))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 7:


                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/eevee.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (35, 35))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 8:


                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/jigglypuff.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (35, 35))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 9:


                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/snorlax.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (45, 45))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 10:


                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/eevee.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (45, 45))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 11:


                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/jigglypuff.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (45, 45))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 12:
                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/meowth.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (55, 55))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 13:
                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/charmander.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (55, 55))
                screen.blit(pokemon_image, pos)

            elif self.game.pokemon_list[p].value == 14:
                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/psyduck.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (55, 55))
                screen.blit(pokemon_image, pos)


            elif self.game.pokemon_list[p].value >= 15:
                pokemon_image = pygame.image.load("../data/BackgroundPics/PokemonsIcons/pikachu.png")
                pokemon_image = pygame.transform.scale(pokemon_image, (62, 62))
                screen.blit(pokemon_image, pos)

    """------------------> END Draw Methods <-----------------"""

    def display(self, graph):
        # global first
        global start
        min_max(graph)
        node_display = -1
        try:
            while self.client.is_running() == 'true':

                end = time.time()

                if first:
                    time.sleep(0.07)
                else:
                    time.sleep(0.07 - (end - start))

                start = time.time()


                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.client.stop_connection()
                        self.client.stop()
                        exit(0)

                self.update_game()
                self.update_info()

                # refresh rate
                clock.tick(60)

                for a in self.game.agent_list:
                    ag: agent = a
                    if ag.src == ag.explore[0]:
                        if ag.targets[ag.src]:
                            ag.attack_mode = True

                screen.fill((255, 255, 255))
                BackGround = Background("../data/BackgroundPics/main_pic.png", [0, 0])
                BackGround.image.set_alpha(180)
                screen.blit(BackGround.image, BackGround.rect)
                self.draw(graph, node_display)
                pygame.display.update()

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.client.stop()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if stop_button.rect.collidepoint(e.pos):
                            stop_button.press()
                            if stop_button.is_clicked:
                                self.client.stop()
                                self.client.stop_connection()
                                sys.exit()

                # choose next edge
                for a in self.game.agent_list:
                    is_moved = False
                    ag: agent = a
                    if ag.dest == -1:
                        if ag.explore.__len__() > 1:
                            is_moved = True
                            ag.explore.pop(0)
                            next_node = ag.explore[0]
                            self.client.choose_next_edge(
                                '{"agent_id":' + str(ag.id) + ', "next_node_id":' + str(next_node) + '}')

                self.client.move()


                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())

        except:
            ConnectionResetError(WindowsError)
        sys.exit()


moves_button = Button(pygame.Rect(SCREEN_TOPLEFT, (SCREEN_BUTTON_R, 40)), (0, 0, 0), "Moves: ")
time_button = Button(pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R, 0), (SCREEN_BUTTON_R, 40)), (0, 0, 0),
                     "Time Left: ")
catches_button = Button(pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R * 2, 0), (SCREEN_BUTTON_R, 40)), (0, 0, 0,),
                        "Catches: ")
stop_button = Button(pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R * 3, 0), (SCREEN_BUTTON_R, 40)), (0, 0, 0,),
                     "STOP")
