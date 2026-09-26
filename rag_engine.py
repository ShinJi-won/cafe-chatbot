"""
카페 챗봇 RAG 엔진
- FAQ 데이터를 임베딩해서 저장해두고,
- 사용자 질문이 오면 가장 관련 있는 FAQ를 찾아서(Retrieval)
- 그 내용을 참고해서 LLM이 자연스러운 답변을 생성(Generation)합니다.
"""

import json
import os
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "cafe_faq.json")


class CafeRAGBot:
    def __init__(self, data_path: str = DATA_PATH):
        with open(data_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)
        self.embeddings = None  # 서버 시작 시 build_index()로 채움

    def build_index(self):
        """모든 FAQ 질문을 임베딩해서 메모리에 저장 (서버 시작 시 1회 실행)"""
        questions = [item["question"] for item in self.faqs]
        response = client.embeddings.create(model=EMBED_MODEL, input=questions)
        self.embeddings = np.array([e.embedding for e in response.data])
        print(f"[RAG] {len(self.faqs)}개 FAQ 임베딩 완료")

    def _embed_query(self, text: str) -> np.ndarray:
        response = client.embeddings.create(model=EMBED_MODEL, input=[text])
        return np.array(response.data[0].embedding)

    def retrieve(self, query: str, top_k: int = 3):
        """질문과 가장 유사한 FAQ top_k개를 찾아서 반환"""
        if self.embeddings is None:
            self.build_index()

        query_vec = self._embed_query(query)

        # 코사인 유사도 계산
        norms = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec)
        sims = self.embeddings @ query_vec / norms

        top_indices = np.argsort(sims)[::-1][:top_k]
        return [self.faqs[i] for i in top_indices]

    def answer(self, query: str) -> str:
        """검색된 FAQ를 컨텍스트로 넣어서 LLM이 자연스러운 답변 생성"""
        relevant_faqs = self.retrieve(query)

        context = "\n".join(
            f"- Q: {item['question']}\n  A: {item['answer']}" for item in relevant_faqs
        )

        system_prompt = (
            "당신은 친절한 카페 안내 챗봇입니다. "
            "아래 제공된 카페 정보를 참고해서 손님의 질문에 자연스럽고 친절하게 답변하세요. "
            "정보에 없는 내용은 추측하지 말고, 매장에 직접 문의하도록 안내하세요.\n\n"
            f"[참고 정보]\n{context}"
        )

        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    # 터미널에서 바로 테스트해볼 수 있는 간단한 실행부
    bot = CafeRAGBot()
    bot.build_index()
    print("카페 챗봇 테스트 (종료하려면 'exit' 입력)")
    while True:
        q = input("\n손님: ")
        if q.lower() == "exit":
            break
        print("챗봇:", bot.answer(q))
