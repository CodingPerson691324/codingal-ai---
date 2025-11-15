import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('photo.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(image_rgb, M, (w, h))

rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
plt.imshow(rotated_rgb)
plt.title('Rotated Image by 45 degrees')
plt.show()

brightness_matrix = np.ones(image.shape, dtype="uint8") * 50
brightened = cv2.add(image_rgb, brightness_matrix)

brighter_rgb = cv2.cvtColor(brightened, cv2.COLOR_BGR2RGB)
plt.imshow(brighter_rgb)
plt.title('Brightened Image')
plt.show()