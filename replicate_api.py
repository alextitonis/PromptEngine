import replicate
from generation_data import GenerationData
from utils import WebImageToBase64

client = None

def InitReplicate(key: str):
    global client
    client = replicate.Client(key)
    
def GenerateText(image_prompt: str):
    base_prompt = """<INSTRUCTIONS>
You are an artist, your only job is to improve image generation prompts!
When you get a simple prompt, you have to improve it and make it more detailed!
If the base prompt is only an object/animal/person, add a background as well!
The output must only be one phrase!
Be Creative!
</INSTRUCTIONS>
<EXAMPLES>
Input: dog
Output: Long haired dog, with blue eyes, lying on the beach, best quality, hd

Input: tree
Output: A palm tree with many coconuts on a pacific island, best quality, hd

Input: door
Output: A hard metal door keeping the secrets of the house locked behind it, best quality, hd

Input: a woman
Output: A red haired woman, wearing a green dress, sitting on a chair, best quality, hd

Input: car
Output: A sleek, silver car speeding down a winding mountain road, best quality, hd

Input: book
Output: A weathered leather-bound book resting on a mahogany desk in a dimly lit library, best quality, hd

Input: mountain
Output: A majestic snow-capped mountain towering above a dense pine forest, best quality, hd

Input: cup
Output: A delicate porcelain cup filled with steaming hot tea, sitting on a lace tablecloth, best quality, hd

Input: city
Output: A bustling cityscape illuminated by the vibrant colors of neon lights reflected in rain-soaked streets, best quality, hd

Input: phone
Output: A modern smartphone with a cracked screen, buzzing with notifications on a cluttered desk, best quality, hd

Input: cake
Output: A decadent chocolate cake adorned with fresh strawberries and whipped cream, displayed on a crystal platter, best quality, hd

Input: ship
Output: A massive cargo ship gliding gracefully across the tranquil waters of a harbor at sunset, best quality, hd

Input: window
Output: A large bay window overlooking a lush garden filled with blooming flowers and chirping birds, best quality, hd

Input: guitar
Output: A vintage acoustic guitar leaning against an old wooden chair in a sunlit room, best quality, hd
</EXAMPLES>

Input: {image_prompt}
Output:
""".replace("{image_prompt}", image_prompt)
    
    output = client.run(
        "mistralai/mixtral-8x7b-instruct-v0.1",
        input={
            "top_k": 50,
            "top_p": 0.9,
            "prompt": base_prompt,
            "temperature": 0.6,
            "max_new_tokens": 128,
            "prompt_template": "<s>[INST] {prompt} [/INST] ",
            "presence_penalty": 0,
            "frequency_penalty": 0
        }
    )
    improved_prompt = "".join(output).strip()
    return improved_prompt

def TextToImage(data: GenerationData):
    image_model = "playgroundai/playground-v2.5-1024px-aesthetic:a45f82a1382bed5c7aeb861dac7c7d191b0fdf74d8d57c4a0e6ed7d4d0bf7d24"
    scheduler = "DPMSolver++"
    if (data.model == "proteus"):
        image_model = "lucataco/proteus-v0.4-lightning:21464a198e9baa3b583f93d8daaaa9e851b91ae1e32accb96ce5081a18a2d87c"
        scheduler = "K_EULER_ANCESTRAL"
        
    output = client.run(
        image_model,
        input={
            "width": data.width,
            "height": data.height,
            "prompt": data.prompt,
            "scheduler": scheduler,
            "num_outputs": 1,
            "guidance_scale": data.guidance_scale,
            "apply_watermark": False,
            "negative_prompt": data.negative_prompt,
            "prompt_strength":  data.prompt_strength,
            "num_inference_steps": data.num_inference_steps
        }
    )
    
    if (len(output) == 0):
        return ""
    
    image_url = output[0]
    return WebImageToBase64(image_url)