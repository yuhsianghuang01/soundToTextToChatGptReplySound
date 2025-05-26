from openai import OpenAI

client = OpenAI(api_key="sk-HZ-ShOnh8z3VdiJmSe9wjQ", base_url="http://llm.aidc.com.tw/v1")

def call_llm_api(prompt):
    """
    Call the LLM API with the given prompt.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # Example usage
    prompt = "What is the capital of France?"
    response = call_llm_api(prompt)
    print(response)