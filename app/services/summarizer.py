import os
from app.config import settings

# Example: Using OpenAI through LangChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def summarize_lab_report(text: str) -> str:
    llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, temperature=0.3, model="gpt-4-turbo")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Summarize the following patient laboratory report for a doctor, focusing on key findings and abnormalities."),
        ("human", "{input_report}")
    ])
    chain = prompt_template | llm
    result = chain.invoke({"input_report": text})
    return result.content if hasattr(result, "content") else str(result)
