import shutil
from pathlib import Path

import requests
from PIL import Image
import openai

from bereal_gpt.described_memory import DescribedMemory
from bereal_gpt.weird_image import WeirdImage


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


class AlternateReality(WeirdImage):
    def __init__(self, described_memory: DescribedMemory, style=None):
        self.described_memory = described_memory
        self.style = style

        self._directory = Path("alternate_reality") / style / str(self.memory_day())
        if not self._directory.exists():
            self._directory.mkdir(parents=True, exist_ok=True)

    @property
    def image_path(self):
        return self._directory.with_suffix(".png")

    def primary_image(self):
        return _generate_image(
            f"A photo containing {self.described_memory.primary_description()}. {self.style}",
            self._directory / "alternate_primary.png",
        )

    def secondary_image(self):
        return _generate_image(
            f"A photo containing {self.described_memory.secondary_description()}. The photo is taken as a selfie. {self.style}",
            self._directory / "alternate_secondary.png",
            size="256x256",
        )

    @classmethod
    def _from_directory(cls, directory, style=None):
        return [cls(memory, style=style) for memory in DescribedMemory.from_directory(directory)]

    def memory_day(self):
        return self.described_memory.memory.memory_day()
