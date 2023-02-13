from clas import Person
from conf import emoji

I_def = {
    'head':         'Непокрытая голова',
    'earrings':     'пустые уши',
    'hands':        'Пустые руки',
    'rings':        'Пальцы без колец',
    'body':         'Голое тело',
    'legs':         'Голые ноги',
    'shoes':        'Босые ноги',
    'bag':          'Сумка пустая, не тянет плечо',
    'achievements': 'Нет достижений',
    }


def inventory_mess(PERS: 'Person', ITEMS: dict, EQUIP: bool = False) -> str:
    "Генерируем сообщение для списка инвентаря"

    I_zero = {
        'head':         ('',),
        'earrings':     ('',),
        'hands':        ('',),
        'rings':        ('',),
        'body':         ('',),
        'legs':         ('',),
        'shoes':        ('',),
        'bag':          ('',),
        'achievements': ('',),
        }

    for key, value in ITEMS.items():
        if type(value) is not list:
            continue
        for item in value:
            I_zero[key] += (' ', emoji(item['emoji']), ' ', item['name'],)

    for key, value in I_zero.items():
        if len(value) < 2:
            I_zero[key] = I_def[key]

    LIST = (
        '*Ваш инвентарь* ', PERS.gamename,
        '\n',
        '\n*Голова:* ',      *I_zero['head'],
        '\n*Уши:* ',         *I_zero['earrings'],
        '\n*В руках:* ',     *I_zero['hands'],
        '\n*Кольца:* ',      *I_zero['rings'],
        '\n*На теле:* ',     *I_zero['body'],
        '\n*Ноги:* ',        *I_zero['legs'],
        '\n*Обувь:* ',       *I_zero['shoes'],
        '\n*Достижения:* ',  *I_zero['achievements'],
        '\n\nВаш персонаж сейчас использует' if EQUIP else '\n\nВ вашей сумке:'
        )

    return ''.join(str(x) for x in LIST)
