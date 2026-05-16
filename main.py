import streamlit as st
import yfinance as yf

# 페이지 설정
st.set_page_config(page_title="경제 지표 대시보드", layout="wide")
st.title("📊 실시간 경제 지표 대시보드")

# 데이터 추출 함수
def get_stock(ticker):
    data = yf.Ticker(ticker).history(period="2d")
    return (data['Close'].iloc[-1], data['Close'].iloc[-1] - data['Close'].iloc[-2])

# 5대 지수 설정
indices = {"미국 10년물 국채 금리": "^TNX", "WTI 유가": "CL=F", "원/달러 환율": "USDKRW=X", "코스피": "^KS11", "코스닥": "^KQ11"}
cols = st.columns(3)

# 상단 지표 배치
for i, (name, ticker) in enumerate(list(indices.items())[:3]):
    val, diff = get_stock(ticker)
    cols[i].metric(name, f"{val:.2f}", f"{diff:.2f}")
    if "국채" in name:
        st.info("💡 **국채 금리 팁:** 금리가 오르면 시장 이자 부담이 커져요. 경제 기초 체력 지표!")

st.divider()
# 하단 지표 배치
cols2 = st.columns(2)
for i, (name, ticker) in enumerate(list(indices.items())[3:]):
    val, diff = get_stock(ticker)
    cols2[i].metric(name, f"{val:.2f}", f"{diff:.2f}")

st.success("✅ 실시간 데이터 업데이트 완료 (Powered by GitHub)")
