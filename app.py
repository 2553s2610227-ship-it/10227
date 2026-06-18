import streamlit as range
import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(
    page_title="📅 수행평가 일정 관리기",
    page_icon="📆",
    layout="wide"
)

# 2. 세션 상태(Session State) 초기화 - 데이터 임시 저장용
if 'evaluations' not in st.session_state:
    # 기본 샘플 데이터 제공
    st.session_state.evaluations = pd.DataFrame([
        {"과목": "수학", "수행평가명": "미적분 탐구 보고서", "마감일": "2026-06-25", "내용": "실생활 속 미적분 활용 사례 조사 및 발표"},
        {"과목": "영어", "수행평가명": "에세이 쓰기", "마감일": "2026-06-30", "내용": "지속 가능한 발전을 주제로 300단어 에세이 작성"}
    ])

# 3. 앱 타이틀 및 소개
st.title("📅 수행평가 일정 정리 플래너")
st.markdown("수행평가 일정을 등록하고 마감일을 한눈에 확인하세요!")

st.divider()

# 4. 사이드바: 새로운 수행평가 추가 기능
st.sidebar.header("➕ 새로운 수행평가 추가")

with st.sidebar.form(key='eval_form', clear_on_submit=True):
    subject = st.text_input("📚 과목명", placeholder="예: 국어, 화학 I")
    title = st.text_input("📝 수행평가명", placeholder="예: 독서 감상문 제출")
    due_date = st.date_input("📆 마감일", min_value=datetime.today())
    content = st.text_area("🔍 상세 내용", placeholder="평가 기준이나 준비물 등을 적어주세요.")
    
    submit_button = st.form_submit_button(label="일정 추가하기")

# 일정 추가 로직
if submit_button:
    if subject and title: # 필수 입력값 체크
        new_data = {
            "과목": subject,
            "수행평가명": title,
            "마감일": due_date.strftime("%Y-%m-%d"),
            "내용": content
        }
        # 기존 데이터프레임에 추가
        st.session_state.evaluations = pd.concat([
            st.session_state.evaluations, 
            pd.DataFrame([new_data])
        ], ignore_index=True)
        st.sidebar.success(f"'{title}' 일정이 성공적으로 추가되었습니다!")
        # 화면 새로고침
        st.rerun()
    else:
        st.sidebar.error("과목명과 수행평가명은 필수 입력 항목입니다.")

# 5. 메인 화면: 등록된 수행평가 일정 보기
st.subheader("📋 현재 등록된 수행평가 목록")

if not st.session_state.evaluations.empty:
    # 마감일 순으로 정렬하여 보여주기
    df_sorted = st.session_state.evaluations.sort_values(by="마감일")
    
    # 캘린더나 데이터프레임 형태로 출력 (Index 제외하고 깔끔하게 표 표시)
    st.dataframe(df_sorted, use_container_width=True, hide_index=True)
    
    # 카드 형태로 자세히 보기
    st.markdown("### 🔍 상세 정보")
    for idx, row in df_sorted.iterrows():
        with st.expander(f"📌 [{row['과목']}] {row['수행평가명']} (D-Day 마감: {row['마감일']})"):
            st.write(f"**상세 내용:** {row['내용'] if row['내용'] else '등록된 내용이 없습니다.'}")
else:
    st.info("등록된 수행평가 일정이 없습니다. 왼쪽 사이드바에서 일정을 추가해보세요!")
