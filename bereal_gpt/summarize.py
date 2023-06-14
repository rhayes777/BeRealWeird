from pathlib import Path

from llama_index import Document, VectorStoreIndex, StorageContext, load_index_from_storage

index_directory = Path(__file__).parent.parent / "indexes"


def make_documents(memories):
    documents = []
    for memory in memories:
        date = str(memory.memory.memory_day())
        documents.append(
            Document(
                memory.primary_description(),
                extra_info={
                    'photo_type': 'Normal',
                    'date': date,
                    'description': f'The description of an image indicating something on {date}.',
                }
            ),
        )
    return documents


# noinspection PyPep8Naming
def index_path(Type):
    return index_directory / Type.__name__


# noinspection PyPep8Naming
def make_index(documents, Type=VectorStoreIndex):
    index = Type.from_documents(documents)
    index.storage_context.persist(str(index_path(Type)))


def load_index(Type):
    storage_context = StorageContext.from_defaults(persist_dir=str(index_path(Type)))
    return load_index_from_storage(storage_context=storage_context)


def get_index(documents, Type=VectorStoreIndex):
    if not index_path(Type).exists():
        make_index(documents, Type)

    return load_index(Type)
