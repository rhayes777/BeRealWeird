from pathlib import Path
from llama_index import Document, ListIndex

from bereal_gpt.described_memory import DescribedMemory

directory = Path(__file__).parent

memories = DescribedMemory.from_directory(directory / "memories")

documents = []
for memory in memories:
    date = str(memory.memory.memory_day())
    documents.append(
        Document(
            memory.primary_description(),
            extra_info={
                'photo_type': 'Normal',
                'date': date,
                'description': 'The description of an image I took using my phone.',
            }
        ),
    )

index = ListIndex.from_documents(documents)

query_engine = index.as_query_engine(
    response_mode="tree_summarize"
)
response = query_engine.query("What was I most often?")
print(response)
