from conf import MAX_HUNGER


def hunger_str(temp: int) -> str:
    return {
        0.00*MAX_HUNGER <= temp: 'Вы не думаете о еде',
        0.25*MAX_HUNGER <= temp: 'Вы думаете, что пора поесть',
        0.50*MAX_HUNGER <= temp: 'Вы испытываете сильный голод',
        0.75*MAX_HUNGER <= temp: 'Вы на грани смерти от истощения',
        }.get(True, '')
