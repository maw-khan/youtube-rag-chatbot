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
# VIDEO TITLE
# =========================

def extract_video_title(url):

    try:

        video_id = extract_video_id(url)

        return f"YouTube Video ({video_id})"

    except:

        return "Unknown Video"


# =========================
# THUMBNAIL URL
# =========================

def get_thumbnail_url(video_url):

    video_id = extract_video_id(video_url)

    return (
        f"https://img.youtube.com/vi/"
        f"{video_id}/0.jpg"
    )


# =========================
# FETCH TRANSCRIPT
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

        api = YouTubeTranscriptApi()

        fetched_transcript = api.fetch(
            video_id
        )

        transcript_data = []

        for item in fetched_transcript:

            transcript_data.append(
                {
                    "text": item.text,
                    "start": item.start
                }
            )

        return transcript_data

    except Exception as e:

        raise Exception(
            f"Transcript Error: {str(e)}"
        )
