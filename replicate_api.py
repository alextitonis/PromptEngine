import random
import replicate
from generation_data import GenerationData
from utils import web_image_to_base64, get_text_until_first_dot_or_newline

def init_replicate(key: str):
    client = replicate.Client(key)
    return client

import random

def generate_text(client: replicate.Client, image_prompt: str) -> str:
    examples = [
        ("dog", "A shaggy, three-legged mutt lounging on a tattered armchair, its tongue lolling out as it dreams of chasing squirrels through sun-dappled glades."),
        ("dog", "A playful golden retriever bounds across a sun-drenched meadow, its fluffy tail wagging joyfully as it chases after a brightly colored frisbee, tongue hanging out in pure canine bliss."),
        ("a floating castle on a valley", "Adrift in a misty, verdant valley, a majestic castle hovers serenely, its spired turrets and buttressed walls suspended by ethereal magic, its shadow gliding across vibrant wildflower meadows and babbling brooks below."),
        ("a floating castle on a valley", "Amidst the rolling hills and lush forests of a picturesque valley, a magnificent castle seems to defy gravity, its towering spires and ancient stonework floating eerily above the ground, casting long shadows over the quaint village nestled below."),
        ("dragon", "A fearsome dragon, scales glittering like diamonds, unfurls its leathery wings as plumes of searing flames erupt from its maw, casting an ominous silhouette against the crimson sky of a smoldering, apocalyptic landscape."),
        ("dragon", "A majestic dragon soars through the skies above a medieval kingdom, its massive wings casting shadows over the villages below, its powerful tail lashing through the clouds as it exhales a burst of shimmering, ethereal mist."),
        ("underwater city", "Beneath the rippling surface of a turquoise sea, an ancient city lies preserved in crystalline perfection, its towering spires and sculptured facades teeming with kaleidoscopic schools of exotic fish darting through petrified streets and archways."),
        ("underwater city", "Deep beneath the waves of a vast, cerulean ocean, the crumbling ruins of a once-thriving underwater metropolis lie scattered across the seabed, its intricate architecture and towering monoliths now home to a myriad of vibrant marine life that drifts among the ancient structures."),
        ("robot", "A sleek, humanoid robot with gleaming metal limbs and a multifaceted visor surveys its surroundings, servomotors whirring as it processes vast streams of data in a stark, minimalist laboratory bathed in the eerie glow of holographic displays."),
        ("robot", "A towering, industrial robot arm whirs and clanks as it precisely welds components on an assembly line, its movements a choreographed dance of precision and power, sparks flying in the dim factory light as it crafts the machines that will shape the future."),
        ("a peaceful garden at sunset", "As the golden rays of the setting sun bathe a secluded garden in warm, gentle light, birds chirp melodies amid blossoming flowerbeds, a stone fountain trickles soothingly, and butterflies flit among the dappled shadows cast by a gnarled willow tree."),
        ("a peaceful garden at sunset", "In a hidden oasis tucked away from the bustling city, a serene Japanese garden basks in the soft, amber glow of the setting sun, its meticulously raked gravel paths winding among ancient bonsai trees and tranquil koi ponds, where lotus blossoms float serenely."),
        ("elephant", "A majestic elephant, its wrinkled skin adorned with intricate patterns of dust, raises its trunk in a trumpeting call, leading its herd across the vast, sun-baked savanna, dwarfed by the towering acacia trees silhouetted against the burnt orange horizon."),
        ("elephant", "A massive, tusked elephant emerges from the cool shadows of a dense jungle, its leathery skin adorned with vibrant painted patterns, carrying a richly adorned howdah on its broad back as it lumbers towards a sacred temple, guided by its mahout."),
        ("abandoned factory", "Amid a desolate wasteland of rusted machinery and crumbling concrete, an abandoned factory looms like a decaying behemoth, its shattered windows gaping like empty eye sockets, the eerie silence broken only by the creaking of twisted metal in the haunting wind."),
        ("abandoned factory", "Once a mighty industrial hub, the crumbling remains of an abandoned factory lie silent and forgotten, its towering smokestacks piercing the gloomy sky like decaying sentinels, while nature reclaims the overgrown grounds with vines and weeds creeping through shattered windows."),
        ("futuristic cityscape", "Towering spires of gleaming metal and glittering glass pierce the skyline of a futuristic cityscape, their sleek facades reflecting the kaleidoscopic neon lights that dance across the bustling streets below, where autonomous vehicles weave among holographic billboards and bustling pedestrians."),
        ("futuristic cityscape", "In the heart of a neon-drenched metropolis, soaring skyscrapers of crystalline glass and chrome reach towards the heavens, their facades alive with cascading holographic advertisements and gleaming skyways that crisscross the skyline, ferrying the city's inhabitants through a dazzling, cyberpunk future."),
        ("alien landscape", "Beneath the crimson glow of a binary star system, an otherworldly landscape unfolds, with twisted spires of crystalline rock erupting from seas of viscous, iridescent sludge, as bizarre, tentacled creatures slither across the alien terrain, their movements casting unsettling shadows in the bizarre, extraterrestrial twilight."),
        ("alien landscape", "On a distant, hostile world, an eerie, alien landscape stretches as far as the eye can see, with towering monoliths of unearthly geometries casting long shadows over undulating dunes of iridescent sand, while strange, amorphous lifeforms pulse and glide across the desolate vistas."),
        ("cosmic nebula", "Swirling clouds of vividly colored gas and dust spiral outward in a cosmic nebula, a kaleidoscope of reds, blues, and violets punctuated by the brilliant glare of newly formed stars, their light illuminating the vast, infinite expanse of the cosmos."),
        ("cosmic nebula", "In the depths of interstellar space, a vast, cosmic nebula unfurls like a vibrant, celestial canvas, with incandescent tendrils of ionized gas and dust coalescing into brilliant, swirling vortices that birth new stars, their radiant light piercing through the colorful nebulae."),
        ("a gigantic robot battling a dragon in a futuristic city", "Amidst the towering skyscrapers and neon-lit streets of a futuristic metropolis, a colossal robot clashes with a fearsome dragon, their titanic forms locked in combat as the robot's energy cannons blast searing beams of light, deflected by the dragon's impenetrable scales and retaliatory gouts of flame."),
        ("a gigantic robot battling a dragon in a futuristic city", "In the heart of a gleaming cyberpunk cityscape, a titanic mechanized warrior trades blows with an ancient, airborne drake, their apocalyptic battle raging through the neon-drenched streets as the robot unleashes a barrage of energy blasts, while the dragon retaliates with gouts of searing plasma."),
        ("a wizard casting a spell", "Within the confines of an ancient, mystical forest, a wizened sorcerer stands before a moss-covered stone altar, arcane runes etched into the ground glowing with eldritch energy as he raises a gnarled staff, chanting an incantation that summons swirling vortices of celestial power."),
        ("a wizard casting a spell", "Deep in the heart of an enchanted woodland, there is a bear watching him, waiting to attack"),
    ]
    random.shuffle(examples)

    base_prompt = """<INSTRUCTIONS>
You are an incredibly creative artist tasked with generating unique and diverse image prompts.
For each input, you must produce an original, detailed, and imaginative description that avoids repeating or closely resembling previous examples. 
Strive for maximum creativity and originality in your outputs, and avoid fixating on specific patterns or descriptions.
Make sure taht if the input is something realistic, then follows the reality standards.
Make sure that the focus of the description is the input ({image_prompt})!
</INSTRUCTIONS>

<EXAMPLES>
"""

    for input_text, example_output in examples:
        base_prompt += f"Input: {input_text}\nOutput: {example_output}\n\n"

    base_prompt += f"""</EXAMPLES>
Input: {image_prompt}
Output: """.replace("{image_prompt}", image_prompt)

    output = client.run(
        "mistralai/mixtral-8x7b-instruct-v0.1",
        input={
            "top_k": 150,
            "top_p": 0.98,
            "prompt": base_prompt,
            "temperature": 0.98,
            "max_new_tokens": 128,
            "prompt_template": "<s>[INST] {prompt} [/INST]",
            "presence_penalty": 0.8,
            "frequency_penalty": 0.8,
        }
    )
    improved_prompt = get_text_until_first_dot_or_newline("".join(output)).replace("*", "").strip()
    return improved_prompt

def generate_image_style(client: replicate.Client, image_prompt: str) -> str:
    base_prompt = """<INSTRUCTIONS>
Which one do you think would fit the best for this painting? {image_prompt}
Just select one of the styles below, without justifying it!
* Realistic
* Cartoon-like
* Hand drowning
* Gothic Dark Style
* Sci-Fy/Futuristic Style
* Pixel Art
* Water Colour
* Mosaic
* Oil Painting
</INSTRUCTIONS>
""".replace("{image_prompt}", image_prompt)
    
    output = client.run(
        "mistralai/mixtral-8x7b-instruct-v0.1",
        input={
            "top_k": 50,
            "top_p": 0.9,
            "prompt": base_prompt,
            "temperature": 0.6,
            "max_new_tokens": 64,
            "prompt_template": "<s>[INST] {prompt} [/INST] ",
            "presence_penalty": 0.1,
            "frequency_penalty": 0.1
        }
    )
    style = get_text_until_first_dot_or_newline("".join(output)).replace("*", "").strip()
    return style

    
def text_to_image(client: replicate.Client, data: GenerationData) -> str:
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
    return web_image_to_base64(image_url)