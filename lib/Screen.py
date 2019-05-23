import pygame
import random

star_amount = 1000


class Screen:

	w = 1000
	h = 1000

	def __init__(self):
		self.screen = pygame.display.set_mode((self.w, self.h))

		self.stars = []
		for i in range(0, star_amount):
			star = {
				'position': (random.randint(0, self.w), random.randint(0, self.h)),
				'shade': random.randint(0, 255),
				'width': random.randint(1, 5)
			}
			self.stars.append(star)
		pygame.display.set_caption('Asteroids')

	def draw_bg(self):
		for star in self.stars:
			pygame.draw.line(self.screen, (star['shade'], star['shade'], star['shade']), star['position'], star['position'])
