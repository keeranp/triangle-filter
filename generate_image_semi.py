import time
import sys
import cv2
import numpy
from math_utils import process_image
from pathlib import Path
from PIL import Image

MAX_ITERATION = 50000

start_time = time.time()

''' Getting the filename and the directory to save the processed files '''
real_image_name = Path(sys.argv[1])
image_directory = str(real_image_name.parent)

''' Setting up the processed image '''
real_image = Image.open(real_image_name)
real_image_pixels = real_image.load()
final_image = Image.new('RGB', (1920, 1080), 'white')
image_size_ratio = (real_image.size[0]/final_image.size[0],real_image.size[0]/final_image.size[0])
images = [final_image] #Array containing all the images for the video

''' Processing the image '''
i = 1
successful_iteration = 0
continue_processing = True

while continue_processing:
    new_image = final_image.copy()
    if process_image(new_image, real_image, real_image_pixels, image_size_ratio, len(sys.argv) >= 3):
        final_image = new_image
        successful_iteration += 1
        if(successful_iteration % 100 == 0):
            images.append(final_image.copy())
    if i % 2000 == 0:
        print('Successful Iteration: ' + str(successful_iteration) + ', iteration: ' + str(i) + ', ' + str(successful_iteration/i))
    if(len(sys.argv) >= 3):
        continue_processing = successful_iteration/i > 0.1 or i < 100
    else:
        continue_processing = i < MAX_ITERATION
    i += 1

real_image.close()

''' Saving processed image '''
### Save processed image as .jpg ###
final_image.save(image_directory+ '/' + real_image_name.stem + '_processed.jpg')

### Save the processing as .avi ###
out = cv2.VideoWriter(
    image_directory+ '/' + real_image_name.stem + '_processed.avi',
    cv2.VideoWriter_fourcc(*'DIVX'),
    10,
    final_image.size
)

for img in images:
    opencv_image = numpy.array(img.convert('RGB'))[:, :, ::-1] #Converting PIL image into OpenCV image
    out.write(opencv_image)
out.release()

print("--- %s seconds ---" % (time.time() - start_time))
