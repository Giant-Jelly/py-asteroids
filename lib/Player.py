import pygame
from pygame.math import Vector2
import math
import random
import time

from lib.Screen import Screen
from lib.Bullet import Bullet

COLORS_WHITE = (255, 255, 255)
MAX_BULLETS = 3
SHOOT_DELAY = 10


class Player:
	w = 30
	h = 40

	def __init__(self):
		self.x = Screen.w / 2
		self.y = Screen.h / 2
		self.vel = 0.2
		self.r_vel = 0.1
		fin_offset = 10
		self.angle = 0
		self.speed_x = 0
		self.speed_y = 0
		self.drag = 0.99
		self.collision_radius = 27
		self.invincible = 0

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
		ox, oy = self.center()
		for point in self.points:
			x, y = point
			xx = (ox + math.cos(self.angle) * (x - ox) - math.sin(self.angle) * (y - oy)) + self.x
			yy = (oy + math.sin(self.angle) * (x - ox) + math.cos(self.angle) * (y - oy)) + self.y
			points.append((xx, yy))

		self.speed_x *= self.drag
		self.speed_y *= self.drag

		if not self.invincible:
			pygame.draw.lines(screen, COLORS_WHITE, False, points, 1)
		else:
			if self.invincible % 40 < 20:
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
		ox, oy = self.center()
		for point in self.booster:
			x, y = point
			xx = (ox + math.cos(self.angle) * (x - ox) - math.sin(self.angle) * (y - oy)) + self.x
			yy = (oy + math.sin(self.angle) * (x - ox) + math.cos(self.angle) * (y - oy)) + self.y
			points.append((xx, yy))

		if random.randint(0, 10) < 7:
			if not self.invincible:
				pygame.draw.lines(screen, COLORS_WHITE, False, points, 1)
			else:
				if self.invincible % 40 < 20:
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

	def center(self):
		x = [p[0] for p in self.points]
		y = [p[1] for p in self.points]
		return round(sum(x) / len(self.points)), round(sum(y) / len(self.points))

	def reset(self):
		self.speed_x = 0
		self.speed_y = 0
		self.angle = 0
		self.x = Screen.w / 2
		self.y = Screen.h / 2

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

