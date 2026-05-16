import streamlit as st
import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy Pro 4.0", layout="wide", initial_sidebar_state="collapsed")

# 🎨 [최종 시인성 보정] 초록색 강화 + 상태 배지 + 차트 최적화
st.markdown("""
    <style>
    .stApp { background-color: #f1f3f5 !important; }
    
    .header-box {
        background-color: #0c1c4f !important;
        padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center;
    }
    .header-box h2 { color: #ffffff !important; font-weight: 900 !important; margin: 0 !important; }

    /* 지표 카드 및 차트 영역 */
    .metric-container {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* 🟢 상승(초록) 수치: 네온 에메랄드 뱃지 */
    [data-testid="stMetricDelta"] > div:has(svg[data-testid="stMetricDeltaIcon-Up"]) {
        color: #ffffff !important;
        background-color: #16a34a !important;
        font-weight: 900 !important;
        padding: 4px 12px !important;
        border-radius: 8px !important;
        font-size: 1.1rem !important;
    }

    /* 상태 표시 배지 스타일 */
    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        margin-top: 5px;
    }
    .status-high { background-color: #fee2e2; color: #b91c1c; } /* 높음: 연빨강 */
    .status-low { background-color: #dcfce7; color: #15803d; }  /* 낮음: 연초록 */
    .status-stable { background-color: #f3f4f6; color: #374151; } /* 안정: 회색 */

    .news-card {
        background-color: #ffffff; padding: 18px; border-radius: 12px;
        margin-bottom: 10px; border: 1px solid #cbd5e1; display: flex; align-items: center;
    }
    .sector-tag {
        background-color: #0c1c4f; color: #ffffff; padding: 4px 10px;
        border-radius: 6px; font-size: 0.8rem; font-weight: 900; margin-right: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 ---
st.markdown('<div class="header-box"><h2>🚀 Vibe Economy Strategy Center</h2></div>', unsafe_allow_html=True)

# 2. 데이터 분석 함수 (1년치 데이터 분석 포함)
@st.cache_data(ttl=3600)
def analyze_economy(ticker):
    try:
        # 1년치 데이터 수집
        hist = yf.Ticker(ticker).history(period="1y")
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2]
        diff = current - prev
        
        # 상태 진단 로직 (1년 최고/최저 대비 현재가 위치)
        min_val = hist['Close'].min()
        max_val = hist['Close'].max()
        range_val = max_val - min_val
        
        if current > min_val + (range_val * 0.75):
            status = ("높음", "status-high")
        elif current < min_val + (range_val * 0.25):
            status = ("낮음", "status-low")
        else:
            status = ("안정", "status-stable")
            
        return current, diff, status, hist['Close']
    except:
        return 0, 0, ("데이터오류", ""), pd.Series()

# 3. 실시간 지표 & 1년 트렌드 차트 (2열 배치)
indices = {"🇺🇸 국채 10년": "^TNX", "🛢️ WTI 유가": "CL=F", "💵 환율(USD)": "USDKRW=X", "🇰🇷 KOSPI": "^KS11", "🇺🇸 NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff, status, history = analyze_economy(ticker)
    with cols[i % 2]:
        # 메인 카드 컨테이너
        with st.container():
            st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")
            # 상태 배지 표시
            st.markdown(f'<span class="status-badge {status[1]}">{status[0]} (1Y 기준)</span>', unsafe_allow_html=True)
            # 1년 트렌드 차트 (작고 세련되게)
            if not history.empty:
                st.line_chart(history, height=120)
        st.write("") # 간격 조절

st.divider()

# 4. 섹터 뉴스 (뉴스 개수 5개로 복구)
st.subheader("📰 섹터별 주요 뉴스 (Top 5)")

def classify_sector(title):
    sectors = {"반도체": ["반도체", "삼성전자", "엔비디아"], "에너지": ["유가", "기름", "배터리"], "금융": ["금리", "환율", "연준"], "조선": ["조선", "배", "선박"], "자동차": ["자동차", "현대차", "기아"]}
    for sector, keywords in sectors.items():
        if any(kw in title for kw in keywords): return sector
    return "경제일반"

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5] # 5개로 정렬!

try:
    news_items = fetch_news()
    for item in news_items:
        sector = classify_sector(item.title)
        st.markdown(f"""
            <div class="news-card">
                <span class="sector-tag">{sector}</span>
                <a href="{item.link}" target="_blank" style="color:#000; text-decoration:none; font-weight:700;">{item.title}</a>
            </div>
            """, unsafe_allow_html=True)
except:
    st.info("뉴스를 연결 중입니다...")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>Vibe Coding Pro v4.0 | Strategy & Trend Mode</p>", unsafe_allow_html=True)
