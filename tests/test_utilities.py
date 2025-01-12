import unittest
from pathlib import Path

from reportlab.lib.units import cm

from fstlabelcreator import utilities

# Get the path of this file.
file_directory_path : Path = Path(__file__).parent.resolve()

# Set paths for the different directories.
path_for_generated_files : Path = Path(f'{file_directory_path}/_generated')
path_for_generated_files_test_utilities : Path = Path(f'{path_for_generated_files}/test_utilities')
path_for_generated_qrcode_files : Path = Path(f'{path_for_generated_files_test_utilities}/qr_codes')
path_for_generated_label_files : Path = Path(f'{path_for_generated_files_test_utilities}/labels')

# Create the directories if they are not already present.
try:
    path_for_generated_files.mkdir()
except FileExistsError:
    pass

try:
    path_for_generated_files_test_utilities.mkdir()
except FileExistsError:
    pass

try:
    path_for_generated_qrcode_files.mkdir()
except FileExistsError:
    pass

try:
    path_for_generated_label_files.mkdir()
except FileExistsError:
    pass


class TestGenerateQRCode(unittest.TestCase):
    # Setup delete all generated files.
    def test_generate_QR_code__00(self):
        QR_code_data = 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'
        utilities.generate_QR_code(QR_code_data, Path(path_for_generated_qrcode_files/'test.svg'))

class TestGenerateQRCodeLabel(unittest.TestCase):
    def test_generate_pID_QR_code_label__00(self):
        data_dict = {'internal_id': 'D092',
                     'product_name': 'Keller PAA',
                     'measurement_range': '0 - 10 bar (a)',
                     'voltage_range': '0 - 10 V',
                     'p_id': 'https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8'
                    }

        utilities.generate_pID_QR_code_label(Path(path_for_generated_label_files/'label.pdf'), Path(path_for_generated_qrcode_files/'test.svg'), data_dict)

class Testgenerate_text_QR_code_label(unittest.TestCase):
    def test_generate_text_QR_code_label__00(self):
        utilities.generate_text_QR_code_label(input_text= 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,',
                                              heading_text= 'Heading',
                                              label_size= (6.35 * cm, 2.96 * cm),
                                              file_name= 'test_text_QR_code_label',
                                              qr_code_directory_path= path_for_generated_qrcode_files,
                                              label_directory_path= path_for_generated_label_files)

