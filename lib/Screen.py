import pygame


class Screen:

	w = 1000
	h = 1000

	def __init__(self):
		self.screen = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption('Asteroids')

