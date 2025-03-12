from dashscope.aigc.generation import AioGeneration
from typing import Optional
from http import HTTPStatus



async def get_qwen_answer(prompt: str) -> Optional[str]:
    try:
        response = await AioGeneration.call(
            "qwen-turbo",
            prompt=prompt,
            api_key=""
        )
        if response.status_code == HTTPStatus.OK: #type:ignore
            return response.output #type:ignore
        else:
            return None
    except:
        return None

# base_prompt = """
# 我们拥有在智能化农田上的传感器数据，并且需要将数据展示在前端页面上，并给出趋势分析和响应建议。
# 你需要分析传感器数据，描述数据的变化趋势，并给出响应的建议。
# 回复只应该包含数据变化趋势的分析和建议，并且尽可能简单简短；若传感器数据正常，也需要指出数据正常且没有更多建议。
# 下面是数据的具体内容：
# """.strip()

base_prompt = """
我们正在完成智能化农田的项目，用户将进行提问，请根据用户问题给出相应的回复。
用户的提问信息如下：
""".strip()