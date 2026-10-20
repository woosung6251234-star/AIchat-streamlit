import streamlit as st
import time
import random

# 페이지 설정
st.set_page_config(page_title="AIchat-streamlit", page_icon="🤖", layout="centered")

# 사이드바 기능 구성
with st.sidebar:
    st.header("⚙️ 챗봇 설정")
    bot_mood = st.selectbox("챗봇의 말투 모드", ["다정형", "장난꾸러기형", "시크형"])
    
    # 대화 기록 초기화 버튼
    if st.button("🗑️ 대화 내용 지우기"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 AIchat-streamlit")
st.caption(f"현재 모드: **{bot_mood}**")
st.markdown("---")

# 대화 기록 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력창
prompt = st.chat_input("메시지를 입력하세요 (예: 심심해, 메뉴 추천, 인공지능, 퀴즈)")

def generate_rule_response(user_text, mood):
    text = user_text.strip()
    
    # 1. 인사
    if any(k in text for k in ["안녕", "반가워", "하이"]):
        if mood == "다정형":
            return "안녕하세요! 만나서 정말 반가워요. 오늘 하루는 어떠신가요? 😊"
        elif mood == "장난꾸러기형":
            return "왓썹! 오늘도 재미있게 놀아보자구! 🤪"
        else:
            return "안녕하세요. 무슨 일이시죠?"

    # 2. 인공지능 관련 질문 (설명형 답변으로 변경)
    elif "인공지능" in text or "ai" in text.lower():
        topics = [
            "인공지능(AI)은 인간의 학습 능력, 추론 능력, 지각 능력을 인공적으로 구현한 컴퓨터 시스템을 뜻합니다.",
            "현재 주목받는 LLM(대형 언어 모델)은 수많은 텍스트 데이터의 맥락을 통계적으로 학습해 문장을 완성해내는 기술입니다.",
            "인공지능의 핵심 분야에는 머신러닝, 딥러닝, 컴퓨터 비전, 자연어 처리(NLP) 등이 있습니다."
        ]
        return random.choice(topics)

    # 3. 메뉴/음식 추천
    elif any(k in text for k in ["배고파", "메뉴", "점심", "저녁", "음식"]):
        menus = ["따뜻한 라면", "치킨과 콜라", "제육볶음", "돈가스", "떡볶이", "마라탕", "초밥"]
        choice = random.choice(menus)
        if mood == "다정형":
            return f"식사는 든든하게 챙겨 드셔야 해요! 오늘은 **'{choice}'** 어떠신가요?"
        elif mood == "장난꾸러기형":
            return f"제가 점지해 드립니다. 오늘 메뉴는 무조건 **'{choice}'** 먹기!"
        else:
            return f"추천 메뉴: {choice}."

    # 4. 심심할 때
    elif any(k in text for k in ["심심해", "놀아줘"]):
        jokes = [
            "Q. 왕이 넘어지면 뭘까요? ➔ A. 킹콩!",
            "Q. 세상에서 가장 가난한 왕은? ➔ A. 최저임금",
            "Q. 신발이 화나면? ➔ A. 신발끈!"
        ]
        return f"심심하시군요! 썰렁 퀴즈 하나 드릴게요.\n\n{random.choice(jokes)}"

    # 5. 시간/현재 정보
    elif any(k in text for k in ["몇 시", "시간", "날짜"]):
        from datetime import datetime
        now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
        return f"현재 시간은 {now} 입니다."

    # 6. 기본 응답
    else:
        if mood == "다정형":
            return f"'{text}'에 대해 말씀해 주셨네요. 더 자세한 이야기가 궁금해요!"
        elif mood == "장난꾸러기형":
            return f"'{text}'? 무슨 소린지 잘 모르겠지만 아무튼 신나네요!"
        else:
            return f"입력값 '{text}'을 확인했습니다."

if prompt:
    # 사용자 입력 화면 출력 및 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 답변 생성
    bot_response = generate_rule_response(prompt, bot_mood)

    # 챗봇 답변 스트리밍 연출 및 화면 출력
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in bot_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # 답변 세션에 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})
