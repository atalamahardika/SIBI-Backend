from fastapi.responses import RedirectResponse
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.utils.predict import predict_image
from PIL import Image
import io
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🚀 Aplikasi FastAPI berhasil dimulai.")

# CORS (izinkan akses dari Laravel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sibi-frontend-production.up.railway.app"],
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

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
