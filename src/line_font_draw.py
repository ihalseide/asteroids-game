import pygame as pg

from . import setup
from . import util as u


def draw_string(surface, color, string, position, scale, rotation=0,
                thickness=1, spacing=1, wrapped=False):
    x, y = position
    scale_x, scale_y = scale
    dx, dy = u.rotate_point(1, 0, rotation)
    dx *= spacing * scale_x
    dy *= spacing * scale_y
    for character in string:
        draw_char(surface, color, character, (x, y), scale, rotation, thickness,
                  wrapped)
        x += dx
        y += dy


def draw_char(surface, color, character, position, scale, rotation=0,
              thickness=1, wrapped=False):
    pos_x, pos_y = position
    scale_x, scale_y = scale
    scale_y = -scale_y  # flip because screen coords
    char_points = setup.FNT[character]  # get the "font" data
    char_points = [tuple(u.transform_point(x, y, pos_x, pos_y, rotation,
                                           scale_x, scale_y))
                   for x, y in char_points]
    iter_points = iter(char_points)
    for point_1 in iter_points:
        point_2 = next(iter_points)
        if wrapped:
            u.draw_wrapped_line(surface, color, point_1, point_2, thickness)
        else:
            pg.draw.line(surface, color, point_1, point_2, thickness)
    return character
