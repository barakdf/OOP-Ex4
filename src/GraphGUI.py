import pygame
import os
from GraphAlgo import *
from DiGraph import *
import math
from pygame import gfxdraw
from tkinter import filedialog as fd

from src import GraphAlgoInterface
from src.GraphAlgo import GraphAlgo

pygame.font.init()
FONT = pygame.font.SysFont("Ariel", 20)
BUTTON_FONT = pygame.font.SysFont("Ariel", 30)
SAVE_LOAD_FONT = pygame.font.SysFont("Ariel", 40)
CONSOLE_FONT = pygame.font.SysFont("Ariel", 30)

screen = pygame.display.set_mode((1600, 800), flags=pygame.RESIZABLE)
SCREEN_TOPLEFT = screen.get_rect().topleft
SCREEN_BUTTON_R = screen.get_width() / 5
RADIUS = 10


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


class ActionButton:
    def __init__(self, rect: pygame.Rect, color, text):
        self.rect = rect
        self.color = color
        self.text = text
        self.is_clicked = False
        self.show = False
        self.insert = False
        self.start = False

    def press(self):
        self.is_clicked = not self.is_clicked

    def showButt(self):
        self.show = not self.show
        self.insert = not self.insert
        self.start = not self.start


class Button:
    def __init__(self, rect: pygame.Rect, color, text, func=None):
        self.rect = rect
        self.color = color
        self.text = text
        self.func = func
        self.is_clicked = False

    def press(self):
        self.is_clicked = not self.is_clicked


class NodeScreen:
    def __init__(self, rect: pygame.rect, id):
        self.id = id
        self.rect = rect


class Console:
    def __init__(self):
        self.func = ""
        self.src = ""
        self.dest = ""
        self.con_text = "welcome to BOY Graph."

    def welcome(self):
        self.func = ""
        self.src = ""
        self.dest = ""
        self.con_text = "welcome to BOY Graph."

    def set_func(self, func_name, src="", dest=""):
        global cities
        if func_name == "ShortestPath":
            init_src = ""
            init_dest = ""
            if src == "":
                src = ".. please choose source"
            else:
                init_src = "src id:"
                if dest == "":
                    dest = ".. please choose destination"
                else:
                    init_dest = "dest id:"
            self.con_text = f"{func_name} {init_src} {src} {init_dest} {dest}"
            # self.func = func_name
        if func_name == "CenterPoint":
            self.con_text = f"The {func_name} of this graph is : {center_id.__getitem__(0)}"

        if func_name == "TSP":
            if cities.__len__() == 0:
                self.con_text = "choose nodes for TSP"
            else:
                self.con_text = f"TSP path {cities}"

    def print_shortest(self, src, dest, path, dist):
        action_button.showButt()
        self.con_text = f"The Shortest Path from {src} to {dest} is {path}. distance: {dist}"

    def print_TSP(self, path, dist):
        global start_tsp
        action_button.showButt()
        print(path)
        start_tsp = False
        self.con_text = f"The TSP path is {path}, and total distance is {dist}"


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


shortest_path = {}
shortest_src_dest = -1
center_id = []
nodes_screen = []

tsp_ans = {}
cities = []
start_tsp = False


class GUI:
    def __init__(self, graph):
        self.graph_algo = GraphAlgo(graph)
        self.display(self.graph_algo)

    # def __init__(self, file: str = None):
    #     graph = DiGraph()
    #     self.graph_algo: GraphAlgoInterface = GraphAlgo(graph)
    #     self.graph_algo.load_from_json(file)
    #     self.display(self.graph_algo)

    def init_graph(self, file: str):
        self.graph_algo.load_from_json(file)
        self.display(self.graph_algo)

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

        pygame.draw.aaline(screen, color, start, end, 4)

        gfxdraw.aapolygon(screen, points, color)
        gfxdraw.filled_polygon(screen, points, color)

    def clicked_center(self, button: Button):
        global center_id
        center = button.func()
        center_id.append(center[0])

    def clicked_shortest(self, button: Button, src=None, dest=None):
        global shortest_path
        shortest_path_func = button.func(int(src), int(dest))
        shortest_path["dist"] = shortest_path_func[0]
        shortest_path["list"]: list = shortest_path_func[1]
        shortest_path["edges"]: list = []
        shortest_path.get("edges")
        print(shortest_path_func[1])
        for i in range(shortest_path["list"].__len__() - 1):
            shortest_path["edges"].append(
                (shortest_path["list"].__getitem__(i), shortest_path["list"].__getitem__(i + 1)))
        print(shortest_path)
        console.print_shortest(src, dest, path=shortest_path["list"], dist=shortest_path["dist"])

    def clicked_tsp(self, button: Button, list_cities):
        global cities
        global tsp_ans
        tsp_ans_func = button.func(list_cities)
        tsp_ans["list"] = tsp_ans_func[0]
        tsp_ans["dist"] = tsp_ans_func[1]
        console.set_func("TSP")
        if start_tsp:
            print("GERE", tsp_ans["list"])
            console.print_TSP(tsp_ans["list"], tsp_ans["dist"])

    """ -------------------------> DRAW <----------------------------"""

    def draw(self, graph: GraphInterface, node_display=-1):
        """draw menu"""
        algo_CLICK_col = (177, 177, 177)
        algo_DEAFULT_col = (222, 223, 219)
        LOAD_SAVE_DEAFULT = (50, 50, 50)
        if center_button.is_clicked:
            pygame.draw.rect(screen, algo_CLICK_col, center_button.rect)
        else:
            pygame.draw.rect(screen, algo_DEAFULT_col, center_button.rect)
        if shortest_button.is_clicked:
            pygame.draw.rect(screen, algo_CLICK_col, shortest_button.rect)
        else:
            pygame.draw.rect(screen, algo_DEAFULT_col, shortest_button.rect)
        if tsp_button.is_clicked:
            pygame.draw.rect(screen, algo_CLICK_col, tsp_button.rect)
        else:
            pygame.draw.rect(screen, algo_DEAFULT_col, tsp_button.rect)
        if load_button.is_clicked:
            pygame.draw.rect(screen, (177, 177, 177), load_button.rect)
        else:
            pygame.draw.rect(screen, LOAD_SAVE_DEAFULT, load_button.rect)
        if save_button.is_clicked:
            pygame.draw.rect(screen, (177, 177, 177), save_button.rect)
        else:
            pygame.draw.rect(screen, LOAD_SAVE_DEAFULT, save_button.rect)

        """Console Draw"""
        pygame.draw.rect(screen, (222, 223, 219), ((0, screen.get_height() - 40), screen.get_rect().bottomright))

        """draw Action_Button"""
        if action_button.show:
            pygame.draw.rect(screen, (200, 191, 231), action_button.rect)

        pygame.draw.rect(screen, (0, 0, 0), ((0, screen.get_height() - 40), screen.get_rect().bottomright), 3)
        pygame.draw.rect(screen, center_button.color, center_button.rect, 3)
        pygame.draw.rect(screen, shortest_button.color, shortest_button.rect, 3)
        pygame.draw.rect(screen, tsp_button.color, tsp_button.rect, 3)
        pygame.draw.rect(screen, load_button.color, load_button.rect, 3)
        pygame.draw.rect(screen, save_button.color, save_button.rect, 3)

        console_text = CONSOLE_FONT.render(console.con_text, True, (0, 0, 0))
        screen.blit(console_text, (5, screen.get_height() - 30))

        if node_display != -1:
            node_text = FONT.render(str(node_display), True, (0, 0, 0))
            screen.blit(node_text, (300, 20))

        """center_point button box draw"""
        center_but_text = BUTTON_FONT.render(center_button.text, True, (0, 0, 0))
        screen.blit(center_but_text, (center_button.rect.topleft[0] + 10, center_button.rect.topleft[1] + 10))

        """shortest_button box draw"""
        shortest_button_text = BUTTON_FONT.render(shortest_button.text, True, (0, 0, 0))
        screen.blit(shortest_button_text, (shortest_button.rect.topleft[0] + 7, shortest_button.rect.topleft[1] + 10))

        """TSP button box draw"""
        tsp_button_text = BUTTON_FONT.render(tsp_button.text, True, (0, 0, 0))
        screen.blit(tsp_button_text,
                    (tsp_button.rect.topleft[0] + 10, tsp_button.rect.topleft[1] + 10))

        """LOAD button box draw"""
        load_button_text = SAVE_LOAD_FONT.render(load_button.text, True, (253, 196, 0))
        screen.blit(load_button_text,
                    (load_button.rect.topleft[0] + SCREEN_BUTTON_R / 4 + 40, load_button.rect.topleft[1] + 7))

        """SAVE button box draw"""
        save_button_text = SAVE_LOAD_FONT.render(save_button.text, True, (253, 196, 0))
        screen.blit(save_button_text,
                    (save_button.rect.topleft[0] + SCREEN_BUTTON_R / 4 + 40, save_button.rect.topleft[1] + 7))

        """Action button box draw"""
        if action_button.show:
            if action_button.insert:
                action_button.text = "INSERT"
            else:
                action_button.text = "START"
            action_button_text = BUTTON_FONT.render(action_button.text, True, (0, 0, 0))
            screen.blit(action_button_text,
                        (action_button.rect.topleft[0] + 40, action_button.rect.topleft[1] + 12))

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

            v = graph.v_size()

            node_radius = RADIUS
            if x is not None and y is not None:
                nodes_screen.append(NodeScreen(pygame.Rect((x - node_radius, y - node_radius), (20, 20)), node.id))

                gfxdraw.aacircle(screen, int(x), int(y), node_radius, (0, 0, 0))

                if node.id in center_id:
                    gfxdraw.aacircle(screen, int(x), int(y), node_radius - 1, (250, 0, 0))
                    gfxdraw.filled_circle(screen, int(x), int(y), node_radius - 1, (250, 0, 0))


                elif shortest_path.get("list"):
                    if node.id in shortest_path["list"]:
                        gfxdraw.aacircle(screen, int(x), int(y), node_radius - 1, (192, 250, 247))
                        gfxdraw.filled_circle(screen, int(x), int(y), node_radius - 1, (192, 250, 247))
                    else:
                        gfxdraw.aacircle(screen, int(x), int(y), node_radius - 1, (250, 204, 58))
                        gfxdraw.filled_circle(screen, int(x), int(y), node_radius - 1, (250, 204, 58))

                else:
                    gfxdraw.aacircle(screen, int(x), int(y), node_radius - 1, (250, 204, 58))
                    gfxdraw.filled_circle(screen, int(x), int(y), node_radius - 1, (250, 204, 58))

                screen.blit(src_text, (x - (node_radius / 2), y - (node_radius / 2)))
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

                        if shortest_path.get("list"):

                            if (node.id, dest.id) in shortest_path["edges"]:
                                self.arrow(src_arrow, dest_arrow, 17, 7, color=(192, 250, 247))
                            else:
                                self.arrow(src_arrow, dest_arrow, 17, 7, color=(255, 255, 255))
                        else:
                            self.arrow(src_arrow, dest_arrow, 17, 7, color=(255, 255, 255))
                except TypeError:
                    pass

    """------------------> END Draw Methods <-----------------"""

    shortest_counter = 0
    path_src = -1

    def display(self, algo):
        global shortest_counter, path_src
        global shortest_src_dest
        global cities, start_tsp
        center_button.func = algo.centerPoint
        shortest_button.func = algo.shortest_path
        tsp_button.func = algo.TSP
        min_max(algo.get_graph())
        node_display = -1

        run = True
        while run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    """Actions of center button"""
                    if center_button.rect.collidepoint(e.pos):
                        center_button.press()
                        action_button.show = False

                        """Stop action of other buttons"""
                        self.stop_other_buttons(center=True)

                        """manage button activity"""
                        if center_button.is_clicked:
                            self.clicked_center(center_button)
                            console.set_func("CenterPoint")
                        else:
                            center_id.clear()

                    """Actions of shortestPath button"""
                    if shortest_button.rect.collidepoint(e.pos):
                        shortest_button.press()
                        action_button.show = True
                        action_button.start = False
                        action_button.insert = True
                        """Stop action of other buttons"""
                        self.stop_other_buttons(shortest=True)

                        """manage button activity"""
                        if shortest_button.is_clicked:
                            shortest_counter = 0
                            print("SHORTEST", shortest_counter)
                            console.set_func("ShortestPath")

                        else:
                            shortest_path.clear()
                            nodes_screen.clear()
                    """Actions of TSP button"""
                    if tsp_button.rect.collidepoint(e.pos):
                        tsp_button.press()
                        action_button.show = True
                        action_button.insert = False
                        action_button.start = True
                        """Stop action of other buttons"""
                        self.stop_other_buttons(tsp=True)

                        """manage button activity"""
                        if tsp_button.is_clicked:
                            console.set_func("TSP")

                    """Actions of LOAD button"""
                    if load_button.rect.collidepoint(e.pos):
                        load_button.press()
                        self.stop_other_buttons(load=True)
                        if load_button.is_clicked:
                            filename = fd.askopenfilename()
                            load_button.is_clicked = False
                            self.init_graph(filename)
                            run = False

                    """Actions of SAVE button"""
                    if save_button.rect.collidepoint(e.pos):
                        save_button.press()
                        if save_button.is_clicked:
                            filename = f"{fd.asksaveasfilename()}.json"
                            save_button.is_clicked = False
                            self.graph_algo.save_to_json(filename)

                    """relevant methods for shortest_path"""
                    if shortest_button.is_clicked:
                        for n in nodes_screen:
                            if n.rect.collidepoint(e.pos):
                                shortest_src_dest = n.id
                                shortest_counter += 1
                                break
                        if shortest_counter == 1:
                            console.set_func("ShortestPath", src=shortest_src_dest)
                            path_src = shortest_src_dest
                        elif shortest_counter == 2:
                            console.set_func("ShortestPath", src=str(path_src), dest=shortest_src_dest)
                            self.clicked_shortest(shortest_button, src=path_src, dest=shortest_src_dest)
                            shortest_counter = 3

                        """relevant methods for TSP"""
                    elif tsp_button.is_clicked:
                        for n in nodes_screen:
                            if n.rect.collidepoint(e.pos):
                                cities.append(n.id)
                                self.clicked_tsp(tsp_button, cities)
                                break
                        if action_button.rect.collidepoint(e.pos):
                            if cities.__len__() > 0:
                                start_tsp = True
                                self.clicked_tsp(tsp_button, cities)
                                cities.clear()


                    elif not center_button.is_clicked and not tsp_button.is_clicked:
                        action_button.show = False
                        console.welcome()

            screen.fill((210, 180, 140))
            self.draw(algo.get_graph(), node_display)
            pygame.display.update()

    def stop_other_buttons(self, tsp=False, shortest=False, center=False, load=False):
        if center:
            if shortest_button.is_clicked:
                shortest_button.press()
                shortest_path.clear()
            if tsp_button.is_clicked:
                tsp_button.press()
                cities.clear()
        if shortest:
            if center_button.is_clicked:
                center_button.press()
                center_id.clear()
            if tsp_button.is_clicked:
                tsp_button.press()
                cities.clear()
        if tsp:
            if shortest_button.is_clicked:
                shortest_button.press()
                shortest_path.clear()
            if center_button.is_clicked:
                shortest_counter = 0
                center_button.press()
                center_id.clear()
        if load:
            if shortest_button.is_clicked:
                shortest_button.press()
                shortest_path.clear()
            if center_button.is_clicked:
                shortest_counter = 0
                center_button.press()
                center_id.clear()
            if tsp_button.is_clicked:
                tsp_button.press()
                cities.clear()


center_button = Button(pygame.Rect(SCREEN_TOPLEFT, (SCREEN_BUTTON_R, 40)), (0, 0, 0), "Center Point Algorithm")
shortest_button = Button(pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R, 0), (SCREEN_BUTTON_R, 40)), (0, 0, 0),
                         "Shortest Path Algorithm")
tsp_button = Button(pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R * 2, 0), (SCREEN_BUTTON_R, 40)), (0, 0, 0,),
                    "TSP Algorithm")
load_button = Button(pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R * 3, 0), (SCREEN_BUTTON_R, 40)), (0, 0, 0,),
                     "LOAD")
save_button = Button(pygame.Rect((SCREEN_TOPLEFT[0] + SCREEN_BUTTON_R * 4, 0), (SCREEN_BUTTON_R, 40)), (0, 0, 0,),
                     "SAVE")
action_button = ActionButton(pygame.Rect((screen.get_rect().right - SCREEN_BUTTON_R / 2, screen.get_height() - 40),
                                         (screen.get_rect().right, screen.get_rect().bottomright[1])), (0, 0, 0),
                             "START")