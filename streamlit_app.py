import streamlit as st
import pandas as pd

# 질문 리스트
questions = [
    "의자가 꼭 앉는 용도로만 사용되어야 할까요? 의자를 전혀 다른 용도로 사용할 수 있는 방법을 최대한 많이 적어보세요.",
    "달걀, 구름, 시계 이 세 단어를 모두 포함한 짧은 이야기를 만들어 보세요.",
    "시간이 거꾸로 흐른다면 우리 생활은 어떻게 달라질까요? 가정에 기반한 아이디어를 자유롭게 제시해보세요.",
    "하루 동안 모든 전자기기가 사라진다면, 당신은 어떤 방법으로 하루를 보낼 건가요?",
    "환경 문제(예: 플라스틱 쓰레기)를 해결할 수 있는 기발한 방법을 생각해보세요. 현실적 적용이 가능할수록 좋아요."
]

# Streamlit 앱 UI
st.set_page_config(page_title="창의력 검사", layout="centered")
st.title("🧠 창의력 검사")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []

if st.session_state.step < len(questions):
    q_idx = st.session_state.step
    st.subheader(f"질문 {q_idx + 1}/{len(questions)}")
    st.write(questions[q_idx])

    answer = st.text_area("✍️ 답변을 입력하세요:", key=f"answer_{q_idx}")

    if st.button("다음 질문"):
        st.session_state.answers.append((questions[q_idx], answer))
        st.session_state.step += 1
        st.rerun()
else:
    st.success("🎉 모든 질문이 완료되었습니다! 결과를 확인하세요.")
    for i, (q, a) in enumerate(st.session_state.answers):
        st.markdown(f"### 질문 {i+1}: {q}")
        st.markdown(f"**답변:** {a}")

    df = pd.DataFrame({
        "질문": [q for q, a in st.session_state.answers],
        "답변": [a for q, a in st.session_state.answers]
    })

    st.download_button(
        label="📥 결과 다운로드",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="창의력_검사_결과.csv",
        mime="text/csv"
    )
