import os
import json
import streamlit as st
from openai import OpenAI
# from dotenv import load_dotenv

# 데이터 로드
# load_dotenv()
client = OpenAI(api_key=os.getenv("GPT_API_KEY"))

# NPC 데이터 로드 함수
def load_npc_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

npc_data = load_npc_data("./NpcData.json")

# GPT API 호출 함수
def chat_with_npc(prompt, npc_description, history):
    try:
        # 메시지 구성
        messages = [{"role": "system", "content": npc_description}] + history + [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(messages=messages, model="gpt-4")
        npc_response = response.choices[0].message.content

        # 감정 분석 추가 호출
        emotion_prompt = f"이 텍스트의 감정을 딱 하나의 단어로 표현하세요.: '{npc_response}'"
        emotion_response = client.chat.completions.create(
            messages=[{"role": "user", "content": emotion_prompt}],
            model="gpt-4"
        )
        emotion = emotion_response.choices[0].message.content.strip()
        return f"({emotion}) {npc_response}"
    except Exception as e:
        return f"Error: {e}"

# 상태 초기화 함수
def initialize_state():
    defaults = {
        "last_input_type": None,
        "current_npc": None,
        "chat_history": [],
        "npc_response_done": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# NPC 변경 시 상태 초기화
def handle_npc_change(selected_npc_key):
    if st.session_state.current_npc != selected_npc_key:
        st.session_state.current_npc = selected_npc_key
        st.session_state.chat_history.clear()
        st.session_state.npc_response_done = True

# NPC 이미지 표시 함수
def display_npc_image(npc_key):
    npc_images = {
        "👧🏾릴리": ("DALL·E_Lily_default.png", "릴리"),
        "👨🏼‍🦰그리모": ("DALL·E_Grimo_default.png", "그리모"),
        "👩🏻‍🦳카시아": ("DALL·E_Kasia_default.png", "카시아"),
    }
    if npc_key in npc_images:
        st.image(npc_images[npc_key][0], caption=npc_images[npc_key][1], width=250)

# 대화 히스토리 출력 함수
def display_chat_history():
    st.markdown("---")
    st.markdown("**💬 대화 히스토리**")
    for message in st.session_state.chat_history:
        role = "**You:**" if message["role"] == "user" else f"**{selected_npc['name']}**:"
        st.markdown(f"{role} {message['content']}")

# Streamlit 애플리케이션
st.title("살아있는 NPC와 함께 풀어내는 이야기")
initialize_state()  # 상태 초기화

# NPC 선택
npc_choices = npc_data["npc_list"]
npc_key = st.radio(
    "NPC를 선택하세요", 
    list(npc_choices.keys()), 
    format_func=lambda x: npc_choices[x]["name"], 
    horizontal=True
)
selected_npc = npc_choices[npc_key]
handle_npc_change(npc_key)
display_npc_image(npc_key)

# 행동 또는 대화 입력
st.markdown("---")
st.subheader("행동 또는 대화 시도")
action, player_write = None, None

if st.session_state.npc_response_done:
    col1, col2 = st.columns(2)

    # 행동 버튼
    with col1:
        actions = {
            "공격하기": "당신은 플레이어로부터 공격을 당했습니다.",
            "선물주기": "당신은 플레이어로부터 선물을 받았습니다.",
            "서성이기": "당신의 주변에서 플레이어가 서성이고 있습니다.",
        }
        cols = st.columns(len(actions))  # actions의 항목 수만큼 열 생성
        for col, (label, message) in zip(cols, actions.items()):
            with col:
                if st.button(label):
                    action = message
                    st.session_state.last_input_type = "action"
                    st.session_state.npc_response_done = False

    # 대화 입력
    with col2:
        player_write = st.text_input("NPC에게 말을 걸어보세요!")
        if player_write and not action:
            st.session_state.last_input_type = "text"
            st.session_state.npc_response_done = False

# 행동과 대화 입력 처리
if st.session_state.last_input_type == "action" and action:
    prompt = action
elif st.session_state.last_input_type == "text" and player_write:
    prompt = player_write.strip()
else:
    prompt = None

# GPT 호출 및 응답 처리
if prompt:
    with st.spinner("🔮 NPC가 반응하는 중..."):
        npc_response = chat_with_npc(prompt, selected_npc["description"], st.session_state.chat_history)
        if st.session_state.last_input_type == "text":
            st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": npc_response})
        st.session_state.npc_response_done = True

    # 응답 출력
    st.markdown(f"**{selected_npc['name']}**:")
    st.markdown(npc_response)

display_chat_history()  # 대화 히스토리 출력
