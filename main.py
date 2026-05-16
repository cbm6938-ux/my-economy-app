import streamlit as st
import feedparser
from datetime import datetime

# 1. 페이지 설정 (화이트 테마 & 모바일 가독성 최우선)
st.set_page_config(page_title="경제 뉴스 브리핑", layout="wide")

# 🎨 디자인 마감: 지인들이 읽기 편한 가장 깔끔한 스타일
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    .news-wrapper {
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #eeeeee;
        background-color: #ffffff;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .sector-label {
        color: #0066cc;
        font-weight: 800;
        font-size: 0.9rem;
        margin-bottom: 6px;
        display: block;
    }
    .news-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #222222 !important;
        text-decoration: none !important;
        line-height: 1.5;
    }
    .news-title:hover { color: #0066cc !important; }
    </style>
    """, unsafe_allow_html=True)

# 헤더 섹션
st.title("📰 실시간 섹터별 경제 브리핑")
st.write(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.divider()

# 2. 뉴스 데이터 엔진 (섹터별 10개 추출)
@st.cache_data(ttl=600)
def fetch_final_news():
    # 사령관님이 명시하신 종목별 섹터 구분
    sectors = {
        "📉 증시/금융": "주식 시장 시황 전망",
        "🏢 부동산": "부동산 정책 가격 동향",
        "💻 산업/기술": "반도체 IT 인공지능 산업",
        "🌍 국제/거시": "환율 금리 세계 경제 소식"
    }
    
    final_list = []
    for name, query in sectors.items():
        url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        # 섹터별로 가장 중요한 2~3개씩 수집
        for entry in feed.entries[:3]:
            final_list.append({"sector": name, "title": entry.title, "link": entry.link})
            if len(final_list) >= 10: break
        if len(final_list) >= 10: break
    return final_list

# 3. 화면 출력 (사령관님이 원하신 깔끔한 뉴스 10개)
try:
    news_data = fetch_final_news()
    if news_data:
        for item in news_data:
            st.markdown(f"""
                <div class="news-wrapper">
                    <span class="sector-label">{item['sector']}</span>
                    <a href="{item['link']}" target="_blank" class="news-title">{item['title']}</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("데이터를 가져오는 중입니다...")
except:
    st.error("뉴스 센터 연결에 문제가 발생했습니다.")

st.divider()
st.caption("사령관의 지휘 하에 운영되는 뉴스 브리핑 시스템 v1.0")
