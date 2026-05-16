import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime
import time

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro 5.0", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [마지막 정밀 튜닝] 단위 표기 일관성 및 최종 가독성 마감
st.markdown("""
<style>
    .stApp { background-color: #f1f3f5 !important; }
    
    .header-box {
        background-color: #0c1c4f !important;
        padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; font-size: 1.6rem !important; }

    .info-text { color: #475569 !important; font-size: 0.8rem !important; font-weight: 700 !important; margin-bottom: 8px !important; }

    /* 지표 카드 스타일 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 800 !important; font-size: 0.95rem !important; }
    
    /* 지수 숫자 */
    div[data-testid="stMetricValue"] { 
        color: #000000 !important; font-weight: 900 !important; font-size: 1.7rem !important; 
    }

    /* 🟢 상승(녹색) 네온 뱃지 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important;           
        background-color: #00c853 !important; 
        font-weight: 900 !important;
        padding: 3px 10px !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    
    /* 🔴 하락(빨간색) 뱃지 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        color: #ffffff !important;           
        background-color: #ef4444 !important; 
        font-weight: 900 !important;
        padding: 3px 10px !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
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

# 2. 데이터 엔진
@st.cache_data(ttl=300)
def get_eco(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        diff = val - d['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

st.markdown('<p class="info-text">※ 각 지수는 전 거래일 종가 기준입니다</p>', unsafe_allow_html=True)

# 3. 지표 및 단위 설정
indices = {
    "🇺🇸 국채 10년": ("^TNX", "%"),
    "🛢️ WTI 유가": ("CL=F", "$"),
    "💵 환율(USD)": ("USDKRW=X", "원"),
    "🇰🇷 KOSPI": ("^KS11", "pt"),
    "🇺🇸 NASDAQ": ("^IXIC", "pt")
}

cols = st.columns(2)
for i, (name, (ticker, unit)) in enumerate(indices.items()):
    val, diff = get_eco(ticker)
    
    # 단위 위치 및 형식 최종 최적화
    if unit == "$":
        display_val = f"${val:,.2f}"
        display_diff = f"{'+' if diff > 0 else ''}${abs(diff):,.2f}" # +$4.25 형식
    else:
        display_val = f"{val:,.2f} {unit}"
        display_diff = f"{diff:+.2f} {unit}"
        
    with cols[i % 2]:
        st.metric(name, display_val, display_diff)

# --- 뉴스 섹션 ---
st.markdown('<p class="section-header">📰 섹터별 주요 소식</p>', unsafe_allow_html=True)
st.markdown('<p class="news-info">※ 뉴스는 45분 마다 최신화 됩니다</p>', unsafe_allow_html=True)

@st.cache_data(ttl=2700)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:10]

def classify_news(title):
    sectors = {"반도체": ["반도체", "삼성전자", "하이닉", "엔비디아"], "건설": ["건설", "부동산", "아파트"], "조선": ["조선", "선박", "수주"], "자동차": ["자동차", "전기차", "배터리"], "금융": ["금리", "환율", "연준"]}
    s_res = "경제일반"
    for s, kws in sectors.items():
        if any(kw in title for kw in kws): s_res = s; break
    imp = "급보" if any(kw in title for kw in ["속보", "긴급", "단독"]) else ("특징주" if any(kw in title for kw in ["특징주", "강세", "상한가"]) else None)
    return s_res, imp

try:
    news_items = fetch_news()
    for item in news_items:
        sector, imp = classify_news(item.title)
        # 시간 계산 로직
        diff = datetime.now() - datetime.fromtimestamp(time.mktime(item.published_parsed))
        rel_time = f"{diff.days}일 전" if diff.days > 0 else (f"{diff.seconds // 3600}시간 전" if diff.seconds // 3600 > 0 else f"{diff.seconds // 60}분 전")
        
        imp_badge = f'<span class="n-badge n-imp">{imp}</span>' if imp else ""
        card_html = f"""<div class="n-card"><div class="n-badge-row"><span class="n-badge n-sector">{sector}</span>{imp_badge}<span class="n-time">⏱ {rel_time}</span></div><a href="{item.link}" target="_blank" class="n-title">{item.title}</a></div>"""
        st.markdown(card_html, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v5.0 | Official Release</p>", unsafe_allow_html=True)
