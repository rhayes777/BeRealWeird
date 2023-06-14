from abc import abstractmethod, ABC

from PIL import Image


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
