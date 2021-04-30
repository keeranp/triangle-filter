import math
import operator
from random import randint
from PIL import ImageDraw, ImageChops
from functools import reduce

def random_position(w, h):
    return (randint(0, w), randint(0, h))


def get_real_image_color(points, real_imagep, size):
    center_x = int((points[0][0] + points[1][0] + points[2][0])/3)
    center_y = int((points[0][1] + points[1][1] + points[2][1])/3)
    color = list(real_imagep[min(size[0]-1, center_x),
                             min(center_y, size[1]-1)])
    color[0] = color[0] + randint(-50, 50)
    color[1] = color[1] + randint(-50, 50)
    color[2] = color[2] + randint(-50, 50)
    return tuple(color)


def draw_triangle(image, real_image, real_image_pixels):
    first_point = random_position(image.size[0], image.size[1])
    second_point = (first_point[0] + randint(-70, 70),
                    first_point[1] + randint(-70, 70))
    third_point = (second_point[0] + randint(-70, 70),
                   second_point[1] + randint(-70, 70))
    coords = [first_point, second_point, third_point]
    color = get_real_image_color(coords, real_image_pixels, image.size)

    crop_points = (min(first_point[0], second_point[0], third_point[0]), min(first_point[1], second_point[1], third_point[1]),
                   max(first_point[0], second_point[0], third_point[0], image.size[0]), max(first_point[1], second_point[1], third_point[1], image.size[1]))
    cropped_image = image.crop(crop_points)
    cropped_real_image = real_image.crop(crop_points)

    previous_rmse = rmse(cropped_real_image, cropped_image)

    draw = ImageDraw.Draw(image)
    draw.polygon(coords, color)

    cropped_image = image.crop(crop_points)
    cropped_real_image = real_image.crop(crop_points)

    rmserr = rmse(cropped_real_image, cropped_image)
    return rmserr < previous_rmse


def rmse(img1, img2):
    h = ImageChops.difference(img1, img2).histogram()
    rmserr = math.sqrt(reduce(operator.add, map(
        lambda h, i: h*(i**2), h, range(256))) / (float(img1.size[0]) * img1.size[1]))
    return rmserr