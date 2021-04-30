import time
import sys
from math_utils import draw_triangle
from pathlib import Path
from PIL import Image

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
