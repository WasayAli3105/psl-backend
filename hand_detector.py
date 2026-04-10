import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import urllib.request
import os

class HandDetector:
    def __init__(self):
        # Model download karo agar nahi hai
        model_path = "hand_landmarker.task"
        
        if not os.path.exists(model_path):
            print("Hand Landmarker model download ho raha hai...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            urllib.request.urlretrieve(url, model_path)
            print("Model download ho gaya!")

        # MediaPipe naya tarika
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        print("Hand Detector Ready!")

    def get_landmarks(self, image_np):
        """
        Image se hand landmarks nikalo
        Returns: 21 points ki list ya None
        """
        try:
            # NumPy image ko MediaPipe image mein convert karo
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            )

            # Detect karo
            result = self.detector.detect(mp_image)

            # Agar haath mila
            if result.hand_landmarks:
                landmarks = result.hand_landmarks[0]

                # 21 points nikalo
                points = []
                for lm in landmarks:
                    points.append([lm.x, lm.y, lm.z])

                return np.array(points).flatten()  # 63 values

            return None

        except Exception as e:
            print(f"Hand Detection Error: {e}")
            return None

    def detect_from_bytes(self, image_bytes):
        """
        Image bytes se landmarks nikalo
        """
        try:
            # Bytes ko image mein convert karo
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                return None

            return self.get_landmarks(image)

        except Exception as e:
            print(f"Image Decode Error: {e}")
            return None