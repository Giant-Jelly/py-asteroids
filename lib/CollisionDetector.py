import pygame


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
	def draw_collider(screen, obj):
		points = [
			(obj.x - obj.w, obj.y - obj.h),
			(obj.x + obj.w, obj.y - obj.h),
			(obj.x + obj.w, obj.y + obj.h),
			(obj.x - obj.w, obj.y + obj.h),
			(obj.x - obj.w, obj.y - obj.h),

		]
		pygame.draw.lines(screen, (0, 255, 0), False, points, 2)




