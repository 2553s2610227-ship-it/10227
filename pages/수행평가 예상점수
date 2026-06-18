import streamlit as st
import google.generativeai as genai
import json
import re

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="수행평가 도우미",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 커스텀 CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

/* 전체 배경 */
.stApp {
    background: #0F1117;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 헤더 영역 */
.hero-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
    border: 1px solid #2a3040;
    border-radius: 16px;
    padding: 36px 40px 28px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: #818cf8;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(99,102,241,0.3);
    margin-bottom: 12px;
}
.hero-title {
    font-family: 'Space Grotesk', 'Noto Sans KR', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-sub {
    color: #64748b;
    font-size: 15px;
    font-weight: 300;
    margin: 0;
}

/* 섹션 카드 */
.section-card {
    background: #161b27;
    border: 1px solid #1e2636;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 6px;
}
.section-title {
    font-size: 17px;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 16px;
}

/* 점수 결과 카드 */
.result-wrapper {
    background: linear-gradient(135deg, #1a1f2e 0%, #131929 100%);
    border: 1px solid #2a3850;
    border-radius: 16px;
    padding: 32px 36px;
    margin-top: 8px;
}
.score-row {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 4px;
}
.score-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 64px;
    font-weight: 700;
    line-height: 1;
}
.score-max {
    font-size: 22px;
    color: #475569;
    font-weight: 400;
}
.score-label {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 20px;
}
.grade-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 24px;
}

/* 피드백 항목 */
.feedback-section {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #1e2636;
}
.feedback-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 12px;
}
.feedback-item {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    align-items: flex-start;
}
.feedback-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-top: 7px;
    flex-shrink: 0;
}
.feedback-text {
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.6;
}

/* 기준 항목 입력 */
.criterion-row {
    background: #0d1117;
    border: 1px solid #1e2636;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 14px;
    color: #94a3b8;
}

/* Streamlit 위젯 커스텀 */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #0d1117 !important;
    border: 1px solid #1e2636 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 10px 28px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
label, .stSelectbox label {
    color: #64748b !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.stSelectbox > div > div {
    background: #0d1117 !important;
    border: 1px solid #1e2636 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* 구분선 */
hr { border-color: #1e2636 !important; }

/* 예시 뱃지 */
.example-badge {
    display: inline-block;
    background: rgba(16,185,129,0.1);
    color: #34d399;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
}

/* 진행 막대 */
.progress-bar-bg {
    background: #1e2636;
    border-radius: 4px;
    height: 6px;
    margin-top: 8px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.8s ease;
}

/* 경고/안내 박스 */
.info-box {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    color: #818cf8;
    margin-bottom: 12px;
}
.warn-box {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    color: #fbbf24;
}

/* 히스토리 카드 */
.history-card {
    background: #0d1117;
    border: 1px solid #1e2636;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
}

/* 탭 스타일 */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
    border-bottom: 1px solid #1e2636 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    border: none !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    color: #818cf8 !important;
    border-bottom: 2px solid #6366f1 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Gemini 초기화 ────────────────────────────────────────────
def init_gemini():
    """Gemini API 초기화"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return True
    except KeyError:
        return False
    except Exception:
        return False


def get_score_from_ai(subject, criteria_list, submission_content, total_score):
    """AI를 통해 수행평가 점수 예측"""
    criteria_text = "\n".join([
        f"- {c['name']} ({c['score']}점): {c['desc']}"
        for c in criteria_list if c['name'].strip()
    ])

    prompt = f"""당신은 공정하고 경험 많은 교사입니다. 학생의 수행평가 결과물을 채점 기준에 따라 평가해주세요.

[과목/주제]
{subject}

[채점 기준] (총 {total_score}점)
{criteria_text}

[학생 제출 내용]
{submission_content}

위 내용을 바탕으로 아래 JSON 형식으로만 응답하세요. JSON 외 다른 텍스트는 절대 포함하지 마세요.

{{
  "total_predicted": <예상 총점 (정수)>,
  "criteria_scores": [
    {{"name": "<기준명>", "max": <최고점>, "predicted": <예상점수>, "reason": "<채점 이유 1-2문장>"}}
  ],
  "strengths": ["<잘한 점 1>", "<잘한 점 2>", "<잘한 점 3>"],
  "improvements": ["<개선할 점 1>", "<개선할 점 2>", "<개선할 점 3>"],
  "overall_comment": "<전체 총평 2-3문장>",
  "grade": "<등급: A+/A/B+/B/C+/C/D>"
}}"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # JSON 추출
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            result = json.loads(json_match.group())
            return result, None
        else:
            return None, "AI 응답을 파싱할 수 없습니다. 다시 시도해주세요."
    except json.JSONDecodeError:
        return None, "AI 응답 형식 오류입니다. 다시 시도해주세요."
    except Exception as e:
        err_msg = str(e)
        if "quota" in err_msg.lower() or "429" in err_msg:
            return None, "API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
        elif "invalid" in err_msg.lower() or "401" in err_msg:
            return None, "API 키가 유효하지 않습니다. Secrets 설정을 확인해주세요."
        else:
            return None, f"AI 오류: {err_msg[:100]}"


def get_grade_color(grade):
    colors = {
        "A+": "#10b981", "A": "#34d399",
        "B+": "#6366f1", "B": "#818cf8",
        "C+": "#f59e0b", "C": "#fbbf24",
        "D": "#ef4444"
    }
    return colors.get(grade, "#6366f1")


def get_score_color(ratio):
    if ratio >= 0.9:
        return "#10b981"
    elif ratio >= 0.75:
        return "#6366f1"
    elif ratio >= 0.6:
        return "#f59e0b"
    else:
        return "#ef4444"


# ── 세션 상태 초기화 ─────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "criteria" not in st.session_state:
    st.session_state.criteria = [
        {"name": "", "score": 10, "desc": ""},
        {"name": "", "score": 10, "desc": ""},
        {"name": "", "score": 10, "desc": ""},
    ]
if "result" not in st.session_state:
    st.session_state.result = None


# ── 헤더 ────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-tag">AI-Powered · 수행평가</div>
    <div class="hero-title">📝 수행평가 도우미</div>
    <div class="hero-sub">채점 기준을 입력하고 제출물을 분석받아 예상 점수를 확인하세요</div>
</div>
""", unsafe_allow_html=True)

# ── API 키 확인 ──────────────────────────────────────────────
api_ready = init_gemini()
if not api_ready:
    st.markdown("""
    <div class="warn-box">
    ⚠️ <b>Gemini API 키가 설정되지 않았습니다.</b><br>
    Streamlit Cloud → Settings → Secrets에서 <code>GEMINI_API_KEY = "your-key"</code>를 추가해주세요.
    </div>
    """, unsafe_allow_html=True)

# ── 탭 ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["✏️  채점 분석", "📊  분석 기록"])

with tab1:
    left_col, right_col = st.columns([1, 1], gap="large")

    # ── 왼쪽: 입력 영역 ──────────────────────────────────────
    with left_col:

        # 1. 기본 정보
        st.markdown('<div class="section-label">STEP 1</div><div class="section-title">기본 정보</div>', unsafe_allow_html=True)

        subject_input = st.text_input(
            "과목 / 수행평가 제목",
            placeholder="예: 중학교 2학년 국어 - 독서 감상문 쓰기",
            help="채점받을 수행평가의 과목과 제목을 입력하세요."
        )

        st.markdown("---")

        # 2. 채점 기준 입력
        st.markdown('<div class="section-label">STEP 2</div><div class="section-title">채점 기준 설정</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">📌 항목명, 배점, 세부 기준을 입력하세요. 항목은 최대 6개까지 추가할 수 있습니다.</div>', unsafe_allow_html=True)

        total_max = 0
        updated_criteria = []

        for i, crit in enumerate(st.session_state.criteria):
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 0.5])
                with c1:
                    name = st.text_input(
                        f"기준 {i+1} 항목명",
                        value=crit["name"],
                        placeholder=f"예: 내용의 충실성",
                        key=f"crit_name_{i}",
                        label_visibility="collapsed"
                    )
                with c2:
                    score = st.number_input(
                        "배점",
                        min_value=1, max_value=100,
                        value=crit["score"],
                        key=f"crit_score_{i}",
                        label_visibility="collapsed"
                    )
                with c3:
                    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                    if st.button("✕", key=f"del_{i}", help="이 항목 삭제"):
                        if len(st.session_state.criteria) > 1:
                            st.session_state.criteria.pop(i)
                            st.rerun()

                desc = st.text_input(
                    f"세부 기준 {i+1}",
                    value=crit["desc"],
                    placeholder="예: 책의 핵심 내용을 정확하게 파악하고 자신의 생각을 논리적으로 서술했는가",
                    key=f"crit_desc_{i}",
                    label_visibility="collapsed"
                )
                updated_criteria.append({"name": name, "score": score, "desc": desc})
                if name.strip():
                    total_max += score

        st.session_state.criteria = updated_criteria

        col_add, col_total = st.columns([1, 1])
        with col_add:
            if len(st.session_state.criteria) < 6:
                if st.button("＋ 기준 추가", key="add_crit"):
                    st.session_state.criteria.append({"name": "", "score": 10, "desc": ""})
                    st.rerun()
        with col_total:
            st.markdown(f"""
            <div style='text-align:right; padding-top:8px;'>
                <span style='color:#475569; font-size:13px;'>총 배점 </span>
                <span style='color:#818cf8; font-size:20px; font-weight:700;'>{total_max}점</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 3. 제출 내용 입력
        st.markdown('<div class="section-label">STEP 3</div><div class="section-title">제출 내용 입력</div>', unsafe_allow_html=True)

        submission = st.text_area(
            "수행평가 제출 내용",
            height=220,
            placeholder="여기에 수행평가 내용을 붙여넣으세요.\n\n예시:\n오늘 나는 '어린 왕자'를 읽고 많은 것을 느꼈다. 어린 왕자가 여러 별을 여행하며 만나는 어른들의 모습은 현대 사회의 단면을 보여준다. 특히 권력만을 탐하는 왕과 허영심에 가득 찬 신사는...",
            label_visibility="collapsed"
        )

        word_count = len(submission.replace(" ", "").replace("\n", "")) if submission else 0
        st.markdown(f'<div style="text-align:right; font-size:12px; color:#475569; margin-top:4px;">글자 수: {word_count:,}자</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # 분석 버튼
        can_analyze = (
            api_ready and
            subject_input.strip() and
            submission.strip() and
            any(c["name"].strip() for c in st.session_state.criteria) and
            total_max > 0
        )

        if st.button("🔍  AI 채점 분석 시작", disabled=not can_analyze):
            valid_criteria = [c for c in st.session_state.criteria if c["name"].strip()]
            with st.spinner("AI가 꼼꼼하게 채점하고 있습니다..."):
                result, error = get_score_from_ai(
                    subject_input,
                    valid_criteria,
                    submission,
                    total_max
                )
            if error:
                st.error(f"❌ {error}")
            elif result:
                # 점수 범위 보정
                result["total_predicted"] = max(0, min(result["total_predicted"], total_max))
                st.session_state.result = {
                    "subject": subject_input,
                    "total_max": total_max,
                    "data": result,
                    "criteria": valid_criteria,
                }
                # 히스토리에 추가
                import datetime
                st.session_state.history.insert(0, {
                    "time": datetime.datetime.now().strftime("%m/%d %H:%M"),
                    "subject": subject_input,
                    "score": result["total_predicted"],
                    "max": total_max,
                    "grade": result.get("grade", "-"),
                })
                if len(st.session_state.history) > 10:
                    st.session_state.history = st.session_state.history[:10]
                st.rerun()

        if not api_ready:
            st.markdown('<div class="warn-box">⚠️ API 키 설정 후 분석 가능합니다.</div>', unsafe_allow_html=True)
        elif not subject_input.strip():
            st.caption("→ 과목/제목을 입력해주세요.")
        elif not any(c["name"].strip() for c in st.session_state.criteria):
            st.caption("→ 채점 기준을 1개 이상 입력해주세요.")
        elif not submission.strip():
            st.caption("→ 제출 내용을 입력해주세요.")

    # ── 오른쪽: 결과 영역 ────────────────────────────────────
    with right_col:
        if st.session_state.result is None:
            # 빈 상태 안내
            st.markdown("""
            <div style='
                height: 500px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                border: 1px dashed #1e2636;
                border-radius: 16px;
                text-align: center;
                padding: 40px;
            '>
                <div style='font-size:48px; margin-bottom:16px;'>📋</div>
                <div style='font-size:18px; font-weight:600; color:#334155; margin-bottom:8px;'>분석 결과가 여기에 표시됩니다</div>
                <div style='font-size:14px; color:#475569; line-height:1.7;'>
                    왼쪽에서<br>
                    채점 기준과 제출 내용을 입력한 후<br>
                    <b style='color:#6366f1'>AI 채점 분석 시작</b> 버튼을 눌러주세요
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            res = st.session_state.result
            d = res["data"]
            total_pred = d["total_predicted"]
            total_max = res["total_max"]
            ratio = total_pred / total_max if total_max > 0 else 0
            score_color = get_score_color(ratio)
            grade = d.get("grade", "B")
            grade_color = get_grade_color(grade)

            # 총점 카드
            st.markdown(f"""
            <div class="result-wrapper">
                <div style='font-size:12px; color:#475569; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:12px;'>
                    {res['subject']}
                </div>
                <div class="score-row">
                    <span class="score-number" style="color:{score_color};">{total_pred}</span>
                    <span class="score-max">/ {total_max}점</span>
                </div>
                <div class="score-label">예상 점수 ({ratio*100:.1f}%)</div>

                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width:{ratio*100:.1f}%; background:{score_color};"></div>
                </div>

                <div style='margin-top:16px;'>
                    <span class="grade-badge" style="background:rgba(99,102,241,0.1); color:{grade_color}; border:1px solid {grade_color}40;">
                        등급: {grade}
                    </span>
                </div>

                <div style='font-size:14px; color:#94a3b8; line-height:1.7; margin-top:8px;'>
                    {d.get("overall_comment", "")}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            # 항목별 점수
            st.markdown('<div class="section-label" style="margin-bottom:10px;">항목별 예상 점수</div>', unsafe_allow_html=True)

            crit_scores = d.get("criteria_scores", [])
            for cs in crit_scores:
                c_pred = cs.get("predicted", 0)
                c_max = cs.get("max", 10)
                c_ratio = c_pred / c_max if c_max > 0 else 0
                c_color = get_score_color(c_ratio)
                st.markdown(f"""
                <div class="history-card">
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
                        <span style='font-size:14px; font-weight:600; color:#e2e8f0;'>{cs.get("name","")}</span>
                        <span style='font-size:16px; font-weight:700; color:{c_color};'>{c_pred}<span style='font-size:12px; color:#475569;'>/{c_max}</span></span>
                    </div>
                    <div class="progress-bar-bg" style='margin-top:0; margin-bottom:8px;'>
                        <div class="progress-bar-fill" style="width:{c_ratio*100:.0f}%; background:{c_color};"></div>
                    </div>
                    <div style='font-size:12px; color:#64748b;'>{cs.get("reason","")}</div>
                </div>
                """, unsafe_allow_html=True)

            # 잘한 점 / 개선점
            col_s, col_i = st.columns(2)
            with col_s:
                st.markdown('<div class="section-label" style="margin-bottom:8px;">✅ 잘한 점</div>', unsafe_allow_html=True)
                for s in d.get("strengths", []):
                    st.markdown(f"""
                    <div class="feedback-item">
                        <div class="feedback-dot" style="background:#10b981;"></div>
                        <div class="feedback-text">{s}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with col_i:
                st.markdown('<div class="section-label" style="margin-bottom:8px;">💡 개선할 점</div>', unsafe_allow_html=True)
                for imp in d.get("improvements", []):
                    st.markdown(f"""
                    <div class="feedback-item">
                        <div class="feedback-dot" style="background:#f59e0b;"></div>
                        <div class="feedback-text">{imp}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button("🔄  새로 분석하기"):
                st.session_state.result = None
                st.rerun()


# ── 탭 2: 분석 기록 ──────────────────────────────────────────
with tab2:
    if not st.session_state.history:
        st.markdown("""
        <div style='text-align:center; padding:60px 20px; color:#334155;'>
            <div style='font-size:40px; margin-bottom:12px;'>📂</div>
            <div style='font-size:16px; font-weight:600; margin-bottom:6px;'>아직 분석 기록이 없습니다</div>
            <div style='font-size:14px; color:#475569;'>채점 분석 탭에서 분석을 진행하면 여기에 기록이 쌓입니다.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-size:13px; color:#475569; margin-bottom:16px;">총 {len(st.session_state.history)}건의 분석 기록</div>', unsafe_allow_html=True)
        for h in st.session_state.history:
            r = h["score"] / h["max"] if h["max"] > 0 else 0
            c = get_score_color(r)
            gc = get_grade_color(h["grade"])
            st.markdown(f"""
            <div class="history-card">
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <div style='font-size:15px; font-weight:600; color:#e2e8f0; margin-bottom:4px;'>{h['subject']}</div>
                        <div style='font-size:12px; color:#475569;'>{h['time']}</div>
                    </div>
                    <div style='text-align:right;'>
                        <span style='font-size:22px; font-weight:700; color:{c};'>{h['score']}</span>
                        <span style='font-size:13px; color:#475569;'>/{h['max']}점</span>
                        <span style='display:block; font-size:13px; font-weight:600; color:{gc}; margin-top:2px;'>{h['grade']} 등급</span>
                    </div>
                </div>
                <div class="progress-bar-bg" style='margin-top:10px;'>
                    <div class="progress-bar-fill" style="width:{r*100:.0f}%; background:{c};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️  기록 초기화"):
            st.session_state.history = []
            st.rerun()
