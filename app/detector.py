import cv2
import numpy as np

def detect_potholes(image_path, area_threshold=300):
    image = cv2.imread(image_path)
    result = {}
    stages = {}

    if image is None:
        return {"potholes": [], "stages": {}, "error": "Image could not be loaded."}

    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    stages["1. Grayscale"] = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)
    stages["2. CLAHE"] = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR)

    # Bilateral Filter
    filtered = cv2.bilateralFilter(contrast, 9, 75, 75)

    # Adaptive Threshold (useful for light potholes)
    adaptive = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY_INV, 15, 10)
    stages["3. Adaptive Threshold"] = cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)

    # Morph operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    morph = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)
    morph = cv2.dilate(morph, kernel, iterations=2)
    stages["4. Morphology"] = cv2.cvtColor(morph, cv2.COLOR_GRAY2BGR)

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    potholes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < area_threshold:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h if h != 0 else 0
        if aspect_ratio > 6.0 or aspect_ratio < 0.15:
            continue

        rect_area = w * h
        extent = float(area) / rect_area if rect_area != 0 else 0
        if extent < 0.15:
            continue

        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        if hull_area == 0:
            continue
        solidity = area / hull_area
        if solidity < 0.3:
            continue

        # Danger score = area * brightness drop
        roi = gray[y:y+h, x:x+w]
        brightness = np.mean(roi)
        darkness = 255 - brightness
        danger_score = int(area * (darkness / 255))

        # Flexible thresholds
        if danger_score > 10000:
            level = "High"
            color = (0, 0, 255)
        elif danger_score > 5000:
            level = "Medium"
            color = (0, 165, 255)
        elif danger_score > 2000:
            level = "Low"
            color = (0, 255, 255)
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
            "solidity": round(solidity, 2),
            "aspect_ratio": round(aspect_ratio, 2),
            "extent": round(extent, 2)
        })

    stages["5. Final Detection"] = original
    result["potholes"] = potholes
    result["stages"] = stages
    result["image"] = original
    return result