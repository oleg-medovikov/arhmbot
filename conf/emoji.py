Dict_emoji = {
    'heart':      '\u2764\uFE0F',
    'brain':      '\ud83e\udde0',
    'dollar':     '\ud83d\udcb5',
    'bank':       '\ud83c\udfe6',
    'clock':      '\ud83d\udd70',
    'luck':       '\ud83c\udf40',
    'speed':      '\ud83c\udfc3',
    'stealth':    '\ud83e\udd77\ud83c\udffb',
    'godliness':  '\ud83d\ude4f',
    'strength':   '\ud83d\udcaa',
    'knowledge':  '\ud83d\udcda',
    'hunger':     '\ud83c\udf57',
    'weary':      '\ud83d\udecf\ufe0f',
    'mail':       '\ud83d\udc8c',
    'note':       '\ud83d\udcd3',
    'film':       '\ud83c\udf9e',
    'redbook':    '\ud83d\udcd5',
    'flashlight': '\ud83d\udd26',
    'sword':      '\ud83d\udde1',
    'axe':        '\ud83e\ude93',
    'gun':        '\ud83d\udd2b',
    'pick':       '\u26cf',
    'syringe':    '\ud83d\udc89',
    'pill':       '\ud83d\udc8a',
    'red':        '\ud83d\udd34',
    'green':      '\ud83d\udfe2',
    'ticket':     '\ud83c\udf9f',
    'suit':       '\ud83e\udd35',
    'penis':      '\ud80c\udcba',
    'leg':        '\ud83e\uddb5',
    'expensive_shoes': '\ud83d\udc5e',
    'shorts':     '\ud83e\ude73',
    'hat':        '\ud83e\udd20',
    'glasses':    '\ud83d\udc53',
    'proof':      '\ud83d\udd0e',
    'shirt':      '\ud83d\udc55',
    'robe':       '\ud83e\udd4b',
    'dress':      '\ud83d\udc57',
    'stopwatch':  '\u23f1',
    }


def emoji(KEY: str) -> str:
    """Хитро декодируем эмодзи, чтобы апи телеги не ругалось"""
    STRING = Dict_emoji.get(KEY, '')
    return STRING.encode('utf-16', 'surrogatepass').decode('utf-16')


def emoji_all() -> list:
    "Возвращаем список всех ключей эмодзи для проверки"
    return list(Dict_emoji.keys())
