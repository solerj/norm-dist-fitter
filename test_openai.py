from openai import OpenAI
client = OpenAI()

resp = client.responses.create(
    model="gpt-4o-mini",
    input="Explain bias vs variance with a tiny numeric example."
)
print(resp.output_text)