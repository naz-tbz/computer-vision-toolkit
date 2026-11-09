import cv2
import os

# ==================================
# Load Cascade Classifiers
# ==================================
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_smile.xml")

if face_cascade.empty() or smile_cascade.empty():
    print("Error: could not load cascade files. Check the 'haarcascades' folder path.")
    exit()

# ==================================
# Folder to Save Smiling Faces
# ==================================
save_folder = "smiling_faces"
os.makedirs(save_folder, exist_ok=True)
saved_count = 0

# ==================================
# Start Webcam
# ==================================
desired_fps = 10
cap = cv2.VideoCapture(0)

original_fps = int(cap.get(cv2.CAP_PROP_FPS))
if original_fps <= 0:
    original_fps = 30
frame_interval = max(1, int(original_fps / desired_fps))

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_interval == 0:

        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the full frame
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Crop the face region (grayscale for detection, color for saving)
            face_gray = gray[y:y + h, x:x + w]
            face_color = frame[y:y + h, x:x + w]

            # Detect smiles inside the cropped face only
            smiles = smile_cascade.detectMultiScale(
                face_gray,
                scaleFactor=1.7,
                minNeighbors=22
            )

            if len(smiles) > 0:
                label = "Smiling :)"
                label_color = (0, 255, 0)

                # Draw rectangle around the smile (inside the face crop)
                sx, sy, sw, sh = smiles[0]
                cv2.rectangle(face_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)

                # Save the cropped smiling face to disk
                saved_count += 1
                filename = os.path.join(save_folder, "smile_" + str(saved_count) + ".jpg")
                cv2.imwrite(filename, face_color)

            else:
                label = "No smile"
                label_color = (0, 0, 255)

            # Draw label above the face rectangle
            cv2.putText(
                frame, label, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, label_color, 2
            )

        cv2.imshow("Face and Smile Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()