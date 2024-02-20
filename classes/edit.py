from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip,
    ColorClip,
)


class Edit:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = VideoFileClip(video_path)


def edit(self):
    pass
