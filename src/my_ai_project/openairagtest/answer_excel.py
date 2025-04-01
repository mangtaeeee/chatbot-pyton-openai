import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


embedding = OpenAIEmbeddings(model="text-embedding-3-small")
collection_name = "ktm-faq"
qdrant = QdrantClient(host="localhost", port=6333)

if not qdrant.collection_exists(collection_name):
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )
    print(f"✅ 컬렉션 '{collection_name}' 생성 완료")

excel_path = "/testdata.xlsx"
df = pd.read_excel(excel_path)

documents = []
for idx, row in df.iterrows():
    question = str(row.get("question", "")).strip()
    answer = str(row.get("answer", "")).strip()
    if not question or not answer:
        continue

    print(f"[{idx}] Q: {question} → A: {answer}")
    doc = Document(
        page_content=f"Q: {question}\nA: {answer}",
        metadata={
            "source": "ktm-faq",
            "row": idx,
            "question": question,
            "answer": answer
        }
    )
    documents.append(doc)


if documents:
    documents = [
        doc for doc in documents
        if doc.page_content and isinstance(doc.page_content, str)
    ]

    vectorstore = QdrantVectorStore(
        client=qdrant,
        collection_name="ktm-faq",
        embedding=embedding
    )

    # ✅ 문서 추가
    vectorstore.add_documents(documents)

    print(f"✅ Qdrant에 {len(documents)}개 문서 벡터 저장 완료!")
else:
    print("⚠️ 저장할 문서가 없습니다.")

results = qdrant.scroll(
    collection_name=collection_name,
    limit=5
)

print("\n📦 Qdrant에 저장된 문서 샘플:")
for i, point in enumerate(results[0]):
    print(f"\n🟡 [{i+1}] ID: {point.id}")
    print(point.payload)