import cv2
import numpy as np


def fisheye_effect(image, strength=0.0005):
    height, width = image.shape[:2]
    map_y, map_x = np.indices((height, width), dtype=np.float32)
    x = map_x - width / 2
    y = map_y - height / 2
    r = np.sqrt(x**2 + y**2)

    theta = np.arctan(r * strength)
    scale = np.ones_like(r)

    mask = r != 0
    scale[mask] = theta[mask] / (r[mask] * strength)

    map_x = scale * x + width / 2
    map_y = scale * y + height / 2

    return cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)


# Загрузка изображения
image = cv2.imread('img/lena.png')
if image is None:
    raise FileNotFoundError("Не удалось загрузить изображение 'img/lena.png'.")

# Применяем эффект рыбьего глаза
distorted = fisheye_effect(image, strength=-0.005)

# Отображаем результат
cv2.imshow('Fisheye Effect', distorted)
cv2.waitKey(0)
cv2.destroyAllWindows()
