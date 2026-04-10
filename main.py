from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier

# FastAPI App
app = FastAPI(
    title="PSL Translator API",
    description="Pakistan Sign Language Translator",
    version="1.0.0"
)

# CORS (Flutter se connect karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Objects banao
detector = HandDetector()
classifier = GestureClassifier()

# ============ ENDPOINTS ============

# 1. Root - Server check karo
@app.get("/")
def root():
    return {
        "message": "PSL Translator API is running! 🤟",
        "status": "ok",
        "version": "1.0.0"
    }

# 2. Health Check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": classifier.is_model_loaded
    }

# 3. Main Translation Endpoint
@app.post("/translate")
async def translate(file: UploadFile = File(...)):
    """
    Image receive karo aur gesture translate karo
    """
    try:
        # Image bytes read karo
        image_bytes = await file.read()

        # Hand landmarks nikalo
        landmarks = detector.detect_from_bytes(image_bytes)

        # Agar haath nahi mila
        if landmarks is None:
            return {
                "success": False,
                "message": "Haath detect nahi hua!",
                "urdu": "",
                "english": ""
            }

        # Gesture predict karo
        result = classifier.predict(landmarks)

        # Agar result mila
        if result:
            return {
                "success": True,
                "gesture": result["gesture"],
                "urdu": result["urdu"],
                "english": result["english"],
                "confidence": result["confidence"]
            }
        else:
            return {
                "success": False,
                "message": "Gesture pehchana nahi gaya!",
                "urdu": "",
                "english": ""
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "urdu": "",
            "english": ""
        }