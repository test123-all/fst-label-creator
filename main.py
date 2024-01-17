from pathlib import Path

from fstlabelcreator import script_functions

# Set the paths
path_for_generated_files: Path = Path(f'./_generated')
path_for_generated_files_text_label_from_excel_sheet: Path = Path(f'{path_for_generated_files}/text_label_from_excel_sheet')
path_to_text_excel_sheet: Path = Path(f'./id_list.xlsx')

script_functions.generate_label_sites_from_excel_sheets(path_for_generated_files= path_for_generated_files_text_label_from_excel_sheet,
                                                        path_to_text_excel_sheet= path_to_text_excel_sheet,
                                                        supported_template= script_functions.SUPPORTED_TEMPLATES['B7651'])

