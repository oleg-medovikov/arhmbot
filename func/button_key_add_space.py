

def button_key_add_space(DICT: dict) -> dict:
    "добавляем пробелы чтобы кнопочки были ровные"
    MAX = len(max(list(DICT.keys()), key=len)) - 1

    DICT_ = {}
    for key, value in DICT.items():
        DICT_[key + '⠀'*(MAX - len(key))] = value

    return DICT_
