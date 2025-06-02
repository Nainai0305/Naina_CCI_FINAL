import cv2
import mediapipe as mp
import speech_recognition as sr
import threading
import time

# === Setup ===
negative_phrases = [
    "palestine", "conservative", "republican", "trump", "maga",
    "right wing", "far right", "liberal", "facts", "truth",
    "freedom", "liberty", "patriot", "patriotic", "nationalist", "debate", "conversation", "vaccine", 
    "republican", "democrat", "cop", "racist", "racism", "abortion", 'pro choice', 'pro life',"claim", "women",
    "choice", "rights", "truth", "hate"   
]

face_detected = False
blackout = False

# === Speech Thread ===
def speech_loop():
    global blackout
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Listening for negative speech...")
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio).lower()
                print("You said:", text)
                for phrase in negative_phrases:
                    if phrase in text:
                        print("⚠️ Negative word detected!")
                        blackout = True
                        time.sleep(2)  # Keep face blacked out briefly
                        blackout = False
                        break
            except Exception as e:
                print("Speech error:", e)

# Start speech recognition on a separate thread
threading.Thread(target=speech_loop, daemon=True).start()

# === MediaPipe + OpenCV ===
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6) as face_detection:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                if blackout:
                    # Draw black rectangle over face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)
                else:
                    # Optionally, draw the face detection box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

        cv2.imshow('Face Blackout on Negative Speech', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
