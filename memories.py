from pathlib import Path
import json
import datetime as dt


class Memory:
    def __init__(self, path: Path):
        self.path = path

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
    def from_directory(cls, path: Path):
        info_paths = path.glob('**/info.json')
        return sorted(cls(p.parent) for p in info_paths)


if __name__ == "__main__":
    path = Path(__file__).parent / "memories"
    memories = Memory.from_directory(path)
    print(len(memories))
    print(memories[0])
    print(memories[-1])
