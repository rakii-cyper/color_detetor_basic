import cv2
import numpy as np


def mask_return(hue):
    range_detect = 15
    low = max(0, hue-range_detect)
    up = min(180, hue+range_detect)

    if hue < 10:
        return np.array([low, 150, 20]), np.array([up, 255, 255]), "RED"
    elif hue < 22:
        return np.array([low, 150, 20]), np.array([up, 255, 255]), "ORANGE"
    elif hue < 33:
        return np.array([low, 150, 20]), np.array([up, 255, 255]), "YELLOW"
    elif hue < 78:
        return np.array([low, 150, 20]), np.array([up, 255, 255]), "GREEN"
    elif hue < 131:
        return np.array([low, 150, 20]), np.array([up, 255, 255]), "BLUE"
    elif hue < 170:
        return np.array([low, 150, 20]), np.array([up, 255, 255]), "VIOLET"
    else:
        return np.array([low, 150, 20]), np.array([up, 255, 255]), "RED"


if __name__ == '__main__':
    image = cv2.imread("crayon.jpg")

    image = cv2.resize(image, (640, 640), interpolation=cv2.INTER_AREA)

    start_position = (10, 50)
    end_position = (630, 580)
    crop_height = 310
    crop_width = 48

    for h in range(start_position[0], end_position[0], crop_height):
        for w in range(start_position[1], end_position[1], 45):
            product_img = image.copy()[h:h+crop_height, w:w+crop_width]
            cv2.imshow("crop:", product_img)

            hsv_image = cv2.cvtColor(product_img, cv2.COLOR_BGR2HSV)
            height, width, _ = product_img.shape
            cx = int(width / 2) - 5
            cy = int(height / 2) - 20
            # Pick pixel value
            pixel_center = hsv_image[cy, cx]
            hue_value = pixel_center[0]
            lower, upper, color = mask_return(hue_value)

            mask = cv2.inRange(hsv_image, lower, upper)
            mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            reg_x_upper, reg_y_upper, reg_x_lower, reg_y_lower = 255, 255, 0, 0

            if len(mask_contours) != 0:
                for mask_contour in mask_contours:
                    if cv2.contourArea(mask_contour) > 100:
                        x, y, w_r, h_r = cv2.boundingRect(mask_contour)
                        reg_x_upper = min(x, reg_x_upper)
                        reg_y_upper = min(y, reg_y_upper)
                        reg_x_lower = max(x + w_r, reg_x_lower)
                        reg_y_lower = max(y + h_r, reg_y_lower)
                        cv2.rectangle(product_img, (x, y), (x + w_r, y + h_r), (255, 255, 255), 1)

                cv2.rectangle(product_img, (reg_x_upper, reg_y_upper), (reg_x_lower, reg_y_lower), (0, 0, 255), 3)

            print(color)
            cv2.imshow("image", product_img)
            key = cv2.waitKey(0)
