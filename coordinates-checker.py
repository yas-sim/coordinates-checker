import numpy as np
import cv2
import argparse

g_mouse_button = False
g_points = []
g_mouse_x = 0
g_mouse_y = 0
g_scale_factor = 1

def onMouse(event, x, y, flags, param):
    global g_mouse_button
    global g_mouse_x, g_mouse_y
    global g_scale_factor
    x *= g_scale_factor
    y *= g_scale_factor
    if event == cv2.EVENT_LBUTTONDOWN:
        if g_mouse_button == False:
            g_mouse_button = True
            g_points.append((x,y))
            print('{},{}'.format(x, y))
    if event == cv2.EVENT_LBUTTONUP:
        g_mouse_button = False
    g_mouse_x = x
    g_mouse_y = y

def drawCursor(img, point):
    img_y, img_x = img.shape[:2]
    cx, cy = point
    cv2.line(img, (cx, 0), (cx, img_y), (  0,0,0), thickness=2, lineType=cv2.LINE_4)
    cv2.line(img, (0, cy), (img_x, cy), (  0,0,0), thickness=2, lineType=cv2.LINE_4)    
    cv2.line(img, (cx, 0), (cx, img_y), (255,0,0), thickness=1, lineType=cv2.LINE_4)
    cv2.line(img, (0, cy), (img_x, cy), (255,0,0), thickness=1, lineType=cv2.LINE_4)

def drawMarkers(img, points):
    for point in points:
        cv2.drawMarker(img, point, (  0,  0,  0), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
        cv2.drawMarker(img, point, (255,255,255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=1)


def main():
    global g_mouse_x, g_mouse_y
    global g_points
    global g_scale_factor
    parser = argparse.ArgumentParser()
    parser.add_argument('-sc', '--scale', type=int, required=False, default=1, help='Image scaling factor (integer, Display image size will be 1/2 when 2 is specified.)')
    parser.add_argument('-s', '--size',  type=str, required=False, help='Image size in XXXxYYY format. E.g. 800x600')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', type=str, required=False, help='Input image file name')
    group.add_argument('-c', '--cam', type=int, required=False, help='number of webCam. starts from 0')
    group.add_argument('-v', '--video', type=str, required=False, help='Input video file name')
    args = parser.parse_args()

    movie_flag = False
    img_x, img_y = (640, 480)       # default image size
    if args.size is not None:
        img_x, img_y = [int(i) for i in args.size.split('x')]
    img = np.full((img_y , img_x, 3), 64, dtype=np.uint8)    # default image (will be used when no input device or file is specified)
    if args.input is not None:
        img = cv2.imread(args.input)
    elif args.cam is not None:
        movie_flag = True
        cap = cv2.VideoCapture(args.cam)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH , img_x)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_y)
        _, img = cap.read()
    elif args.video is not None:
        movie_flag = True
        cap = cv2.VideoCapture(args.video)
        _, img = cap.read()

    g_scale_factor = args.scale

    img_y, img_x = img.shape[:2]
    print('Canvas shape = {}x{}'.format(img_x, img_y))

    cv2.namedWindow('Canvas')
    cv2.setMouseCallback('Canvas', onMouse)

    mag_area = 32
    img_mag = np.zeros((img_y+mag_area*2, img_x+mag_area*2, 3), dtype=np.uint8)

    print('*** Key operation:')
    print('ESC        : Exit program')
    print('p or space : Pause/Resume movie')

    pause_flag = False
    key = -1
    while key != 27:

        if pause_flag == False and movie_flag == True:
            sts, img = cap.read()
            if sts ==False:
                if not args.video is None:
                    cap.release()
                    cap = cv2.VideoCapture(args.video)  # Re-open input movie
                    continue

        # Draw a cross cursor
        tmpimg = img.copy()
        cx, cy = (g_mouse_x, g_mouse_y)
        drawMarkers(tmpimg, g_points)
        drawCursor(tmpimg, (cx, cy))
        # auxiliary line from the previous point (yellow line)
        if len(g_points)>0:
            cv2.line(tmpimg, g_points[-1], (cx, cy), (0,255,0), thickness=1, lineType=cv2.LINE_AA, ) 

        dispimg = cv2.resize(tmpimg, (0,0), fx=1/g_scale_factor, fy=1/g_scale_factor)
        cv2.imshow('Canvas', dispimg)

        # Magnify around the cursor point - Generate an image with black fringe, crop, and magnify
        img_mag[mag_area:-mag_area, mag_area:-mag_area] = tmpimg     # adding fringe to the image 
        mag = cv2.resize(img_mag[cy:cy+mag_area*2, cx:cx+mag_area*2], (0,0), fx=8, fy=8, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('x8', mag)

        key = cv2.waitKey(100)

        if movie_flag==True and (key==ord('p') or key==ord(' ')):
            pause_flag, msg = (True, 'Paused') if pause_flag==False else (False, 'Resumed')
            print(msg)            

if __name__ == '__main__':
    main()
