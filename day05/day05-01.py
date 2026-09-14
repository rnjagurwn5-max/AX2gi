import os
from openai import OpenAI

# client = OpenAI(api_key="=your_api_key_here")
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "친절한 도우미"},
#         ]
# )

# print(response.choices[0].message.content)


from openai import OpenAI

def ask_llm(api_key, model, question):
    client = OpenAI(api_key=api_key)
    
    # 1. 누락된 API 호출 구문 추가
    response = client.chat.completions.create(
        model=model,  # 2. "model" -> model (따옴표 제거)
        messages=[
            {"role": "system", "content": "친절한 도우미"},
            {"role": "user", "content": question}  # 3. "question" -> question (따옴표 제거)
        ]
    )
    
    return response.choices[0].message.content, response.usage

# 실제 사용 시 API 키 전체를 넣어주세요.
my_api_key = "your_api_key_here" 
answer, usage = ask_llm(my_api_key, "gpt-4o-mini", "안녕하세요. 오늘 날씨 어떤가요?") 

print("Answer:", answer)
# 참고용: 토큰 사용량 출력.
print("Usage:", usage.total_tokens) 

