# from nonebot import on_command, CommandSession, permission as perm
# from nekobot.tool import is_number
#
# counter = 0
#
#
# @on_command('test', only_to_me=False, permission=perm.IS_SUPERUSER)
# async def test(session: CommandSession):
#     key = session.get('key', prompt='噢噢噢')
#
#
# @test.args_parser
# async def _(session: CommandSession):
#
#     if session.is_first_run:
#         return
#
#     session.pause('啊啊啊')
#     print(1)
#
#     session.args[session.current_key] = session.current_arg_text
