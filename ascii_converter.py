
from  PIL              import  Image
from  utils            import  die
from  convert          import  convert
from  functools        import  partial
from  multiprocessing  import  Pool

import cv2

import os
import bz2
import time


# `~` isn't used in frames
_EMPTY_FRAME = '~~EMPTY~FRAME~~'


def convert_image_to_ascii(image_path: str, size: int, light: bool) -> str:
    '''
    covert a given image to ascii with the given size
    '''
    image = Image.open(image_path)
    return convert(image, size, light)


def play_video_as_ascii(video_path: str, size: int, light: bool):
    '''
    play video as it's being converted
    '''
    video = cv2.VideoCapture(video_path)

    while True:
        ret, frame = video.read()
        if not ret:
            os.system('clear')
            return

        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv2_image)
        try:
            ascii_frame = convert(pil_image, size, light)
            os.system('clear')
            print(ascii_frame)

        except KeyboardInterrupt:
            os.system('clear')
            return

        except:      # black screen causes an index out of range error
            pass



def convert_video_to_ascii(video_path: str, size: int, light: bool) -> str:
    '''
    convert video to ascii
    output should be in a format that we can write to file
    '''
    video = cv2.VideoCapture(video_path)
    FPS = video.get(cv2.CAP_PROP_FPS)

    # print(f'coverting {video_path}\nplease wait')

    _convert = partial(_convert_frame, size = size, light = light)

    done = 0
    done_frames = ''
    try:
        for frames in _chunk_frames(video, int(FPS)):
            with Pool(8) as pool:
                ascii_frames = pool.map(_convert, frames)
                done += len(ascii_frames)
                print(f'frames done: {done}', end = '\r')

                done_frames += '\n\n'.join(ascii_frames) + '\n\n'

        print('\ndone')

    except KeyboardInterrupt:
        die('\naborted while converting video')

    return str(FPS) + '\n\n' + done_frames


def play_ascii_video_from_file(file_path: str):
    '''
    play video from the given file (that we created) in the given fps
    '''
    try:
        with bz2.open(file_path, 'rb') as file:
            [fps, *frames] = file.read().decode().split('\n\n')
            fps = float(fps)

        for frame in frames:
            os.system('clear')

            if frame == _EMPTY_FRAME:
                print()
            else:
                print(frame)

            time.sleep(1 / fps)

        os.system('clear')

    except KeyboardInterrupt:
        os.system('clear')
        return

    except FileNotFoundError:
        die(f'invalid file path: {file_path}')




def _chunk_frames(video, number_of_frames):
    '''
    gets chunks of n frames from videos
    '''
    done = False
    while not done:
        frames = []
        for _ in range(number_of_frames):
            ret, frame = video.read()
            if not ret:
                done = True
                break

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img)
            frames.append(pil_image)

        yield frames


def _convert_frame(frame: None, size: int, light: bool):
    '''
    covert a given frame to ascii

    only to be used when writing video to file
    '''
    try:
        return convert(frame, size, light)

    except:      # black screen causes an index out of range error
        return _EMPTY_FRAME

