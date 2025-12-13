import cv2
import numpy as numpy

def apply_color_filter(image, filter_type):

    filtered_image = image.copy()

    if filter_type == 'red_tint':
        filtered_image[:, :, 1] = 0  # Zero out green channel
        filtered_image[:, :, 0] = 0  # Zero out blue channel
    elif filter_type == 'blue_tint':
        filtered_image[:, :, 1] = 0  # Zero out green channel
        filtered_image[:, :, 2] = 0  # Zero out red channel
    elif filter_type == 'green_tint':
        filtered_image[:, :, 0] = 0  # Zero out blue channel
        filtered_image[:, :, 2] = 0  # Zero out red channel
    elif filter_type == 'increase_red':
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], 50)  # Increase red channel#
    elif filter_type == 'decrease_blue':
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], 150)  # Decrease blue channel

    return filtered_image

image_path = 'photo.jpg'
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not read the image.")
else:

    filter_type = 'original'

    print('click one of the following keys to apply filter:')
    print('r - red tint')
    print('b - blue tint')
    print('g - green tint')
    print('i - increase red channel')
    print('d - decrease blue channel')
    print('q - quit')

    while True:

        filtered_image = apply_color_filter(image, filter_type)

        cv2.imshow('Image Filter', filtered_image)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('r'):
            filter_type = 'red_tint'
        elif key == ord('b'):
            filter_type = 'blue_tint'
        elif key == ord('g'):
            filter_type = 'green_tint'
        elif key == ord('i'):
            filter_type = 'increase_red'
        elif key == ord('d'):
            filter_type = 'decrease_blue'
        elif key == ord('q'):
            print('exiting...')
            break
        else:
            print('invalid key! please use one of the above keys!!!')

cv2.destroyAllWindows()