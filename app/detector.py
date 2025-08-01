import cv2
import numpy as np

def detect_potholes(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Histogram equalization for better contrast
    enhanced = cv2.equalizeHist(gray)

    # Blur + Edge detection
    blur = cv2.GaussianBlur(enhanced, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    potholes = []
    result_img = img.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 600 or area > 20000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h

        if aspect_ratio < 0.3 or aspect_ratio > 3.5:
            continue  # ignore very tall or wide shapes

        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [cnt], -1, 255, -1)
        mean_inside = cv2.mean(gray, mask=mask)[0]
        mean_outside = cv2.mean(gray)[0]

        # Only consider if it's significantly darker inside the contour
        if mean_outside - mean_inside < 15:
            continue

        potholes.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "area": area
        })

        # Color coding for visualization
        if area > 10000:
            color = (0, 0, 255)    # Red
        elif area > 3000:
            color = (255, 0, 0)    # Blue
        else:
            color = (0, 255, 0)    # Green

        cv2.drawContours(result_img, [cnt], -1, color, 2)

    return {
        "potholes": potholes,
        "stages": {
            "Masked": gray,
            "Enhanced": enhanced,
            "Binary": edges,
            "Final": result_img
        }
    }
