from pathlib import Path

from fstlabelcreator import utilities


qr_code_data_list = ['https://w3id.org/fst/resource/1ed6c2f8-282a-64b4-94d0-4ee51dfba10e',
                     'https://w3id.org/fst/resource/018bb4b1-db4a-7bbd-a299-ee3b49b5d7f5',
                     'https://w3id.org/fst/resource/018bb4b1-db48-73b8-9d82-8a8ffb6ee225']

# Get path of the current dir
dir_path = Path(__name__).parent.resolve()

qr_code_file_base_name = 'qr_code'
for i, qr_code_data_item in enumerate(qr_code_data_list):
    utilities.generate_QR_code(qr_code_data=qr_code_data_item, qr_code_file_path=f'{dir_path}/{qr_code_file_base_name}{i}.svg')
