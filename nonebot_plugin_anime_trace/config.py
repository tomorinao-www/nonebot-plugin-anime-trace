from pydantic import BaseModel


class Config(BaseModel):
    # 是否合并转发消息
    animetrace_send_forward: bool = True
    # 是否检测ai图
    animetrace_ai_detect: bool = True
    # 是否分多条消息发送:角色,作品,链接
    animetrace_extract: bool = True
    # 是否发送萌娘百科链接
    animetrace_moegirl: bool = False
    # 自定义搜索链接, 设置为空""则取消
    animetrace_url: str = "zh.wikipedia.org/w/index.php?search="
    # 命令符
    animetrace_cmd: str = "#"
    # 命令关键字
    animetrace_keyword: set[str] = {"识别", "角色", "人物"}
    # 响应优先级
    animetrace_priority: int = 10
    # 动漫模型
    animetrace_model_anime: str = "anime_model_lovelive"
    # galgame模型
    animetrace_model_gal: str = "game_model_kirakira"
    # 一个角色最多返回几个识别结果
    animetrace_max_num: int = 3
    # bot昵称
    nickname: list[str] = ["anime trace"]
