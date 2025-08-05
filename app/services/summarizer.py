from app.config import settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def summarize_lab_report(text: str) -> str:
    api_key = settings.OPENAI_API_KEY
    print("DEBUG: Using OpenAI API Key:", api_key)  # For debugging only, remove once working

    llm = ChatOpenAI(
        api_key=api_key,
        temperature=0.3,
        model="gpt-4-turbo"
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a medical expert. Given the following lab report text, generate a structured JSON summary."
         "Lab Report:\n[[content]]Respond ONLY with JSON. Let the text be concise."
         "JSON Format:\n"
         "{{\n"
         '  "Possible Disease": "...",\n'
         '  "Possible Conditions": "...",\n'
         '  "Tips": "...",\n'
         '  "Type of Doctor to visit": "..."'
         "\n}}"
        ),
        ("human", "{input_report}")
    ])
    chain = prompt_template | llm
    result = chain.invoke({"input_report": text})
    return result.content if hasattr(result, "content") else str(result)
