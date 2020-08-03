from nonebot import on_command, CommandSession
from nekobot.info import song_library
from nekobot.info import character_info
from nekobot.plugins.arena import arena
import random
from nekobot.tool import is_number
import pandas as pd

cy2_pool_dict = song_library.cy2_pool

cy2_pool_list = song_library.cy2_pool_list


def condition_check(song, conditions):
    is_chaos = -1
    if 'hd' in conditions or 'hard' in conditions or '困难' in conditions:
        is_chaos = 0
    if not conditions:
        return True
    counter = 0
    for condition in conditions:
        if condition in ['hd', 'hard', '困难']:
            if '(Glitch)' not in song:
                counter += 1
        if condition in ['马', '🐴'] and is_chaos == -1:
            if song in song_library.cy2_horse_music:
                counter += 1
        if condition in ['不马', '不🐴', '🦄️'] and is_chaos == -1:
            if song in song_library.cy2_horse_music:
                counter += 1
        if condition.lower() in ['chaos', '混沌']:
            if '(Glitch)' not in song and is_chaos == -1:
                counter += 1
        if condition.lower() in ['glitch', '绿', '绿谱']:
            if '(Glitch)' in song and is_chaos == -1:
                counter += 1
        if '.' in condition and is_number(condition):   # 精细难度选歌
            if float(condition) == cy2_pool_dict[song]['difficulty'][is_chaos]:
                counter += 1
        if condition == '付费':
            if cy2_pool_dict[song]['song_package'] != 'free':
                counter += 1
        if condition == '免费':
            if cy2_pool_dict[song]['song_package'] == 'free':
                counter += 1
        if condition.lower() in ['mai', 'maimai']:
            if cy2_pool_dict[song]['song_package'] == 'maimai DX+':
                counter += 1
        if condition.lower() in ['djmax', 'dj']:
            if 'DJ MAX' in cy2_pool_dict[song]['song_package']:
                counter += 1
        if condition.endswith('-') and is_number(condition[:-1]):   # 设置上限
            if cy2_pool_dict[song]['difficulty'][is_chaos] <= float(condition[:condition.find('-')]):
                counter += 1
        elif '-' in condition and is_number(condition[:condition.find('-')]) and \
                is_number(condition[condition.find('-') + 1:]):   # 按区间
            if float(condition[:condition.find('-')]) <= cy2_pool_dict[song]['difficulty'][is_chaos]\
                    <= float(condition[condition.find('-') + 1:]):
                counter += 1
        if character_info.character_interpreter(condition) in character_info.character_info:  # 按人物
            if character_info.character_interpreter(condition) == song[song.find('[') + 1:-1].lower():
                counter += 1
        if condition.endswith('+') and is_number(condition[:-1]):  # 设置下限
            if cy2_pool_dict[song]['difficulty'][is_chaos] >= float(condition[:condition.find('+')]):
                counter += 1
        if condition.isdigit() and int(condition) in range(3, 17):  # 按难度
            if int(condition) == int(cy2_pool_dict[song]['difficulty'][is_chaos]):
                counter += 1
        else:
            is_artist = False
            for pool_song in cy2_pool_dict:
                if condition.lower() in cy2_pool_dict[pool_song]['artist'].lower():
                    is_artist = True
                    break
            if is_artist:
                if condition.lower() in cy2_pool_dict[song]['artist'].lower():
                    counter += 1
    standard = len(conditions)
    for keyword in ['评论', '评价']:
        if keyword in conditions:
            standard -= pd.value_counts(conditions).loc[keyword]
    if counter == standard:
        return True
    else:
        return False


def draw(msg):
    sp = str(msg).lower().split()
    cmd, *conditions = sp
    random.shuffle(cy2_pool_list)
    pool = cy2_pool_list
    result = None
    for song in pool:
        if condition_check(song, conditions):
            result = song
            break
    return result


@on_command('抽歌', only_to_me=False, privileged=True)
async def _(session: CommandSession):
    msg = session.ctx['message']
    group_id = 0
    if 'group_id' in session.ctx:
        group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    if group_id in arena and user_id in arena[group_id]['player'] and 'is_hard' in arena[group_id]['modifier']:
        msg += ' hd'
    song = draw(msg)
    if not song:
        result = '条件设定有误'
    else:
        is_chaos = 1
        if 'hd' in str(msg) or 'hard' in str(msg) or '困难' in str(msg) or '(Glitch)' in song:
            is_chaos = 0
        difficulty = cy2_pool_dict[song]['difficulty'][is_chaos]
        result = '(' + str(difficulty) + ')' + song
        if '评论' in str(msg) or '评价' in str(msg):
            result += '\n这里是评论'
        if group_id in arena and user_id in arena[group_id]['player']:
            if 0 < arena[group_id]['process'] < len(arena[group_id]['player']):
                result = '请等待本局结束再抽歌哟'
            else:
                result = '经济：' + result
                arena[group_id]['song'] = {'name': song, 'difficulty': difficulty}
                arena[group_id]['locked'] = True
    await session.send(result)

