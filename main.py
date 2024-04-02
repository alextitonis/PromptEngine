from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generation_data import GenerationData
from generation_result import GenerationResult
from dotenv import load_dotenv
from replicate_api import InitReplicate, GenerateText, TextToImage
import os

load_dotenv()
REPLICATE_KEY = os.environ.get("REPLICATE_KEY")
InitReplicate(REPLICATE_KEY)

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
    improvted_prompt = GenerateText(data.prompt)
    data.prompt = improvted_prompt
    result_image = TextToImage(data)
    result = GenerationResult(image=result_image, prompt=data.prompt)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host='0.0.0.0', port=7777, reload=True)