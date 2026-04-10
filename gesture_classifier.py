import numpy as np
from gestures import GESTURES, GESTURE_NAMES

class GestureClassifier:
    def __init__(self):
        self.model = None
        self.is_model_loaded = False
        print("Gesture Classifier Ready!")

    def load_model(self, model_path):
        """
        Trained model load karo
        """
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(model_path)
            self.is_model_loaded = True
            print(f"Model Loaded: {model_path}")
            return True
        except Exception as e:
            print(f"Model Load Error: {e}")
            return False

    def predict(self, landmarks):
        """
        Landmarks se gesture predict karo
        """
        try:
            # Agar model load hai
            if self.is_model_loaded and self.model is not None:
                # Model se predict karo
                landmarks_input = landmarks.reshape(1, -1)
                prediction = self.model.predict(landmarks_input)
                gesture_index = np.argmax(prediction)
                confidence = float(np.max(prediction))
                gesture_name = GESTURE_NAMES[gesture_index]
            else:
                # Model nahi hai to dummy result do
                gesture_name = "salam"
                confidence = 0.95

            # Gesture ka matlab nikalo
            if gesture_name in GESTURES:
                result = GESTURES[gesture_name]
                return {
                    "gesture": gesture_name,
                    "urdu": result["urdu"],
                    "english": result["english"],
                    "confidence": confidence
                }
            else:
                return None

        except Exception as e:
            print(f"Prediction Error: {e}")
            return None