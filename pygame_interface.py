# -*- coding: utf8 -*-

import pygame
from pygame.locals import *
import os
import random

class Pygame:

    BLOCK_PX_SIZE = 30

    def __init__(self, maze_dico, charac1, charac2, *items):
        self.maze_dico = self.maze_convert(maze_dico)
        self.charac1 = charac1
        self.charac2 = charac2
        self.items = items
        self.position_charac1 = None
        self.item_dic = {}
        self.resolution()

    def maze_convert(self, maze_dico):
        # maze_dico in pixel size and x/y coordinates inversion for graph usage
        for key, value in list(maze_dico.items()):
            maze_dico[((key[1] * Pygame.BLOCK_PX_SIZE), (key[0] * Pygame.BLOCK_PX_SIZE))] = value
            # key (0, 0) is the single common key between original and updated dico. Should not be removed
            if key != ((0, 0)):
                del maze_dico[key]
        return maze_dico

    def get_max_line(self):
        return max([key[0] for key in self.maze_dico.keys()])

    def get_max_row(self):
        return max([key[1] for key in self.maze_dico.keys()])

    def resolution(self):
        self.x_resolution = (self.get_max_row() + Pygame.BLOCK_PX_SIZE)
        self.y_resolution = (self.get_max_line() + Pygame.BLOCK_PX_SIZE)

    def format_move_pos(self, direction):
        return tuple(list(self.position_charac1.move(direction)))[0:2]

    def new_pos(self, direction):
        if self.format_move_pos(direction) in self.maze_dico and self.maze_dico[self.format_move_pos(direction)] != "W":
            self.position_charac1 = self.position_charac1.move(direction)
        return self.position_charac1

    # def items_dic(self):                  # JE NE PEUX PAS UTILISER CETTE FONCTION CAR EN DEHORS PYGAME.INIT()
    #     pos_list = [key for key, value in self.maze_dico.items() if value == "P"]
    #     for item in self.items:
    #         print(self.items)
    #         print(item)
    #         item = pygame.image.load(os.path.dirname(__file__) + "/" + "images" + "/" + item + ".png").convert_alpha()
    #         rand_numb = random.randint(0, len(pos_list) - 1)
    #         item_dic[item] = pos_list.pop(rand_numb)
    #     return self.item_dic


    def graphic_maze(self):

        pygame.init()

        # Pygame window opening
        fenetre = pygame.display.set_mode((self.y_resolution, self.x_resolution))

        # backgroung load
        fond = pygame.image.load(os.path.dirname(__file__) + "/" + "images" + "/" + "background.jpg").convert()

        # wall block load
        wall = pygame.image.load(os.path.dirname(__file__) + "/" + "images" + "/" + "wall.png").convert_alpha()

        # charac image import
        self.charac1_image = pygame.image.load(os.path.dirname(__file__) + "/" + "images" + "/" + self.charac1.name + ".png").convert_alpha()
        self.charac2_image = pygame.image.load(os.path.dirname(__file__) + "/" + "images" + "/" + self.charac2.name + ".png").convert_alpha()

        # items loading
        pos_list = [key for key, value in self.maze_dico.items() if value == "P"]
        for item in self.items:
            item = pygame.image.load(os.path.dirname(__file__) + "/" + "images" + "/" + item + ".png").convert_alpha()
            rand_numb = random.randint(0, len(pos_list) - 1)
            self.item_dic[item] = pos_list.pop(rand_numb)


        # define graphical init position of character (first occurrence of "S" value in maze_dico)
        self.position_charac1 = self.charac1_image.get_rect(topleft=[key for key, value in self.maze_dico.items() if value == "S"][0])
        self.position_charac2 = self.charac2_image.get_rect(topleft=[key for key, value in self.maze_dico.items() if value == "A"][0])

        # Graph loop
        continuer = 1

        # direction move keys variable assignment
        left = (-Pygame.BLOCK_PX_SIZE, 0)
        right = (Pygame.BLOCK_PX_SIZE, 0)
        up = (0, -Pygame.BLOCK_PX_SIZE)
        down = (0, Pygame.BLOCK_PX_SIZE)

        while continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continuer = 0
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.new_pos(left)
                    elif event.key == K_RIGHT:
                        self.new_pos(right)
                    elif event.key == K_UP:
                        self.new_pos(up)
                    elif event.key == K_DOWN:
                        self.new_pos(down)
             #Re-collage
            fenetre.blit(fond, (0, 0))
            [fenetre.blit(wall, key) for key, value in self.maze_dico.items() if value == "W"]
            fenetre.blit(self.charac2_image, self.position_charac2)
            fenetre.blit(self.charac1_image, self.position_charac1)
            for key, value in self.item_dic.items():
                fenetre.blit(key, value)

            #Rafraichissement
            pygame.display.flip()



if __name__ == "__main__":
    pass