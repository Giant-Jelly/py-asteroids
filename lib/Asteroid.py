import pygame
import random
import math

from lib.Screen import Screen

COLORS_WHITE = (255, 255, 255)
ran_low = 1
ran_high = 1


class Asteroid:
	w = random.randint(50, 100)
	h = random.randint(50, 100)

	def __init__(self, starting_pos):
		self.x, self.y = starting_pos

		self.starting_pos = starting_pos
		self.angle = 0
		self.r_vel = random.randint(10, 100) / 1000
		self.speed_x = random.randint(70, 500) / 100
		self.speed_y = random.randint(70, 500) / 100
		self.start_angle = random.randint(1, 360)
		self.points = [
			(0, 0 - self.h),
			(0 - self.w / 1.5 + random.randint(ran_low, ran_high), 0 - self.h / 1.5 + random.randint(ran_low, ran_high)),
			(0 - self.w + random.randint(ran_low, ran_high), 0 + random.randint(ran_low, ran_high)),
			(0 - self.w / 1.5 + random.randint(ran_low, ran_high), 0 + self.h / 1.5 + random.randint(ran_low, ran_high)),
			(0, 0 + self.h),
			(0 + self.w / 1.5 + random.randint(ran_low, ran_high), 0 + self.h / 1.5 + random.randint(ran_low, ran_high)),
			(0 + self.w + random.randint(ran_low, ran_high), 0 + random.randint(ran_low, ran_high)),
			(0 + self.w / 1.5 + random.randint(ran_low, ran_high), 0 - self.h / 1.5 + random.randint(ran_low, ran_high)),
			(0, 0 - self.h),
		]

	def draw(self, surface):
		self.x += self.speed_x * math.sin(self.start_angle)
		self.y += self.speed_y * math.cos(self.start_angle)

		points = []
		ox, oy = self.get_center()
		for point in self.points:
			x, y = point
			xx = (ox + math.cos(self.angle) * (x - ox) - math.sin(self.angle) * (y - oy)) + self.x
			yy = (oy + math.sin(self.angle) * (x - ox) + math.cos(self.angle) * (y - oy)) + self.y
			points.append((xx, yy))

		self.angle += self.r_vel
		pygame.draw.lines(surface, COLORS_WHITE, False, points, 1)

		self.collisions()

	def get_center(self):
		x = [p[0] for p in self.points]
		y = [p[1] for p in self.points]
		return sum(x) / len(self.points), sum(y) / len(self.points)

	def collisions(self):
		screen_collision_offset = 0
		# Screen Collision
		# Right
		if self.x > Screen.w + screen_collision_offset + self.w:
			self.x = 0 - screen_collision_offset - self.w

		# Left
		if self.x < 0 - screen_collision_offset - self.w:
			self.x = Screen.w + screen_collision_offset + self.w

		# Bottom
		if self.y > Screen.h + screen_collision_offset + self.h:
			self.y = 0 - screen_collision_offset - self.h

		# Top
		if self.y < 0 - screen_collision_offset - self.h:
			self.y = Screen.h + screen_collision_offset + self.h


