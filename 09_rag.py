from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

# from dotenv import load_dotenv
# load_dotenv()
load_dotenv()
pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

split_docs =  text_splitter.split_documents(documents=docs)

embedder = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Inject data in database
# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)
# print("Injection Done")

retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder
)

def find_relevant_chunks(query):
    relevant_chunks = retriever.similarity_search(query, k=4)
    # print("Relevant chunks : ", relevant_chunks)
    return relevant_chunks

query = input("> Enter user query :");
relevant_chunks     = find_relevant_chunks(query)
# print(relevant_chunks)

for chunk in relevant_chunks:
    print("Pages : ", chunk.metadata["page"])
    print("Content : ", chunk.page_content)

context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])
print("context :",context_text)


SYSTEM_PROMPT=f"""
You are an helpful AI assistant who responds based on the available context.

Context: {context_text}

Use available context and genererate a accurate output for given user query.

Rules: 
- You must take available context and generate output
- Output strictly be in JSON format.
"""

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]
)

print("🤖 : ", response.choices[0].message.content)