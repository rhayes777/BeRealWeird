from pathlib import Path
import json
import datetime as dt
from PIL import Image

from bereal_gpt.weird_image import WeirdImage


class Memory(WeirdImage):
    def __init__(self, path: Path):
        self.path = path

    def sub_image(self):
        image = self.secondary_image()
        new_size = (image.width // 4, image.height // 4)

        # Rescale the image
        image.thumbnail(new_size)
        return image

    @property
    def image_path(self):
        return self.path / 'combined.png'

    def primary_image(self):
        return Image.open(self.primary_path)

    def secondary_image(self):
        return Image.open(self.secondary_path)

    @property
    def primary_path(self):
        jpg_path = self.path / 'primary.jpg'
        if jpg_path.exists():
            return jpg_path
        return self.path / 'primary.webp'

    @property
    def secondary_path(self):
        jpg_path = self.path / 'secondary.jpg'
        if jpg_path.exists():
            return jpg_path
        return self.path / 'secondary.webp'

    @property
    def info_path(self):
        return self.path / 'info.json'

    def info_dict(self):
        with open(self.info_path, 'r') as f:
            return json.load(f)

    def memory_day(self):
        return dt.date.fromisoformat(self.info_dict()['memoryDay'])

    def __lt__(self, other):
        return self.memory_day() < other.memory_day()

    def __repr__(self):
        return f"Memory({self.memory_day()})"

    @classmethod
    def _from_directory(cls, path: Path, **kwargs):
        info_paths = path.glob('**/info.json')
        return sorted(cls(p.parent) for p in info_paths)
