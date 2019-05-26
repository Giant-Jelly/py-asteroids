import pygame.freetype
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
pygame.font.init()
info = pygame.freetype.Font('/Users/giantjelly/Library/Fonts/Quicksand-Light.ttf', 30)
title = pygame.freetype.Font('/Users/giantjelly/Library/Fonts/Quicksand-Medium.ttf',50)

fps = 60
previous = time.time() * 1000
run = True
dead = False
current_level = 1
timer = 0
asteroids = []
level_started = False
spawn_safe_zone_size = 500
game_start_time = 200
score = 0

lives = 3
hit = False
hit_cooldown = 0
respawn_time = 60
respawn_timer = 0

invincible_timer = 0


def get_safe_location():
	xx = random.randint(0, Screen.w)
	yy = random.randint(0, Screen.h)

	return xx, yy


def spawn_asteroids():
	asteroid_count = parameters.starting_asteroid_count*current_level
	for i in range(0, asteroid_count):
		while True:
			x, y = get_safe_location()
			if (Screen.w / 2) + (spawn_safe_zone_size / 2) > x > (Screen.w / 2) - (spawn_safe_zone_size / 2):
				if (Screen.h / 2) + (spawn_safe_zone_size / 2) > y > (Screen.h / 2) - (spawn_safe_zone_size / 2):
					# If asteroid is in safe location just get a new one
					continue
			break

		asteroids.append(Asteroid((x, y), 1))


def draw_asteroids():
	for asteroid in asteroids:
		global invincible_timer
		# CollisionDetector.draw_circle_collider(Screen.screen, asteroid)
		if invincible_timer == 0:
			if CollisionDetector.circle_collision(Player, asteroid):
				global hit
				global hit_cooldown
				global lives

				if not hit:
					hit_cooldown = 60
					lives -= 1
					if asteroid.size != 3:
						asteroids.append(Asteroid((asteroid.x, asteroid.y), asteroid.size + 1))
						asteroids.append(Asteroid((asteroid.x, asteroid.y), asteroid.size + 1))
					global score
					asteroids.remove(asteroid)

				hit = True
				invincible_timer = hit_cooldown + 200
				if lives == 0:
					# Player hit asteroid
					print("You died, press 'r' to restart")
					global dead
					dead = True
					break
				else:
					global respawn_timer
					Player.reset()
					respawn_timer = respawn_time

		for bullet in Player.bullets:
			if CollisionDetector.circle_collision(bullet, asteroid):
				# Bullet hit asteroid
				if asteroid.size != 3:
					asteroids.append(Asteroid((asteroid.x, asteroid.y), asteroid.size + 1))
					asteroids.append(Asteroid((asteroid.x, asteroid.y), asteroid.size + 1))
				global score
				score += asteroid.size * 10
				asteroids.remove(asteroid)
				Player.bullets.remove(bullet)
				break

		asteroid.draw(Screen.screen)
	global timer
	if len(asteroids) == 0 and timer > game_start_time:
		parameters.starting_asteroid_count += 4
		global current_level
		current_level += 1
		timer = 0


while run:
	# Handle fps properly
	current = time.time() * 1000
	elapsed = current - previous
	previous = current
	delay = 1000.0 / fps - elapsed
	delay = max(int(delay), 0)
	Screen.screen.fill(COLORS_BLACK)
	Screen.draw_bg()
	Player.invincible = invincible_timer

	keys = pygame.key.get_pressed()

	if not dead:
		if not respawn_timer:
			Player.draw(Screen.screen)

		else:
			respawn_timer -= 1

		if hit:
			hit_cooldown -= 1

		if hit_cooldown == 0:
			hit = False

		if invincible_timer:
			invincible_timer -= 1

		draw_asteroids()

		if timer == game_start_time:
			spawn_asteroids()
			level_started = True

		if not respawn_timer:
			# Controls
			if keys[pygame.K_LEFT]:
				Player.angle -= Player.r_vel

			if keys[pygame.K_RIGHT]:
				Player.angle += Player.r_vel

			if keys[pygame.K_UP]:
				Player.fly(Screen.screen)

			# if keys[pygame.K_SPACE]:
			# 	Player.shoot()

			if keys[pygame.K_TAB]:
				Player.teleport()

		# Events
		for event in pygame.event.get():

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				Player.shoot()

		timer += 1

	if keys[pygame.K_r]:
		Player.__init__()
		asteroids = []
		timer = 0
		current_level = 1
		dead = False
		lives = 3
		hit = False
		score = 0

	if keys[pygame.K_ESCAPE]:
		run = False

	# Events
	for event in pygame.event.get():

		# Quit when closed
		if event.type == pygame.QUIT:
			run = False

	info.render_to(Screen.screen, (50, 10), 'Score - ' + str(score), parameters.COLORS_WHITE)
	info.render_to(Screen.screen, (Screen.w - 200, 10), 'Lives - ' + str(lives), parameters.COLORS_WHITE)
	if timer < game_start_time:
		title.render_to(Screen.screen, (Screen.w / 2 - 70, 200), 'Level ' + str(current_level), parameters.COLORS_WHITE)
	# Screen.screen.blit(text, (Screen.w / 2 - text.get_width() / 2, Screen.h / 2 - text.get_height() / 2))
	pygame.display.flip()
	pygame.time.delay(delay)

pygame.quit()






