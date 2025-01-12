import unittest
from pathlib import Path


from fstlabelcreator import script_functions

# Get path of this file.
file_directory_path : Path = Path(__file__).parent.resolve()

# Set the paths for the needed directories.
path_for_generated_files = Path(f'{file_directory_path}/_generated')
path_for_generated_files_pID_label_from_excel_sheet : Path = Path(f'{path_for_generated_files}/pID_label_from_excel_sheet')
path_for_generated_files_text_label_from_excel_sheet : Path = Path(f'{path_for_generated_files}/text_label_from_excel_sheet')


path_to_sensor_excel_sheet: Path = Path(f'{file_directory_path}/info_Messtechnik_Uebersicht_FST_Wetterich.xlsx')
path_to_text_excel_sheet: Path = Path(f'{file_directory_path}/id_list.xlsx')

# Create the directories if not already present.
try:
    path_for_generated_files.mkdir()
except FileExistsError:
    pass

try:
    path_for_generated_files_pID_label_from_excel_sheet.mkdir()
except FileExistsError:
    pass

try:
    path_for_generated_files_text_label_from_excel_sheet.mkdir()
except FileExistsError:
    pass

class Testgenerate_sensor_pID_label_sites_from_excel_sheets(unittest.TestCase):
    # Setup delete all generated files.
    def test_generate_sensor_pID_label_sites_from_excel_sheets__00(self):
        # TODO: Write more tests where the label starts in the default position (position 1) or on another row, where the maximum label
        #  amount is exceeded and so on.
        script_functions.generate_sensor_pID_label_sites_from_excel_sheets(path_for_generated_files= path_for_generated_files_pID_label_from_excel_sheet,
                                                                           path_to_sensor_excel_sheet= path_to_sensor_excel_sheet,
                                                                           responsible_WiMi= 'Rexer',
                                                                           label_start_position_number= 3)

class Testgenerate_label_sites_from_excel_sheets(unittest.TestCase):
    # Setup delete all generated files.
    def test_generate_label_sites_from_excel_sheets__00(self):
        script_functions.generate_label_sites_from_excel_sheets(path_for_generated_files= path_for_generated_files_text_label_from_excel_sheet,
                                                                path_to_text_excel_sheet= path_to_text_excel_sheet,
                                                                supported_template= script_functions.SUPPORTED_TEMPLATES['L6011'])

