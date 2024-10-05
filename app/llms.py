from typing import Any, Optional, Dict
from langchain_fireworks import ChatFireworks
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))


FIREFUNC_MODEL: str = "accounts/fireworks/models/firefunction-v2"
LLAMA_70B_MODEL: str = "accounts/fireworks/models/llama-v3p1-70b-instruct"

model4omini = ChatOpenAI(model="gpt-4o-mini")
model4o = ChatOpenAI(model="gpt-4o")

llama_70b = ChatFireworks(model=LLAMA_70B_MODEL)
firefunc = ChatFireworks(model=FIREFUNC_MODEL)
