from clas import Person, PersonStatus, Inventory

STAT_LIST = [
   'speed', 'stealth', 'strength', 'knowledge',
   'godliness', 'luck', 'experience', 'bless', 'proof',
   'hunger', 'weary', 'money', 'health', 'mind',
   'location', 'death'
        ]


async def applying_effects(PERS: 'Person', STAT: 'PersonStatus', DICT: dict):
    "Накладываем на персонажа разные эффекты после прохождения ивентов"
    MESS = ""
    for key, value in DICT.items():
        try:
            MOD = {
                key in STAT_LIST:   STAT.change(key, value),
                key == 'time':      STAT.waste_time(int(value)),
                key == 'item':      Inventory.add(PERS.p_id, int(value)),
                key == 'drop_item': Inventory.drop(PERS.p_id, int(value)),
                    }[True]
        except KeyError:
            continue

        await MOD

        if key in ('item'):
            MESS += '\n\n' + MOD[1]

    return MESS
