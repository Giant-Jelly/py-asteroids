import math
import pygame

from lib import parameters
from lib.Screen import Screen


class Bullet:

	def __init__(self, x, y, angle):
		self.x = x
		self.y = y
		self.angle = angle
		self.vel = 15
		self.lifetime = 50
		self.life = self.lifetime

		self.bullet = [
			(0, -3),
			(0, -6),
		]

	def draw(self, screen):
		self.x += self.vel * math.sin(self.angle)
		self.y -= self.vel * math.cos(self.angle)

		points = []
		for point in self.bullet:
			x = point[0] * math.cos(self.angle) - point[1] * math.sin(self.angle) + self.x + 50
			y = point[0] * math.sin(self.angle) + point[1] * math.cos(self.angle) + self.y + 50
			points.append((x, y))

		self.collisions()

		pygame.draw.lines(screen, parameters.COLORS_WHITE, False, points, 3)

	def collisions(self):
		screen_collision_offset = 15
		# Screen collision
		# Right
		if self.x > Screen.w + screen_collision_offset:
			self.x = -55 - screen_collision_offset

		# Left
		if self.x < -55 - screen_collision_offset:
			self.x = Screen.w + screen_collision_offset

		# Bottom
		if self.y > Screen.h + screen_collision_offset:
			self.y = -55 - screen_collision_offset

		# Top
		if self.y < -55 - screen_collision_offset:
			self.y = Screen.h + screen_collision_offset
