import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.prompts import PromptTemplate
from qdrant_client import QdrantClient

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

qdrant = QdrantClient(host="localhost", port=6333)

embedding = OpenAIEmbeddings(model="text-embedding-3-small")

collection_name = "ktm-faq"
vectorstore = QdrantVectorStore(
    client=qdrant,
    collection_name=collection_name,
    embedding=embedding
)

llm = ChatOpenAI(model="gpt-3.5-turbo")
custom_prompt = PromptTemplate.from_template("""
당신은 KT 고객 FAQ 비서입니다.
아래의 문서 내용을 기반으로 질문에 대답하세요.

만약 관련된 정보가 문서 안에 전혀 없거나 불확실하다면,
반드시 다음과 같이 답변하세요:

"안녕하세요! 질문을 다시 해주세요."

=========
{context}
=========
질문: {question}
답변:
""")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": custom_prompt}
)


question = "외계인이 되고싶어"

result = qa_chain.invoke({"query": question})

print("\n🟢 답변:")
print(result["result"])