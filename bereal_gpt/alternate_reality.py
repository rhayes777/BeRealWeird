import shutil
from pathlib import Path

import requests
from PIL import Image
import openai

from bereal_gpt.described_memory import DescribedMemory


def _generate_image(prompt: str, image_path: Path, size="1024x1024"):
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

    return Image.open(image_path)


class AlternateReality:
    def __init__(self, described_memory: DescribedMemory):
        self.described_memory = described_memory

    def primary_image(self):
        return _generate_image(
            self.described_memory.primary_description(),
            self.described_memory.memory.primary_path.with_name("alternate_primary.png"),
        )

    def secondary_image(self):
        return _generate_image(
            self.described_memory.secondary_description(),
            self.described_memory.memory.secondary_path.with_name("alternate_secondary.png"),
            size="256x256",
        )

    @classmethod
    def from_directory(cls, directory):
        return list(map(cls, DescribedMemory.from_directory(directory)))
