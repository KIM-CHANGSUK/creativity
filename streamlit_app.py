import streamlit as st
import pandas as pd
import os
import openai

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# 질문 리스트
questions = [
    "의자가 꼭 앉는 용도로만 사용되어야 할까요? 의자를 전혀 다른 용도로 사용할 수 있는 방법을 최대한 많이 적어보세요.",
    "달걀, 구름, 시계 이 세 단어를 모두 포함한 짧은 이야기를 만들어 보세요.",
    "시간이 거꾸로 흐른다면 우리 생활은 어떻게 달라질까요? 가정에 기반한 아이디어를 자유롭게 제시해보세요.",
    "하루 동안 모든 전자기기가 사라진다면, 당신은 어떤 방법으로 하루를 보낼 건가요?",
    "환경 문제(예: 플라스틱 쓰레기)를 해결할 수 있는 기발한 방법을 생각해보세요. 현실적 적용이 가능할수록 좋아요."
]

# GPT 평가 함수
def gpt_score(question, answer):
    prompt = f"""
    질문: {question}
    답변: {answer}

    이 답변의 창의성을 다음 기준에 따라 평가해 주세요:
    - 창의성 (10점 만점): 새롭고 독창적인가?
    - 구체성 (10점 만점): 구체적으로 설명했는가?
    - 구성력 (10점 만점): 논리적으로 연결되었는가?

    각 항목 점수와 총점, 간단한 피드백을 포함해 주세요.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT 오류: {str(e)}"

# Streamlit 앱 UI
st.set_page_config(page_title="GPT 창의력 평가", layout="centered")
st.title("🧠 GPT 기반 창의력 검사")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.scores = []

if st.session_state.step < len(questions):
    q_idx = st.session_state.step
    st.subheader(f"질문 {q_idx + 1}/{len(questions)}")
    st.write(questions[q_idx])

    answer = st.text_area("✍️ 답변을 입력하세요:", key=f"answer_{q_idx}")

    if st.button("다음 질문"):
        st.session_state.answers.append((questions[q_idx], answer))
        with st.spinner("GPT가 평가 중입니다..."):
            result = gpt_score(questions[q_idx], answer)
        st.session_state.scores.append(result)
        st.session_state.step += 1
        st.rerun()
else:
    st.success("🎉 모든 질문이 완료되었습니다! 결과를 확인하세요.")
    for i, (q, a) in enumerate(st.session_state.answers):
        st.markdown(f"### 질문 {i+1}: {q}")
        st.markdown(f"**답변:** {a}")
        st.markdown(f"**GPT 평가:**\n{st.session_state.scores[i]}")

    df = pd.DataFrame({
        "질문": [q for q, a in st.session_state.answers],
        "답변": [a for q, a in st.session_state.answers],
        "GPT 평가": st.session_state.scores
    })

    st.download_button(
        label="📥 결과 다운로드",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="창의력_검사_결과.csv",
        mime="text/csv"
    )
