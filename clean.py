from datasets import Dataset
import re

# Load your raw lines
with open("./training_data.txt", "r", encoding="utf-8") as f:
    raw_lines = f.readlines()

# Convert to LLaMA2-style format
converted = []
for line in raw_lines:
    match = re.match(r"###Human:\s*(.*?)\s*###Assistant:\s*(.*)", line.strip())
    if match:
        instruction = match.group(1).strip()
        response = match.group(2).strip()
        formatted = f"<s>[INST] {instruction} [/INST] {response} </s>"
        converted.append({"text": formatted})

# Create Hugging Face dataset
dataset = Dataset.from_list(converted)

# Save to disk
dataset.save_to_disk("woxsen_dataset_llama2")
print("✅ Dataset converted and saved to 'woxsen_dataset_llama2'")
print(dataset[])