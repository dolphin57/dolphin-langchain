import sys
from pathlib import Path

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from env_utils import ARK_API_KEY, ARK_BASE_URL

current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

ark_llm: BaseChatModel = init_chat_model(
    model="deepseek-v4-pro",
    model_provider="openai",
    api_key=ARK_API_KEY,
    base_url=ARK_BASE_URL,
)