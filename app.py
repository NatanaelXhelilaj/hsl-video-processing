from flask import Flask
from flask_restful import Api, Resource

import datetime
import os
import sys

import ffmpeg_streaming
from ffmpeg_streaming import Formats

app = Flask(__name__)
api = Api(app)


def monitor(ffmpeg, duration, time_, time_left, process):
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]" %
        (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
    )
    sys.stdout.flush()


class ProcessVideo(Resource):
    def get(self, token, videoName):
        if token != 'N7KTwCjYH4ZGwC4YSn3YXgxpj7x3FKj7kYTwt8EzH2ZnATUwqyUWxW5OHphO1rYJAq0pT7GJanadlA8O':
            return "Not allowed", 401

        video = ffmpeg_streaming.input(
            'http://192.168.0.177:3000/tempVideo/' + token + '/' + videoName)
        hls = video.hls(Formats.h264())
        hls.auto_generate_representations()
        videoNameNoExt = videoName.split('.')[0]

        try:
            hls.output(os.path.join(sys.path[1], videoNameNoExt, videoNameNoExt), monitor=monitor)
        except:
            return "Internal server error", 500

        return "videoName/" + token + '/' + videoName, 200


api.add_resource(ProcessVideo, '/videoProcessing/<token>/<videoName>')

if __name__ == '__main__':
    app.run()
