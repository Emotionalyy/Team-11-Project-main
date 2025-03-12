from typing import Optional
from pydantic import BaseModel

from utils import base_prompt


class LLMQuestionModel(BaseModel):

    question: str
    """提问内容"""

    prompt: str = base_prompt
    """用户提供的 Base Prompt"""