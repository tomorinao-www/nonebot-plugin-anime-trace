<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-anime-trace

_✨ 通过ai.animedb.cn的api识别动漫、galgame角色 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/tomorinao-www/nonebot-plugin-anime-trace.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-anime-trace">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-anime-trace.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>


<!-- ## 📖 介绍

 -->


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

示例: #识别gal

大括号内{}为必要参数, 中括号内[]为可选参数, 默认使用动漫模型

附带一张图片、或回复一张图片、或再发送一张图片

可以自定义命令符、命令关键字

## ⚙️ 配置

如果需要自定义配置，请在 nonebot2 项目的`.env`文件中添加配置

| 配置项                 | 必填 | 默认值                 | 说明 |
|:----------------------:|:---:|:----------------------:|:----:|
| animetrace_cmd         | 否 | "#"                     | 命令符 |
| animetrace_keyword     | 否 | ["识别", "角色", "人物"] | 命令关键字 |
| animetrace_priority    | 否 | 10                      | 响应优先级 |
| animetrace_model_anime | 否 | "pre_stable"            | 动漫模型 |
| animetrace_model_gal   | 否 | "game_model_kirakira"   | galgame模型 |
| animetrace_max_num     | 否 | 3                       | 一个角色最多返回几个识别结果 |
| nickname               | 否 | ["anime trace"]         | bot昵称列表 |
