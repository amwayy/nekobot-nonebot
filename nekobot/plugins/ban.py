from nonebot import on_natural_language, CommandSession
from nonebot import permission as perm


@on_natural_language(keywords=['neko我婆', 'Neko我婆', 'NEKO我婆'], only_to_me=False, permission=perm.GROUP)
async def _(session: CommandSession):
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60)
    await session.send(f'[CQ:at,qq={user_id}] [该用户已被禁言]')



