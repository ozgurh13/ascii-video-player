
# https://codereview.stackexchange.com/a/278577

from  PIL  import  Image
import numpy as np


CHARSET = (
    "@$B%8&WM#*oahkbdpqwm"
    "ZO0QLCJUYXzcvunxrjft"
    "/\|()1{}[]?-_+~<>i!l"
    "I;:,\"^`'. "
)


def resize(image: Image.Image, new_width: int = 500) -> Image.Image:
    width, height = image.size
    new_height = new_width * height / width / 2.5
    return image.resize((round(new_width), round(new_height)))


def pixel_to_ascii(pixels: np.ndarray, light_mode: bool = False) -> str:
    direction = 1 if light_mode else -1
    charset_str = CHARSET[::direction]
    charset = np.array(tuple(charset_str), dtype='U1')

    minp = pixels.min()
    maxp = pixels.max()
    scaled = (pixels - minp) / (maxp - minp) * (len(CHARSET) - 1)
    indices = np.around(scaled).astype(int)

    ascii_array = charset[indices]
    rows = ascii_array.view(f'U{pixels.shape[1]}')[:, 0]
    return '\n'.join(rows)


def convert(
    pil_image: Image.Image,
    new_width: int = 500,
    light_mode: bool = False
) -> str:
    greyscale_image = resize(pil_image.convert('F'), new_width)
    return pixel_to_ascii(np.array(greyscale_image), light_mode)

