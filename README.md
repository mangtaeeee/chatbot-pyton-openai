이 프로젝트는 OpenAI, LangChain, Qdrant를 활용하여 파일에 기반한 질문 응답 시스템을 구현합니다.

## 🚀 구성 요소

- **LangChain**: RAG 체인 구성
- **Qdrant**: 벡터 검색 데이터베이스
- **OpenAI**: 임베딩 및 GPT 응답 생성
- **Pandas**: 엑셀 문서 처리
- **dotenv**: 환경 변수 관리

## ⚙️ 설치 및 실행

### 1. Poetry 환경 설정

```bash
poetry install

.env 파일 생성 후 다음 추가:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

2. Qdrant 실행 (로컬)

docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

3. 벡터 삽입 (엑셀 → Qdrant)

poetry run python src/my_ai_project/embed_excel.py

4. 질문 실행

poetry run python src/my_ai_project/ask_question.py

FAQ에 없는 질문 시 응답:

안녕하세요! 질문을 다시 해주세요.

📁 파일 구조 예시

my-ai-project/
├── .env
├── pyproject.toml
└── src/
    └── my_ai_project/
        ├── embed_excel.py
        └── ask_question.py



⸻
