import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import PGVector
from langchain.document_loaders import PyPDFLoader

# Setzen Sie Ihren OpenAI API-Key
os.environ["OPENAI_API_KEY"] = "Ihr-OpenAI-API-Key"

# Verbindungsstring für die Postgres-Datenbank
CONNECTION_STRING = "postgresql://user:password@localhost:5432/vectordb"

# PDF-Dokumente laden
pdf_path = "path/to/your/document.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Verbesserten Text Splitter verwenden
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""],
)
docs = text_splitter.split_documents(documents)

# Embeddings erstellen und in den Vectorstore speichern
embeddings = OpenAIEmbeddings()
db = PGVector.from_documents(
    docs,
    embeddings,
    connection_string=CONNECTION_STRING,
    collection_name="demo_collection",
)

# Ähnlichkeitssuche durchführen
query = "Ihre Suchanfrage hier"
results = db.similarity_search(query)

print(f"Top {len(results)} ähnlichste Dokumente für die Anfrage '{query}':")
for doc in results:
    print(f"Inhalt: {doc.page_content[:100]}...")
    print(f"Metadaten: {doc.metadata}")
    print("---")
