import streamlit as st

# 앱 제목
st.title("💌 연애 코칭 앱")

# 설명
st.write("연애 고민을 입력하면 간단한 조언을 제공합니다.")

# 사용자 입력
question = st.text_area("연애 고민을 적어주세요")

# 버튼 클릭
if st.button("코칭 받기"):

    # 입력 없을 때
    if question.strip() == "":
        st.warning("고민을 입력해주세요.")
    
    else:
        # 아주 단순한 규칙 기반 답변
        if "고백" in question:
            answer = "상대의 반응을 천천히 살피면서 솔직하게 표현해보세요."
        
        elif "헤어" in question:
            answer = "감정보다 상황을 먼저 정리하고 충분히 대화해보는 게 좋아요."
        
        elif "연락" in question:
            answer = "너무 조급해하지 말고 상대의 리듬도 존중해보세요."
        
        else:
            answer = "상대방의 감정을 존중하면서 솔직하게 대화하는 것이 가장 중요합니다."

        # 결과 출력
        st.success("코칭 결과")
        st.write(answer)
