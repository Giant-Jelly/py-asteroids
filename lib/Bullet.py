import math
import pygame

from lib import parameters
from lib.Screen import Screen


class Bullet:

	w = 3
	h = 6

	def __init__(self, x, y, angle):
		self.x = x
		self.y = y
		self.angle = angle
		self.vel = 15
		self.lifetime = 50
		self.life = self.lifetime
		self.collision_radius = self.h

		self.points = [
			(0, 3),
			(0, -3),
		]

	def draw(self, screen):
		self.x += self.vel * math.sin(self.angle)
		self.y -= self.vel * math.cos(self.angle)

		points = []
		for point in self.points:
			x = point[0] * math.cos(self.angle) - point[1] * math.sin(self.angle) + self.x
			y = point[0] * math.sin(self.angle) + point[1] * math.cos(self.angle) + self.y
			points.append((x, y))

		self.collisions()

		pygame.draw.lines(screen, parameters.COLORS_WHITE, False, points, 3)

	def center(self):
		x = [p[0] for p in self.points]
		y = [p[1] for p in self.points]
		return round(sum(x) / len(self.points)), round(sum(y) / len(self.points))

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
