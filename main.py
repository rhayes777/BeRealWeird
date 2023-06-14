from pathlib import Path

from bereal_gpt.described_memory import DescribedMemory
from bereal_gpt.summarize import get_index, make_documents

directory = Path(__file__).parent

memories = DescribedMemory.from_directory(directory / "memories")

engine = get_index(make_documents(memories)).as_query_engine()

print(engine.query("What was I doing on the first of January?"))
