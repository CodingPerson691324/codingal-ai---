import cv2
import numpy as np
import matplotlib.pyplot as plt

def show(title, img):
    if len(img.shape) == 2:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

img = cv2.imread('photo.jpg')
if img is None:
    print("Error: Image not found.")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
show("original Image", gray)

print('pick an option:')
print('1 canny edge detection')
print('2 sobel edge detection')
print('3 laplacian edge detection')
print('4 gaussian blur')
print('5 median blur')

choice = input('Enter your choice (1-5): ')

if choice == '1':
    edges = cv2.Canny(gray, 100, 200)
    show("Canny Edge Detection", edges)

elif choice == '2':
    sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    sobel = cv2.magnitude(sx, sy)
    show("Sobel Edge Detection", sobel)

elif choice == '3':
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    lap = np.abs(lap).astype(np.uint8)
    show("Laplacian Edge Detection", lap)

elif choice == '4':
    blur = cv2.GaussianBlur(gray, (55, 55), 0)
    show("Gaussian Blur", blur)

elif choice == '5':
    median = cv2.medianBlur(gray, 45)
    show("Median Blur", median)

else:
    print("Invalid choice. Please select a number between 1 and 5.")