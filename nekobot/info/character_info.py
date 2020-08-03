character_info = {'paff': ['泡芙'], 'neko#φωφ': ['neko', '野猫'],
                  'robo_head': ['robo', 'robo head', '萝卜', '萝卜头'], 'ivy': [],
                  'crystal punk': ['cp'], 'vanessa': ['v姐'],
                  'miku': ['初音', '初音未来'], 'kizuna ai': ['爱酱', '绊爱', 'ai'],
                  'xenon': ['x', 'simon', 'x哥', '头盔哥'],
                  'conner': ['老师'], 'cherry': ['大姐头'], 'joe': ['细菌王', '第三象限唯一神'],
                  'sagar': [], 'rin': [], 'aroma': [], 'nora': [],
                  'neko': ['小neko'],
                  }


def character_interpreter(text):
    is_character = False
    for character in character_info:
        if text.lower() in character_info[character] or text.lower() == character:
            return character
    if not is_character:
        return text