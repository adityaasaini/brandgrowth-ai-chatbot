# ============================================
# Libraries import kar rahe hain
# ============================================
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer

# ============================================
# STEP 1 — website_data.txt file padho
# ============================================
print("Data file padh rahe hain...")

with open("website_data.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

print(f"Total text: {len(full_text)} characters")

# ============================================
# STEP 2 — Text ko chunks mein todo
# Kyun? Poora text ek saath nahi de sakte AI ko
# Chhote pieces mein denge — accurate answers milenge
# ============================================
print("Chunks bana rahe hain...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,    # har chunk 500 characters ka
    chunk_overlap=50   # thoda overlap — context na toote
)

chunks = splitter.split_text(full_text)

print(f"Total chunks bane: {len(chunks)}")

# ============================================
# STEP 3 — Sentence Transformer model load karo
# Yeh text ko numbers (vectors) mein convert karega
# Taaki similar content dhundh sakein
# ============================================
print("AI model load ho raha hai — thoda wait karo...")

model = SentenceTransformer('all-MiniLM-L6-v2')

# ============================================
# STEP 4 — Har chunk ko vector mein convert karo
# ============================================
print("Vectors bana rahe hain...")

vectors = model.encode(chunks)

print(f"Vectors bane: {len(vectors)}")

# ============================================
# STEP 5 — ChromaDB mein store karo
# Yeh hamara vector database hai
# Yahan se relevant chunks dhundhe jaayenge
# ============================================
print("ChromaDB mein save kar rahe hain...")

# Local ChromaDB client banao
client = chromadb.PersistentClient(path="./chroma_db")

# Pehle se collection hai toh delete karo
try:
    client.delete_collection("doctor_website")
except:
    pass

# Naya collection banao
collection = client.create_collection("doctor_website")

# Saare chunks aur vectors store karo
collection.add(
    documents=chunks,
    embeddings=vectors.tolist(),
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print("=" * 40)
print("SUCCESS! Sab kuch ChromaDB mein save ho gaya!")
print(f"Total chunks stored: {len(chunks)}")
print("=" * 40)