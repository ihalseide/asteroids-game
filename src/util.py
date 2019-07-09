
import math

import pygame
from pygame.math import Vector2

def draw_wrapped_lines(screen, color, closed, points, width=1):
	prev_point = points[0]
	# draw between all points in "plan"
	for point in points:
		draw_wrapped_line(screen, color, prev_point, point, width)
		prev_point = point
	draw_wrapped_line(screen, color, points[-1], points[0])

def draw_wrapped_point(screen, color, point):
	x, y = point
	rect = screen.get_rect()
	wx, wy = x % rect.width, y % rect.height
	screen.set_at((round(wx), round(wy)), color)

def draw_wrapped_line(screen, color, p1, p2, width=1):
	rect = screen.get_rect()
	pygame.draw.line(screen, color, p1, p2, width)
	if not rect.collidepoint(p1) or not rect.collidepoint(p2):
		p1_x, p1_y = p1
		p2_x, p2_y = p2
		# draw with wrapped x
		if p1_x < 0 or p1_x > rect.width or p2_x < 0 or p2_x > rect.width:
			pygame.draw.line(screen, color, (p1_x+rect.width, p1_y), (p2_x+rect.width, p2_y), width)
			pygame.draw.line(screen, color, (p1_x-rect.width, p1_y), (p2_x-rect.width, p2_y), width)
		# draw with wrapped y
		if p1_y < 0 or p1_y > rect.height or p2_y < 0 or p2_y > rect.height:
			pygame.draw.line(screen, color, (p1_x, p1_y+rect.height), (p2_x, p2_y+rect.height), width)
			pygame.draw.line(screen, color, (p1_x, p1_y-rect.height), (p2_x, p2_y-rect.height), width)
	
def is_point_inside_circle(px, py, cx, cy, cRadius):
	return distance(px, py, cx, cy) < cRadius
	
def distance_squared(x1, y1, x2, y2):
	dx = x1 - x2
	dy = y1 - y2
	return dx*dx + dy*dy
	
def distance(x1, y1, x2, y2):
	return math.sqrt(distance_squared(x1, y1, x2, y2))
	
def do_circles_overlap(x1, y1, r1, x2, y2, r2):
	return distance(x1, y1, x2, y2) <= r1 + r2
	
def translate_point(x, y, dx, dy):
	nx = x + dx
	ny = y + dy
	return Vector2(nx, ny)
	
def scale_point(x, y, x_scale, y_scale):
	nx = x * x_scale
	ny = y * y_scale
	return Vector2(nx, ny)
	
def rotate_point(x, y, angle):
	c = math.cos(angle)
	s = math.sin(angle)
	# rotation matrix
	nx = x*c - y*s
	ny = y*c + x*s
	return Vector2(nx, ny)
	
def transform_point(x, y, dx, dy, angle, x_scale, y_scale):
	new_point = scale_point(x, y, x_scale, y_scale)
	new_point = rotate_point(new_point.x, new_point.y, angle)
	new_point = translate_point(new_point.x, new_point.y, dx, dy)
	return new_point

def avg(arr):
	return sum(arr) / len(arr)
	

