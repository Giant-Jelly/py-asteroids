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

	for i in range(0, asteroid_count):
		asteroids.append(Asteroid((random.randint(0, Screen.w), random.randint(0, Screen.h))))


def draw_asteroids():
	for asteroid in asteroids:
		CollisionDetector.draw_collider(Screen.screen, asteroid)
		CollisionDetector.draw_collider(Screen.screen, Player)
		if CollisionDetector.box_collision(Player, asteroid):
			# Player hit asteroid
			print("YOU DIED")
			global run
			global dead
			run = False
			dead = True

		asteroid.draw(Screen.screen)


while run:
	# Handle fps properly
	current = time.time() * 1000
	elapsed = current - previous
	previous = current
	delay = 1000.0 / fps - elapsed
	delay = max(int(delay), 0)

	Screen.screen.fill(COLORS_BLACK)
	Player.draw(Screen.screen)

	draw_asteroids()

	if timer == 60:
		spawn_asteroids()
		level_started = True

	# Controls
	keys = pygame.key.get_pressed()

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

	if keys[pygame.K_ESCAPE]:
		run = False

	# Events
	for event in pygame.event.get():

		# Quit when closed
		if event.type == pygame.QUIT:
			run = False

	pygame.display.flip()
	pygame.time.delay(delay)
	timer += 1


if dead:
	time.sleep(10)
	pygame.quit()

else:
	pygame.quit()






