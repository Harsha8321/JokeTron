import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Step 1: Load a small and efficient model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Your sample jokes
jokes = [
    "Why did the computer get cold? Because it left its Windows open.",
    "Why don’t skeletons ever go to hospitals? They don’t have the guts.",
    "I'm afraid for the calendar. Its days are numbered.",
    "I used to be a banker, but I lost interest."
]

# Step 3: Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(jokes, convert_to_numpy=True)

# Step 4: Structure for pgvector
pgvector_records = [
    {
        "joke": joke,
        "embedding": emb.tolist()  # pgvector stores list of floats
    }
    for joke, emb in zip(jokes, embeddings)
]

# Step 5: Use relative path to save output
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)  # Create folder if it doesn't exist
output_file = output_dir / "joketron_pgvector_demo.pkl"

with open(output_file, "wb") as f:
    pickle.dump(pgvector_records, f)

print(f"✅ Embeddings saved to {output_file}")
