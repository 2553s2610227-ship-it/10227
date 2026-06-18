import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. 페이지 기본 설정 및 디자인 레이아웃 정의
st.set_page_config(
    page_title="수행평가 도우미 시간표",
    page_icon="📝",
    layout="wide"
)

# 2. 세션 상태(Session State) 초기화 (앱을 새로고침하기 전까지 데이터를 유지하는 공간)
if "timetable_data" not in st.session_state:
    # 초기에 보여줄 샘플 시간표 데이터 설정
    st.session_state.timetable_data = {
        "교시": ["1교시", "2교시", "3교시", "4교시", "5교시", "6교시", "7교시"],
        "월": ["국어", "수학", "영어", "과학", "사회", "음악", "자율"],
        "화": ["수학", "영어", "체육", "국어", "미술", "미술", "동아리"],
        "수": ["과학", "사회", "수학", "영어", "진로", "컴퓨터", ""],
        "목": ["영어", "국어", "과학", "역사", "기술가정", "기술가정", "자치"],
        "금": ["사회", "수학", "국어", "영어", "한문", "체육", ""]
    }

if "evaluations_list" not in st.session_state:
    # 초기에 보여줄 샘플 수행평가 내용 설정
    st.session_state.evaluations_list = [
        {"과목": "과학", "내용": "실험 보고서 작성 및 제출", "마감일": date.today(), "완료": False},
        {"과목": "수학", "내용": "대단원 평가 오답노트 작성", "마감일": date.today(), "완료": False}
    ]

# 3. 앱 제목 및 상단 가이드라인
st.title("🚀 스마트 수행평가 도우미 시간표")
st.markdown("우리 반 시간표를 확인하고, 과목별 수행평가 일정과 D-Day를 스마트하게 관리하세요!")
st.write("---")

# 4. 상단 통계 대시보드 (수행평가 현황 요약)
today_date = date.today()
incomplete_tasks = [task for task in st.session_state.evaluations_list if not task["완료"]]
today_urgent_tasks = [task for task in incomplete_tasks if task["마감일"] == today_date]

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric(label="📊 남은 수행평가", value=f"{len(incomplete_tasks)} 개")
with stat_col2:
    st.metric(label="🚨 오늘 마감 수행평가", value=f"{len(today_urgent_tasks)} 개")
with stat_col3:
    st.metric(label="📅 오늘 날짜", value=today_date.strftime("%Y년 %m월 %d일"))

st.write("---")

# 5. 메인 레이아웃 분할 (좌측: 시간표 관리, 우측: 수행평가 관리)
main_left, main_right = st.columns([4, 3])

# --- 좌측 영역: 주간 시간표 관리 ---
with main_left:
    st.subheader("🏫 이번 주 학급 시간표")
    
    # 세션에 저장된 데이터를 판다스 데이터프레임으로 바꾼 뒤 웹에 표시
    df_current_timetable = pd.DataFrame(st.session_state.timetable_data)
    st.dataframe(df_current_timetable, use_container_width=True, hide_index=True)
    
    # 시간표 직접 수정 기능 제공
    with st.expander("✏️ 시간표 과목 직접 수정하기"):
        st.info("테이블 안의 과목을 직접 더블클릭하여 수정한 뒤 하단의 '변경사항 저장하기' 버튼을 누르세요.")
        try:
            edited_timetable_df = st.data_editor(df_current_timetable, use_container_width=True, hide_index=True)
            if st.button("변경사항 저장하기", key="save_timetable_btn"):
                st.session_state.timetable_data = edited_timetable_df.to_dict(orient="list")
                st.success("시간표가 성공적으로 업데이트되었습니다!")
                st.rerun()
        except Exception as error:
            st.error(f"시간표를 수정하는 중 오류가 발생했습니다: {error}")

# --- 우측 영역: 수행평가 내용 등록 및 알림 목록 ---
with main_right:
    st.subheader("📝 수행평가 내용 등록 및 조회")
    
    # 수행평가 추가를 위한 서브 폼(Form) 생성
    with st.form(key="add_evaluation_form", clear_on_submit=True):
        st.write("**🆕 새로운 수행평가 추가**")
        
        # 현재 시간표에 등록되어 있는 유효한 과목들을 자동으로 수집하여 선택지로 제공
        extracted_subjects = set()
        for day_column in ["월", "화", "수", "목", "금"]:
            extracted_subjects.update(st.session_state.timetable_data[day_column])
        valid_subjects = sorted([subj for subj in extracted_subjects if subj.strip() != ""])
        
        # 만약 시간표가 비어있을 경우를 대비한 기본 과목 리스트 예외처리
        if not valid_subjects:
            valid_subjects = ["국어", "수학", "영어", "과학", "사회"]
            
        selected_subject = st.selectbox("수행평가 과목", valid_subjects)
        input_content = st.text_input("수행평가 핵심 내용 (예: PPT 발표자료 제출)")
        selected_due_date = st.date_input("제출 마감일", value=today_date)
        
        submit_form_button = st.form_submit_button(label="도우미에 등록")
        
        if submit_form_button:
            if not input_content.strip():
                st.warning("수행평가 내용을 반드시 입력해주세요.")
            else:
                new_evaluation_item = {
                    "과목": selected_subject,
                    "내용": input_content,
                    "마감일": selected_due_date,
                    "완료": False
                }
                st.session_state.evaluations_list.append(new_evaluation_item)
                st.success(f"📌 [{selected_subject}] 수행평가가 정상 등록되었습니다.")
                st.rerun()

    st.write("---")
    
    # 등록된 수행평가 목록 표시부
    st.write("**📋 마감일 기준 수행평가 타임라인**")
    
    if not st.session_state.evaluations_list:
        st.info("현재 등록된 수행평가 과제가 없습니다. 편안한 하루 보내세요! 🎉")
    else:
        # 인덱스 순서대로 루프를 돌며 개별 카드 형태로 출력
        for item_index, eval_item in enumerate(st.session_state.evaluations_list):
            # 마감일까지의 D-Day 일수 계산
            calculated_d_day = (eval_item["마감일"] - today_date).days
            
            if calculated_d_day == 0:
                d_day_label = "🚨 D-Day (오늘까지!)"
            elif calculated_d_day > 0:
                d_day_label = f"⏳ D-{calculated_d_day}"
            else:
                d_day_label = f"❌ 만료 ({abs(calculated_d_day)}일 경과)"
            
            # 완료 여부에 따라 제목 스타일 구분
            completion_status_emoji = "✅" if eval_item["완료"] else "📌"
            expander_title = f"{completion_status_emoji} [{eval_item['과목']}] {d_day_label}"
            
            with st.expander(expander_title, expanded=not eval_item["완료"]):
                st.write(f"**과제 내용**: {eval_item['내용']}")
                st.write(f"**마감 날짜**: {eval_item['마감일'].strftime('%Y-%m-%d')}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if not eval_item["완료"]:
                        if st.button("완료 체크", key=f"complete_btn_{item_index}"):
                            st.session_state.evaluations_list[item_index]["완료"] = True
                            st.rerun()
                    else:
                        if st.button("완료 취소", key=f"incomplete_btn_{item_index}"):
                            st.session_state.evaluations_list[item_index]["완료"] = False
                            st.rerun()
                with col_btn2:
                    if st.button("삭제", key=f"delete_btn_{item_index}"):
                        st.session_state.evaluations_list.pop(item_index)
                        st.success("삭제되었습니다.")
                        st.rerun()
