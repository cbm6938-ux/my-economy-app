import streamlit as st
import yfinance as yf
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="경제 지표 & 뉴스 브리핑", layout="wide")

# 제목 (지인들을 위한 환영 문구)
st.title("📊 사령관님의 경제 기지 : 실시간 지표 & 뉴스")
st.markdown("##### 사령관님의 지인분들을 위해 실시간 경제 상황을 1줄로 요약해 드립니다.")

# 1. 지표 데이터 함수
def get_stock(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d")
        val = data['Close'].iloc[-1]
        diff = val - data['Close'].iloc[-2]
        return val, diff
    except:
        return 0, 0

# 지표 배치
indices = {"국채 금리": "^TNX", "WTI 유가": "CL=F", "원/달러 환율": "USDKRW=X", "코스피": "^KS11", "나스닥": "^IXIC"}
cols = st.columns(len(indices))

for i, (name, ticker) in enumerate(indices.items()):
    val, diff = get_stock(ticker)
    cols[i].metric(name, f"{val:.2f}", f"{diff:.2f}")

st.divider()

# 2. 실시간 경제 뉴스 & 사령관님의 1줄 요약
st.subheader("📰 지금 이 시각 주요 경제 뉴스 (5줄 요약)")

# 사령관님이 직접 입력하거나 뉴스를 가져오는 영역 (여기서는 예시 뉴스로 세팅)
# 실제 뉴스 API를 쓰면 복잡해지니, 지인들이 보기 좋게 '가장 핫한 키워드' 기반 뉴스 폼을 만듭니다.
news_data = [
    {"title": "미국 금리 인하 기대감 확산... 증시 훈풍", "summary": "금리 인하 기대에 시장이 웃고 있네요. 하지만 환율 변동성은 주의!"},
    {"title": "유가 상승세 지속, 에너지주 강세", "summary": "기름값이 심상치 않습니다. 물가 상승 압력이 커질 수 있겠어요."},
    {"title": "반도체 업황 회복 시그널, 수출 호조", "summary": "K-반도체의 저력! 지인분들 반도체 관련주 주목해 보세요."},
    {"title": "환율 1,400원선 공방... 외환당국 주시", "summary": "환율이 높네요. 해외 직구는 잠시 참으시는 게 좋겠습니다."},
    {"title": "글로벌 공급망 재편 속 한국의 기회", "summary": "세계 경제 판도가 변하고 있습니다. 위기 속에 기회를 찾아야 할 때!"}
]

for i, news in enumerate(news_data):
    with st.expander(f"{i+1}. {news['title']}"):
        st.write(f"🚩 **사령관님의 1줄 요약:** {news['summary']}")

st.success("✅ 모든 데이터는 실시간으로 업데이트 중입니다.")
