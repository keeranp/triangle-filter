import math
import operator
from random import randint
from PIL import ImageDraw, ImageChops
from functools import reduce

def random_position(w, h):
    return (randint(0, w), randint(0, h))

def get_real_image_color(points, real_imagep, size):
    ''' Gets the color of the pixel at the center of a triangle '''
    center_x = int((points[0][0] + points[1][0] + points[2][0])/3)
    center_y = int((points[0][1] + points[1][1] + points[2][1])/3)
    color = list(real_imagep[min(size[0]-1, center_x), min(center_y, size[1]-1)])
    color[0] = color[0] + randint(-50, 50)
    color[1] = color[1] + randint(-50, 50)
    color[2] = color[2] + randint(-50, 50)
    return tuple(color)

def create_triangle_coords(image_size):
    ''' Create randomly coordinates of a triangle on an image according to the image size '''
    first_point = random_position(image_size[0], image_size[1])
    second_point = (first_point[0] + randint(-50, 50),
                    first_point[1] + randint(-50, 50))
    third_point = (second_point[0] + randint(-50, 50),
                   second_point[1] + randint(-50, 50))
    return [first_point, second_point, third_point]

def draw_triangle(image, coords, color):
    draw = ImageDraw.Draw(image)
    draw.polygon(coords, color)

def process_image(image, real_image, real_image_pixels, image_size_ratio, precise):
    coords = create_triangle_coords(real_image.size)
    color = get_real_image_color(coords, real_image_pixels, real_image.size)

    if precise:
        crop_points = (
            min(coords[0][0], coords[1][0], coords[2][0]), min(coords[0][1], coords[1][1], coords[2][1]),
            max(coords[0][0], coords[1][0], coords[2][0], image.size[0]), max(coords[0][1], coords[1][1], coords[2][1], image.size[1])
        )

        cropped_image = image.crop(crop_points)
        cropped_real_image = real_image.crop(crop_points)

        previous_rmse = rmse(cropped_real_image, cropped_image)

        test_image = image.copy()
        draw_triangle(test_image, coords, color)

        cropped_image = test_image.crop(crop_points)

        rmserr = rmse(cropped_real_image, cropped_image)

        if(rmserr < previous_rmse):
            resized_coords = []
            for coord in coords:
                resized_coords.append((int(coord[0] / image_size_ratio[0]), int(coord[1] / image_size_ratio[1])))
            draw_triangle(image, resized_coords, color)
        return rmserr < previous_rmse
    else:
        resized_coords = []
        for coord in coords:
            resized_coords.append((int(coord[0] / image_size_ratio[0]), int(coord[1] / image_size_ratio[1])))
        draw_triangle(image, resized_coords, color)
        return True

def rmse(img1, img2):
    h = ImageChops.difference(img1, img2).histogram()
    rmserr = math.sqrt(reduce(operator.add, map(
        lambda h, i: h*(i**2), h, range(256))) / (float(img1.size[0]) * img1.size[1]))
    return rmserr