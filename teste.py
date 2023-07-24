import cv2
from scipy import ndimage
import numpy as np

def show(img):
    proporcao = 0.3
    nova_largura = int(img.shape[1] * proporcao)
    nova_altura = int(img.shape[0] * proporcao)
    imagem_redimensionada = cv2.resize(img, (nova_largura, nova_altura))
    cv2.imshow("show", imagem_redimensionada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img_path = "img/capture/3.jpg"

img = cv2.imread(img_path, 0)
img1 = cv2.imread(img_path)

kernel = 2
thr_canny = 0.1
sig_canny = 1
theta_resolution = 90
rho_resolution = 1

img = cv2.filter2D(img, -1, kernel)
img = ndimage.median_filter(img, size=(7, 7))
img = cv2.Canny(img, int(thr_canny * 255), int(sig_canny * 255))
lines = cv2.HoughLines(img, 1.5, np.pi / 180, 120, None, 3, 0)

vertical_lines = []
horizontal_lines = []

for line in lines:
    rho, theta = line[0]
    angle_degrees = np.degrees(theta)

    # Identificar linhas verticais e horizontais
    if 85 <= angle_degrees <= 95:
        horizontal_lines.append(line)
    elif 175 <= angle_degrees <= 185:
        vertical_lines.append(line)

intersection_points = []

# Encontrar os pontos de interseção entre as linhas
for h_line in horizontal_lines:
    for v_line in vertical_lines:
        rho_h, theta_h = h_line[0]
        rho_v, theta_v = v_line[0]

        A = np.array([[np.cos(theta_h), np.sin(theta_h)], [np.cos(theta_v), np.sin(theta_v)]])
        B = np.array([rho_h, rho_v])
        intersection_point = np.linalg.solve(A, B)
        intersection_points.append(intersection_point)

# # Desenhar os pontos de interseção na imagem
# for point in intersection_points:
#     x, y = map(int, point)
#     cv2.circle(img, (x, y), 5, 255, -1)

# Criar uma imagem preta para desenhar os pontos de interseção
result_img = np.zeros_like(img)

# Desenhar os pontos de interseção na imagem resultante
for point in intersection_points:
    x, y = map(int, point)
    cv2.circle(result_img, (x, y), 5, 255, -1)




# Aplicar dilatação nos pontos de interseção
kernel_dilate = np.ones((3, 3), np.uint8)
result_img = cv2.dilate(result_img, kernel_dilate, iterations=1)

#show(result_img)



cnts = cv2.findContours(result_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]


ROI_number = 0
roi_arr = []
shapes = []

for c in cnts:
    area = cv2.contourArea(c)
    if area > 1000:

        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img1, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = img1[y:y+h, x:x+w]
        shapes.append(img1[y:y+h, x:x+w].shape)
        # cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
        roi_arr.append(ROI)
        ROI_number += 1


show(img1)