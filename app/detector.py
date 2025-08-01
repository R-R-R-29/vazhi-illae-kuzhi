import cv2
import numpy as np

def detect_potholes(image_path, area_threshold=500):
    image = cv2.imread(image_path)
    result = {}
    stages = {}

    if image is None:
        return {"potholes": [], "stages": {}, "error": "Image could not be loaded."}

    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    stages["1. Grayscale"] = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Enhance contrast with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)
    stages["2. CLAHE"] = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR)

    # Use a light bilateral filter to preserve edges
    filtered = cv2.bilateralFilter(contrast, 9, 75, 75)

    # Morphological closing to reduce small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel)
    stages["3. Morph Close"] = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)

    # Sharpen edges
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(closed, -1, sharpen_kernel)
    stages["4. Sharpened"] = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)

    # Adaptive Canny edges
    med = np.median(sharpened)
    lower = int(max(0, 0.66 * med))
    upper = int(min(255, 1.33 * med))
    edges = cv2.Canny(sharpened, lower, upper)
    stages["5. Edges"] = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Dilate to connect broken contours
    dilated = cv2.dilate(edges, kernel, iterations=2)
    stages["6. Dilated"] = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)

    # Contour detection
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    potholes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < area_threshold:
            continue

        # Shape filtering: filter out elongated lines or flat stains
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

        # Convexity: potholes are usually concave
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        if hull_area == 0:
            continue
        solidity = area / hull_area

        # Heuristic filter: good solidity + few points in approx
        if solidity < 0.5:
            continue  # skip open or too irregular shapes


        x, y, w, h = cv2.boundingRect(cnt)
        roi = gray[y:y+h, x:x+w]
        brightness = np.mean(roi)
        darkness = 255 - brightness
        danger_score = int(area * (darkness / 255))

        if danger_score > 15000:
            level = "High"
            color = (0, 0, 255)
        elif danger_score > 8000:
            level = "Medium"
            color = (0, 165, 255)
        else:
            continue

        cv2.rectangle(original, (x, y), (x + w, y + h), color, 2)
        cv2.putText(original, level, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        potholes.append({
            "bbox": (x, y, w, h),
            "area": int(area),
            "brightness": int(brightness),
            "danger_score": danger_score,
            "danger_level": level,
            "solidity": round(solidity, 2)
        })

    stages["7. Final Detection"] = original

    result["potholes"] = potholes
    result["stages"] = stages
    result["image"] = original
    return result