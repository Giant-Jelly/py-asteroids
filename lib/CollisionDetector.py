import pygame

from lib import helper

collision_threshold = 10  # in px


class CollisionDetector:

	@staticmethod
	def box_collision(a, b):
		# Check if a is inside b
		if a.x > b.x and a.x + a.w < b.x + b.w:
			print(b.x)
			# X collision
			if a.y > b.y and a.y - a.h < b.y - b.h:
				print("hit-y")
				# Y collision
				return True

		# No collision
		return False

	@staticmethod
	def circle_collision(a, b):
		if helper.pythagoras(a.x - b.x, a.y - b.y) < (a.collision_radius + b.collision_radius) - collision_threshold:
			# Collision
			return True

		return False

	@staticmethod
	def draw_box_collider(screen, obj):
		points = [
			(obj.x - obj.w, obj.y - obj.h),
			(obj.x + obj.w, obj.y - obj.h),
			(obj.x + obj.w, obj.y + obj.h),
			(obj.x - obj.w, obj.y + obj.h),
			(obj.x - obj.w, obj.y - obj.h),

		]
		pygame.draw.lines(screen, (0, 255, 0), False, points, 2)

	@staticmethod
	def draw_circle_collider(screen, obj):

		pygame.draw.circle(screen, (0, 255, 0), (round(obj.x), round(obj.y)), obj.collision_radius, 2)




