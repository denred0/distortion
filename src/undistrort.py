import numpy as np
import cv2

src = cv2.imread("data/1.jpg", cv2.IMREAD_GRAYSCALE)
width = src.shape[1]
height = src.shape[0]

distCoeff = np.zeros((4, 1), np.float64)

# TODO: add your coefficients here!
k1 = 0.0  # negative to remove barrel distortion
k2 = 0.0
p1 = 0.0
p2 = 0.0

distCoeff[0, 0] = k1
distCoeff[1, 0] = k2
distCoeff[2, 0] = p1
distCoeff[3, 0] = p2

# assume unit matrix for camera
cam = np.eye(3, dtype=np.float32)

cx1 = width / 2.0
cy1 = height / 2.0
cx2 = cx1
cy2 = cy1

f1 = 10.0
f2 = 5.0
lamb = -0.0

# cam[0, 2] = cx  # define center x
# cam[1, 2] = cy  # define center y
# cam[0, 0] = f  # define focal length x
# cam[1, 1] = f  # define focal length y

XYZ = np.zeros((src.shape[0], src.shape[1], 3))
uv = np.zeros((src.shape[0], src.shape[1], 2))
src_convert = np.zeros_like(src)

if lamb == 0:

    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            XYZ[i, j][0] = (i - cx1) / f1
            XYZ[i, j][1] = (j - cy1) / f1
            XYZ[i, j][2] = 1

    for i in range(XYZ.shape[0]):
        for j in range(XYZ.shape[1]):
            uv[i, j][0] = XYZ[i, j][0] * f2 + cx2 * XYZ[i, j][2]
            uv[i, j][1] = XYZ[i, j][1] * f2 + cy2 * XYZ[i, j][2]

    # for i in range(src_convert.shape[0]):
    #     for j in range(src_convert.shape[1]):
    #         if int(uv[i, j][0]) < src_convert.shape[0] and int(uv[i, j][0]) > 0 and int(uv[i, j][1]) < \
    #                 src_convert.shape[1] and int(uv[i, j][1]) > 0:
    #             src_convert[i, j] = src[int(uv[i, j][0]), int(uv[i, j][1])]
    for i in range(uv.shape[0]):
        for j in range(uv.shape[1]):
            if int(uv[i, j][0]) >= 0 and int(uv[i, j][0]) < uv.shape[0] and int(uv[i, j][1]) >= 0 and int(uv[i, j][1]) < \
                    uv.shape[1]:
                src_convert[int(uv[i, j][0]), int(uv[i, j][1])] = src[i, j]

    # here the undistortion will be computed
    # dst = cv2.undistort(src, cam, distCoeff)
else:
    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            XYZ[i, j][0] = (i - cx1) / f1
            XYZ[i, j][1] = (j - cy1) / f1
            XYZ[i, j][2] = 1  # + lamb * (((i - cx) / f)  2 + ((j - cy) / f)  2)

    # for i in range(XYZ.shape[0]):
    #     for j in range(XYZ.shape[1]):
    #         if (-XYZ[i, j][2] + lamb * (XYZ[i, j][0]  2 + XYZ[i, j][1]  2)) != 0:
    #             uv[i, j][0] = (XYZ[i, j][0] * f1 + cx1) / (
    #                     -XYZ[i, j][2] + lamb * (XYZ[i, j][0]  2 + XYZ[i, j][1]  2))
    #         else:
    #             uv[i, j][0] = 0
    #
    #         if (-XYZ[i, j][2] + lamb * (XYZ[i, j][0]  2 + XYZ[i, j][1]  2)) != 0:
    #             uv[i, j][1] = (XYZ[i, j][1] * f1 + cy1) / (
    #                     -XYZ[i, j][2] + lamb * (XYZ[i, j][0]  2 + XYZ[i, j][1]  2))
    #         else:
    #             uv[i, j][1] = 0

    for i in range(XYZ.shape[0]):
        for j in range(XYZ.shape[1]):
            # x = (XYZ[i, j][0] * f1 - cx1) / f1
            # y = (XYZ[i, j][1] * f1 - cy1) / f1

            # r2 = np.sqrt((XYZ[i, j][0] / 30.6)  2 + (XYZ[i, j][1] / 30.6)  2)
            #
            # xd = XYZ[i, j][0] * (1 - lamb * r2 ** 2 + lamb * r2 ** 4)
            # yd = XYZ[i, j][1] * (1 - lamb * r2 ** 2 + lamb * r2 ** 4)

            # uv[i, j][0] = (XYZ[i, j][0] * f1 + cx1) * (1 - lamb * ((XYZ[i, j][0] / 30.6)  2 + (XYZ[i, j][1] / 30.6)  2))
            # uv[i, j][1] = (XYZ[i, j][1] * f1 + cy1) * (1 - lamb * ((XYZ[i, j][0] / 30.6)  2 + (XYZ[i, j][1] / 30.6)  2))
            # yd = XYZ[i, j][1] * (1 - lamb * r2 ** 2 + lamb * r2 ** 4)

            x = (XYZ[i, j][0]) * (1 + lamb * ((XYZ[i, j][0] / 32.0) ** 2 + (XYZ[i, j][1] / 32.0) ** 2))
            y = (XYZ[i, j][1]) * (1 + lamb * ((XYZ[i, j][0] / 32.0) ** 2 + (XYZ[i, j][1] / 32.0) ** 2))

            x = (x * f2 + cx2)
            y = (y * f2 + cy2)

            uv[i, j] = [x, y]
            # uv[i, j][0] = XYZ[i, j][0] / 1 * f1 * (1 + lamb * (XYZ[i, j][0]  2 + XYZ[i, j][1]  2)) + cx1
            # uv[i, j][1] = XYZ[i, j][1] / 1 * f1 * (1 + lamb * (XYZ[i, j][0]  2 + XYZ[i, j][1]  2)) + cy1

            # uv[i, j][0] = XYZ[i, j][0] * f1 + cx1 * (
            #         1 - lamb * ((XYZ[i, j][0] / 30.6)  2 + (XYZ[i, j][1] / 30.6)  2))
            # uv[i, j][1] = XYZ[i, j][1] * f1 + cy1 * (
            #         1 - lamb * ((XYZ[i, j][0] / 30.6)  2 + (XYZ[i, j][1] / 30.6)  2))

            # u = XYZ[i, j][0]  # * f1 + cx1
            # v = XYZ[i, j][1]  # * f1 + cy1
            #
            # x_d = u * (1 - lamb * ((XYZ[i, j][0] / 30.6)  2 + (XYZ[i, j][1] / 30.6)  2))
            # y_d = v * (1 - lamb * ((XYZ[i, j][0] / 30.6) ** 2 + (XYZ[i, j][1]


    # delta_x = np.max(uv[:,:,0]) - uv.shape[0]
    # delta_y = np.max(uv[:,:,1]) - uv.shape[1]
    #
    # if delta_x > 0:
    #     for i in range(uv.shape[0]):
    #         for j in range(uv.shape[1]):
    #             if uv[i, j][0] > 0:
    #                 uv[i, j][0] -= delta_x
    #             else:
    #                 uv[i, j][0] += delta_x
    #
    # if delta_y > 0:
    #     for i in range(uv.shape[0]):
    #         for j in range(uv.shape[1]):
    #             if uv[i, j][1] > 0:
    #                 uv[i, j][1] -= delta_y
    #             else:
    #                 uv[i, j][1] += delta_y



    for i in range(uv.shape[0]):
        for j in range(uv.shape[1]):
            if int(uv[i, j][0]) >= 0 and int(uv[i, j][0]) < uv.shape[0] and int(uv[i, j][1]) >=0 and int(uv[i, j][1]) < uv.shape[1]:
                src_convert[int(uv[i, j][0]), int(uv[i, j][1])] = src[i, j]


cv2.imshow('dst', src_convert)
cv2.waitKey(0)
cv2.destroyAllWindows()