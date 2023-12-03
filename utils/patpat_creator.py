
# Credit and thanks to @mintpixels and @biellsilva on the discord.py discord for the orginal
# and rewrite of this 

import aiohttp

from PIL import Image
from PIL.Image import Image as IMG
from typing import Any, Union
from io import BytesIO
import os
from .gif_converter import TransparentAnimatedGifConverter


class PatPatCreator:
    def __init__(self, image_url: str) -> None:
        self.image_url = image_url
        self.max_frames = 10
        self.resolution = (150, 150)
        self.frames: list[IMG] = []

    async def create_gif(self):
        img_bytes = await self.__get_image_bytes()

        base = Image.open(img_bytes).convert('RGBA').resize(self.resolution)

        for i in range(self.max_frames):
            squeeze = i if i < self.max_frames / 2 else self.max_frames - i
            width = 0.8 + squeeze * 0.02
            height = 0.8 - squeeze * 0.05
            offsetX = (1 - width) * 0.5 + 0.1
            offsetY = (1 - height) - 0.08

            canvas = Image.new('RGBA', size=self.resolution, color=(0, 0, 0, 0))
            canvas.paste(base.resize((round(width * self.resolution[0]), round(height * self.resolution[1]))), 
                                     (round(offsetX * self.resolution[0]), round(offsetY * self.resolution[1])))
            pat_hand = Image.open(f'./assets/pat_hand/pet{i}.gif').convert('RGBA').resize(self.resolution)

            canvas.paste(pat_hand, mask=pat_hand)
            self.frames.append(canvas)

        gif_image, save_kwargs = await self.__animate_gif(self.frames)

        buffer = BytesIO()
        gif_image.save(buffer, **save_kwargs)
        buffer.seek(0)

        return buffer
        
    
    async def __animate_gif(self, images: list[IMG], durations: Union[int, list[int]] = 20) -> tuple[IMG, dict[str, Any]]:
        save_kwargs: dict[str, Any] = {}
        new_images: list[IMG] = []

        for frame in images:
            thumbnail = frame.copy() 
            thumbnail_rgba = thumbnail.convert(mode='RGBA')
            thumbnail_rgba.thumbnail(size=frame.size, reducing_gap=3.0)
            converter = TransparentAnimatedGifConverter(img_rgba=thumbnail_rgba)
            thumbnail_p = converter.process() 
            new_images.append(thumbnail_p)

        output_image = new_images[0]
        save_kwargs.update(
            format='GIF',
            save_all=True,
            optimize=False,
            append_images=new_images[1:],
            duration=durations,
            disposal=2,  # Other disposals don't work
            loop=0)
        
        return output_image, save_kwargs
        

    async def __get_image_bytes(self):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=self.image_url) as res:

                if res.status != 200:
                    raise FileNotFoundError(res.status, res.url)
                
                return BytesIO(await res.read())