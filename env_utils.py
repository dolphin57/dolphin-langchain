import os
import dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
dotenv.load_dotenv(env_path)

ARK_API_KEY = os.getenv("ARK_API_KEY")
ARK_BASE_URL = os.getenv("ARK_BASE_URL")
