from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def generate(input_query, top_chunks):

    context = []
    for i in range(len(top_chunks)):
        context.append(top_chunks[i][2]['text'])
        
    context = "\n\n---\n\n".join(context)
    
    prompt = f"""Answer the question using only the provided context. If the answer isn't in the context, say "I don't know based on the provided information."
    Context: {context} 
    Question: {input_query}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content