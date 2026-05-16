import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime
import time

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro 4.7", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [최종 시각 최적화] 지수 카드 복구 + 네온 그린 뱃지 + 코드 노출 차단
st.markdown("""
<style>
    /* 전체 배경색 */
    .stApp { background-color: #f1f3f5 !important; }
    
    /* 상단 헤더 박스 */
    .header-box {
        background-color: #0c1c4f !important;
        padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; font-size: 1.8rem !important; }

    /* 지표 상단 안내 문구 */
    .info-text { color: #475569 !important; font-size: 0.85rem !important; font-weight: 700 !important; margin-bottom: 10px !important; }

    /* 📊 [지수 카드 복구] 하얀색 카드 형태와 테두리 재설정 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    
    /* ❗ 지수 숫자: 완전한 검정색 (시인성 극대화) */
    div[data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 2.3rem !important; 
    }

    /* 🟢 [네온 그린 복구] 상승(Up) 수치 뱃지 스타일 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important;           
        background-color: #00c853 !important; 
        font-weight: 900 !important;
        padding: 5px 14px !important;
        border-radius: 10px !important;
        font-size: 1.25rem !important;
        box-shadow: 0 0 10px rgba(0, 200, 83, 0.4);
    }
    
    /* 🔴 하락(Down) 수치 기본 스타일 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        color: #dc2626 !important;
        font-weight: 600 !important;
    }

    /* 뉴스 섹션 레이아웃 */
    .section-header { color: #000000 !important; font-size: 1.5rem !important; font-weight: 900 !important; border-left: 10px solid #0c1c4f; padding-left: 15px; margin-top: 40px; }
    .news-info { color: #64748b !important; font-size: 0.8rem !important; font-weight: 600 !important; margin-bottom: 20px; margin-left: 15px; }

    /* 뉴스 카드: 코드 노출 방지를 위한 한 줄 렌더링 스타일 */
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

# 2. 데이터 수집 엔진 (5분 주기)
@st.cache_data(ttl=300)
def get_eco(ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        diff = val - d['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 지수 기준 안내 문구
st.markdown('<p class="info-text">※ 각 지수는 전 거래일 종가 기준입니다</p>', unsafe_allow_html=True)

# 3. 실시간 지표 (2열 배치 및 카드 복구)
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

@st.cache_data(ttl=2700) # 사령관님 전용 45분 주기
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:10]

# 뉴스 카드 출력
try:
    news_items = fetch_news()
    for item in news_items:
        sector, imp = classify_news(item.title)
        rel_time = get_rel_time(item.published_parsed)
        imp_badge = f'<span class="n-badge n-imp">{imp}</span>' if imp else ""
        
        # 코드 블록 현상 방지를 위해 들여쓰기 없는 한 줄 HTML 렌더링
        card_html = f"""<div class="n-card"><div class="n-badge-row"><span class="n-badge n-sector">{sector}</span>{imp_badge}<span class="n-time">⏱ {rel_time}</span></div><a href="{item.link}" target="_blank" class="n-title">{item.title}</a></div>"""
        st.markdown(card_html, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v4.7 | Complete Fleet Recovery</p>", unsafe_allow_html=True)
