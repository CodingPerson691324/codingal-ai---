import cv2
import matplotlib.pyplot as plt

image = cv2.imread('photo.jpg')

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.title('RGB Image')
plt.show()

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(image_gray, cmap='gray')
plt.title('Grayscale Image')
plt.show()

cropped_image = image[50:150, 100:300]
cropped_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
plt.imshow(cropped_rgb)
plt.title('cropped region')
plt.show()