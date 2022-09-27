from styleframe import StyleFrame, Styler, utils
import pandas as pd 

def write_styling_excel_file(path,df,sheet_name):
    "Создает отформатированный файл экслеля"
    if len(df) == 0:
        for col in df.columns:
            df.loc[0,col] = 'Внесите значение...'

    excel_writer = StyleFrame.ExcelWriter(path)
    sf = StyleFrame(df)
    sf.apply_headers_style(
            cols_to_style=set(df.columns),
            styler_obj=Styler(
                bg_color=utils.colors.grey,
                bold=True,
                border_type=utils.borders.dash_dot
                )
            )
    sf.apply_column_style(
            cols_to_style=set(df.columns),
            styler_obj=Styler(
                horizontal_alignment=utils.horizontal_alignments.left,
                wrap_text=True,
                font=utils.fonts.dejavu_sans
                ),
            style_header=False
            )
    StyleFrame.A_FACTOR = len(df.columns)*1.2
    StyleFrame.P_FACTOR = 1.1

    sf.to_excel(
        excel_writer = excel_writer,
        best_fit = set(df.columns),
        row_to_add_filters=0,
        sheet_name= sheet_name,
            )
    excel_writer.save()
    return 
