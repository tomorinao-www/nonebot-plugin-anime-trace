from datetime import datetime

import pytest
from nonebug import App
from nonebot.adapters.console import User, Message, MessageEvent


def make_event(message: str = "") -> MessageEvent:
    return MessageEvent(
        time=datetime.now(),
        self_id="test",
        message=Message(message),
        user=User(id="user"),
    )


@pytest.mark.asyncio
async def test_example(app: App):
    from nonebot_plugin_anime_trace import acg_trace

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot()
        event = make_event("#识别")
        ctx.receive_event(bot, event)
        ctx.should_pass_rule(acg_trace)
        ctx.should_pass_permission(acg_trace)
