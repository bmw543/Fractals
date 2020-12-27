from PIL import Image, ImageDraw, ImageFont
import math
import imageio
import numpy as np

# init parameters

length = 4 # length of the real and imaginary axes - smaller values will create a zoomed image
pixels = 200 # length of the x and y axes in pixels
max_iterations = 1000 # if the recursive function does not diverge after this many iterations, it is assumed to converge
frames = 200 # number of frames in the GIF
outside_layers = 15 # if a pixel takes more than this number of iterations, it is a constant color

generate_new_images = True

fp_images = 'C:/Users/Thomas/Desktop/Coding/Fractals/Julia Set/Images'
images_common_name = 'julia'
fp_gifs = 'C:/Users/Thomas/Desktop/Coding/Fractals/Julia Set/Gifs/julia_set.gif'

fnt = ImageFont.truetype("Courier Prime Code.ttf", 20) # text font

green = (120 * 255 / 360, 75.5 * 255 / 100, 54.5 * 255 / 100)
white = (0, 0, 255)
red = (0, int(80.9 * 255 / 100), int(69.8 * 255 / 100))

# functions

def iterations(zp, c): # determine how many iterations of the form z = z^2 + c before the value diverges
    z = zp
    n = 0
    while abs(z) <= 2 and n <= max_iterations:
        z = (z * z) + c
        n += 1
    return n

# main

filenames = np.empty(frames, dtype='object') # generate the filename order for the animated GIF
for f in range(frames):
    filenames[f] = fp_images + '/julia' + str(f) + '.png'

if(generate_new_images):
    for f in range(frames):
        frame = Image.new('HSV', (pixels, pixels), tuple(map(lambda x: int(x), green))) # create a new PIL frame
        draw = ImageDraw.Draw(frame) # create a new draw image for the frame
        c = complex((math.cos(f * 2 * math.pi / frames)), (math.sin(f * 2 * math.pi / frames))) # c is a complex number along the unit circle

        for x in range(pixels): # for each pixel
            for y in range(pixels):
                z = complex(((x - pixels / 2) * length / pixels), ((y - pixels / 2) * length / pixels))
                n = iterations(z, c) # calculate the

                if n < max_iterations:
                    if n > outside_layers:
                        color = white # constant surrounding color
                    else:
                        saturation = int(255 - 255 * n / outside_layers)
                        value = int(170 + 85 * n / outside_layers)
                        color = (0, saturation, value)

                    draw.point([x, y], color)

        frame.convert('RGB').save(fp_images + '/' + images_common_name + str(f) + '.png', 'PNG') # save each frame
        print(f)

print('converting...')

with imageio.get_writer(fp_gifs, mode='I') as writer: # generate animated GIF
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

print('done!')