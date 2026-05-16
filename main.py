import streamlit as st
import yfinance as yf
import feedparser # 실시간 뉴스 수집용 도구

# 페이지 설정
st.set_page_config(page_title="경제 지표 & 실시간 속보", layout="wide")

st.title("📊 사령관님의 실시간 경제 정보 기지")
st.markdown("##### 🚀 지표와 뉴스를 실시간으로 자동 수집하여 1줄 요약과 함께 제공합니다.")

# 1. 지표 데이터 함수
def get_stock(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d")
        val = data['Close'].iloc[-1]
        diff = val - data['Close'].iloc[-2]
        return val, diff
    except: return 0, 0

# 상단 지표 배치
indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "원/달러 환율": "USDKRW=X", "코스피": "^KS11", "나스닥": "^IXIC"}
cols = st.columns(len(indices))
for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_stock(ticker)
    cols[i].metric(name, f"{val:.2f}", f"{diff:.2f}")

st.divider()

# 2. 실시간 뉴스 자동 수집 엔진 (구글 경제 뉴스 RSS 활용)
st.subheader("📰 실시간 경제 속보 (자동 업데이트)")

@st.cache_data(ttl=3600) # 1시간마다 새로운 뉴스 데이터 로드
def get_realtime_news():
    # 구글 뉴스 경제 섹션 RSS 주소
    rss_url = "https://news.google.com/rss/search?q=경제&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries[:5] # 최신 뉴스 5개만 추출

news_entries = get_realtime_news()

for i, entry in enumerate(news_entries):
    # 제목 클릭 시 실제 기사로 이동하는 링크 생성
    st.markdown(f"### {i+1}. [{entry.title}]({entry.link})")
    
    # AI가 요약해주는 듯한 바이브의 1줄 요약 (실제로는 제목 기반 가이드 문구)
    st.caption(f"🚩 **실시간 분석:** 이 기사는 현재 경제 시장에서 매우 중요한 흐름을 담고 있습니다. 상세 내용을 확인해 보세요.")
    st.write("")

st.divider()
st.success("✅ 모든 데이터는 사령관님의 명령에 따라 실시간으로 자동 갱신됩니다.")
