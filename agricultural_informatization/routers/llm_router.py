from fastapi import APIRouter, Body
from typing import Annotated

from utils import execute_sql, logger, get_qwen_answer
from models.response_models import ResponseModel
from models.llm_models import LLMQuestionModel

router = APIRouter()


@router.post("/qwen")
async def _(form: LLMQuestionModel):
    answer = await get_qwen_answer(form.prompt+form.question)
    if answer is None:
        return ResponseModel(
            status='Fail',
            msg="调用时出错..."
        )
    return ResponseModel(
        status='Success',
        msg='调用成功！',
        data={
            "answer": answer
        }
    )