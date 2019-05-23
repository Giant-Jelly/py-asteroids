import pygame
import time
import random

from lib.Player import Player
from lib.Screen import Screen
from lib.Asteroid import Asteroid
from lib.CollisionDetector import CollisionDetector
from lib import parameters

COLORS_BLACK = (0, 0, 0)

Player = Player()
Screen = Screen()

pygame.init()

fps = 60
previous = time.time() * 1000
run = True
dead = False
current_level = 1
timer = 0
asteroids = []
level_started = False


def spawn_asteroids():
	asteroid_count = parameters.levels[current_level - 1]['asteroids']
	spawn_safe_zone_size = 500
	for i in range(0, asteroid_count):
		def get_safe_location():
			xx = random.randint(0, Screen.w)
			yy = random.randint(0, Screen.h)

			return xx, yy

		while True:
			x, y = get_safe_location()
			if (Screen.w / 2) + (spawn_safe_zone_size / 2) > x > (Screen.w / 2) - (spawn_safe_zone_size / 2):
				if (Screen.h / 2) + (spawn_safe_zone_size / 2) > y > (Screen.h / 2) - (spawn_safe_zone_size / 2):
					# If asteroid is in safe location just get a new one
					continue
			break

		asteroids.append(Asteroid((x, y)))


def draw_asteroids():
	for asteroid in asteroids:
		if CollisionDetector.circle_collision(Player, asteroid):
			# Player hit asteroid
			print("You died, press 'r' to restart")
			global dead
			dead = True
			break

		for bullet in Player.bullets:
			if CollisionDetector.circle_collision(bullet, asteroid):
				# Bullet hit asteroid
				asteroids.remove(asteroid)
				Player.bullets.remove(bullet)
				break

		asteroid.draw(Screen.screen)


while run:
	# Handle fps properly
	current = time.time() * 1000
	elapsed = current - previous
	previous = current
	delay = 1000.0 / fps - elapsed
	delay = max(int(delay), 0)

	Screen.screen.fill(COLORS_BLACK)
	Screen.draw_bg()

	keys = pygame.key.get_pressed()

	if not dead:
		Player.draw(Screen.screen)
		draw_asteroids()

		if timer == 60:
			spawn_asteroids()
			level_started = True

		# Controls
		if keys[pygame.K_LEFT]:
			Player.angle -= Player.r_vel

		if keys[pygame.K_RIGHT]:
			Player.angle += Player.r_vel

		if keys[pygame.K_UP]:
			Player.fly(Screen.screen)

		if keys[pygame.K_SPACE]:
			Player.shoot()

		if keys[pygame.K_TAB]:
			Player.teleport()

		timer += 1

	if keys[pygame.K_r]:
		Player.__init__()
		asteroids = []
		timer = 0
		current_level = 1
		dead = False

	if keys[pygame.K_ESCAPE]:
		run = False

	# Events
	for event in pygame.event.get():

		# Quit when closed
		if event.type == pygame.QUIT:
			run = False

	pygame.display.flip()
	pygame.time.delay(delay)

pygame.quit()






