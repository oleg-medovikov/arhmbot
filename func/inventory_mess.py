from clas import Person
from conf import emoji

I_def = {
    'head':     'Непокрытая голова',
    'onehand':  'Пустые руки',
    'twohands': 'Пустые руки',
    'body':     'Голое тело',
    'legs':     'Голые ноги',
    'shoes':    'Босые ноги',
    'bag':      'Сумка пустая, не тянет плечо',
    }


def inventory_mess(PERS: 'Person', INV: list) -> str:
    "Генерируем сообщение для списка инвентаря"

    I_zero = {
        'head':     ('',),
        'onehand':  ('',),
        'twohands': ('',),
        'body':     ('',),
        'legs':     ('',),
        'shoes':    ('',),
        'bag':      ('',),
        }

    for item in INV:
        I_zero[item['slot']] += (' ', emoji(item['emoji']), ' ', item['name'],)

    I_zero['hands'] = {
        len(I_zero['onehand']) + len(I_zero['twohands']) < 3: I_def['onehand'],
        len(I_zero['onehand']) > 1:     I_zero['onehand'],
        len(I_zero['twohands']) > 1:    I_zero['twohands'],
            }[True]

    for key, value in I_zero.items():
        if key == 'hands':
            continue
        if len(value) < 2:
            I_zero[key] = I_def[key]

    LIST = (
        '*Ваш инвентарь* ', PERS.gamename,
        '\n',
        '\n*Голова:* ',  *I_zero['head'],
        '\n*В руках:* ', *I_zero['hands'],
        '\n*На теле:* ', *I_zero['body'],
        '\n*Ноги:* ',    *I_zero['legs'],
        '\n*Обувь:* ',   *I_zero['shoes'],
        '\n\nВ вашей сумке:'
        )

    return ''.join(str(x) for x in LIST)
