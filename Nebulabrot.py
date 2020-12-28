# The nebulabrot

# The 'nebulabrot' is a variation of the Mandelbrot set - instead of graphing the complex values that are in the Mandelbrot set, the nebulabrot traces the paths that values _not_ in the set take as they diverge
# When using a single color, the nebulabrot is a probability map of the divergence paths - a random complex value within the specified image boundaries is chosen, and if it is not in the set, its path is graphed
# In this program, these paths are tracked separately for red, green, and blue channels, each channel using a different number of iterations to determine whether values are in the set or not
# This creates the nebula-like ghostly image as all three channel layers are added to obtain the final image color values for each pixel

# Rendering the nebulabrot takes an inordinate amount of time - multiprocessing is used to increase processor utilization and speed up rendering for large images

import multiprocessing
from PIL import Image, ImageDraw
import time
import random
import numpy as np

# parameters

width = 3000
height = 3000

rightBound = 2
leftBound = -2
topBound = 2
bottomBound = -2

totalSamples = 2000000 # the total number of random values whose paths are traced - higher values create a less noisy and more detailed image, but increase computation time

load = False # if load is true, new iterations will be added to previously saved values, increasing image fidelity - data is always saved as numpy arrays after processing is finished

fp_data = "C:/Users/Thomas/Desktop/Coding/Fractals/Nebulabrot/Data" # directory for saved data
fp_image = "C:/Users/Thomas/Desktop/Coding/Fractals/Nebulabrot/Images" # directory for finished images
filename = "nebulabrot"

rIterations = 50000 # maximum iterations before the value is assumed not to diverge for each color, the ratios and values change the look of the final image
gIterations = 5000
bIterations = 500

# setup

samples = int(totalSamples/4) # samples are divided for each of the four processes
deltaX = abs((rightBound - leftBound))/width
deltaY = abs((topBound - bottomBound))/height
    
red = np.zeros((height, width)) # a new matrix pixels for each color
green = np.zeros((height, width))
blue = np.zeros((height, width))

# calculations 

def addMatrix(matrix1, matrix2):
    for x in range(width):
        for y in range(height):
            matrix1[x,y] += matrix2[x,y]
    return(matrix1)

def iterations(c,j):
    z = 0
    n = 0
    if j == 0: # j is the color
        maxIterations = rIterations
    elif j == 1:
        maxIterations = gIterations
    else:
        maxIterations = bIterations
    while abs(z) <= 2 and n <= maxIterations:
        z = (z*z) + c
        n += 1
    return n

def recordPath(c,j):
    z = 0
    while z.real < rightBound and z.real > leftBound and z.imag < topBound and z.imag > bottomBound:
        z = (z*z) + c
        y = z.imag/deltaY
        x = z.real/deltaX
        y = int(y + height/2)
        x = int(x + width/2)
        if (z.real < rightBound and z.real > leftBound and z.imag < topBound and z.imag > bottomBound):
            if j == 0:
                red[x,y] += 1
            elif j == 1:
                green[x,y] += 1
            else:
                blue[x,y] += 1

def randNumber(j): # finds a random complex value within the image borders and not in the Mandelbrot set
    if j == 0:
        maxIterations = rIterations
    elif j == 1:
        maxIterations = gIterations
    else:
        maxIterations = bIterations
    inSet = 1
    real = random.uniform(-2, 2)
    imag = random.uniform(-2, 2)
    c = complex(real,imag)
    n = iterations(c,j)
    if n <= maxIterations:
        inSet = 0
    return (c, inSet)

def runSample(): # run a batch of samples - this function is assigned to each multiprocessing task
    print (multiprocessing.current_process().name + ' started')
    for j in range (3):
        start = time.time()
        for i in range (samples):
            inSet = 1
            while inSet == 1:
                c, inSet = randNumber(j)
            recordPath(c,j)
            if multiprocessing.current_process().name == 'Process-1':
                if i % 10000 == 0:
                    timeLeft = (3 * samples - (j+1) * i) * ((time.time() - start)/(i+1))
                    print(str(int(timeLeft/60)) + "m " + str(int(timeLeft % 60)) + "s")
    np.save(fp_data + "/" + 'red' + str(multiprocessing.current_process().name), red) # each process saves its data before it closes
    np.save(fp_data + "/" + 'green' + str(multiprocessing.current_process().name), green)
    np.save(fp_data + "/" + 'blue' + str(multiprocessing.current_process().name), blue)
    print('done')
            

if __name__ == "__main__":

    # setup
    
    im = Image.new('RGB', (width, height), (0, 0, 0)) # create the image canvas
    draw = ImageDraw.Draw(im)
    
    p1 = multiprocessing.Process(target = runSample, args = ())
    p2 = multiprocessing.Process(target = runSample, args = ())
    p3 = multiprocessing.Process(target = runSample, args = ())
    p4 = multiprocessing.Process(target = runSample, args = ())
   
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    print('Processing done')
    
    red1 = np.load(fp_data + "/" + 'redProcess-1.npy') # after all processes are complete, the data from each process is loaded back into memory
    red2 = np.load(fp_data + "/" + 'redProcess-2.npy')
    red3 = np.load(fp_data + "/" + 'redProcess-3.npy')
    red4 = np.load(fp_data + "/" + 'redProcess-4.npy')
   
    green1 = np.load(fp_data + "/" + 'greenProcess-1.npy')
    green2 = np.load(fp_data + "/" + 'greenProcess-2.npy')
    green3 = np.load(fp_data + "/" + 'greenProcess-3.npy')
    green4 = np.load(fp_data + "/" + 'greenProcess-4.npy')
  
    blue1 = np.load(fp_data + "/" + 'blueProcess-1.npy')
    blue2 = np.load(fp_data + "/" + 'blueProcess-2.npy')
    blue3 = np.load(fp_data + "/" + 'blueProcess-3.npy')
    blue4 = np.load(fp_data + "/" + 'blueProcess-4.npy')
  
    red = addMatrix(red1, red2) # the matrices are added to combine the data from the processes
    red = addMatrix(red, red3)
    red = addMatrix(red, red4)
 
    blue = addMatrix(blue1, blue2)
    blue = addMatrix(blue, blue3)
    blue = addMatrix(blue, blue4)
   
    green = addMatrix(green1, green2)
    green = addMatrix(green, green3)
    green = addMatrix(green, green4)
    
    if load == True: # if existing data is saved, it will be added as well
        red = addMatrix(np.load(fp_data + "/" + 'nebulabrot_red2.npy'), red)
        green = addMatrix(np.load(fp_data + "/" + 'nebulabrot_green2.npy'), green)
        blue = addMatrix(np.load(fp_data + "/" + 'nebulabrot_blue2.npy'), blue)
    
    np.save(fp_data + "/" + 'nebulabrot_red2', red) # the final matrices are saved so new iterations can be added to existing data later
    np.save(fp_data + "/" + 'nebulabrot_green2', green)
    np.save(fp_data + "/" + 'nebulabrot_blue2', blue)
        
    rmax = np.max(red) # the highest value pixel for each color, i.e. the number of diverging paths that cross a given pixel
    print('rmax:' + str(rmax))
    gmax = np.max(green)
    print('gmax:' + str(gmax))
    bmax = np.max(blue)
    print('bmax:' + str(bmax))
    for x in range(width):
        for y in range(height): 
            Red = 3 * int((red[x,y]/rmax * 255)) # all values are scaled by the maximum, so there is no "overexposure" where values greater than 255 are truncated
            Green = 3 * int((green[x,y]/gmax * 255))
            Blue = 3 * int((blue[x,y]/bmax * 255))
            draw.point([x, y], (Red , Green, Blue))

    im.convert('RGB').save(fp_image + "/" + filename + '.png', 'PNG') # the final image is saved to the images directory
            
    
