from pathlib import Path

from bereal_gpt.memories import Memory
from bereal_gpt.describe import describe

memories = Memory.from_directory(Path(__file__).parent / "memories")
for memory in memories[-10:]:
    print(memory.memory_day(), describe([memory.primary_image()]))
