import calendar
from collections import defaultdict
from pathlib import Path

import openai

from bereal_gpt.described_memory import DescribedMemory


months = defaultdict(list)
for memory in DescribedMemory.from_directory(Path(__file__).parent.parent / "memories"):
    months[calendar.month_name[memory.memory.memory_day().month]].append(memory)


all_summaries = []


for month, memories in months.items():
    print(month + ":")
    string = "\n".join(memory.primary_description() for memory in memories)

    result = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Here is a list of things that I did in {month}:\n\n{string}\n\n Here is a short poetic summary of what I did:\n\n",
        max_tokens=2048,
    )
    text = result["choices"][0]["text"]
    print(text + "\n")
    all_summaries.append(text)


string = "\n".join(all_summaries)

print("Year:")

result = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Here is a list of summaries describing what I did each month:\n\n{string}\n\n Here is a short poem describing what I did through the year:\n\n",
)
