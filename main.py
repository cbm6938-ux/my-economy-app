import streamlit as st
import yfinance as yf
import feedparser
import re
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [정밀 타격 디자인] 초록색만 단독 강화 + 요약 선명도 확보
st.markdown("""
    <style>
    .stApp { background-color: #f1f3f5 !important; }
    
    .header-box {
        background-color: #1e3a8a !important;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 800 !important; margin: 0 !important; }
    .header-box p { color: #cbd5e1 !important; font-size: 0.9rem !important; margin-top: 8px !important; }

    /* 지표 카드 스타일 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 16px !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 700 !important; }

    /* 🟢 [사령관 지시] 초록색(상승) 지표만 단독으로 진하게 보정 */
    /* Streamlit의 상승 화살표가 포함된 태그를 타겟팅 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #064e3b !important; /* 초강력 다크 그린 */
        font-weight: 900 !important;
        background: rgba(6, 78, 59, 0.1);
        padding: 2px 10px;
        border-radius: 5px;
    }

    /* 🔴 빨간색(하락)은 시스템 기본값(또는 부드러운 색상)으로 유지 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        font-weight: 400 !important; /* 기본 두께로 환원 */
        background: transparent !important;
    }

    /* 섹션 제목 선명하게 고정 */
    .section-header {
        color: #0f172a !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #1e3a8a;
        padding-bottom: 5px;
        margin: 30px 0 15px 0;
        display: inline-block;
    }

    /* 뉴스 요약 텍스트 가독성 */
    .news-card {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #ced4da !important;
        border-left: 8px solid #1e3a8a !important;
    }
    .news-link { color: #1e3a8a !important; font-weight: 800 !important; font-size: 1.1rem !important; text-decoration: none !important; }
    .summary-text { color: #475569 !important; font-size: 0.95rem !important; margin-top: 10px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <h2>🚀 Vibe Economy Dashboard</h2>
        <p>실시간 경제 지표 브리핑 | {datetime.now().strftime("%Y.%m.%d %H:%M")} Live</p>
    </div>
    """, unsafe_allow_html=True)

# 2. 데이터 수집
@st.cache_data(ttl=300)
def get_eco(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        diff = val - d['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 3. 실시간 지표 (2열 배치)
indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

# --- 뉴스 섹션 ---
st.markdown('<p class="section-header">📰 오늘의 실시간 요약</p>', unsafe_allow_html=True)

# 4. 실시간 뉴스 & 본문 추출형 요약 엔진
@st.cache_data(ttl=600)
def fetch_news():
    # 실제 기사 내용이 풍부한 뉴스 피드로 교체
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

def get_real_summary(item):
    # 제목과 중복되지 않는 본문 내용을 찾기 위한 로직
    title = item.title
    # RSS summary에서 HTML 태그 제거
    summary_raw = item.get('summary', '')
    clean_content = re.sub('<[^<]+?>', '', summary_raw)
    
    # 제목이 요약에 포함되어 있다면 해당 부분을 제거
    summary_final = clean_content.replace(title, "").strip()
    
    # 만약 요약이 비어있다면 제목 뒤의 추가 텍스트라도 가져옴
    if not summary_final or len(summary_final) < 10:
        summary_final = "본문 기사에서 실시간 업데이트된 세부 내용을 확인하십시오."
    
    return summary_final[:150] + "..." if len(summary_final) > 150 else summary_final

try:
    news_items = fetch_news()
    for item in news_items:
        real_summary = get_real_summary(item)
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank" class="news-link">{item.title}</a>
                <p class="summary-text">🚩 <b> 요약:</b> {real_summary}</p>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v3.4 | Selective Visibility Tuning</p>", unsafe_allow_html=True)
