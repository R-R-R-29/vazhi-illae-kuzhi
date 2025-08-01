import cv2

def detect_potholes(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    potholes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 15000:  # Adjustable depending on test images
            x, y, w, h = cv2.boundingRect(cnt)
            potholes.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "area": area
            })

    return potholes, img  # Return image for overlay too

