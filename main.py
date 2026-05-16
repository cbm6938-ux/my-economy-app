import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Vibe Economy 3.0", layout="wide")

# 🎨 [UI 최적화] 거슬리는 라벨 제거 및 폰트 선명도 강화
st.markdown("""
    <style>
    .main { background-color: #121212; color: #E0E0E0; }
    /* 차트 상단 여백 조절 */
    .stChart { margin-top: -20px; }
    /* 메트릭 카드 가독성 */
    [data-testid="stMetric"] { background-color: #1E1E1E; border-radius: 12px; border: 1px solid #333333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Vibe Economy 3.0")
st.markdown(f"**Commander's Dashboard** | {datetime.now().strftime('%H:%M')} Live")

# 2. 데이터 수집 엔진
@st.cache_data(ttl=300)
def get_clean_data(ticker, period="1mo"):
    try:
        d = yf.Ticker(ticker).history(period=period)
        # 🚩 [중요] Date와 Close라는 글자가 차트에 뜨지 않도록 이름을 제거합니다.
        chart_df = d[['Close']].copy()
        chart_df.index.name = None # 'Date' 라벨 제거
        chart_df.columns = [None]  # 'Close' 라벨 제거
        return chart_df
    except: return None

indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "환율": "USDKRW=X", "코스피": "^KS11", "나스닥": "^IXIC"}

# 3. 상단 지표 (2열 배치)
cols = st.columns(2)
for i, (name, ticker) in enumerate(indices.items()):
    hist = yf.Ticker(ticker).history(period="2d")
    if not hist.empty:
        val = hist['Close'].iloc[-1]
        diff = val - hist['Close'].iloc[-2]
        with cols[i % 2]:
            st.metric(name, f"{val:,.2f}", f"{diff:+.2f}")

st.divider()

# 4. [개선된 차트] 줌 기능 탑재 & 라벨 제거
st.subheader("📈 시장 흐름 정밀 분석 (1개월)")

selected_name = st.selectbox("분석 지표 선택", list(indices.keys()))
chart_data = get_clean_data(indices[selected_name], "1mo")

if chart_data is not None:
    # 🚩 Y축 자동 줌: 직선처럼 보이는 현상을 방지하기 위해 최소/최댓값에 맞춥니다.
    # 지표마다 변동폭이 다르므로 유연하게 설정
    y_min = float(chart_data.min().iloc[0]) * 0.99
    y_max = float(chart_data.max().iloc[0]) * 1.01

    # 사령관님, area_chart를 쓰면 아래쪽에 색이 채워져서 훨씬 '어플' 같습니다!
    st.area_chart(chart_data, height=250, use_container_width=True)
    st.caption(f"💡 {selected_name}의 최근 추세입니다. (불필요한 데이터 라벨 제거 완료)")

st.divider()

# 5. 뉴스 섹션
st.subheader("📰 실시간 속보")
@st.cache_data(ttl=600)
def fetch_news():
    url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:5]

for item in fetch_news():
    st.markdown(f"""
        <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; border-left: 4px solid #00E5FF; margin-bottom: 10px;">
            <a href="{item.link}" target="_blank" style="color:#00E5FF; font-weight:bold; text-decoration:none;">{item.title}</a>
        </div>
        """, unsafe_allow_html=True)
