import openai

def openai_response(prompt, personality = "You are a helpful assistant."):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":
            personality},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\nUser:"]
    )
    return response["choices"][0]["message"]["content"]