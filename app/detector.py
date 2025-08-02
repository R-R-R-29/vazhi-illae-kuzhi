# Import OpenCV for image processing and NumPy for numerical operations
import cv2
import numpy as np

# Function to detect potholes in an image using multiple processing stages
def detect_potholes(image_path, area_threshold=300):
    image = cv2.imread(image_path)  # Load the image from the given path
    result = {}  # Dictionary to hold final results
    stages = {}  # Dictionary to hold intermediate processing stages

    if image is None:  # Check if image was loaded successfully
        return {"potholes": [], "stages": {}, "error": "Image could not be loaded."}

    original = image.copy()  # Make a copy of the original image for drawing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    stages["1. Grayscale"] = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # Store grayscale image for visualization

    # CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))  # Create CLAHE object
    contrast = clahe.apply(gray)  # Apply CLAHE to grayscale image
    stages["2. CLAHE"] = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR)  # Store contrast-enhanced image

    # Bilateral Filter
    filtered = cv2.bilateralFilter(contrast, 9, 75, 75)  # Apply bilateral filter to reduce noise while keeping edges

    # Adaptive Threshold (useful for light potholes)
    adaptive = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY_INV, 15, 10)  # Convert image to binary using adaptive threshold
    stages["3. Adaptive Threshold"] = cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)  # Store thresholded image

    # Morph operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # Create elliptical structuring element
    morph = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)  # Apply closing to fill small holes
    morph = cv2.dilate(morph, kernel, iterations=2)  # Dilate to merge close regions
    stages["4. Morphology"] = cv2.cvtColor(morph, cv2.COLOR_GRAY2BGR)  # Store morphological result

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Detect contours

    potholes = []  # List to store detected potholes

    for cnt in contours:  # Loop through each contour
        area = cv2.contourArea(cnt)  # Calculate area of the contour
        if area < area_threshold:  # Skip small contours
            continue

        x, y, w, h = cv2.boundingRect(cnt)  # Get bounding box
        aspect_ratio = float(w) / h if h != 0 else 0  # Compute aspect ratio
        if aspect_ratio > 6.0 or aspect_ratio < 0.15:  # Filter out unusual shapes
            continue

        rect_area = w * h
        extent = float(area) / rect_area if rect_area != 0 else 0  # Compute extent (area coverage)
        if extent < 0.15:  # Skip low coverage areas
            continue

        hull = cv2.convexHull(cnt)  # Create convex hull around contour
        hull_area = cv2.contourArea(hull)  # Area of convex hull
        if hull_area == 0:
            continue
        solidity = area / hull_area  # Compute solidity
        if solidity < 0.3:  # Skip contours with low solidity
            continue

        # Danger score = area * brightness drop
        roi = gray[y:y+h, x:x+w]  # Extract region of interest from grayscale image
        brightness = np.mean(roi)  # Calculate average brightness
        darkness = 255 - brightness  # Invert to get darkness
        danger_score = int(area * (darkness / 255))  # Compute danger score based on area and darkness

        # Flexible thresholds
        if danger_score > 10000:  # High danger
            level = "High"
            color = (0, 0, 255)  # Red
        elif danger_score > 5000:  # Medium danger
            level = "Medium"
            color = (0, 165, 255)  # Orange
        elif danger_score > 2000:  # Low danger
            level = "Low"
            color = (0, 255, 255)  # Yellow
        else:
            continue  # Skip if not dangerous enough

        # Draw rectangle and label on the original image
        cv2.rectangle(original, (x, y), (x + w, y + h), color, 2)
        cv2.putText(original, level, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Append pothole details to the list
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

    stages["5. Final Detection"] = original  # Store final image with annotations
    result["potholes"] = potholes  # Add pothole data to result
    result["stages"] = stages  # Add all intermediate stages
    result["image"] = original  # Add final image to result
    return result  # Return the final result dictionary