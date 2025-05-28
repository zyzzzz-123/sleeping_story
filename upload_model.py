import requests

API_KEY = "64a699198245430c987e4bfaa0b884a0"  # 替换为你的 Fish Audio API Key

response = requests.post(
    "https://api.fish.audio/model",
    files=[
        ("voices", open("input.m4a", "rb")),
    ],
    data=[
        ("visibility", "private"),
        ("type", "tts"),
        ("title", "Demo"),
        ("train_mode", "fast"),
        ("enhance_audio_quality", "true"),
    ],
    headers={
        "Authorization": f"Bearer {API_KEY}",
    },
)

print(response.json()) 