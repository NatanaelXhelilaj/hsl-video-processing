import ffmpeg_streaming
from ffmpeg_streaming import Formats
import os
import sys
import datetime


def monitor(ffmpeg, duration, time_, time_left, process):
   per = round(time_ / duration * 100)
   sys.stdout.write(
       "\rTranscoding...(%s%%) %s left [%s%s]" %
       (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
   )
   sys.stdout.flush()


video = ffmpeg_streaming.input(
	#'https://mediapilot.io/tempVideo/N7KTwCjYH4ZGwC4YSn3YXgxpj7x3FKj7kYTwt8EzH2ZnATUwqyUWxW5OHphO1rYJAq0pT7GJanadlA8O/852522612ea58da8cdbf0148b200b9f2.mp4'
    'banana.mp4'
)
hls = video.hls(Formats.h264())
hls.auto_generate_representations()

hls.output(os.path.join(os.path.abspath('/'), 'spaces', 'hls-video-storage', 'banana2', 'banana2'), monitor=monitor)
