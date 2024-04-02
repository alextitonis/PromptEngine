from pydantic import BaseModel

class GenerationResult(BaseModel):
    image: str
    prompt: str