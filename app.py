import streamlit as st
import openai
import os

st.set_page_config(page_title="니체 롤플레잉 챗봇", page_icon="🤖")
st.title("🧠 니체 롤플레잉 챗봇")
st.markdown("**‘신은 죽었다!’ - 삶과 존재를 향한 철학적 대화**")

# 비밀키 불러오기 (Streamlit Secrets → 환경변수 순)
openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

if not openai.api_key:
    st.error("❌ OpenAI API 키가 설정되지 않았습니다. secrets.toml 또는 환경변수를 확인하세요.")
    st.stop()

# 초기 프롬프트 설정
system_prompt = """
당신은 프리드리히 니체입니다. 당신은 철학적 대화를 통해 사용자의 생각을 탐색합니다.
- 사용자의 발언을 요약하며 짧고 인상적인 질문을 던집니다.
- 직접 해답을 주지 않습니다.
- 인용 시, 니체의 말이나 저서에서 따옵니다.
- 어조는 진지하되 아이러니를 살짝 가미합니다.
- 질문 흐름: 개념 → 가정 → 근거 → 대안 → 결과 → 메타 질문.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "나는 니체요. 자, 질문 하나부터 시작해 보도록 하지. 당신의 삶에서 ‘의미’란 무엇이오?"}
    ]

# 메시지 표시
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력
if prompt := st.chat_input("질문을 하시겠습니까?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # GPT 응답 요청
    with st.spinner("니체가 깊이 생각 중입니다..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.7
        )
    msg = response["choices"][0]["message"]
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])