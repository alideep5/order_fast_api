import base64
from fastapi import APIRouter
from datetime import datetime, timedelta, timezone
import jwt
from app.api.dto.video_url import VideoURL
from app.common.model.app_config import AppConfig


class FileController(APIRouter):
    def __init__(self, app_config: AppConfig, prefix: str = "/file"):
        super().__init__(prefix=prefix, tags=["File"])

        self.app_config = app_config

        self.add_api_route(
            path="/get-demo-video-url",
            methods=["POST"],
            endpoint=self._get_demo_video_url,
            summary="Get demo video URL",
            description="Endpoint to get the URL of the demo video.",
        )

    async def _get_demo_video_url(self) -> VideoURL:
        demo_video_id = "a7054106fa1206c7c10e493bf47f3160"

        CLOUDFLARE_SIGNING_KEY = base64.b64decode(
            self.app_config.cloudflare_pem.encode()
        ).decode()

        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=120)
        exp_timestamp = int(expiration_time.timestamp())

        payload = {
            "sub": demo_video_id,
            "exp": exp_timestamp,
        }

        signed_token = jwt.encode(payload, CLOUDFLARE_SIGNING_KEY, algorithm="RS256")

        video_url = f"https://customer-{self.app_config.customer_id}.cloudflarestream.com/{demo_video_id}/manifest/video.m3u8?token={signed_token}"

        return VideoURL(video_url=video_url, expires_at=expiration_time)
