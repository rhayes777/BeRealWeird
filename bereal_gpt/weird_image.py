from abc import abstractmethod, ABC

from PIL import Image


class ImageCollection:
    def __init__(self, images):
        self.images = images
        self._memory_day_map = {
            str(image.memory_day()): image
            for image in images
        }

    def __iter__(self):
        return iter(self.images)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        if isinstance(index, str):
            return self._memory_day_map[index]
        return self.images[index]


class WeirdImage(ABC):
    def image(self):
        path = self.image_path
        if path.exists():
            return Image.open(path)

        primary = self.primary_image()
        secondary = self.sub_image()
        border = 10
        primary.paste(secondary, (border, border))
        primary.save(path)
        return primary

    def sub_image(self):
        return self.secondary_image()

    @abstractmethod
    def primary_image(self):
        pass

    @abstractmethod
    def secondary_image(self):
        pass

    @property
    @abstractmethod
    def image_path(self):
        pass

    @classmethod
    @abstractmethod
    def _from_directory(cls, directory, **kwargs):
        pass

    @classmethod
    def from_directory(cls, directory, **kwargs):
        return ImageCollection(cls._from_directory(directory, **kwargs))

    @abstractmethod
    def memory_day(self):
        pass
