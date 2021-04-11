###########
#
#Sinogram converter
#
#Author: Eoghan O'Connor
#
#
#
#Description: This source code converts a sinogram into the captured image.
#             1)The coloured sinogram is seperated into 3 channels Red,Green,Blue.
#             A greyscale sinogram is also created.
#             2)Each colour channel and the greyscale are reconstructed without
#             a filter. 
#             3)The images are converted to frequency domain using fft.
#             4)Each channel and greyscale are passed through a ramp filter
#             5)All channels and greyscale are converted to the spatial domain.
#             6)Then they are reconstructed using back propagation
#             7)They are then rescaled to an 8 bit image and cropped accordingly.
#             9)The colour channels are resconstructed back to 1 image.
#             10)A hamming and hanning window is applied to the greyscale image.
#
############

#Imports
import numpy as np 
import imutils
from skimage.transform import rotate ## Image rotation routine
import scipy.fftpack as fft          ## Fast Fourier Transform
import imageio                       ## Used to save images
import math

#Converts the sinogram single channel 
#to frequency domain using fast fourier transform
def ch_fft(channel):
    #Build 1-d FFTs of an array of projections, each projection 1 row of the array.
    return fft.rfft(channel, axis=1)

# Filter the projections of each channel
# using a ramp filter
def ramp_filter(ch_proj):
    #Ramp filter a 2-d array of 1-d FFTs (1-d FFTs along the rows).
    ramp = np.floor(np.arange(0.5, ch_proj.shape[1]//2 + 0.1, 0.5))
    return ch_proj * ramp


# Return channel using inverse fast fourier transform
#to the spatial domain
def inverse_fft(channel):
    return fft.irfft(channel, axis=1)


# Returns the reconstructed image 
# by back projecting the filtered projections
def back_projection(channel):
    
    #laminogram equal to images height
    laminogram = np.zeros((channel.shape[1],channel.shape[1]))
    dTheta = 180.0 / channel.shape[0]
    
    #rotate image and plot values on linogram
    for i in range(channel.shape[0]):
        arr = np.tile(channel[i],(channel.shape[1],1))
        temp = rotate(arr, dTheta*i)
        laminogram += temp
    return laminogram

# Crops image into square
def crop(channel):
    
    #square length= diameter/square root(2)
    side=int(channel.shape[0]/math.sqrt(2))
    new_ch=[]
    
    #width start and end points
    s_width=int((channel.shape[0]/2)-side/2)
    e_width=int((channel.shape[0]/2)+side/2)

    #height start and end points
    s_height=int((channel.shape[1]/2)-side/2)
    e_height=int((channel.shape[1]/2)+side/2)

    #cropping channel 
    for i in channel[s_width:e_width]:
        new_ch.append(i[s_height:e_height])
    new_ch=np.reshape(new_ch,(side,side))
    return new_ch

# Rescales channel to 8bit channel
def ch_rescale(channel):
    cr_ch=crop(channel)
    chi,clo= cr_ch.max(),cr_ch.min()
    chnorm=255*(cr_ch-clo)/(chi-clo)
    ch8bit=np.floor(chnorm).astype('uint8')
    return ch8bit


## Statements
##Import coloured image (RGB)
print("Original Sinogram")
sonogram = imutils.imread('sinogram.png',greyscale=False)
imutils.imshow(sonogram)
imageio.imwrite('originalSinogramImage.png', sonogram)





##splitting the image into 3 colours
red=[]
green=[]
blue=[]
for col in sonogram:
    for row in col:
        red.append(row[0])
        green.append(row[1])
        blue.append(row[2])


#Reshaping the colours to give rows
red=np.reshape(red,(360,658))
green=np.reshape(green,(360,658))
blue=np.reshape(blue,(360,658))



#Reconstruction of each colour channel without any filtering
print("Reconstruction with no filtering")
unfiltered_red = back_projection(red)
unfiltered_green = back_projection(green)
unfiltered_blue = back_projection(blue)

imutils.imshow(unfiltered_red)

imageio.imwrite('unfiltered_red.png', unfiltered_red)
imageio.imwrite('unfiltered_green.png', unfiltered_green)
imageio.imwrite('unfiltered_blue.png', unfiltered_blue)




#Convert channels to Frequency domain
print("Converting colour channels to frequency domain using fft")
red_fft=ch_fft(red)
green_fft=ch_fft(green)
blue_fft=ch_fft(blue)


#Ramp channels
print("Passing converted fft colour channels through ramp filter")
red_ramp=ramp_filter(red_fft)
green_ramp=ramp_filter(green_fft)
blue_ramp=ramp_filter(blue_fft)




#Converting colour channels to spacial domain using inverse FFT
print("Colour channels Spatial domain")
spatial_dom_red = inverse_fft(red_ramp)
spatial_dom_green = inverse_fft(green_ramp)
spatial_dom_blue = inverse_fft(blue_ramp)


#Back projecting colour channels
print("Back projecting coloured channels")
recon_im_red = back_projection(spatial_dom_red)
recon_im_green = back_projection(spatial_dom_green)
recon_im_blue = back_projection(spatial_dom_blue)

print("Back projected colour channels")
imutils.imshow(recon_im_red)

#Rescaling channels to 8 bit and cropping image
print("Converting channels to 8 bit and cropping channel images")
red_rescaled= ch_rescale(recon_im_red)
green_rescaled= ch_rescale(recon_im_green)
blue_rescaled= ch_rescale(recon_im_blue)

print("Rescaled and cropped colour channel images")
imutils.imshow(red_rescaled)

#Reconstruct all channels to one image
print("Rsconstructed coloured image")
image=np.dstack((red_rescaled,green_rescaled,blue_rescaled))
imutils.imshow(image)
imageio.imwrite('final.png', image)