import base64
import json
from typing import cast
from fastapi import APIRouter
from datetime import datetime, timedelta, timezone
from app.api.dto.video_url import VideoURL
from app.common.model.app_config import AppConfig
from jwt import algorithms, encode
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


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
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=120)
        exp_timestamp = int(expiration_time.timestamp())

        jwk_json = base64.b64decode(self.app_config.cloudflare_jwk).decode("utf-8")

        signing_key = cast(RSAPrivateKey, algorithms.RSAAlgorithm.from_jwk(jwk_json))

        jwk_dict = json.loads(jwk_json)

        kid = jwk_dict.get("kid")

        headers = {"kid": kid, "alg": "RS256"}
        payload = {
            "sub": demo_video_id,
            "kid": kid,
            "exp": exp_timestamp,
        }

        signed_token = encode(payload, signing_key, algorithm="RS256", headers=headers)

        video_url = f"https://customer-{self.app_config.customer_id}.cloudflarestream.com/{signed_token}/manifest/video.m3u8"

        return VideoURL(video_url=video_url, expires_at=expiration_time)
