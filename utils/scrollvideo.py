"""module with functions to make text-scroll videos"""
import os
from math import ceil
from typing import NoReturn
import ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageColor


# defaults constants
RESOLUTION = (100, 100)
FPS: int = 25
DURATION: int = 3
TEXT: str = 'LOREM IPSUM'
FONT: ImageFont = ImageFont.truetype('Futura', RESOLUTION[1])
TEXT_COLOR: ImageColor = 'black'
BG_COLOR: ImageColor = 'white'


def scale_to_height(image: Image,
                    new_h: int
                    ) -> Image:
    """return scaled to height PIL.Image"""
    image_w, image_h = image.size
    scale_modifer = new_h / image_h
    return image.resize((int(image_w * scale_modifer), new_h))


def text_image(text: str = TEXT,
               font: ImageFont = FONT,
               color: ImageColor = TEXT_COLOR
               ) -> Image:
    """return transparent PIL.Image with text"""

    resolution = ceil(font.getlength(text)), font.size
    text_position = (resolution[0] // 2, resolution[1] // 2)
    image = Image.new("RGBA", resolution)
    draw = ImageDraw.Draw(image)
    draw.text(text_position,
              text, fill=color, anchor='mm',
              font=font)
    return image


def clip_image(image: Image,
               bg_color: ImageColor = BG_COLOR,
               resolution: tuple[int, int] = RESOLUTION,
               duration: int = DURATION,
               fps: int = FPS
               )-> Image:
    """return PIL.Image from PIL.Image, color and video settings 
    add colored background 
    and scale to height of video 
    and width scaled to proportional of frames"""

    scaled_image = scale_to_height(image, RESOLUTION[1])
    clip_h = resolution[1]
    scaled_image_h, _ = scaled_image.size
    frames = duration*fps
    clip_in_frames = ceil((scaled_image_h + resolution[0]) / frames)
    clip_w = clip_in_frames * frames + resolution[0]

    clip = Image.new("RGBA", (clip_w, clip_h), bg_color)
    image_start_x = (clip_w - ceil(scaled_image_h) + 1) // 2
    clip.alpha_composite(scaled_image, (image_start_x, 0))
    return clip


def save_scroll_video(clip: Image,
                      resolution: tuple[int, int],
                      duration: int,
                      fps: int,
                      output_path: str = 'video',
                      tmp_path: str = 'tmp',
                      name: str = 'video'
                      ) -> NoReturn:
    """save video clip from PIL.Image scrolled right to left"""

    frames = duration*fps
    clip_w = clip.size[0]
    scroll_speed = (clip_w - resolution[0]) // frames

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    clip.save(f'{tmp_path}/text_clip.png')
    (
        ffmpeg
        .input(f'{tmp_path}/text_clip.png',
               y=None,
               loop=1,
               t=DURATION)
        .output(f'{output_path}/{name}.mp4',
                filter_complex=f"""color=white:
                s={resolution[0]}x{resolution[1]},
                fps=fps={FPS}[clip];
                [clip][0]overlay=
                x=-{scroll_speed}*n:
                y=0:
                shortest=1[video]""",
                map="[video]")
        .run()
    )

    os.remove(f'{tmp_path}/text_clip.png')
    if os.listdir(tmp_path) == []:
        os.rmdir(tmp_path)


if __name__ == "__main__":
    # save video vith scrolled right to left text use defaults
    save_scroll_video(clip_image(text_image()),
                      resolution=RESOLUTION,
                      duration=DURATION,
                      fps=FPS)
