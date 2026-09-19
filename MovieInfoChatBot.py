import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage
)
from langchain_core.prompts import ChatPromptTemplate

# Load .env
load_dotenv()


# =========================
# GEMINI MODEL
# =========================
 
model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)



from langchain_core.output_parsers import PydanticOutputParser


from pydantic import BaseModel
from typing import Optional , List



class Movie(BaseModel):
    title:str
    release_year: int
    genre: List[str]
    director: Optional[str] 
    cast: List[str]
    rating:Optional[float]
    summary:str    
    
    
    
parser= PydanticOutputParser(pydantic_object=Movie)



prompt = ChatPromptTemplate.from_messages([
    ("system", """
Extract movie information from the paragraph
        {format_instruction}
     """),
    ("human", "{paragraph}")
])

para = input("give you paragraph")

final_prompt = prompt.invoke(
    {"paragraph":para,
     'format_instruction':parser.get_format_instructions()
    }
)
response = model.invoke(final_prompt)

# Gemini ka actual text nikalo
if isinstance(response.content, list):
    text = "".join(
        block.get("text", "")
        for block in response.content
        if isinstance(block, dict)
    )
else:
    text = response.content

# JSON ko Pydantic model mein parse karo
result = parser.parse(text)

print(result)