import time
import sys
import math
import operator
from functools import reduce
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
from random import randint


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


start_time = time.time()

SUCCESSFUL_ITERATION = []

real_image_name = Path(sys.argv[1])
real_image = Image.open(sys.argv[1])
processed_image_directory = str(real_image_name.parent)
real_image_pixels = real_image.load()
final_image = Image.new('RGB', real_image.size, 'white')
successful_iteration = 0
gif_images = [final_image]

i = 1
successful_iteration = 0
final_image.save(processed_image_directory+ '/' + real_image_name.stem + '_processed.jpg')

while successful_iteration/i > 0.1 or i < 100:
    new_image = final_image.copy()
    if draw_triangle(new_image, real_image, real_image_pixels):
        final_image = new_image
        successful_iteration += 1
        if(successful_iteration % 100 == 0):
            gif_images.append(final_image.copy())
    if i % 2000 == 0:
        print('Successful Iteration: ' + str(successful_iteration) + ', iteration: ' + str(i))
    SUCCESSFUL_ITERATION.append(successful_iteration)
    i += 1

final_image.save(processed_image_directory+ '/' + real_image_name.stem + '_processed.jpg')
gif_images[0].save(
    processed_image_directory+ '/' + real_image_name.stem + '_processed.gif',
    save_all=True,
    append_images=gif_images[1:],
    optimize=True,
    loop=0
)
real_image.close()
# os.system('ffmpeg -i out/out.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4')
print("--- %s seconds ---" % (time.time() - start_time))
final_image.show()
