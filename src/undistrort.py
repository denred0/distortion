import numpy as np
import cv2

src = cv2.imread("data/1.jpg", cv2.IMREAD_GRAYSCALE)
width = src.shape[1]
height = src.shape[0]

f1 = 10.0
cx1 = width / 2.0
cy1 = height / 2.0
lamb1 = 0.0

f2 = 5.0
cx2 = width / 2.0
cy2 = height / 2.0
lamb2 = -0.0

src_convert = np.zeros_like(src)
XY = np.indices(src.shape, dtype=float)

XY[0] = (XY[0] - cx1) / f1
XY[1] = (XY[1] - cy1) / f1
Z = 1 + lamb1 * (((XY[0] - cx1) / f1) ** 2 + ((XY[1] - cy1) / f1) ** 2)

max_x = np.max(XY[0])
max_y = np.max(XY[1])

u = XY[0] / Z * f2 * (1 + lamb2 * ((XY[0] / max_x) ** 2 + (XY[1] / max_y) ** 2)) + cx2
v = XY[1] / Z * f2 * (1 + lamb2 * ((XY[0] / max_x) ** 2 + (XY[1] / max_y) ** 2)) + cx2

src_convert[u.astype(int), v.astype(int)] = src

cv2.imshow('dst', src_convert)
cv2.waitKey(0)
cv2.destroyAllWindows()

# for i in range(uv2.shape[0]):
#     for j in range(uv2.shape[1]):
#         if int(uv2[i, j][0]) >= 0 and int(uv2[i, j][0]) < uv2.shape[0] and int(uv2[i, j][1]) >= 0 and int(uv2[i, j][1]) < \
#                 uv2.shape[1]:
#             src_convert[(uv2[i, j, 0]), (uv2[i, j, 1])] = src[i, j]

# for i in range(src.shape[0]):
#     for j in range(src.shape[1]):
#         XYZ[i, j][0] = (i - cx1) / f1
#         XYZ[i, j][1] = (j - cy1) / f1
#         XYZ[i, j][2] = 1 + lamb1 * (((i - cx1) / f1) ** 2 + ((j - cy1) / f1) ** 2)
#
# max_x = np.max(XYZ[:, 0])
# max_y = np.max(XYZ[:, 1])
#
# for i in range(XYZ.shape[0]):
#     for j in range(XYZ.shape[1]):
#         if XYZ[i, j][2] != 0:
#             uv[i, j][0] = XYZ[i, j][0] / XYZ[i, j][2] * f2 * (
#                     1 + lamb2 * ((XYZ[i, j][0] / max_x) ** 2 + (XYZ[i, j][1] / max_y) ** 2)) + cx2
#             uv[i, j][1] = XYZ[i, j][1] / XYZ[i, j][2] * f2 * (
#                     1 + lamb2 * ((XYZ[i, j][0] / max_x) ** 2 + (XYZ[i, j][1] / max_y) ** 2)) + cy2
#
# for i in range(uv.shape[0]):
#     for j in range(uv.shape[1]):
#         if int(uv[i, j][0]) >= 0 and int(uv[i, j][0]) < uv.shape[0] and int(uv[i, j][1]) >= 0 and int(uv[i, j][1]) < \
#                 uv.shape[1]:
#             src_convert[int(uv[i, j][0]), int(uv[i, j][1])] = src[i, j]


