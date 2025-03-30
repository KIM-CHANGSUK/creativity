import streamlit as st
import pandas as pd
import io

# 질문 리스트
questions = [
    "의자가 꼭 앉는 용도로만 사용되어야 할까요? 의자를 전혀 다른 용도로 사용할 수 있는 방법을 최대한 많이 적어보세요.",
    "달걀, 구름, 시계 이 세 단어를 모두 포함한 짧은 이야기를 만들어 보세요.",
    "시간이 거꾸로 흐른다면 우리 생활은 어떻게 달라질까요? 가정에 기반한 아이디어를 자유롭게 제시해보세요.",
    "하루 동안 모든 전자기기가 사라진다면, 당신은 어떤 방법으로 하루를 보낼 건가요?",
    "환경 문제(예: 플라스틱 쓰레기)를 해결할 수 있는 기발한 방법을 생각해보세요. 현실적 적용이 가능할수록 좋아요.",
    "당신이 새로운 나라를 만든다면, 어떤 규칙 3가지를 만들고 왜 그렇게 정했는지 설명해보세요.",
    "자주 사용하는 물건 하나(예: 칫솔, 이어폰 등)의 디자인을 새롭게 바꾼다면 어떻게 바꾸고 싶은가요?",
    "친구와 크게 다퉜을 때, 기존과 다른 방식으로 화해할 수 있는 창의적인 방법을 제시해보세요.",
    "하늘을 나는 가방이 현실에 존재한다면, 어디에 사용하면 좋을까요? 3가지 이상 활용처를 제안해보세요.",
    "자신이 살아온 이야기를 '식물'에 비유해 보세요. 어떤 식물에 가장 비슷하다고 생각하나요? 이유는?"
]

# Streamlit 앱 기본 설정
st.set_page_config(page_title="창의력 검사", layout="centered")
st.title("🧠 창의력 검사")

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = -1  # 정보 입력 단계
    st.session_state.answers = []
    st.session_state.name = ""
    st.session_state.gender = ""
    st.session_state.age = ""

# 참가자 정보 입력 단계
if st.session_state.step == -1:
    st.subheader("👤 참가자 정보 입력")

    name = st.text_input("이름")
    gender = st.radio("성별", ["남자", "여자"])
    age = st.text_input("나이", placeholder="숫자만 입력하세요")

    if st.button("검사 시작하기"):
        if name and age:
            st.session_state.name = name
            st.session_state.gender = gender
            st.session_state.age = age
            st.session_state.step = 0
            st.rerun()
        else:
            st.warning("이름과 나이를 모두 입력해주세요.")

# 질문 응답 단계
elif st.session_state.step < len(questions):
    q_idx = st.session_state.step
    st.subheader(f"질문 {q_idx + 1}/{len(questions)}")
    st.write(questions[q_idx])

    answer = st.text_area("✍️ 답변을 입력하세요:", key=f"answer_{q_idx}")

    if st.button("다음 질문"):
        st.session_state.answers.append((questions[q_idx], answer))
        st.session_state.step += 1
        st.rerun()

# 결과 출력 및 다운로드 단계
else:
    st.success("🎉 모든 질문이 완료되었습니다! 결과를 확인하세요.")
    st.markdown(f"**이름:** {st.session_state.name} &nbsp;&nbsp;&nbsp; **성별:** {st.session_state.gender} &nbsp;&nbsp;&nbsp; **나이:** {st.session_state.age}")

    for i, (q, a) in enumerate(st.session_state.answers):
        st.markdown(f"### 질문 {i+1}: {q}")
        st.markdown(f"**답변:** {a}")

    # 질문-답변 테이블 생성
    df = pd.DataFrame({
        "질문": [q for q, a in st.session_state.answers],
        "답변": [a for q, a in st.session_state.answers]
    })

    # CSV 파일 생성 (이름/성별/나이 → 빈 줄 → 질문/답변)
    csv_buffer = io.StringIO()
    csv_buffer.write(f"이름,{st.session_state.name}\n")
    csv_buffer.write(f"성별,{st.session_state.gender}\n")
    csv_buffer.write(f"나이,{st.session_state.age}\n")
    csv_buffer.write("\n")  # 한 줄 띄우기
    df.to_csv(csv_buffer, index=False)

    st.download_button(
        label="📥 결과 다운로드 (CSV)",
        data=csv_buffer.getvalue().encode("utf-8-sig"),
        file_name=f"창의력_검사_결과_{st.session_state.name}.csv",
        mime="text/csv"
    )
