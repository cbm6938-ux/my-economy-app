import streamlit as st
import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime

# 1. 페이지 설정 및 테마 강제 고정 (시스템 설정을 무시하고 가시성 확보)
st.set_page_config(page_title="Vibe Economy Pro 4.0", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [전략 센터 디자인] 가독성 끝판왕 스타일링
st.markdown("""
    <style>
    /* 배경색 강제 고정 (라이트/미드톤 밸런스) */
    .stApp { background-color: #f1f3f5 !important; }
    
    /* 상단 헤더: 남색 배경에 흰색 글자 (절대 가독성) */
    .header-box {
        background-color: #0c1c4f !important;
        padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; font-size: 1.8rem !important; }
    .header-box p { color: #bfdbfe !important; font-size: 0.9rem !important; margin-top: 5px !important; }

    /* 지표 카드 및 차트 영역 */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    label[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    
    /* ❗ 지수 숫자: 완전한 검정색으로 시인성 확보 */
    div[data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 2.2rem !important; 
    }

    /* 🟢 [핵심] 상승(녹색) 수치: 네온 에메랄드 뱃지 스타일 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important;           
        background-color: #00c853 !important; /* 최고 채도 녹색 */
        font-weight: 900 !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
        box-shadow: 0 0 10px rgba(0, 200, 83, 0.4);
    }

    /* 🔴 하락(빨간색) 수치: 기본 스타일 유지 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Down"]) {
        color: #dc2626 !important;
        font-weight: 600 !important;
        background: transparent !important;
    }

    /* 상태 배지 (높음/낮음/안정) */
    .status-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 850;
        margin-top: 10px;
        margin-bottom: 10px;
        border: 1px solid rgba(0,0,0,0.1);
    }
    .status-high { background-color: #fee2e2; color: #b91c1c; } /* 높음 */
    .status-low { background-color: #dcfce7; color: #15803d; }  /* 낮음 */
    .status-stable { background-color: #f3f4f6; color: #374151; } /* 안정 */

    /* 뉴스 섹션 제목 */
    .section-header {
        color: #000000 !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        border-left: 10px solid #0c1c4f;
        padding-left: 15px;
        margin: 40px 0 20px 0;
    }

    /* 뉴스 카드 및 섹터 태그 */
    .news-card {
        background-color: #ffffff !important;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #cbd5e1 !important;
        display: flex;
        align-items: center;
    }
    .sector-tag {
        background-color: #0c1c4f;
        color: #ffffff !important;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 900;
        margin-right: 15px;
        white-space: nowrap;
    }
    .news-link { color: #000000 !important; font-weight: 800 !important; font-size: 1.05rem !important; text-decoration: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown(f"""
    <div class="header-box">
        <h2>🚀 Vibe Economy Strategy Center</h2>
        <p>사령관의 1년 트렌드 분석 기지 | {datetime.now().strftime("%Y.%m.%d %H:%M")} Live</p>
    </div>
    """, unsafe_allow_html=True)

# 2. 데이터 분석 엔진 (1년치 분석)
@st.cache_data(ttl=3600)
def analyze_economy(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="1y")
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2]
        diff = current - prev
        
        # 1년 최고/최저 기준 상태 진단
        min_1y, max_1y = hist['Close'].min(), hist['Close'].max()
        range_1y = max_1y - min_1y
        if current > min_1y + (range_1y * 0.75):
            status = ("높음", "status-high")
        elif current < min_1y + (range_1y * 0.25):
            status = ("낮음", "status-low")
        else:
            status = ("안정", "status-stable")
            
        return current, diff, status, hist['Close']
    except:
        return 0, 0, ("데이터오류", ""), pd.Series()

# 3. 실시간 지표 & 1년 트렌드 그래프 (2열 배치)
indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff, status, history = analyze_economy(ticker)
    with cols[i % 2]:
        with st.container():
            st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")
            # 상태 배지 표시
            st.markdown(f'<span class="status-badge {status[1]}">{status[0]} (1Y 트렌드)</span>', unsafe_allow_html=True)
            # 1년 트렌드 차트
            if not history.empty:
                st.line_chart(history, height=150, use_container_width=True)
        st.write("") # 간격 확보

st.markdown('<p class="section-header">📰 섹터별 주요 소식 (Top 5)</p>', unsafe_allow_html=True)

# 4. 뉴스 섹터 분류 및 출력 (5개 고정)
def classify_sector(title):
    sectors = {
        "반도체": ["반도체", "삼성전자", "하이닉스", "엔비디아"],
        "건설/부동산": ["건설", "부동산", "아파트", "재건축"],
        "조선/해운": ["조선", "선박", "해운", "LNG"],
        "자동차/배터리": ["자동차", "전기차", "배터리", "현대차"],
        "AI/빅테크": ["AI", "인공지능", "구글", "애플", "MS"],
        "금융/정책": ["금리", "환율", "연준", "은행", "정부"]
    }
    for sector, keywords in sectors.items():
        if any(kw in title for kw in keywords): return sector
    return "경제일반"

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5] # 정예 5개

try:
    news_items = fetch_news()
    for item in news_items:
        sector = classify_sector(item.title)
        st.markdown(f"""
            <div class="news-card">
                <span class="sector-tag">{sector}</span>
                <a href="{item.link}" target="_blank" class="news-link">{item.title}</a>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Strategy v4.0 | Mission Complete</p>", unsafe_allow_html=True)
