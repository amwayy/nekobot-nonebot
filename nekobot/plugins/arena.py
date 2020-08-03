import random

import pandas as pd
from nonebot import on_command, CommandSession
from nonebot import permission as perm

from nekobot.tool import is_number

user_info = pd.read_excel(r'C:\Users\asus\Desktop\user_info.xls')

arena = {}

arena_result1 = ''


@on_command('发起经济', aliases='加入经济', only_to_me=False, permission=perm.GROUP)
async def arena_begin(session: CommandSession):
    cmd, *modifier = str(session.ctx['message']).lower().split()
    cmd = cmd[1:]
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    if session.ctx['sender']['card'] != '':
        nickname = session.ctx['sender']['card']
    else:
        nickname = session.ctx['sender']['nickname']

    blocked = False

    if cmd == '发起经济':  # 在arena字典中生成该群的目录
        if group_id in arena and user_id not in arena[group_id]['player']:
            await session.send('当前有经济正在进行，你可以直接加入哟')
            blocked = True
        else:
            arena[group_id] = {}
            arena[group_id]['player'] = {}
            arena[group_id]['process'] = 0
            arena[group_id]['locked'] = False
            arena[group_id]['modifier'] = []
            if 'hd' in modifier or 'hard' in modifier or '困难' in modifier:
                arena[group_id]['modifier'].append('is_hard')
    if cmd == '加入经济':
        if group_id not in arena:
            await session.send('当前没有经济')
    if group_id in arena and not blocked:  # 经济已经发起
        prompt = ''
        if cmd == '加入经济' and arena[group_id]['locked']:
            arena[group_id]['player'][user_id] = {'nickname': nickname, 'is_first_round': True,
                                                  'counter': 0, 'waiting': True}
            prompt = '本局玩家已锁定，等待本局结束后将自动加入经济'
        elif user_id not in arena[group_id]['player']:
            arena[group_id]['player'][user_id] = {'nickname': nickname, 'is_first_round': True, 'counter': 0}
            rank = None
            for i in range(len(user_info['id'])):
                if user_info.loc[i, 'id'] == user_id:
                    rank = user_info.loc[i, 'rank']
                    prompt = f'{cmd[:2]}成功！\n你当前的rank值为{"%.2f" % rank}'
                    break
            if not rank:  # 初次使用
                index = len(user_info['id']) + 2
                prompt = f'{cmd[:2]}成功！\n你是使用NekoBot经济功能的第{index}名用户！'
        global arena_result1
        while arena[group_id]['player'][user_id]['counter'] < 10000:
            if user_id in arena[group_id]['player'] and 'is_first_round' in arena[group_id]['player'][user_id]:
                tp = session.get('tp' + str(arena[group_id]['player'][user_id]['counter']), prompt=prompt)
                arena[group_id]['player'][user_id].pop('is_first_round')
            else:
                tp = session.get('tp' + str(arena[group_id]['player'][user_id]['counter']))
            arena[group_id]['player'][user_id]['counter'] += 1
            if is_number(tp):
                tp = float(tp)
                if 100 < tp < 1000:
                    tp = tp / 10
                if 1000 <= tp:
                    tp = tp / 100
                if 'tp' not in arena[group_id]['player'][user_id]:
                    arena[group_id]['process'] += 1
                arena[group_id]['player'][user_id]['tp'] = tp
            current_players = []
            for player in arena[group_id]['player']:
                if not arena[group_id]['player'][player].get('waiting'):
                    current_players.append(player)

            if arena[group_id]['process'] == len(current_players):
                tp_info = []
                for player in current_players:
                    tp_info.append(arena[group_id]['player'][player]['tp'])
                sorted_tp = sorted(list(set(tp_info)))
                arena_result1 = '本局排名：'
                for i in range(len(sorted_tp)):
                    arena_result1 += '\n' + str(i + 1) + '. ' + str("%.2f" % sorted_tp[len(sorted_tp) - i - 1])
                    for player in current_players:
                        if arena[group_id]['player'][player]['tp'] == sorted_tp[len(sorted_tp) - i - 1]:
                            arena_result1 += ' @' + arena[group_id]['player'][player]['nickname']
                await session.send(arena_result1)

                arena_result2 = '本局rank变动：'
                for player in current_players:
                    rank = 0
                    b30 = []
                    b30_songs = {}
                    r10 = []
                    r10_songs = {}
                    user_index = len(user_info['id'])
                    for i in range(len(user_info['id'])):
                        if user_info.loc[i, 'id'] == player:
                            user_index = i
                            rank = user_info.loc[i, 'rank']
                            b30 = eval(user_info.loc[i, 'b30'])
                            b30_songs = eval(user_info.loc[i, 'b30 songs'])
                            r10 = eval(user_info.loc[i, 'r10'])
                            r10_songs = eval(user_info.loc[i, 'r10 songs'])
                            break
                    if not r10:
                        user_info.loc[user_index, 'id'] = player
                        user_info.loc[user_index, 'nickname'] = nickname
                    tp = arena[group_id]['player'][player]['tp']
                    if tp >= 90:
                        current_song_rank = (tp - 90) * arena[group_id]['song']['difficulty'] / 10
                    else:
                        current_song_rank = 0
                    current_song = arena[group_id]['song']['name']
                    if current_song in b30_songs and current_song_rank > b30_songs[current_song]:
                        b30_to_delete = 0
                        for b30_rank in b30:
                            if b30_rank == b30_songs[current_song]:
                                b30_to_delete = b30_rank
                                break
                        if b30_to_delete in b30:
                            b30.remove(b30_to_delete)
                        b30.append(current_song_rank)
                        b30_songs[current_song] = current_song_rank
                    elif not b30 or len(b30) < 30 and current_song not in b30_songs:
                        b30_songs[current_song] = current_song_rank
                        b30.append(current_song_rank)
                    elif current_song_rank > b30[0]:
                        song_to_delete = None
                        for song in b30_songs:
                            if b30_songs[song] == b30[0]:
                                song_to_delete = song
                                break
                        if song_to_delete:
                            b30_songs.pop(song_to_delete)
                        b30_songs[current_song] = current_song_rank
                        b30.pop(0)
                        b30.append(current_song_rank)
                    b30 = sorted(b30)

                    r10.append(current_song_rank)
                    discarded_r10 = None
                    if len(r10) == 11:
                        discarded_r10 = r10[0]
                        r10.pop(0)
                    new_rank = (sum(b30) + sum(r10)) / 40
                    if new_rank < rank and tp >= 99 and len(r10) > 1:
                        r10.pop(-1)
                        r10.insert(0, discarded_r10)
                        delta_rank = 'keep'
                    else:
                        for song in r10_songs:
                            r10_songs.pop(song)
                            break
                        r10_songs[current_song + str("%.2f" % current_song_rank)] = current_song_rank
                        delta_rank = str("%.2f" % (round(new_rank, 2) - round(rank, 2)))
                        if float(delta_rank) > 0:
                            delta_rank = '+' + delta_rank
                        if float(delta_rank) == 0:
                            delta_rank = 'keep'
                        rank = new_rank
                    user_info.loc[user_index, 'rank'] = rank
                    user_info.loc[user_index, 'b30'] = str(b30)
                    user_info.loc[user_index, 'b30 songs'] = str(b30_songs)
                    user_info.loc[user_index, 'r10'] = str(r10)
                    user_info.loc[user_index, 'r10 songs'] = str(r10_songs)
                    user_info.to_excel(r'C:\Users\asus\Desktop\user_info.xls', index=None)
                    arena_result2 += '\n' + arena[group_id]['player'][player]['nickname'] \
                                     + f'：{"%.2f" % rank}(' + delta_rank + ')'
                await session.send(arena_result2)

                arena[group_id]['process'] = 0
                arena[group_id]['locked'] = False
                for player in current_players:
                    arena[group_id]['player'][player].pop('tp')

                waiting_players = []
                for player in arena[group_id]['player']:
                    if arena[group_id]['player'][player].get('waiting'):
                        waiting_players.append(player)
                if len(waiting_players) > 0:
                    reminder = ''
                    for waiting_player in waiting_players:
                        arena[group_id]['player'][waiting_player].pop('waiting')
                        reminder += f'[CQ:at,qq={waiting_player}] '
                    reminder += '\n上一局结束了哟，已自动加入下一局经济'
                    await session.send(reminder)

                players = []
                for player in arena[group_id]['player']:
                    players.append(player)
                drawer = random.choice(players)
                await session.send(f'有请[CQ:at,qq={drawer}] 抽歌~')

                arena[group_id].pop('song')


@arena_begin.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        return

    user_id = session.ctx['user_id']
    group_id = session.ctx['group_id']

    if not is_number(session.current_arg_text):
        if session.current_arg_text in ['/发起经济', '/加入经济']:
            session.pause('你已经在经济中了哟')
        if session.current_arg_text == '/退出经济':
            if user_id in arena[group_id]['player']:
                arena[group_id]['player'].pop(user_id)
            session.pause('退出成功！')
            if len(arena[group_id]['player']) < 2:
                arena.pop(group_id)
                await session.send('人数不足2，经济关闭')
            session.finish()
        if session.current_arg_text in ['neko我婆', 'Neko我婆', 'NEKO我婆']:
            group_id = session.ctx['group_id']
            user_id = session.ctx['user_id']
            await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60)
            session.pause(f'[CQ:at,qq={user_id}] [该用户已被禁言]')
        if group_id in arena and user_id in arena[group_id]['player']:
            session.pause()

    if is_number(session.current_arg_text) and group_id in arena and user_id in arena[group_id]['player']:
        if 'song' not in arena[group_id]:
            session.pause('请先抽歌（选歌）')
        if float(session.current_arg_text) > 10000 or float(session.current_arg_text) < 0:
            session.pause('tp值不合法')
        else:
            session.args[session.current_key] = session.current_arg_text
            print(session.args)


@on_command('退出经济', only_to_me=False, permission=perm.GROUP)
async def _(session: CommandSession):
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    if group_id not in arena:
        await session.send('当前没有经济')
    elif user_id not in arena[group_id]['player']:
        await session.send('你还没有加入经济哟')


@on_command('玩家', aliases=['player', 'players'], only_to_me=False, permission=perm.GROUP, privileged=True)
async def _(session: CommandSession):
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    if group_id not in arena:
        await session.send('当前没有经济')
    else:
        current_players = []
        for player in arena[group_id]['player']:
            if not arena[group_id]['player'][player].get('waiting'):
                current_players.append(player)
        waiting_players = []
        for player in arena[group_id]['player']:
            if player not in current_players:
                waiting_players.append(player)
        remaining_players = []
        result = '本局玩家共' + str(len(current_players)) + '人：\n'
        for player in current_players:
            if 'tp' not in arena[group_id]['player'][player]:
                remaining_players.append(player)
            result += arena[group_id]['player'][player]['nickname'] + '\n'
        if user_id in arena[group_id]['player'] and len(remaining_players) <= 3 and 'song' in arena[group_id]:
            result += '----------\n这些玩家还没有提交成绩：\n'
            for player in remaining_players:
                result += f'[CQ:at,qq={player}] \n'
        if len(waiting_players) != 0:
            result += '----------\n另有这些玩家等待下局加入：'
            for waiting_player in waiting_players:
                result += '\n' + arena[group_id]['player'][waiting_player]['nickname']
        await session.send(result)