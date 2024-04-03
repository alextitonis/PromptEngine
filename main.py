from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generation_data import GenerationData
from generation_result import GenerationResult
from dotenv import load_dotenv
from replicate_api import init_replicate, text_to_image, generate_text, generate_image_style
import os

load_dotenv()
REPLICATE_KEY = os.environ.get("REPLICATE_KEY")
replicate_client = init_replicate(REPLICATE_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(data: GenerationData) -> GenerationResult:
    improvted_prompt = generate_text(client=replicate_client, image_prompt=data.prompt)
    style = generate_image_style(client=replicate_client, image_prompt=improvted_prompt)
    improvted_prompt = improvted_prompt + ", " + style
    data.prompt = improvted_prompt
    result_image = text_to_image(client=replicate_client, data=data)
    result = GenerationResult(image=result_image, prompt=data.prompt)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host='0.0.0.0', port=7777, reload=True)