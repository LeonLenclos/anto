#!/usr/bin/env python3

"""A small game"""

import pygame
import sys
import numpy as np

def load_image(name):
    image = pygame.image.load(name)
    return image

class Ant():
    """The Ant, main character of the game"""

    # Constants
    WALKING, BOUNCING, DOWN, UP = 0, 1, 2, 3
    LEFT, RIGHT = True, False

    def __init__(self, pos=(0, 0)):
        """Init the Ant with a position"""
        self.sprites = {}
        self.sprites[Ant.WALKING] = Sprite("walk", range(4))
        self.sprites[Ant.BOUNCING] = Sprite("bounce", range(6))
        # For now, no animations for up and down, so i just copy bouncing
        self.sprites[Ant.DOWN] = self.sprites[Ant.UP] = self.sprites[Ant.BOUNCING]

        self.state = Ant.BOUNCING
        self.current_sprite = self.sprites[self.state]
        self.speed = 6
        self.dir = Ant.RIGHT
        self.pos = pos
        self.width =  self.sprites[0].rect.width
        self.height = self.sprites[0].rect.height
        print(self.height)

    def up(self):
        self.state = Ant.UP

    def down(self):
        self.state = Ant.DOWN

    def left(self):
        self.move(Ant.LEFT)

    def right(self):
        self.move(Ant.RIGHT)

    def update(self, world_width):
        # Position

        if self.pos[0] < 0 - self.width:
            self.pos[0] = world_width
        elif self.pos[0] > world_width:
            self.pos[0] = 0 - self.width

        # Animation
        self.current_sprite = self.sprites[self.state]
        self.current_sprite.flip = self.dir
        self.current_sprite.update()

        # Reset
        self.state = Ant.BOUNCING

    def draw(self, surface, pos=(0, 0)):
        pos = np.add(self.pos, pos)
        self.current_sprite.draw(surface, pos)

    def move(self, dir):
        self.dir = dir
        self.pos = np.add(self.pos, (self.speed if not dir else -self.speed, 0))
        self.state = Ant.WALKING

class Sprite(pygame.sprite.Sprite):
    def __init__(self, name, iterable):
        super(Sprite, self).__init__()
        self.images = []
        for i in iterable:
            self.images.append(load_image('sprite/{}/{}.png'.format(name, i)))
        # assuming both images are 64x64 pixels

        self.index = 0
        self.image = self.images[self.index]
        size = self.image.get_rect().size
        self.rect = pygame.Rect(0, 0, *size)
        self.flip = False

    def update(self):
        '''This method iterates through the elements inside self.images and
        displays the next one each tick. For a slower animation, you may want to
        consider using a timer of some sort so it updates slower.'''
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def draw(self, surface, pos=(0, 0)):
        surface.blit(self.image, pos)

def main():
    pygame.init()
    size = width, height = 500, 200
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    fg = load_image('sprite/world/fg.png')
    bg = load_image('sprite/world/bg.png')

    ant = Ant()


    while True:

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]: ant.right()
        elif pressed[pygame.K_LEFT]: ant.left()
        elif pressed[pygame.K_DOWN]: ant.down()
        elif pressed[pygame.K_UP]: ant.up()

        ant.update(world_width=width)

        screen.fill((220, 220, 220))
        screen.blit(bg, (0, 0))
        ant.draw(screen, (0, height-27-ant.height))
        screen.blit(fg, (0, 0))
        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()
