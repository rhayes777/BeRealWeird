from pathlib import Path

from llama_index import ListIndex
from llama_index.indices.response import ResponseMode
from llama_index.query_engine import RetrieverQueryEngine

from bereal_gpt.described_memory import DescribedMemory
from bereal_gpt.summarize import get_index, make_documents

directory = Path(__file__).parent

memories = DescribedMemory.from_directory(directory / "memories")

for memory in memories:
    print(f"{memory.memory.memory_day()}: {memory.primary_description()}")

index = get_index(make_documents(memories), Type=ListIndex)

retriever = index.as_retriever()
engine = RetrieverQueryEngine.from_args(retriever, response_mode=ResponseMode.TREE_SUMMARIZE)

print(engine.query("What was I doing during January?"))
