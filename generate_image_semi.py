import time
import sys
import cv2
import numpy
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
images = [final_image]

i = 1
successful_iteration = 0
final_image.save(processed_image_directory+ '/' + real_image_name.stem + '_processed.jpg')

while successful_iteration/i > 0.1 or i < 100:
    new_image = final_image.copy()
    if draw_triangle(new_image, real_image, real_image_pixels):
        final_image = new_image
        successful_iteration += 1
        if(successful_iteration % 100 == 0):
            images.append(final_image.copy())
    if i % 2000 == 0:
        print('Successful Iteration: ' + str(successful_iteration) + ', iteration: ' + str(i))
    SUCCESSFUL_ITERATION.append(successful_iteration)
    i += 1
real_image.close()

''' Saving processed image '''

### Save processed image as .jpg ###
final_image.save(processed_image_directory+ '/' + real_image_name.stem + '_processed.jpg')

### Save the processing as .avi ###
out = cv2.VideoWriter(
    processed_image_directory+ '/' + real_image_name.stem + '_processed.avi',
    cv2.VideoWriter_fourcc(*'DIVX'),
    10,
    final_image.size
)

for img in images:
    opencv_image = numpy.array(img.convert('RGB'))[:, :, ::-1] #Converting PIL image into OpenCV image
    out.write(opencv_image)
out.release()

print("--- %s seconds ---" % (time.time() - start_time))
