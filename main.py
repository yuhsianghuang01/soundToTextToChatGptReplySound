from openai import OpenAI

client = OpenAI(api_key="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", 
                base_url="https://api.groq.com/openai/v1"
                )




def call_llm_api(prompt):
    """
    Call the LLM API with the given prompt.
    """
    response = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "system", "content": "回覆的內容請永遠使用繁體中文"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # Example usage
    prompt = "What is the capital of France?"
    response = call_llm_api(prompt)
    print(response)