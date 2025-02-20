<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/refs/heads/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/88c60174f63914be62251ffc192cb8b408bbc845/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></a>
</div>

<div align="center">

# nonebot-plugin-anime-trace

_✨ 通过 ai.animedb.cn 的 api 识别动漫、galgame 角色 ✨_

<a href="https://github.com/tomorinao-www/nonebot-plugin-anime-trace/blob/main/LICENSE">
  <img src="https://img.shields.io/github/license/tomorinao-www/nonebot-plugin-anime-trace.svg" alt="License">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-anime-trace">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-anime-trace.svg?style=flat&logo=pypi&logoColor=fff&labelColor=3775A9" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-anime-trace">
  <img src="https://img.shields.io/badge/Python-3.10+-f09?style=flat&logo=Python&logoColor=fc5&labelColor=3776AB" alt="Python">
</a>
<a href="https://github.com/tomorinao-www/naotool">
  <img src="https://img.shields.io/github/stars/tomorinao-www/nonebot-plugin-anime-trace.svg?style=social" alt="stars">
</a>
<a href="https://github.com/tomorinao-www/naotool">
  <img src="https://img.shields.io/github/forks/tomorinao-www/nonebot-plugin-anime-trace.svg?style=social" alt="forks">
</a>
</div>

## 最新情报

网站 api 更新，已适配。 2025/02/20

前两天网站抽风，现已恢复正常。2023/08/25

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-anime-trace

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

    pip install nonebot-plugin-anime-trace

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-anime-trace"]

</details>

## 🎉 使用

默认配置下

命令: {#} {识别|角色|人物|} [gal|动漫]

说明：命令符不是命令头，只要包含命令符和命令关键字就会触发响应，例如“foo 识别 foo#foo”也可以触发

大括号内{}为必要关键字, 中括号内[]为可选参数, 默认使用动漫模型

附带一张图片、或回复一张图片、或再发送一张图片

可以自定义命令符、命令关键字

<details open>
<summary>
示例:
</summary>

| ![image](./img/use_ex01.jpg) | ![image](./img/use_ex02.jpg) |
| ---------------------------- | ---------------------------- |

| ![image](./img/use_ex03.jpg) | ![image](./img/use_ex04.jpg) |
| ---------------------------- | ---------------------------- |

</details>

## ⚙️ 配置

如果需要自定义配置，请在 nonebot2 项目的`.env`文件中添加配置

```py
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
    animetrace_model_anime: str = "pre_stable"
    # galgame模型
    animetrace_model_gal: str = "game_model_kirakira"
    # 一个角色最多返回几个识别结果
    animetrace_max_num: int = 3
    # bot昵称
    nickname: list[str] = ["anime trace"]
```

动漫模型和 galgame 模型请前往 [ai.animedb.cn](https://ai.animedb.cn)查看

## 常见问题 Q&A

### 没有识别到任何角色

网站没有识别到该图中的角色

### 出错啦~可能是图里角色太多了 content:{code:-1}

网站处理图片出错，可能是图中角色过多、或者网站后端挂了，可以尝试裁剪图片

### 识别失败，换张图片试试吧~<Response [504 Gateway Time-out]>

网站接收图片出错，可能是图中角色过多、或者网站后端挂了，可以尝试裁剪图片

### 其他

请先去[ai.animedb.cn](https://ai.animedb.cn)尝试能否识别，若能识别，联系我更新；若不能识别，等待站长修复

## TODO

- [x] 增加 ai 绘图鉴别
- [ ] 添加结果图片对比
- [ ] 跨平台兼容

## 跨平台兼容

### 合并转发消息

> send_group_forward_msg
>
> | 字段     | 类型       | 说明           |
> | -------- | ---------- | -------------- |
> | group_id | uint       | 群号           |
> | messages | List[Node] | 自定义转发消息 |

> Node
>
> | 字段    | 类型                                | 说明     |
> | ------- | ----------------------------------- | -------- |
> | uin     | string                              | QQ 号    |
> | name    | string                              | 昵称     |
> | content | List[OneBotSegment] / OneBotSegment | 消息内容 |

> send_private_forward_msg
>
> | 字段     | 类型       | 说明           |
> | -------- | ---------- | -------------- |
> | user_id  | uint       | 好友 QQ 号     |
> | messages | List[Node] | 自定义转发消息 |

## 赞助

> 救救 developer，孩子吃不起饭了
> | ![donate-wx](./img/donate-wx.jpg) | ![donate-wx](./img/donate-alipay.jpg) |
> | --------------------------------- | ------------------------------------- |
