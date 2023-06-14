import shutil
from pathlib import Path

import requests
from PIL import Image
import openai

from bereal_gpt.described_memory import DescribedMemory


def _generate_image(prompt: str, image_path: Path, size="1024x1024", ratio=(1.5 / 2)):
    if not image_path.exists():
        image = openai.Image.create(
            prompt=prompt,
            size=size,
        )
        url = image.data[0]["url"]

        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(image_path, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

    image = Image.open(image_path)
    width, height = image.size
    new_width = int(height * ratio)
    left = int((width - new_width) / 2)
    return image.crop((left, 0, left + new_width, height))


class AlternateReality:
    def __init__(self, described_memory: DescribedMemory):
        self.described_memory = described_memory

    def image(self):
        path = self.described_memory.memory.path / "alternate_reality.png"
        if path.exists():
            return Image.open(path)

        primary = self.primary_image()
        secondary = self.secondary_image()
        border = 10
        primary.paste(secondary, (border, border))
        primary.save(path)
        return primary

    def primary_image(self):
        return _generate_image(
            f"A photo containing {self.described_memory.primary_description()}",
            self.described_memory.memory.path / "alternate_primary.png",
        )

    def secondary_image(self):
        return _generate_image(
            f"A photo containing {self.described_memory.secondary_description()}. The photo is taken as a selfie.",
            self.described_memory.memory.path / "alternate_secondary.png",
            size="256x256",
        )

    @classmethod
    def from_directory(cls, directory):
        return list(map(cls, DescribedMemory.from_directory(directory)))
