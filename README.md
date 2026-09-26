# 카페 AI 챗봇 (RAG 기반)

카페 FAQ 정보를 바탕으로 손님 질문에 자동으로 답변하는 챗봇입니다.
RAG(Retrieval-Augmented Generation) 구조로, 질문과 가장 관련 있는 카페 정보를 찾아서
그 내용을 참고해 자연스러운 답변을 만들어냅니다.

## 1. 준비물

- Python 3.9 이상
- OpenAI API 키 (https://platform.openai.com 에서 발급)

## 2. 설치

```bash
cd cafe_chatbot
pip install -r requirements.txt
```

## 3. API 키 설정

터미널에서 아래처럼 환경변수로 설정합니다.

**Mac/Linux**
```bash
export OPENAI_API_KEY="sk-여러분의-키"
```

**Windows (PowerShell)**
```powershell
$env:OPENAI_API_KEY="sk-여러분의-키"
```

## 4. 실행

```bash
uvicorn main:app --reload
```

실행 후 브라우저에서 http://127.0.0.1:8000 접속하면 채팅 화면이 나옵니다.

## 5. 카페 정보 수정하기

`data/cafe_faq.json` 파일을 열어서, 실제 카페의 영업시간·메뉴·자주 묻는 질문으로
question/answer 내용을 바꿔주시면 됩니다. category는 자유롭게 추가/수정 가능합니다.

예시:
```json
{
  "category": "메뉴/주문",
  "question": "아메리카노 가격이 얼마인가요?",
  "answer": "아메리카노는 4,500원입니다."
}
```

FAQ를 추가/수정한 뒤에는 서버를 껐다가 다시 켜주세요 (임베딩을 새로 만들어야 합니다).

## 6. 협업 시 역할 분담 예시

- **AI/백엔드 담당**: rag_engine.py, main.py (RAG 로직, API 서버)
- **프론트엔드/연동 담당**: static/index.html (채팅 화면), 카카오톡 채널 연동 작업

## 7. 다음 단계 (선택)

- 카카오톡 채널과 연동하려면 카카오 i 오픈빌더 또는 카카오톡 채널 API 문서를 참고해
  `/chat` 엔드포인트를 카카오 스킬 서버 형식에 맞게 응답하도록 수정하면 됩니다.
- 배포는 Railway, Render 등 무료/저가 호스팅에 올리면 외부에서도 접속 가능한 URL이 생깁니다.
