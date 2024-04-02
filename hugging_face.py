from huggingface_hub import InferenceClient
from utils import PilToBase64
from generation_data import GenerationData

client = None

def InitInference(hf_key):
    global client
    client = InferenceClient(token=hf_key)

def TextToImage(data: GenerationData):
    image_model = "playgroundai/playground-v2.5-1024px-aesthetic"
    if (data.model == "proteus"):
        image_model = "dataautogpt3/ProteusV0.4-Lightning"

    image = client.text_to_image(
            prompt=data.prompt,
            negative_prompt=data.negative_prompt, 
            height=data.height,    
            width=data.width, 
            num_inference_steps=data.num_inference_steps, 
            guidance_scale=data.guidance_scale,
            model=image_model
    )
    return PilToBase64(image)