from pydantic import BaseModel

class GenerationResult(BaseModel):
    image: str
    error: str