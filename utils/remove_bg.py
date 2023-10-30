import cv2
import numpy as np

# Загрузите изображение
image = cv2.imread('../images/Trainers_animations/First trainer/Go_forward/1.png')

# Преобразуйте изображение в формат HSV (Оттенок, Насыщенность, Яркость)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Определите диапазон цветов, которые соответствуют вашему фону (в данном случае - белый)
lower_white = np.array([0, 0, 200])
upper_white = np.array([255, 255, 255])

# Создайте маску, которая выделяет области, соответствующие фону
mask = cv2.inRange(hsv, lower_white, upper_white)

# Инвертируйте маску (делаем фон черным, а объекты - белыми)
mask_inv = cv2.bitwise_not(mask)

# Создайте изображение, где фон - черный, а объекты - остаются без изменений
result = cv2.bitwise_and(image, image, mask=mask_inv)

# Сохраните результат
cv2.imwrite('result_image.jpg', result)

# Отобразите результат на экране
cv2.imshow('Result Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()


