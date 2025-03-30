import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# OpenAI API 키 설정
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 질문 리스트
questions = [
    "의자가 꼭 앉는 용도로만 사용되어야 할까요? 의자를 전혀 다른 용도로 사용할 수 있는 방법을 최대한 많이 적어보세요.",
    "달걀, 구름, 시계 이 세 단어를 모두 포함한 짧은 이야기를 만들어 보세요.",
    "시간이 거꾸로 흐른다면 우리 생활은 어떻게 달라질까요?",
    "하루 동안 모든 전자기기가 사라진다면 어떻게 보낼 건가요?",
    "플라스틱 쓰레기를 줄일 기발한 방법은?"
]

# GPT 평가 함수
def gpt_score(question, answer):
    prompt = f"""
    질문: {question}
    답변: {answer}

    아래 기준으로 평가해 주세요:
    - 창의성 (10점 만점)
    - 구체성 (10점 만점)
    - 구성력 (10점 만점)

    각 점수와 총점, 간단한 피드백을 포함해 주세요.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT 오류: {str(e)}"

# Streamlit 앱
st.title("🧠 GPT 창의력 평가")
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.scores = []

if st.session_state.step < len(questions):
    q_idx = st.session_state.step
    st.subheader(f"질문 {q_idx + 1}")
    st.write(questions[q_idx])
    answer = st.text_area("✍️ 답변을 입력하세요", key=f"answer_{q_idx}")

    if st.button("다음"):
        st.session_state.answers.append((questions[q_idx], answer))
        with st.spinner("GPT가 평가 중입니다..."):
            score = gpt_score(questions[q_idx], answer)
        st.session_state.scores.append(score)
        st.session_state.step += 1
        st.rerun()
else:
    st.success("🎉 모든 질문이 완료되었습니다!")
    for i, (q, a) in enumerate(st.session_state.answers):
        st.markdown(f"### 질문 {i+1}: {q}")
        st.markdown(f"**답변:** {a}")
        st.markdown(f"**GPT 평가:**\n{st.session_state.scores[i]}")
