from datetime import datetime
from pydantic import BaseModel


class VideoURL(BaseModel):
    video_url: str
    expires_at: datetime
