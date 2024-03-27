from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama

from app.logger import logger
from app.schemas import Message


model = Llama('/models/llama-2-7b-chat.Q4_K_M.gguf')

system_prompt = """You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

# store conversation
conversation = []

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
    """
    Generates new prompt utilizing previous conversation.
    Sample output:
        <s>[INST] <<SYS>> {your_system_message} <</SYS>>
        {user_message_1} [/INST] {model_reply_1}</s>
        <s>[INST] {user_message_2} [/INST]
    """
    final_prompt = f'<s>[INST] <<SYS>> {system_prompt} <</SYS>> '
    if conversation:
        for message in conversation:
            final_prompt += f"{message['me']} [/INST] {message['llm']}</s><s>[INST] \n"

    return final_prompt + f'{prompt} [/INST]'


@app.post("/")
async def read_root(request: Message) -> dict:
    logger.info(f'INCOMING PROMPT: {request.message}')
    prompt = get_prompt(request.message)
    output = model(prompt, max_tokens=500)['choices'][0]['text']
    logger.info(f'LLM RESPONSE: {output}')

    conversation.append({
        'me': request.message,
        'llm': output,
    })

    return {
        "id": 1,
        "user": "LLM",
        "content": output,
    }
