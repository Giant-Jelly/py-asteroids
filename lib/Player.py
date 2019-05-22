import pygame
from pygame.math import Vector2
import math
import random

from lib.Screen import Screen
from lib.Bullet import Bullet

COLORS_WHITE = (255, 255, 255)
MAX_BULLETS = 3
SHOOT_DELAY = 5


class Player:
	w = 30
	h = 40

	def __init__(self):
		self.forward = Vector2(0, -1)

		self.x = 0
		self.y = 0
		self.vel = 0.2
		self.r_vel = 0.1
		fin_offset = 10
		self.angle = 0
		self.speed_x = 0
		self.speed_y = 0
		self.drag = 0.99

		self.points = [
			(0, 0 - (self.h / 2)),
			(0 + (self.w / 2), 0 + (self.h / 2)),
			(0 + (self.w / 2) - fin_offset, 0 + (self.h / 2) - fin_offset),
			(0 - (self.w / 2) + fin_offset, 0 + (self.h / 2) - fin_offset),
			(0 - (self.w / 2), 0 + (self.h / 2)),
			(0, 0 - (self.h / 2)),
		]

		self.booster = [
			(0 + (self.w / 2) - fin_offset, 0 + (self.h / 2) - fin_offset + 5),
			(0 - (self.w / 2) + fin_offset, 0 + (self.h / 2) - fin_offset + 5),
			(0, 0 + (self.h / 2) + 5),
			(0 + (self.w / 2) - fin_offset, 0 + (self.h / 2) - fin_offset + 5),
		]

		self.bullets = []
		self.shoot_delay = 0

		self.teleport_cooldown = 300
		self.teleport_timer = 0

	def draw(self, screen):
		self.x += self.speed_x
		self.y -= self.speed_y
		points = []

		for point in self.points:
			# x = point[0] * math.cos(self.angle) - point[1] * math.sin(self.angle) + self.x + 50
			# y = point[0] * math.sin(self.angle) + point[1] * math.cos(self.angle) + self.y + 50
			x = point[0] * math.cos(self.angle) - point[1] * math.sin(self.angle) + self.x + 50
			y = point[0] * math.sin(self.angle) + point[1] * math.cos(self.angle) + self.y + 50
			points.append((x, y))

		self.speed_x *= self.drag
		self.speed_y *= self.drag

		pygame.draw.lines(screen, COLORS_WHITE, False, points, 1)

		self.collisions()

		for bullet in self.bullets:
			bullet.life -= 1
			if bullet.life == 0:
				self.bullets.remove(bullet)

			bullet.draw(screen)

		if self.teleport_timer > 0:
			self.teleport_timer -= 1

		if self.shoot_delay:
			self.shoot_delay -= 1

	def fly(self, screen):
		# Can only move forward in asteroids
		self.speed_x += self.vel * math.sin(self.angle)
		self.speed_y += self.vel * math.cos(self.angle)

		points = []
		for point in self.booster:
			x = point[0] * math.cos(self.angle) - point[1] * math.sin(self.angle) + self.x + 50
			y = point[0] * math.sin(self.angle) + point[1] * math.cos(self.angle) + self.y + 50
			points.append((x, y))

		if random.randint(0,10) < 7:
			pygame.draw.lines(screen, COLORS_WHITE, False, points, 1)

	def shoot(self):
		if len(self.bullets) < MAX_BULLETS and self.shoot_delay == 0:
			bullet = Bullet(self.x, self.y, self.angle)
			self.bullets.append(bullet)
			self.shoot_delay = SHOOT_DELAY

	def teleport(self):
		if self.teleport_timer == 0:
			self.x = random.randint(10, Screen.w - 10)
			self.y = random.randint(10, Screen.h - 10)
			self.teleport_timer = self.teleport_cooldown

	def collisions(self):
		screen_collision_offset = 15
		# Ship collision
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

