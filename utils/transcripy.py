import re

from youtube_transcript_api import (
    YouTubeTranscriptApi
)


# =========================
# EXTRACT VIDEO ID
# =========================

def extract_video_id(url):

    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"

    match = re.search(pattern, url)

    if match:

        return match.group(1)

    return None


# =========================
# GET TRANSCRIPT
# =========================

def get_video_transcript(video_url):

    try:

        video_id = extract_video_id(
            video_url
        )

        if not video_id:

            raise Exception(
                "Invalid YouTube URL"
            )

        transcript = (
            YouTubeTranscriptApi
            .get_transcript(video_id)
        )

        full_text = ""

        for item in transcript:

            full_text += (
                item["text"] + " "
            )

        return full_text

    except Exception as e:

        raise Exception(
            f"Transcript error: {str(e)}"
        )
