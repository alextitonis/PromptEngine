from pydantic import BaseModel

class GenerationData(BaseModel):
    prompt: str
    model: str
    negative_prompt: str
    height: int = 1024 
    width: int = 1024 
    num_inference_steps: int = 8
    guidance_scale: int = 2
