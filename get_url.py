
from  utils  import  die

import re
import youtube_dl

def get_url(video_url: str, quality = 1080) -> str:
    '''
    turn a url into one that cv2 can use
    '''
    with youtube_dl.YoutubeDL({'forceurl': True}) as yt:
        info = yt.extract_info(video_url, download = False)

    urls = []

    # get qualities lower than or equal to given quality
    for item in info['formats']:
        url = item['url']

        format_note = item.get('format_note', None)
        if format_note not in (None, 'tiny'):
            video_quality = int(format_note[:-1])    # get rid of last 'p'
            if video_quality <= quality:
                urls.append((video_quality, url))
        else:
            '''
            extract width and height
            example
                1920x1080
                2560x1440
                3840x2160
            '''
            dimentions = re.findall('\d+x\d+', item['format'])
            if not dimentions:
                continue

            width, height = dimentions[0].split('x')
            height = int(height)
            if height <= quality:
                urls.append((height, url))

    try:
        (_, url) = max(urls, key = lambda x: x[0], default = None)
        return url

    except TypeError:
        die(f'No usable formats found under {quality}p')

