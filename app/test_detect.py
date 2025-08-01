from detector import detect_potholes

image_path = "../images/sample_road.jpg"
results, _ = detect_potholes(image_path)

for i, pothole in enumerate(results):
    print(f"Pothole {i+1}: {pothole}")
