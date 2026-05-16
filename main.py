import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime
import time

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro 4.6", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [긴급 복구] 모든 스타일을 하나의 블록으로 통합 및 코드 블록 현상 방지
st.markdown("""
<style>
    .stApp { background-color: #f1f3f5 !important; }
    .header-box {
        background-color: #0c1c4f !important;
        padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; font-size: 1.8rem !important; }
    .info-text { color: #475569 !important; font-size: 0.85rem !important; font-weight: 700 !important; margin-bottom: 10px !important; }
    
    /* 지표 숫자 디자인 */
    div[data-testid="stMetricValue"] { color: #000000 !important; font-weight: 900 !important; font-size: 2.3rem !important; }
    
    /* 🟢 상승(녹색) 네온 뱃지 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important; background-color: #00c853 !important; 
        font-weight: 900 !important; padding: 5px 14px !important; border-radius: 10px !important;
    }

    /* 뉴스 섹션 제목 및 안내 */
    .section-header { color: #000000 !important; font-size: 1.5rem !important; font-weight: 900 !important; border-left: 10px solid #0c1c4f; padding-left: 15px; margin-top: 40px; }
    .news-info { color: #64748b !important; font-size: 0.8rem !important; font-weight: 600 !important; margin-bottom: 20px; margin-left: 15px; }

    /* 뉴스 카드: 코드 블록 방지를 위해 간결하게 재설계 */
    .n-card {
        background-color: #ffffff; padding: 18px; border-radius: 12px; margin-bottom: 12px;
        border: 1px solid #cbd5e1; display: block; text-decoration: none !important;
    }
    .n-badge-row { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
    .n-badge { padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 850; display: inline-block; color: white; }
    .n-sector { background-color: #0c1c4f; }
    .n-imp { background-color: #ef4444; }
    .n-time { color: #64748b; font-size: 0.8rem; margin-left: auto; font-weight: 600; }
    .n-title { color: #000000 !important; font-weight: 800 !important; font-size: 1.1rem !important; line-height: 1.5; display: block; }
</style>
""", unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown('<div class="header-box"><h2>🚀 Vibe Economy Dashboard</h2></div>', unsafe_allow_html=True)

# 2. 데이터 수집 엔진
@st.cache_data(ttl=300)
def get_eco(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        diff = val - d['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

st.markdown('<p class="info-text">※ 각 지수는 전 거래일 종가 기준입니다</p>', unsafe_allow_html=True)

indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)
for name, ticker in indices.items():
    val, diff = get_eco(ticker)
    with list(cols)[0 if name in ["🇺🇸 국채 10년", "💵 환율(USD)", "🇺🇸 NASDAQ"] else 1]:
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

# ❗ [핵심 해결책] 들여쓰기 없는 깨끗한 HTML 문자열 생성
try:
    news_items = fetch_news()
    for item in news_items:
        sector, imp = classify_news(item.title)
        rel_time = get_rel_time(item.published_parsed)
        imp_badge = f'<span class="n-badge n-imp">{imp}</span>' if imp else ""
        
        # 들여쓰기를 모두 제거하여 코드 블록 현상을 방지함
        card_html = f"""<div class="n-card"><div class="n-badge-row"><span class="n-badge n-sector">{sector}</span>{imp_badge}<span class="n-time">⏱ {rel_time}</span></div><a href="{item.link}" target="_blank" class="n-title">{item.title}</a></div>"""
        st.markdown(card_html, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v4.6 | Zero-Code-Leak Mode</p>", unsafe_allow_html=True)
