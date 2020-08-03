from nonebot import on_command, CommandSession
from nonebot import permission as perm


@on_command('小牌子', only_to_me=False, permission=perm.GROUP_ADMIN)
async def _(session: CommandSession):
    sp = str(session.ctx['message']).split()
    group_id = session.ctx['group_id']
    user_id = sp[1]
    special_title = sp[2]
    await session.bot.set_group_special_title(group_id=group_id, user_id=user_id, special_title=special_title)
    await session.send('设置成功')