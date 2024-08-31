from pydantic import BaseModel


class Config(BaseModel):
    # 是否检测ai图
    animetrace_ai_detect: bool = False
    # 命令符
    animetrace_cmd: str = "#"
    # 命令关键字
    animetrace_keyword: set[str] = {"识别", "角色", "人物"}
    # 响应优先级
    animetrace_priority: int = 10
    # 动漫模型
    animetrace_model_anime: str = "pre_stable"
    # galgame模型
    animetrace_model_gal: str = "game_model_kirakira"
    # 一个角色最多返回几个识别结果
    animetrace_max_num: int = 3
    # bot昵称
    nickname: list[str] = ["anime trace"]

