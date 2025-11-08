import cv2

image = cv2.imread('photo.jpg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

resized_image = cv2.resize(gray_image, (224, 224))

cv2.imshow('Processed Image', resized_image)

key = cv2.waitKey(0)

if key == ord('s'):

    cv2.imwrite('grayscale_resized_image.jpg')
    print('image saved as grayscale_resized_image.jpg')
else:
    print('image not saved')

    cv2.destroyAllWindows()