import numpy as np
import cv2
import argparse

g_mouse_button = False
g_img = None
g_mouse_x = 0
g_mouse_y = 0

def onMouse(event, x, y, flags, param):
    global g_mouse_button
    global g_mouse_x, g_mouse_y
    if event == cv2.EVENT_LBUTTONDOWN:
        if g_mouse_button == False:
            g_mouse_button = True
            cv2.drawMarker(g_img, (x,y), (  0,  0,  0), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
            cv2.drawMarker(g_img, (x,y), (255,255,255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=1)
            print('{},{}'.format(x, y))
    if event == cv2.EVENT_LBUTTONUP:
        g_mouse_button = False
    g_mouse_x = x
    g_mouse_y = y

def main():
    global g_img
    global g_mouse_x, g_mouse_y
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=False, help='Input image file name')
    parser.add_argument('-s', '--size',  type=str, required=False, help='Image size in XXXxYYY format. E.g. 800x600')
    args = parser.parse_args()

    if args.input is None and args.size is None:
        print('Either one of "--input" or "--size" option must be specified')

    if not args.input is None:
        g_img = cv2.imread(args.input)
    else:
        img_x, img_y = [int(i) for i in args.size.split('x')]
        g_img = np.full((img_x , img_y, 3), 64, dtype=np.uint8)
    
    img_y, img_x, _ = g_img.shape
    print('Canvas shape = {}x{}'.format(img_x, img_y))

    cv2.namedWindow('Canvas')
    cv2.setMouseCallback('Canvas', onMouse)

    mag_area = 32
    img_mag = np.zeros((img_y+mag_area*2, img_x+mag_area*2, 3), dtype=np.uint8)

    key = -1
    while key != 27:

        # Draw a cross cursor
        tmpimg = g_img.copy()
        cv2.line(tmpimg, (g_mouse_x, 0), (g_mouse_x, img_y), (  0,0,0), thickness=2, lineType=cv2.LINE_4)
        cv2.line(tmpimg, (0, g_mouse_y), (img_x, g_mouse_y), (  0,0,0), thickness=2, lineType=cv2.LINE_4)    
        cv2.line(tmpimg, (g_mouse_x, 0), (g_mouse_x, img_y), (255,0,0), thickness=1, lineType=cv2.LINE_4)
        cv2.line(tmpimg, (0, g_mouse_y), (img_x, g_mouse_y), (255,0,0), thickness=1, lineType=cv2.LINE_4)    
        cv2.imshow('Canvas', tmpimg)

        # Magnify around the cursor point - Generate an image with black fringe, crop, and magnify
        img_mag[mag_area:-mag_area, mag_area:-mag_area] = tmpimg
        mag = cv2.resize(img_mag[g_mouse_y:g_mouse_y+mag_area*2, g_mouse_x:g_mouse_x+mag_area*2], (0,0), fx=8, fy=8)
        cv2.imshow('x8', mag)

        key = cv2.waitKey(100)

if __name__ == '__main__':
    main()
