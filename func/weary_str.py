from conf import MAX_WEARY


def weary_str(temp: int) -> str:
    return {
        0.00*MAX_WEARY <= temp: 'Вы бодры и свежи',
        0.25*MAX_WEARY <= temp: 'Вы испытываете усталость',
        0.50*MAX_WEARY <= temp: 'Вы сильно утомлены',
        0.75*MAX_WEARY <= temp: 'Вы на грани срыва',
        }.get(True, '')
