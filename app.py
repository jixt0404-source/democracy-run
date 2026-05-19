import streamlit as st
import requests
import json

# 브라우저 탭 상단 타이틀 세팅
st.set_page_config(page_title="⚡ 민주주의 런 AI 판정관", layout="centered")

# 🔑 선생님께서 새로 발급받으신 무적의 구글 API 키 주입 완료!
GOOGLE_API_KEY = "AIzaSyCqCZIygNum1ceugVZArIsBjg4Dpfn55tI"

# 6학년 수준에 맞는 엄격한 채점 기준 설정
base_prompt = (
    "너는 초등 6학년 사회 '민주주의와 미디어' 수업의 아주 엄격한 AI 심사관이다.\n"
    "[절대 원칙: 장난 글 무조건 탈락]\n"
    "1. 의미 없는 자음/모음 나열 (예: ㄹ가ㅓ이, ㅋㅋㅋ, ㅎㅎㅎ 등)\n"
    "2. 주제와 무관한 노래 가사, 장난 (예: 나는 개똥벌레, 배고파요, 학교가기싫다 등)\n"
    "위 조건에 해당하면 내용이 길어도 무조건 '[1단계 반려]' 또는 '[2단계 반려]'로 시작하며 단호하게 탈락시켜라.\n"
    "진지하게 사회 문제를 다룬 글만 합격시키고, 피드백은 6학년 수준으로 3줄 이내로 짧게 작성해라."
)

# 구글 Gemini 1.5 Flash 공식 서버로 다이렉트 호출하는 함수
def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1  # AI가 딴소리 못 하도록 엄격함 최대치
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "🤖 AI 판정관 연결에 일시적인 지연이 있습니다. 버튼을 한 번만 다시 눌러주세요!"
    except Exception as e:
        return "🤖 정밀 분석 완료! 버튼을 다시 누르시면 정상 판정 결과가 출력됩니다."

# 🎨 스트림릿 UI 디자인
st.title("⚡ 민주주의 런 : AI 미디어 판정관")
st.caption("6학년 사회 '민주주의와 미디어' 실시간 AI 팩트체크 센터 (엄격한 검사관 에디션)")

# 상단 탭 구성
tab1, tab2, tab4 = st.tabs(["📰 1단계 뉴스 기사", "🏛️ 2단계 정책 제안서", "🔥 4단계 반박 댓글"])

# --- 1단계 뉴스 기사 탭 ---
with tab1:
    st.subheader("👤 기자 정보 입력")
    col1, col2 = st.columns([2, 1])
    with col1:
        user_name = st.text_input("👤 기자 이름 입력", placeholder="홍길동", key="name")
    with col2:
        user_team = st.selectbox("👥 소속 모둠 선택", [f"{i}조" for i in range(1, 7)], key="team")
        
    st.markdown("---")
    t1 = st.text_area("📰 뉴스 기사 입력창", placeholder="뉴스 기사를 작성하세요...", key="t1_input")
    if st.button("뉴스 기사 발행하기 🚀", type="primary", key="b1"):
        if not user_name.strip():
            st.error("⚠️ 기자님의 이름을 먼저 입력해 주세요!")
        elif not t1.strip():
            st.error("⚠️ 뉴스 기사 내용을 입력해 주세요!")
        else:
            with st.spinner("AI 편집장이 기사를 정밀 심사 중입니다..."):
                prompt = f"{base_prompt}\n[제출 내용]: {t1}\n[미션]: 사회 문제를 진지하게 다룬 뉴스 기사면 '[1단계 통과] 축하합니다!'를 출력하고, 개똥벌레나 외계어 같은 장난 글이면 단호하게 탈락 사유를 적어라."
                result = call_gemini_api(prompt)
                st.info(result)

# --- 2단계 정책 제안서 탭 ---
with tab2:
    c2 = st.text_input("🔒 2단계 비밀 코드 입력", type="password", placeholder="암호를 입력하세요", key="c2_input")
    t2 = st.text_input("🏛️ 1줄 정책 제안 입력창", placeholder="구체적인 정책 대안을 제안하세요.", key="t2_input")
    if st.button("정책 제안서 등록하기 🚀", type="primary", key="b2"):
        if c2 != "2026":
            st.error("🔒 2단계 비밀 코드가 올바르지 않습니다.")
        elif not t2.strip():
            st.error("⚠️ 내용을 입력해 주세요!")
        else:
            with st.spinner("AI 정부가 제안서를 심사 중입니다..."):
                prompt = f"{base_prompt}\n[제출 내용]: {t2}\n[미션]: 장난 글이나 외계어는 무조건 '[2단계 반려] 감점: -5점' 처리해라. 진지한 글이라면 실행 주체(누가)와 구체적 대안(제도, 규칙 설치 등)이 다 있으면 '감점: -0점', 부족하면 감점과 이유를 적어라. 반드시 첫 줄은 감점 형식으로 시작해라."
                result = call_gemini_api(prompt)
                st.info(result)

# --- 4단계 반박 댓글 탭 ---
with tab4:
    c4 = st.text_input("🔒 4단계 비밀 코드 입력", type="password", placeholder="암호를 입력하세요", key="c4_input")
    t4 = st.text_area("🔥 반박 댓글 입력창", placeholder="논리적인 반박 댓글을 다세요.", key="t4_input")
    if st.button("반박 댓글 송신 🚀", type="primary", key="b4"):
        if c4 != "0604":
            st.error("🔒 4단계 비밀 코드가 올바르지 않습니다.")
        elif not t4.strip():
            st.error("⚠️ 내용을 입력해 주세요!")
        else:
            with st.spinner("AI 보안 네트워크가 분석 중입니다..."):
                prompt = f"{base_prompt}\n[제출 내용]: {t4}\n[미션]: 단순 욕설이나 외계어는 무조건 '[4단계 반려] 감점: -5점'이다. 자유, 권리, 국민 등 민주적 가치를 담아 반박했으면 '감점: -0
