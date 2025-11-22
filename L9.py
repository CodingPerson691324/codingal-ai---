import cv2
import matplotlib.pyplot as plt

img = cv2.imread('photo.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

h, w, _= img.shape

r1_w, r1_h = 25, 25
r1_x, r1_y = 20, 20
cv2.rectangle(img, (r1_x, r1_y), (r1_x + r1_w, r1_y + r1_h), (0, 255, 255), 1)

r2_w, r2_h = 25, 25
r2_x, r2_y = w - r2_w - 20, h - r2_h - 20
cv2.rectangle(img, (r2_x, r2_y), (r2_x + r2_w, r2_y + r2_h), (255, 0, 255), 1)

c1 = (r1_x + r1_w // 2, r1_y + r1_h // 2)
c2 = (r2_x + r2_w // 2, r2_y + r2_h // 2)

cv2.circle(img, c1, 5, (0, 255, 0), -1)
cv2.circle(img, c2, 5, (0, 0, 255), -1)

cv2.line(img, c1, c2, (0, 255, 0), 1)

arrow_x = w - 50
start = (arrow_x, 20)
end = (arrow_x, h - 100)

cv2.arrowedLine(img, start, end, (255, 255, 0), 1)
cv2.arrowedLine(img, end, start, (255, 255, 0), 1)

cv2.putText(img, f'Height: {h}px', (arrow_x - 150, h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 1)
cv2.putText(img, 'region 1', (r1_x, r1_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)

cv2.putText(img, 'region 2', (r2_x, r2_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 255), 1)

plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.axis('off')
plt.title('Image with Annotations')
plt.show()