import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI


def multiply(a:float, b:float) -> float:
    """ useful for multiplying two numbers. """
    return a * b

llm = GoogleGenAI(
    model = 'gemini-2.5-flash',
    api_key = 'please key placeholder'
)

agent = FunctionAgent(
    name = 'calc',
    description = 'multiplies numbers',
    tools = [multiply],
    llm = llm
)

async def main():
    response = await agent.run("what is 1234 * 4567?")
    print(f"Agent response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
