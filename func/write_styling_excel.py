import pandas as pd


def write_styling_excel(path: str, df: pd.DataFrame, sheet_name: str):
    "форматируем колонки файла эксель"
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, na_rep='NaN')

        # автонастройка ширины колонок
        # решил что больше ничего и не нужно
        for column in df:
            width = max(df[column].astype(str).map(len).max(), len(column))
            if width > 45:
                width = 45

            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, width)

        writer.save()
