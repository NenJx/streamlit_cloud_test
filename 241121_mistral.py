import os
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv("MISTRAL_API_KEY")

result1 = " "
result2 = " "

client = Mistral(api_key)   # 클라이언트 생성
model = "mistral-large-latest"  # ai 모델

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": """Context: 만약 누군가가 조용하다면 그들은 흰색입니다.
            \n만약 누군가가 젊고 빨갛다면 그들은 흰색입니다. 젊은 사람들은 친절합니다. 만약 누군가가 친절하다면 그들은 둥급니다.
            모든 조용한 사람들은 젊습니다. 빨갛고, 큰 사람들은 친절합니다. 둥근, 빨간 사람들은 흰색입니다. 만약 누군가가 둥글다면 그들은 조용합니다.
            해리는 젊습니다. 밥은 빨강입니다. 밥은 큽니다. \nQuestion: "이것은 해리는 조용하지 않다"라는 문장이 참 인지를 암시하나요?
            \n\n질문의 답변에 필요한 내용을 Context에서 추출해서 나열하세요.""",
        },
    ]
)
result1 = chat_response.choices[0].message.content
print(result1)


chat_response = client.chat.complete(
    model= model,
     messages = [
        {
            "role": "user",
            "content": "파이썬은 재밌어를 영어로 번역해줘.",
        },
    ]
)
result2 = chat_response.choices[0].message.content
print(result2)