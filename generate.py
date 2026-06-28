from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def generate(input_query, top_chunks):

    context = []
    for i in range(len(top_chunks)):
        context.append(top_chunks[i][2]['text'])
        
    context = "\n\n---\n\n".join(context)
    
    prompt = f"""You are answering questions using the provided context from astrophysics articles.
                Use the context to answer the question. You may reason from and connect information in the 
                context to address the question, even if it isn't stated word-for-word. If the context partially 
                addresses the question, give what it does say and be clear about what it doesn't cover. Only 
                say "I don't know based on the provided information." if the context contains nothing relevant 
                to the question at all. Do not invent facts that aren't supported by the context.
                Context: {context}
                Question: {input_query}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content