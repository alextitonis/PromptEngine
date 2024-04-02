from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generation_data import GenerationData
from generation_result import GenerationResult
from hugging_face import InitInference, TextToImage
from dotenv import load_dotenv
import os

load_dotenv()
HF_KEY = os.environ.get("HF_KEY")
InitInference(HF_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(data: GenerationData):
    print(data)
    result = GenerationResult(image="", error="")
    result_image = TextToImage(data)

    print(type(result_image))
    if type(result_image) == str:
       result.image = result_image
    else:
        result.error = result_image

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host='0.0.0.0', port=7777, reload=True)