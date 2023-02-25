# Sinogram


Description: 
Using a hamming and a hanning window the Sinogram image into the original image.
This source code converts a sinogram into the captured image.
<br>          1)The coloured sinogram is seperated into 3 channels Red,Green,Blue.
<br>           A greyscale sinogram is also created.
<br>          2)Each colour channel and the greyscale are reconstructed without
<br>            a filter. 
<br>          3)The images are converted to frequency domain using fft.
<br>          4)Each channel and greyscale are passed through a ramp filter
<br>          5)All channels and greyscale are converted to the spatial domain.
<br>          6)Then they are reconstructed using back propagation
<br>          7)They are then rescaled to an 8 bit image and cropped accordingly.
<br>          9)The colour channels are resconstructed back to 1 image.
<br>          10)A hamming and hanning window is applied to the greyscale image.

<br>
<br>
Input image
<br>

Sinogram:
![image](https://user-images.githubusercontent.com/45408401/113201000-eddafe80-9260-11eb-8f1d-da3bbb6cb88f.png) 

Original: 
![image](https://user-images.githubusercontent.com/45408401/113201560-8a9d9c00-9261-11eb-9ca3-5033d5ca53ec.png)





