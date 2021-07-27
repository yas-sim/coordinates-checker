# X,Y Coordinate picker (digitizer)  

### Description:  
Small tool to pickup points in an image and display the coordinate of the points. This is very handy and useful when you want to know the coordinate of points in an image.  
The tool has magnify function. You can pick the desired points precisely.  

![img](./resources/coordinate-digitizer.gif)

### How to run:  
```sh
python coordinate-digitizer.py [--input image_file] [--size XXXxYYY]
```

| options| description|
|----|----|
|-i or --input|Input image file name|
|-s or --size|Size of image (tool will create gray image with this size)|
