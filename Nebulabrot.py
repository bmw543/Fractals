import multiprocessing
from PIL import Image, ImageDraw
import time
import random
import numpy as np

#parameters
width = 3000
height = 3000

rightBound = 2
leftBound = -2
topBound = 2
bottomBound = -2

totalSamples = 20000

load = False

fp_data = "C:/Users/Thomas/Desktop/Coding/Fractals/Nebulabrot/Data"
fp_image = "C:/Users/Thomas/Desktop/Coding/Fractals/Nebulabrot/Images"
filename = "nebulabrot3"

rIterations = 500
gIterations = 500
bIterations = 500

#setup
samples = int(totalSamples/4)
deltaX = abs((rightBound - leftBound))/width
deltaY = abs((topBound - bottomBound))/height

#pixels = np.zeros((height, width))
    
red = np.zeros((height, width))
green = np.zeros((height, width))
blue = np.zeros((height, width))

#calculations
def addMatrix(matrix1, matrix2):
    for x in range(width):
        for y in range(height):
            matrix1[x,y] += matrix2[x,y]
    return(matrix1)

def iterations(c,j):
    z = 0
    n = 0
    if j == 0:
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

def randNumber(j):
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

def runSample():
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
    np.save(fp_data + "/" + 'red' + str(multiprocessing.current_process().name), red)
    np.save(fp_data + "/" + 'green' + str(multiprocessing.current_process().name), green)
    np.save(fp_data + "/" + 'blue' + str(multiprocessing.current_process().name), blue)
    print('done')
            

if __name__ == "__main__":

#setup
    im = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    p1 = multiprocessing.Process(target = runSample, args = ())
    p2 = multiprocessing.Process(target = runSample, args = ())
    p3 = multiprocessing.Process(target = runSample, args = ())
    p4 = multiprocessing.Process(target = runSample, args = ())
    #p5 = multiprocessing.Process(target = runSample, args = ())
    #p6 = multiprocessing.Process(target = runSample, args = ())
    #p7 = multiprocessing.Process(target = runSample, args = ())
    #p8 = multiprocessing.Process(target = runSample, args = ())
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    #p5.start()
    #p6.start()
    #p7.start()
    #p8.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    #p5.join()
    #p6.join()
    #p7.join()
    #p8.join()
    
    
    print ('Processing done')
    
    red1 = np.load(fp_data + "/" + 'redProcess-1.npy')
    red2 = np.load(fp_data + "/" + 'redProcess-2.npy')
    red3 = np.load(fp_data + "/" + 'redProcess-3.npy')
    red4 = np.load(fp_data + "/" + 'redProcess-4.npy')
    #red5 = np.load('redProcess-5.npy')
    #red6 = np.load('redProcess-6.npy')
    #red7 = np.load('redProcess-7.npy')
    #red8 = np.load('redProcess-8.npy')
    
    green1 = np.load(fp_data + "/" + 'greenProcess-1.npy')
    green2 = np.load(fp_data + "/" + 'greenProcess-2.npy')
    green3 = np.load(fp_data + "/" + 'greenProcess-3.npy')
    green4 = np.load(fp_data + "/" + 'greenProcess-4.npy')
    #green5 = np.load('greenProcess-5.npy')
    #green6 = np.load('greenProcess-6.npy')
    #green7 = np.load('greenProcess-7.npy')
    #green8 = np.load('greenProcess-8.npy')
    
    blue1 = np.load(fp_data + "/" + 'blueProcess-1.npy')
    blue2 = np.load(fp_data + "/" + 'blueProcess-2.npy')
    blue3 = np.load(fp_data + "/" + 'blueProcess-3.npy')
    blue4 = np.load(fp_data + "/" + 'blueProcess-4.npy')
    #blue5 = np.load('blueProcess-5.npy')
    #blue6 = np.load('blueProcess-6.npy')
    #blue7 = np.load('blueProcess-7.npy')
    #blue8 = np.load('blueProcess-8.npy')
    
    red = addMatrix(red1, red2)
    red = addMatrix(red, red3)
    red = addMatrix(red, red4)
    #red = addMatrix(red, red5)
    #red = addMatrix(red, red6)
    #red = addMatrix(red, red7)
    #red = addMatrix(red, red8)
    blue = addMatrix(blue1, blue2)
    blue = addMatrix(blue, blue3)
    blue = addMatrix(blue, blue4)
    #blue = addMatrix(blue, blue5)
    #blue = addMatrix(blue, blue6)
    #blue = addMatrix(blue, blue7)
    #blue = addMatrix(blue, blue8)
    green = addMatrix(green1, green2)
    green = addMatrix(green, green3)
    green = addMatrix(green, green4)
    #green = addMatrix(green, green5)
    #green = addMatrix(green, green6)
    #green = addMatrix(green, green7)
    #green = addMatrix(green, green8)
    
    if load == True:
        red = addMatrix(np.load(fp_data + "/" + 'nebulabrot_red2.npy'), red)
        green = addMatrix(np.load(fp_data + "/" + 'nebulabrot_green2.npy'), green)
        blue = addMatrix(np.load(fp_data + "/" + 'nebulabrot_blue2.npy'), blue)
    
    np.save(fp_data + "/" + 'nebulabrot_red2', red)
    np.save(fp_data + "/" + 'nebulabrot_green2', green)
    np.save(fp_data + "/" + 'nebulabrot_blue2', blue)
        
    #maximum = np.max(pixels)
    rmax = np.max(red)
    print('rmax:' + str(rmax))
    gmax = np.max(green)
    print('gmax:' + str(gmax))
    bmax = np.max(blue)
    print('bmax:' + str(bmax))
    for x in range(width):
        for y in range(height): 
            Red = 3 * int((red[x,y]/rmax * 255))
            Green = 3 * int((green[x,y]/gmax * 255))
            Blue = 3 * int((blue[x,y]/bmax * 255))
            draw.point([x, y], (Red , Green, Blue))

    im.convert('RGB').save(fp_image + "/" + filename + '.png', 'PNG')
            
    