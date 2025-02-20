import ssl
import re
from base64 import b64encode
from io import BytesIO

from PIL import Image
from urllib.parse import quote
from nonebot import logger, on_keyword, get_plugin_config
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageSegment,
    PrivateMessageEvent,
    GroupMessageEvent,
    MessageEvent,
)
from nonebot.adapters.onebot.v11.helpers import extract_image_urls
from nonebot.params import Arg
from nonebot.rule import Rule
from nonebot.exception import ActionFailed, ApiNotAvailable, SkippedException
from nonebot.internal.matcher import Matcher
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata


from naotool import NOException, get_imgs, AutoCloseAsyncClient
from .config import Config


__plugin_meta__ = PluginMetadata(
    name="识别动漫gal角色",
    description="通过ai.animedb.cn的api识别动漫、galgame角色",
    usage="""命令: {#} {识别|角色|人物} [gal|动漫]
示例: #识别gal
大括号内{}为必要关键字, 中括号内[]为可选参数, 默认为动漫模型
附带一张图片、或回复一张图片、或再发送一张图片
可以自定义命令符、命令关键字""",
    type="application",
    homepage="https://github.com/tomorinao-www/nonebot-plugin-anime-trace",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

conf: Config = get_plugin_config(Config)


async def _cmd_check(bot: Bot, event: MessageEvent):
    txt_msg = event.message.extract_plain_text().strip()
    return conf.animetrace_cmd in txt_msg


acg_trace = on_keyword(
    conf.animetrace_keyword,
    rule=Rule(_cmd_check),
    priority=conf.animetrace_priority,
    block=True,
)


@acg_trace.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher, state: T_State):
    # 选择模型
    txt_msg = event.message.extract_plain_text().strip()
    if "gal" in txt_msg:
        state["model"] = conf.animetrace_model_gal
        state["mode"] = "galgame"
    else:
        state["model"] = conf.animetrace_model_anime
        state["mode"] = "动漫"
    # 获取图片链接
    message = event.reply.message if event.reply else event.message
    if imgs := message["image"]:
        matcher.set_arg("imgs", imgs)


@acg_trace.got("imgs", prompt="请发送需要识别的图片")
async def get_image(state: T_State, imgs: Message = Arg()):
    img_urls = extract_image_urls(imgs)
    if not img_urls:
        await acg_trace.reject("没有找到图片, 请重新发送")
    state["img_urls"] = img_urls


@acg_trace.handle()
async def main(bot: Bot, event: MessageEvent, state: T_State):
    # 拿到图片
    img_urls = state["img_urls"]
    img_url = re.sub(r"&amp;", "&", img_urls[0])  # 处理 HTML 转义符

    ssl_context = ssl.create_default_context()  # 创建 SSL 兼容上下文，适配 QQ 服务器
    ssl_context.options |= (
        ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
    )  # 关闭不兼容的 TLS 版本
    ssl_context.set_ciphers("HIGH:!aNULL:!MD5")  # 只允许高强度加密
    ntqq_img_client = AutoCloseAsyncClient(
        verify=ssl_context
    )  # 适用于 QQ 服务器的 HTTP 客户端
    try:
        base_img: Image.Image = await get_imgs(img_url, ntqq_img_client)
    except Exception as e:
        acg_trace.finish(f"获取图片失败\n{repr(e)}", at_sender=True)

    # 发送请求
    url = "https://api.animetrace.com/v1/search"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
        ),
    }
    model = state["model"]
    ai_detect = 1 if conf.animetrace_ai_detect else 0
    bio = BytesIO()
    base_img.save(bio, format="JPEG")
    img_b64 = b64encode(bio.getvalue()).decode()
    data = {
        "is_multi": 1,
        "model": model,
        "ai_detect": ai_detect,
        "base64": img_b64,
    }
    try:
        async with AutoCloseAsyncClient() as client:
            res = await client.post(
                url=url,
                headers=headers,
                data=data,
                timeout=30,
            )
            content = res.json()
    except Exception as e:
        logger.exception(f"post({url})失败{repr(e)}")
        await acg_trace.finish(
            f"识别失败，换张图片试试吧~\n{res}\n{repr(e)}", at_sender=True
        )

    # 检查识别结果
    if content["code"] != 0:
        await acg_trace.finish(
            f"出错啦~可能是图里角色太多了~\ncontent:{content}", at_sender=True
        )
    char_nums = len(content["data"])
    if char_nums == 0:
        await acg_trace.finish(f"没有识别到任何角色\ncontent:{content}", at_sender=True)

    # 构造消息
    message_list = construct_msg(state, base_img, content, char_nums)

    # 发送消息
    try:
        nickname = conf.nickname[0]
    except Exception as e:
        logger.warning("Warn: config.nickname 配置错误!", e)
        nickname = "animetrace"
    try:
        if not conf.animetrace_send_forward:
            raise NOException(
                "准备发送单条消息, 因为: config.animetrace_send_forward="
                f"{conf.animetrace_send_forward}"
            )
        await send_forward(bot, event, message_list, nickname)
    except ActionFailed as e:
        logger.error("api操作失败, 可能有风控风险", e)
    except NOException as e:
        # 表示没有异常，只用于跳出try（借鉴了nonebot的skip异常，finish异常等）
        logger.debug(e)
        # 单条消息发送
        for msg in message_list:
            await acg_trace.send(msg)
    except SkippedException as e:
        logger.debug(e)
        raise
    except Exception as e:
        logger.error(e)
        raise


def construct_msg(
    state: T_State,
    base_img: Image.Image,
    content: dict,
    char_nums: int,
) -> list[Message]:
    res_start_msg = Message(
        f"共识别到{char_nums}个角色\n更多模型请访问:https://ai.animedb.cn"
    )
    if content["ai"]:
        res_start_msg = "该图可能是ai绘图!\n" + res_start_msg
    message_list = [res_start_msg]
    mode = state["mode"]
    for item in content["data"]:
        width, height = base_img.size
        box = item["box"]
        box = (
            box[0] * width,
            box[1] * height,
            box[2] * width,
            box[3] * height,
        )
        img_bytes = BytesIO()
        item_img = base_img.crop(box)
        item_img.save(img_bytes, format="JPEG")
        char = item["character"]
        may_num = min(conf.animetrace_max_num, len(char))
        txt_msg = Message(f"该角色有{may_num}种可能\n")
        if conf.animetrace_extract:  # 分多条消息发送:角色,作品,链接
            extract_msg(message_list, mode, img_bytes, char, may_num, txt_msg)
        else:
            merge_msg(message_list, mode, img_bytes, char, may_num, txt_msg)
    return message_list


def merge_msg(
    message_list: list,
    mode: str,
    img_bytes: BytesIO,
    char: dict,
    may_num: int,
    txt_msg: Message,
):
    for i in range(may_num):
        name = char[i]["character"]
        q = quote(name)
        txt_msg += (
            f"\n{i+1}\n"
            f"角色:{name}\n"
            f"来自{mode}:{char[i]['work']}\n"
            + (
                f"萌娘百科:zh.moegirl.org.cn/index.php?search={q}\n"
                if conf.animetrace_moegirl
                else ""
            )
            + (f"{conf.animetrace_url}{q}" if conf.animetrace_url else "")
        )
    message = txt_msg + MessageSegment.image(img_bytes.getvalue())
    message_list.append(message)


def extract_msg(
    message_list: list,
    mode: str,
    img_bytes: BytesIO,
    char: dict,
    may_num: int,
    txt_msg: Message,
):
    message_list.append(txt_msg)
    for i in range(may_num):
        name = char[i]["character"]
        q = quote(name)
        message_list.append(Message(f"{i+1}"))
        message_list.append(Message(f"{name}"))
        message_list.append(Message(f"来自{mode}:{char[i]['work']}"))
        if conf.animetrace_moegirl:
            message_list.append(
                Message(f"萌娘百科:zh.moegirl.org.cn/index.php?search={q}")
            )
        if conf.animetrace_url:
            message_list.append(Message(f"{conf.animetrace_url}{q}"))
    message_list.append(MessageSegment.image(img_bytes.getvalue()))


async def send_forward(
    bot: Bot,
    event: MessageEvent,
    message_list: list[Message],
    nickname: str,
):
    """
    send_group_forward_msg |
    send_private_forward_msg |
    send_forward_msg
    """
    msgs = [
        MessageSegment(
            type="node",
            data={
                "name": nickname,
                "uin": bot.self_id,
                "content": Message(msg),
            },
        )
        for msg in message_list
    ]
    # 发送转发消息
    data = {}
    data["messages"] = msgs
    if isinstance(event, GroupMessageEvent):
        t = "group"
        data["group_id"] = event.group_id
    elif isinstance(event, PrivateMessageEvent):
        t = "private"
        data["user_id"] = event.user_id
    api = f"send_{t}_forward_msg"
    try:
        await bot.call_api(api=api, **data)
    except ApiNotAvailable as e:
        logger.info(f"api: {api}调用失败", e)
        await bot.send_forward_msg(**data)
