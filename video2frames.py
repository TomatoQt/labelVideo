"""
视频拆分为一帧一帧的，方便打标
"""
import cv2
import os
import shutil


class VideoFrame(object):
    _defalts = {
        "input_video_path": "E:/DATA/20210719/channel1-2021-07-19-10-08-04.h264",  # 选取视频
        "output_frames_path": "frames/",
        "start_time": 0,  # 起始时间(s)
        "end_time": 0,  # 结束时间(s)，默认全部截取
        "output_video_size": (1920, 1080)  # (宽,高)
    }

    def __init__(self, input_video_path=None):
        if input_video_path:
            self._defalts["input_video_path"] = input_video_path
        print(self._defalts["input_video_path"])
        self._defalts["output_frames_path"] = 'frames/' + \
                                              str(self._defalts["input_video_path"]).split('/')[-1].split('.')[0] + '/'
        self.__dict__.update(self._defalts)

    def split(self):
        # 重新运行程序自动清除上次的帧，防止不同视频切分有覆盖
        if os.path.exists(self.output_frames_path):
            shutil.rmtree(self.output_frames_path)
        os.mkdir(self.output_frames_path)

        start_time = self.start_time  # 起始时间(s)
        end_time = self.end_time  # 结束时间(s)

        videoCapture = cv2.VideoCapture(self.input_video_path)  # 视频文件打开
        fps_loadedVideo = videoCapture.get(cv2.CAP_PROP_FPS)
        videoCapture.set(cv2.CAP_PROP_POS_FRAMES, start_time * fps_loadedVideo + 1)  # 设置读取视频的起始帧

        # 输出导入视频的信息
        fps_loadedVideo = videoCapture.get(cv2.CAP_PROP_FPS)
        size_loadedVideo = (videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH), videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('FPS(Loaded):{}\nSIZE(Loaded):{}'.format(fps_loadedVideo, size_loadedVideo))
        print('\nSIZE(OUT):{}'.format(self.output_video_size))

        currentFrame = start_time * fps_loadedVideo + 1  # 起始帧

        while True:
            success, frame = videoCapture.read()
            if success == False:
                print('end')
                break
            if end_time != 0 and (currentFrame > end_time * fps_loadedVideo + 1):
                break
            (width, height) = self.output_video_size
            frame = frame[:, (width-height)//2-1:width-1-(width-height)//2]  # [height, width]
            cv2.imwrite(self.output_frames_path + str(self._defalts["input_video_path"]).split('/')[-1].split('.')[0]
                        + '_' + str(currentFrame).split('.')[0] + '.jpg', frame)
            currentFrame += 1

        print('finish.')


if __name__ == '__main__':
    video2frames = VideoFrame()
    video2frames.split()
