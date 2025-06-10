from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.utils.predict import predict_image
from PIL import Image
import io

app = FastAPI()

# CORS (izinkan akses dari Laravel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    try:
        prediction = predict_image(image)
        return {"prediction": prediction}
    except ValueError as e:
        return {"error": str(e)}
