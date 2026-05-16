import streamlit as st
import yfinance as yf
import feedparser
import re
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy 3.0", layout="wide", initial_sidebar_state="collapsed")

# 🎨 UI 디자인 (더 밝고 선명한 미드나잇 블루 테마)
st.markdown("""
    <style>
    .main { background-color: #1a202c; color: #f7fafc; }
    .header-container { padding: 1rem 0; border-bottom: 2px solid #4a5568; margin-bottom: 2rem; }
    .title-text { font-size: 2.2rem !important; font-weight: 800; color: #63b3ed; margin: 0; }
    
    /* 지표 카드 디자인 */
    [data-testid="stMetric"] { 
        background-color: #2d3748; 
        border-radius: 15px; padding: 20px; border: 1px solid #4a5568;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    [data-testid="stMetricLabel"] { color: #a0aec0 !important; font-size: 1.1rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 2rem !important; }

    /* 뉴스 카드 디자인 (1줄 요약 강조) */
    .news-card { 
        background-color: #2d3748; padding: 20px; border-radius: 15px; 
        margin-bottom: 15px; border: 1px solid #4a5568; border-left: 8px solid #4299e1; 
    }
    .news-title { color: #ebf8ff !important; font-size: 1.2rem !important; font-weight: bold; text-decoration: none; }
    .summary-box { 
        background-color: #1a202c; padding: 10px 15px; border-radius: 8px; 
        margin-top: 12px; border: 1px solid #4a5568;
    }
    .summary-text { color: #63b3ed !important; font-size: 1rem; font-weight: 500; margin: 0; }
    
    .status-tag { display: inline-block; padding: 3px 10px; border-radius: 5px; font-size: 0.85rem; font-weight: bold; margin-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-container"><p class="title-text">📊 Vibe Economy 3.0</p></div>', unsafe_allow_html=True)

# 2. 지표 분석 함수 (객관적 상태 판단)
@st.cache_data(ttl=300)
def get_analysis(name, ticker):
    try:
        d = yf.Ticker(ticker).history(period="2d")
        val = d['Close'].iloc[-1]
        change = val - d['Close'].iloc[-2]
        pct = (change / d['Close'].iloc[-2]) * 100
        
        if pct > 0.5: status, color = "📈 상승세 (주의)", "#fc8181"
        elif pct < -0.5: status, color = "📉 하락세 (기회)", "#68d391"
        else: status, color = "➡️ 안정화 (보합)", "#cbd5e0"
        
        return val, change, status, color
    except: return 0, 0, "확인불가", "#718096"

indices = {"미국채 금리": "^TNX", "WTI 유가": "CL=F", "환율(USD)": "USDKRW=X", "KOSPI": "^KS11", "NASDAQ": "^IXIC"}
cols = st.columns(2)

for i, (name, ticker) in enumerate(indices.items()):
    val, diff, status, color = get_analysis(name, ticker)
    with cols[i % 2]:
        st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")
        st.markdown(f'<span class="status-tag" style="background-color: {color}; color: #1a202c;">{status}</span>', unsafe_allow_html=True)
        st.write("")

st.divider()

# 3. 실시간 뉴스 자동 요약 엔진
st.subheader("📰 사령관의 실시간 1줄 브리핑")

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)
    return feed.entries[:5]

try:
    for item in fetch_news():
        # RSS 설명글에서 첫 문장만 추출하여 1줄 요약 생성
        raw_summary = clean_html(item.summary)
        summary_line = raw_summary.split('.')[0] + '.' if raw_summary else "클릭하여 상세 내용을 확인하세요."
        
        st.markdown(f"""
            <div class="news-card">
                <a href="{item.link}" target="_blank" class="news-title">{item.title}</a>
                <div class="summary-box">
                    <p class="summary-text">🚩 <b>사령관의 1줄 요약:</b> {summary_line}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
except:
    st.error("데이터 통신 중...")

st.markdown(f"<p style='text-align: center; color: #a0aec0; margin-top: 30px;'>{datetime.now().strftime('%Y-%m-%d %H:%M')} 실시간 운용 중</p>", unsafe_allow_html=True)
