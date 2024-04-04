# PromptEngine

Results:
https://docs.google.com/spreadsheets/d/15Lf2b-Bs8c9aoUAyryrQhZN9v7L3LBBt-zKHdXXAbBs/edit?usp=sharing 

```
curl --request POST \
  --url https://promptengine-production.up.railway.app/generate \
  --data '{
    "prompt": "bush",
    "negative_prompt": "nsfw",
    "model": "playground",
    "num_inference_steps": 30,
    "guidance_scale": 6
}'
```
