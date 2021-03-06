# coding: utf-8


import pygame
from pygame.locals import *
import os
import random


""" This class manage the graphical part of the game"""


class Pygame:

    BLOCK_PX_SIZE = 30
    BANNER_HEIGHT = 82

    def __init__(self, maze_dico, charac1, charac2, *items):
        self.maze_dico = self.maze_convert(maze_dico)
        self.charac1 = charac1
        self.charac2 = charac2
        self.items = items
        self.position_charac1 = None
        self.item_dic = {}
        pygame.init()
        self.caption = str(charac1.name).capitalize() + " a ramassé : "
        pygame.display.set_caption(self.caption)
        self.x_res = (self.get_max_row() + Pygame.BLOCK_PX_SIZE)
        self.y_res = (self.get_max_line() + Pygame.BLOCK_PX_SIZE)
        # graph loop
        self.game_loop = 1
        # Pygame window opening
        self.window = pygame.display.set_mode((self.y_res, self.x_res + Pygame.BANNER_HEIGHT))
        # backgroung load
        self.background = pygame.Surface(self.window.get_size())
        img_path = os.path.dirname(__file__) + "/" + "images" + "/"
        # banner load
        self.banner = pygame.image.load(img_path + "banner.png").convert()
        # wall block load
        self.wall = pygame.image.load(img_path + "wall.png").convert_alpha()
        # charac image import
        self.charac1_image = pygame.image.load(img_path + self.charac1.name + ".png").convert_alpha()
        self.charac2_image = pygame.image.load(img_path + self.charac2.name + ".png").convert_alpha()
        # define graphical init position of character (first occurrence of "S" value in maze_dico)
        self.position_charac1 = \
            self.charac1_image.get_rect(topleft=[key for key, value in self.maze_dico.items() if value == "S"][0])
        self.position_charac2 = \
            self.charac2_image.get_rect(topleft=[key for key, value in self.maze_dico.items() if value == "A"][0])
        self.items_dic()
        self.murdoc = pygame.transform.scale(pygame.image.load(img_path + "murdoc.jpg").convert(),
                                             (self.y_res, self.x_res))
        self.victory = pygame.transform.scale(pygame.image.load(img_path + "victory.jpg").convert(),
                                              (self.y_res, self.x_res))
        self.menu = 0
        self.win = 0

    def maze_convert(self, maze_dico):
        # maze_dico in pixel size and x/y coordinates inversion for graph usage
        for key, value in list(maze_dico.items()):
            maze_dico[((key[1] * Pygame.BLOCK_PX_SIZE), (key[0] * Pygame.BLOCK_PX_SIZE))] = value
            # key (0, 0) is the single common key between original and updated dico. Should not be removed
            if key != (0, 0):
                del maze_dico[key]
        return maze_dico

    def get_max_line(self):
        return max([key[0] for key in self.maze_dico.keys()])

    def get_max_row(self):
        return max([key[1] for key in self.maze_dico.keys()])

    def format_pos(self, rect):
        return tuple(rect)[:2]

    def format_move_pos(self, direction):
        return tuple(list(self.position_charac1.move(direction)))[:2]

    def new_pos(self, direction):
        if self.format_move_pos(direction) in self.maze_dico and self.maze_dico[self.format_move_pos(direction)] != "W":
            self.position_charac1 = self.position_charac1.move(direction)
        return self.position_charac1

    def items_dic(self):
        pos_list = [key for key, value in self.maze_dico.items() if value == "P"]
        for item in self.items:
            rand_numb = random.randint(0, len(pos_list) - 1)
            # create an items dictionary. Key = item's name. Value is a list with 3 indexes
            # {"item_name": [random_position, picked_state 0=unpicked 1=already picked_up, image surface rect]}
            self.item_dic[item] = [pos_list.pop(rand_numb), 0,
                                   pygame.image.load(os.path.dirname(__file__) + "/"
                                                     + "images" + "/" + item + ".png").convert_alpha()]
        return self.item_dic

    def test_win(self):
        if self.format_pos(self.position_charac1) == self.format_pos(self.position_charac2) and sum(
                [value[1] for value in self.item_dic.values()]) == len(self.items):
            self.caption = "VOUS AVEZ GAGNE !!! BRAVO !!!"
            pygame.display.set_caption(self.caption)
            self.menu = 1
            self.win = 1
            # pygame.time.delay(3000)
        elif self.format_pos(self.position_charac1) == self.format_pos(self.position_charac2) and sum(
                [value[1] for value in self.item_dic.values()]) != len(self.items):
            self.caption = "PERDU !!! IL MANQUAIT DES OBJETS !!!"
            pygame.display.set_caption(self.caption)
            self.menu = 1
            self.win = 0

    def items_display(self):
        for key, value in self.item_dic.items():
            # test if charac came on item position. If yes, counter item value[1] is set to 1
            if self.format_pos(self.position_charac1) == value[0] and value[1] != 1:
                self.item_dic[key][1] = 1
                self.caption += (str(key).capitalize() + " - ")
                if sum([value[1] for value in self.item_dic.values()]) == len(self.items):
                    self.caption += " GO !  "
            elif value[1] != 1:
                self.window.blit(value[2], value[0])

    def inventory_banner_update(self):
        for key, value in self.item_dic.items():
            if value[1] == 1 and key == "tube":
                self.window.blit(value[2], (105, self.x_res + 5))
            elif value[1] == 1 and key == "ether":
                self.window.blit(value[2], (5, self.x_res + 5))
            elif value[1] == 1 and key == "aiguille":
                self.window.blit(value[2], (205, self.x_res + 5))

    def game_display(self):
        self.window.blit(self.background, (0, 0))
        self.background.fill((200, 180, 130))
        self.window.blit(self.banner, (0, self.x_res))
        [self.window.blit(self.wall, key) for key, value in self.maze_dico.items() if value == "W"]
        self.window.blit(self.charac2_image, self.position_charac2)
        self.window.blit(self.charac1_image, self.position_charac1)
        self.inventory_banner_update()
        self.items_display()
        pygame.display.set_caption(self.caption)
        pygame.display.flip()

    def game_init(self):
        self.win = 0
        self.caption = str(self.charac1.name).capitalize() + " a ramassé : "
        self.position_charac1 = \
            self.charac1_image.get_rect(topleft=[key for key, value in self.maze_dico.items() if value == "S"][0])

    def end_menu_display(self):
        if self.win == 1:
            self.window.blit(self.victory, (0, 0))
        elif self.win == 0:
            self.window.blit(self.murdoc, (0, 0))

    def graphic_maze(self):
        # direction move keys variable assignment
        left = (-Pygame.BLOCK_PX_SIZE, 0)
        right = (Pygame.BLOCK_PX_SIZE, 0)
        up = (0, -Pygame.BLOCK_PX_SIZE)
        down = (0, Pygame.BLOCK_PX_SIZE)
        pygame.key.set_repeat(50, 30)

        while self.game_loop:
            self.game_init()

            while self.menu != 1 and self.game_loop != 0:
                pygame.time.Clock().tick(30)
                for event in pygame.event.get():
                    if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                        self.game_loop = 0
                    if event.type == KEYDOWN:
                        if event.key == K_LEFT:
                            self.new_pos(left)
                        elif event.key == K_RIGHT:
                            self.new_pos(right)
                        elif event.key == K_UP:
                            self.new_pos(up)
                        elif event.key == K_DOWN:
                            self.new_pos(down)
                self.game_display()
                self.test_win()

            while self.menu == 1 and self.game_loop != 0:
                pygame.time.Clock().tick(30)
                for event in pygame.event.get():
                    if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                        self.menu = 0
                        self.game_loop = 0

                    elif event.type == KEYDOWN and event.key == K_RETURN:
                        self.items_dic()
                        self.menu = 0

                self.end_menu_display()
                pygame.display.flip()


if __name__ == "__main__":
    pass
