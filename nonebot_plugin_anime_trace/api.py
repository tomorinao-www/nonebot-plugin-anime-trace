from base64 import b64encode
from io import BytesIO
from PIL import Image
from naotool import AutoCloseAsyncClient
from .model import AnimeTraceResult


async def search(
    base_img: Image.Image, model: str, ai_detect: int = 0
) -> AnimeTraceResult:
    url = "https://api.animetrace.com/v1/search"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
        ),
    }
    bio = BytesIO()
    base_img.save(bio, format="JPEG")
    img_b64 = b64encode(bio.getvalue()).decode()
    data = {
        "is_multi": 1,
        "model": model,
        "ai_detect": ai_detect,
        "base64": img_b64,
    }
    async with AutoCloseAsyncClient() as client:
        res = await client.post(
            url=url,
            headers=headers,
            data=data,
            timeout=30,
        )
        return AnimeTraceResult.parse_raw(res.content)
