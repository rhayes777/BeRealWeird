from pathlib import Path

from bereal_gpt.memories import Memory
from bereal_gpt.described_memory import DescribedMemory

memories = Memory.from_directory(Path(__file__).parent / "memories")
for memory in memories[:10]:
    print(DescribedMemory(memory).primary_description())
