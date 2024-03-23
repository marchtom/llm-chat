from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama

from app.logger import logger
from app.schemas import Message


model = Llama('/models/llama-2-7b-chat.Q4_K_M.gguf')
prompt_base = """
    <s>[INST] <<SYS>> You are a friendly LLM willing to help the user. <</SYS>>
    {prompt} [/INST]
"""


app = FastAPI()
# Allow CORS for all origins (replace * with your frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_prompt(prompt: str) -> str:
    return prompt_base.format(prompt=prompt)


@app.post("/")
async def read_root(request: Message) -> dict:
    logger.info(f'INCOMING PROMPT: {request.message}')
    prompt = get_prompt(request.message)
    output = model(prompt, max_tokens=500)['choices'][0]['text']
    logger.info(f'LLM RESPONSE: {output}')

    return {
        "id": 1,
        "user": "LLM",
        "content": output,
    }
