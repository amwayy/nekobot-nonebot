from nonebot import on_command, CommandSession
from nekobot.info import song_library
from nekobot.plugins.select_song import song_interpreter


@on_command('曲目信息', only_to_me=False, privileged=True)
async def _(session: CommandSession):
    sp = str(session.ctx['message']).split()
    if len(sp) == 1:
        await session.send('曲目名称不可为空')
    else:
        is_legal = False
        assigned_song = song_interpreter(sp[1])
        if assigned_song == 'v':
            assigned_song = 'V.[Ivy]'
            is_legal = True
        elif assigned_song == 'il':
            assigned_song = 'iL[Ivy]'
            is_legal = True
        elif assigned_song == 'ii':
            assigned_song = 'II[Vanessa]'
            is_legal = True
        elif assigned_song == 'd r g':
            assigned_song = 'D R G[Ivy]'
            is_legal = True
        else:
            for song in song_library.cy2_pool:
                if assigned_song in song.lower():
                    assigned_song = song
                    is_legal = True
                    break
        if not is_legal:
            await session.send('曲目名称不合法')
        else:
            song_info = song_library.cy2_pool[assigned_song]
            if len(song_info['difficulty']) == 1:
                difficulty = song_info['difficulty'][0]
                assigned_song = f'({difficulty}){assigned_song}'
            artist = song_info['artist']
            song_info_str = f'{assigned_song}\n曲师：{artist}\n'
            glitch_chart = assigned_song[:assigned_song.find('[')] + '(Glitch)' + assigned_song[assigned_song.find('['):]
            if glitch_chart not in song_library.cy2_pool:
                difficulty = song_info['difficulty']
                song_info_str += f'hard谱面难度：{difficulty[0]}，chaos谱面难度：{difficulty[1]}\n'
            else:
                difficulty = song_info['difficulty']
                glitch_difficulty = song_library.cy2_pool[glitch_chart]['difficulty']
                song_info_str += f'hard谱面难度：{difficulty[0]}，chaos谱面难度：{difficulty[1]}，' \
                                 f'glitch谱面难度：{glitch_difficulty[0]}\n'
            if song_info['song_package'] == 'free':
                purchase_info = '免费'
            else:
                purchase_info = '付费，隶属' + song_info['song_package'] + '曲包'
            song_info_str += '本曲' + purchase_info
            await session.send(song_info_str)