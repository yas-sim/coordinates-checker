# X,Y Coordinates checker  

### Description:  
Small tool to pickup points in an image and display the coordinates of the points. This is very handy and useful when you want to know the coordinates of points in an image.  
The tool has magnify function. You can pick the desired points precisely.  
The tool can accept an image file, an movie file or a webCam as image input. You can pause the movie playback for precise point picking.  

![img](./resources/coordinate-digitizer.gif)

### How to run:  
```sh
python coordinates-checker.py [--input image_file | --size XXXxYYY | --cam webCam_number --video movie_file]
```

| options| description|
|----|----|
|`-i` or `--input`|Input image file name|
|`-s` or `--size`|Size of image (tool will create gray image with this size)|
|`-c` or `--cam`|ID number of webCam (camera). Starting from 0|
|`-v` or `--video`|Input video file name|  
|`-sc` or `--scale`|Scale factor of display image. Display image size will be 1/2 when 2 is specified| 

|key|description|
|----|----|
|`ESC`|Exit program|
|`p` or `<space>`|Pause / resume movie|

### Command line examples:  
```sh
python coordinates-checker.py --input input.jpg
python coordinates-checker.py --video movie.mp4
python coordinates-checker.py --cam 0
python coordinates-checker.py --cam 0 --size 1920x1080 -sc 2
```
