from datasets import load_from_disk

# ✅ Load your saved dataset from disk
dataset = load_from_disk("./woxsen_dataset_llama2")
print(dataset)

# ✅ Optional: Use only a sample to reduce training time
# dataset = dataset.select(range(1000))  # Uncomment to train on a subset
# print(f"Dataset size after sampling: {len(dataset)}")

# ✅ Inspect the dataset structure
print("\nDataset features:")
print(dataset.features)

print("\nFirst example:")
print(dataset[0])
