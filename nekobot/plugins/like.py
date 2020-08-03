from nonebot import on_command, CommandSession

import time

like_info = {}


@on_command('赞', aliases='点赞', only_to_me=False, privileged=True)
async def _(session: CommandSession):
    user_id = session.ctx['user_id']
    today = time.strftime("%Y-%m-%d", time.localtime())
    if user_id in like_info and today > like_info[user_id]:
        await session.bot.send_like(user_id=user_id, times=10)
        await session.send('赞了哟')
    elif user_id not in like_info:
        like_info[user_id] = today
        await session.bot.send_like(user_id=user_id, times=10)
        await session.send('赞了哟')
    else:
        await session.send('今天已经赞过了哟')