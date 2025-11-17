import os
from tools import *
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     return ("It's always sunny in {city}!")

# # Initialize the OpenAI chat model
# model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=os.getenv("OPENAI_API_KEY"))

# # Define tools (example: a simple search tool)
# tools = [get_weather]

# agent = create_agent(
#     model=model,
#     tools=tools,
#     system_prompt="You are a helpful assistant",
# )

# # Run the agent
# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
# )

# print(result["messages"][-1].content)