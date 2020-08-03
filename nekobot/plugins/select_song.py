from nonebot import on_command, CommandSession
from nekobot.info import song_library
from nekobot.plugins.arena import arena
import re


def song_interpreter(request_song_name):
    is_requesting_glitch = False

    request_song_name = request_song_name.rstrip()

    if request_song_name.endswith('评论') or request_song_name.endswith('评价'):
        request_song_name = request_song_name[: -3]

    if request_song_name.startswith('绿') and '绿屎' not in request_song_name and '绿希' not in request_song_name \
            or request_song_name.endswith('绿谱'):   # 绿谱
        is_requesting_glitch = True
        if request_song_name.startswith('绿'):
            request_song_name = request_song_name[1:]
        if request_song_name.endswith('绿谱'):
            request_song_name = request_song_name[:-2]

    if request_song_name.startswith('^'):   # 首字母
        alpha_pattern = re.compile(r'^\w$')
        for song in song_library.cy2_pool:
            initial = ''
            for word in song[:song.find('[')].split(' '):
                while len(word) > 0 and not alpha_pattern.match(word[0]):
                    word = word[1:]
                if len(word) > 0:
                    initial += word[0]
            if initial.lower() == request_song_name[1:].lower():
                if is_requesting_glitch and 'glitch' not in song.lower():
                    return song[:song.find('[')].lower() + '(glitch)'
                else:
                    return song[:song.find('[')].lower()

    if request_song_name.lower() == 'v':
        return 'v'
    if request_song_name.lower() == 'il':
        return 'il'
    if request_song_name.lower() == 'chaos':
        return 'chaos'

    else:
        for song in song_library.cy2_pool:
            for nickname in song_library.cy2_pool[song]['aliases']:
                if request_song_name.lower() in str(nickname):
                    if is_requesting_glitch and 'glitch' not in song.lower():
                        return song[:song.find('[')].lower() + '(glitch)'
                    else:
                        return song[:song.find('[')].lower()

    if is_requesting_glitch and 'glitch' not in request_song_name.lower():
        return request_song_name.lower() + '(glitch)'
    else:
        return request_song_name.lower()


@on_command('选歌', aliases='点歌', only_to_me=False, privileged=True)
async def _(session: CommandSession):
    group_id = 0
    if 'group_id' in session.ctx:
        group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    msg = str(session.ctx['message'])
    sp = str(session.ctx['message']).split(maxsplit=1)
    if len(sp) == 1:
        await session.send('曲目名称不可为空')
    else:
        is_legal = False
        assigned_song = song_interpreter(sp[1])
        if assigned_song == 'v':
            assigned_song = 'V.[Ivy]'
            is_legal = True
        elif assigned_song == 'd r g':
            assigned_song = 'D R G[Ivy]'
            is_legal = True
        elif assigned_song == 'ii':
            assigned_song = 'II[Vanessa]'
            is_legal = True
        else:
            words = assigned_song.split()
            for song in song_library.cy2_pool:
                counter = 0
                for word in words:
                    if word.lower() in song[:song.find('[')].lower():
                        counter += 1
                if counter == len(words):
                    assigned_song = song
                    is_legal = True
                    break
        if not is_legal:
            await session.send('曲目名称不合法')
        else:
            difficulty = song_library.cy2_pool[assigned_song]['difficulty'][-1]
            if group_id in arena and user_id in arena[group_id]['player'] and 'is_hard' in arena[group_id]['modifier']:
                difficulty = song_library.cy2_pool[assigned_song]['difficulty'][0]
            result = '(' + str(difficulty) + ')' + assigned_song
            if '评论' in str(msg) or '评价' in str(msg):
                result += '\n这里是评论'
            if group_id in arena and user_id in arena[group_id]['player']:
                if 0 < arena[group_id]['process'] < len(arena[group_id]['player']):
                    result = '请等待本局结束再选歌哟'
                else:
                    result = '经济：' + result
                    arena[group_id]['song'] = {'name': assigned_song, 'difficulty': difficulty}
                    arena[group_id]['locked'] = True
            await session.send(result)


