import streamlit as st
import google.generativeai as genai
import json
import re
import datetime

# 커스텀 CSS 디자인 스타일 유지
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');
.hero-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
    border: 1px solid #2a3040;
    border-radius: 16px;
    padding: 36px 40px 28px 40px;
    margin-bottom: 32px;
}
.hero-title { font-size: 36px; font-weight: 700; color: #f1f5f9; }
.section-card { background: #161b27; border: 1px solid #1e2636; border-radius: 12px; padding: 24px 28px; }
.result-wrapper { background: linear-gradient(135deg, #1a1f2e 0%, #131929 100%); border: 1px solid #2a3850; border-radius: 16px; padding: 32px 36px; }
.score-number { font-size: 64px; font-weight: 700; }
.history-card { background: #0d1117; border: 1px solid #1e2636; border-radius: 10px; padding: 16px 20px; margin-bottom: 10px; }
.feedback-item { display: flex; gap: 10px; margin-bottom: 10px; }
.feedback-dot { width: 6px; height: 6px; border-radius: 50%; margin-top: 7px; flex-shrink: 0; }
.info-box { background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.2); border-radius: 8px; padding: 12px 16px; color: #818cf8; }
.warn-box { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 8px; padding: 12px 16px; color: #fbbf24; }
.progress-bar-bg { background: #1e2636; border-radius: 4px; height: 6px; overflow: hidden; }
.progress-bar-fill { height: 100%; transition: width 0.8s ease; }
</style>
""", unsafe_allow_html=True)

# Gemini 초기화 함수
def init_gemini():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return True
    except Exception:
        return False

def get_score_from_ai(subject, criteria_list, submission_content, total_score):
    criteria_text = "\n".join([f"- {c['name']} ({c['score']}점): {c['desc']}" for c in criteria_list if c['name'].strip()])
    prompt = f"""당신은 공정하고 경험 많은 교사입니다. 학생의 수행평가 결과물을 채점 기준에 따라 평가해주세요.
[과목/주제] {subject}
[채점 기준] (총 {total_score}점) {criteria_text}
[학생 제출 내용] {submission_content}

아래 JSON 형식으로만 응답하세요. JSON 외 다른 텍스트는 절대 포함하지 마세요.
{{
  "total_predicted": <예상 총점 (정수)>,
  "criteria_scores": [
    {{"name": "<기준명>", "max": <최고점>, "predicted": <예상점수>, "reason": "<채점 이유>"}}
  ],
  "strengths": ["<잘한 점>"],
  "improvements": ["<개선할 점>"],
  "overall_comment": "<전체 총평>",
  "grade": "<등급>"
}}"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")
        response = model.generate_content(prompt)
        json_match = re.search(r'\{[\s\S]*\}', response.text.strip())
        if json_match:
            return json.loads(json_match.group()), None
        return None, "AI 응답 파싱 실패"
    except Exception as e:
        return None, f"오류: {str(e)}"

# 색상 지정 함수
def get_grade_color(grade):
    return {"A+": "#10b981", "A": "#34d399", "B+": "#6366f1", "B": "#818cf8", "C+": "#f59e0b", "C": "#fbbf24", "D": "#ef4444"}.get(grade, "#6366f1")

def get_score_color(ratio):
    if ratio >= 0.9: return "#10b981"
    elif ratio >= 0.75: return "#6366f1"
    elif ratio >= 0.6: return "#f59e0b"
    return "#ef4444"

# 세션 상태 초기화
if "history" not in st.session_state: st.session_state.history = []
if "criteria" not in st.session_state: st.session_state.criteria = [{"name": "", "score": 10, "desc": ""}] * 3
if "result" not in st.session_state: st.session_state.result = None

# 상단 헤더
st.markdown("""
<div class="hero-header">
    <div class="hero-title">📝 AI 수행평가 모의 채점기</div>
    <div style="color:#64748b;">채점 기준을 입력하고 나의 제출안을 미리 피드백 받으세요.</div>
</div>
""", unsafe_allow_html=True)

api_ready = init_gemini()
if not api_ready:
    st.markdown('<div class="warn-box">⚠️ 비밀키 설정을 확인해주세요 (Secrets 내 GEMINI_API_KEY).</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✏️ 채점 분석", "📊 분석 기록"])

with tab1:
    left_col, right_col = st.columns([1, 1], gap="large")
    with left_col:
        st.subheader("📋 정보 입력")
        subject_input = st.text_input("과목 / 수행평가 제목", placeholder="예: 국어 - 독서 감상문")
        
        st.markdown('<div class="info-box">📌 항목명, 배점, 세부 기준을 입력하세요.</div>', unsafe_allow_html=True)
        total_max = 0
        updated_criteria = []
        for i, crit in enumerate(st.session_state.criteria):
            c1, c2, c3 = st.columns([3, 1, 0.5])
            with c1: name = st.text_input(f"기준 {i+1} 항목명", value=crit["name"], key=f"crit_name_{i}")
            with c2: score = st.number_input("배점", min_value=1, max_value=100, value=crit["score"], key=f"crit_score_{i}")
            with c3:
                st.write("")
                if st.button("✕", key=f"del_{i}") and len(st.session_state.criteria) > 1:
                    st.session_state.criteria.pop(i)
                    st.rerun()
            desc = st.text_input(f"세부 기준 {i+1}", value=crit["desc"], key=f"crit_desc_{i}")
            updated_criteria.append({"name": name, "score": score, "desc": desc})
            if name.strip(): total_max += score
        
        st.session_state.criteria = updated_criteria
        if len(st.session_state.criteria) < 6 and st.button("＋ 기준 추가"):
            st.session_state.criteria.append({"name": "", "score": 10, "desc": ""})
            st.rerun()
            
        submission = st.text_area("수행평가 제출 내용 작성", height=200, placeholder="여기에 내용을 적으세요...")
        
        can_analyze = api_ready and subject_input.strip() and submission.strip() and total_max > 0
        if st.button("🔍 AI 채점 시작", disabled=not can_analyze):
            valid_criteria = [c for c in st.session_state.criteria if c["name"].strip()]
            with st.spinner("AI 분석 중..."):
                result, error = get_score_from_ai(subject_input, valid_criteria, submission, total_max)
                if result:
                    result["total_predicted"] = max(0, min(result["total_predicted"], total_max))
                    st.session_state.result = {"subject": subject_input, "total_max": total_max, "data": result}
                    st.session_state.history.insert(0, {
                        "time": datetime.datetime.now().strftime("%m/%d %H:%M"),
                        "subject": subject_input, "score": result["total_predicted"], "max": total_max, "grade": result.get("grade", "-")
                    })
                    st.rerun()

    with right_col:
        st.subheader("📊 채점 결과")
        if st.session_state.result is None:
            st.info("왼쪽에서 내용을 채우고 버튼을 누르면 AI 리포트가 출력됩니다.")
        else:
            res = st.session_state.result
            d = res["data"]
            ratio = d["total_predicted"] / res["total_max"]
            s_color = get_score_color(ratio)
            
            st.markdown(f"""
            <div class="result-wrapper">
                <h3>{res['subject']}</h3>
                <div class="score-number" style="color:{s_color};">{d['total_predicted']} <span style="font-size:20px; color:gray;">/ {res['total_max']}점</span></div>
                <p><b>등급: {d.get('grade','-')}</b></p>
                <p>{d.get('overall_comment','')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            for cs in d.get("criteria_scores", []):
                st.markdown(f"""
                <div class="history-card">
                    <b>{cs.get('name')}</b> ({cs.get('predicted')}/{cs.get('max')}점)
                    <div style="font-size:12px; color:gray;">{cs.get('reason')}</div>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    if not st.session_state.history:
        st.write("기록이 없습니다.")
    else:
        for h in st.session_state.history:
            st.markdown(f"""
            <div class="history-card">
                <b>{h['subject']}</b> - {h['score']}/{h['max']}점 (등급: {h['grade']}) <br>
                <small style="color:gray;">{h['time']}</small>
            </div>
            """, unsafe_allow_html=True)
