import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime
import time

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro 4.8", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [경량화 디자인] 카드 크기 축소 및 고대비 유지
st.markdown("""
<style>
    .stApp { background-color: #f1f3f5 !important; }
    
    .header-box {
        background-color: #0c1c4f !important;
        padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; font-size: 1.6rem !important; }

    .info-text { color: #475569 !important; font-size: 0.8rem !important; font-weight: 700 !important; margin-bottom: 8px !important; }

    /* 📊 [지표 카드 경량화] 패딩 및 크기 축소 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important; /* 여백 축소 */
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 800 !important; font-size: 0.95rem !important; }
    
    /* 지수 숫자: 콤팩트하게 조정 */
    div[data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 1.8rem !important; /* 크기 축소 */
    }

    /* 🟢 상승(녹색) 네온 뱃지: 콤팩트화 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important;           
        background-color: #00c853 !important; 
        font-weight: 900 !important;
        padding: 3px 10px !important;
        border-radius: 8px !important;
        font-size: 1.1rem !important;
    }
    
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        color: #dc2626 !important;
        font-weight: 600 !important;
    }

    /* 뉴스 섹션 */
    .section-header { color: #000000 !important; font-size: 1.4rem !important; font-weight: 900 !important; border-left: 10px solid #0c1c4f; padding-left: 15px; margin-top: 30px; }
    .news-info { color: #64748b !important; font-size: 0.8rem !important; font-weight: 600 !important; margin-bottom: 15px; margin-left: 15px; }

    .n-card {
        background-color: #ffffff; padding: 15px; border-radius: 12px; margin-bottom: 10px;
        border: 1px solid #cbd5e1; display: block; text-decoration: none !important;
    }
    .n-badge-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
    .n-badge { padding: 3px 8px; border-radius: 5px; font-size: 0.7rem; font-weight: 850; display: inline-block; color: white; }
    .n-sector { background-color: #0c1c4f; }
    .n-imp { background-color: #ef4444; }
    .n-time { color: #64748b; font-size: 0.75rem; margin-left: auto; font-weight: 600; }
    .n-title { color: #000000 !important; font-weight: 800 !important; font-size: 1rem !important; line-height: 1.4; display: block; }
</style>
""", unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown('<div class="header-box"><h2>🚀 Vibe Economy Dashboard</h2></div>', unsafe_allow_html=True)

# 2. 데이터 수집 엔진 (5분 주기)
@st.cache_data(ttl=300)
def get_eco(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        diff = val - d['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

st.markdown('<p class="info-text">※ 각 지수는 전 거래일 종가 기준입니다</p>', unsafe_allow_html=True)

# 3. 지표 2열 배치
indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)
for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_eco(ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

# --- 뉴스 섹션 ---
st.markdown('<p class="section-header">📰 섹터별 주요 소식</p>', unsafe_allow_html=True)
st.markdown('<p class="news-info">※ 뉴스는 45분 마다 최신화 됩니다</p>', unsafe_allow_html=True)

def classify_news(title):
    sectors = {"반도체": ["반도체", "삼성전자", "하이닉", "엔비디아"], "건설": ["건설", "부동산", "아파트"], "조선": ["조선", "선박", "수주"], "자동차": ["자동차", "전기차", "배터리"], "금융": ["금리", "환율", "연준"]}
    s_res = "경제일반"
    for s, kws in sectors.items():
        if any(kw in title for kw in kws): s_res = s; break
    imp = "급보" if any(kw in title for kw in ["속보", "긴급", "단독"]) else ("특징주" if any(kw in title for kw in ["특징주", "강세", "상한가"]) else None)
    return s_res, imp

def get_rel_time(pub_struct):
    try:
        diff = datetime.now() - datetime.fromtimestamp(time.mktime(pub_struct))
        if diff.days > 0: return f"{diff.days}일 전"
        if diff.seconds // 3600 > 0: return f"{diff.seconds // 3600}시간 전"
        return f"{diff.seconds // 60}분 전"
    except: return "최근"

@st.cache_data(ttl=2700)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:10]

try:
    news_items = fetch_news()
    for item in news_items:
        sector, imp = classify_news(item.title)
        rel_time = get_rel_time(item.published_parsed)
        imp_badge = f'<span class="n-badge n-imp">{imp}</span>' if imp else ""
        card_html = f"""<div class="n-card"><div class="n-badge-row"><span class="n-badge n-sector">{sector}</span>{imp_badge}<span class="n-time">⏱ {rel_time}</span></div><a href="{item.link}" target="_blank" class="n-title">{item.title}</a></div>"""
        st.markdown(card_html, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v4.8 | Compact View Mode</p>", unsafe_allow_html=True)
