from pathlib import Path

from reportlab.lib.units import cm
import pandas as pd

from . import utilities

# TODO: FIXME: Maybe move the supported templates into their own python file.
class SupportedTemplate:
    def __init__(self,
                 LABEL_SIZE,
                 RECOMMENDED_MAX_LABEL_PRINT_SIZE,
                 ROW_MAX_LABEL_COUNT,
                 COLUMN_MAX_LABEL_COUNT,
                 MEASURED_START_POSITION,
                 MEASURED_x_DISTANCE_PER_STEP,
                 MEASURED_y_DISTANCE_PER_STEP):

        self.LABEL_SIZE = LABEL_SIZE
        self.RECOMMENDED_MAX_LABEL_PRINT_SIZE = RECOMMENDED_MAX_LABEL_PRINT_SIZE
        self.ROW_MAX_LABEL_COUNT = ROW_MAX_LABEL_COUNT
        self.COLUMN_MAX_LABEL_COUNT = COLUMN_MAX_LABEL_COUNT
        self.MEASURED_START_POSITION = MEASURED_START_POSITION
        self.MEASURED_x_DISTANCE_PER_STEP = MEASURED_x_DISTANCE_PER_STEP
        self.MEASURED_y_DISTANCE_PER_STEP = MEASURED_y_DISTANCE_PER_STEP

SUPPORTED_TEMPLATES = {
    ## AVERY Zweckform B7651 (Sensor p_ID Labels)
    'B7651': SupportedTemplate(LABEL_SIZE=  (3.8 * cm, 2.1 * cm),
                               RECOMMENDED_MAX_LABEL_PRINT_SIZE=  (3.35 * cm, 1.65 * cm),
                               ROW_MAX_LABEL_COUNT=  13,
                               COLUMN_MAX_LABEL_COUNT=  5,
                               MEASURED_START_POSITION=  (0.65 * cm, (29.7 - 3) * cm),
                               MEASURED_x_DISTANCE_PER_STEP=  4.06 * cm,
                               MEASURED_y_DISTANCE_PER_STEP=  -2.12 * cm,
    ),
    ## AVERY Zweckform L6011
    'L6011': SupportedTemplate(LABEL_SIZE=  (6.35 * cm, 2.96 * cm),
                               RECOMMENDED_MAX_LABEL_PRINT_SIZE=  (5.9 * cm, 2.5 * cm),
                               ROW_MAX_LABEL_COUNT=  9,
                               COLUMN_MAX_LABEL_COUNT=  3,
                               MEASURED_START_POSITION=  (0.91 * cm, (29.7 - 4.27) * cm),
                               MEASURED_x_DISTANCE_PER_STEP=  6.6 * cm,
                               MEASURED_y_DISTANCE_PER_STEP=  -2.96 * cm,
                               ),
    ## AVERY Zweckform L6009
    'L6009': SupportedTemplate(LABEL_SIZE=  (4.57 * cm, 2.12 * cm),
                               RECOMMENDED_MAX_LABEL_PRINT_SIZE=  (4.08 * cm, 1.62 * cm),
                               ROW_MAX_LABEL_COUNT=  12,
                               COLUMN_MAX_LABEL_COUNT=  4,
                               MEASURED_START_POSITION=  (1.19 * cm, (29.7 - 4.022) * cm),
                               MEASURED_x_DISTANCE_PER_STEP=  4.83 * cm,
                               MEASURED_y_DISTANCE_PER_STEP=  -2.117 * cm,
                               ),
}

def generate_sensor_pID_label_sites_from_excel_sheets(path_for_generated_files: [str, Path],
                                                      path_to_sensor_excel_sheet: [str, Path],
                                                      responsible_WiMi: str,
                                                      label_start_position_number: int = 1):
    # TODO:FIXME: This is a hardcoded function that only works for sensors from sensor Excel tables. Maybe there is a
    #  way to somehow generalize this function.
    path_for_generated_qrcode_files: Path = path_for_generated_files / 'qr_codes'
    path_for_generated_label_files: Path = path_for_generated_files / 'labels'

    # Create the directories if they are not already present.
    try:
        path_for_generated_qrcode_files.mkdir()
    except FileExistsError:
        pass

    try:
        path_for_generated_label_files.mkdir()
    except FileExistsError:
        pass

    # TODO: Currently the sheet names could be necessary to check for special columns.
    SHEET_NAMES = ['Druck', 'Weg', 'Kraft', 'Temperatur', 'Volumenstrom', 'Leistung'] # 'Beschleunigung'

    # Load and process the Excel sheets.
    for sheet in SHEET_NAMES:
        df = pd.read_excel(f"{Path(path_to_sensor_excel_sheet)}", sheet_name=sheet)
        for index, row in df.iterrows():
            # If the responsible_WiMi isn't as expected continue with the next entry.
            if row['Verantwortlicher WiMi'] != responsible_WiMi:
                continue

            def _format_read_numbers_to_float_or_int(input: str) -> [int, float, str]:
                try:
                    input_as_integer = int(input)
                    input_as_float = float(input)
                except ValueError:
                    # TODO: Maybe a warning?
                    return 'n.conver.'

                if (input_as_integer - input_as_float) == 0:
                    return input_as_integer
                else:
                    return input_as_float

            # Build the data dict.
            if str(row['Ident-Nummer']) == 'nan':
                internal_id = '-'
            else:
                internal_id = row['Ident-Nummer']

            data_dict = {'internal_id': internal_id,
                         'product_name': f'{row["Hersteller"]} {row["Bezeichnung"]}',
                         'measurement_range':
                                f'{_format_read_numbers_to_float_or_int(row["Messbereich von"])} - {_format_read_numbers_to_float_or_int(row["Messbereich bis"])} {row["Messbereich Einheit"]}',
                         'output_range':
                                f'{_format_read_numbers_to_float_or_int(row["Ausgabebereich von"])} - {_format_read_numbers_to_float_or_int(row["Ausgabebereich bis"])} {row["Ausgabebereich Einheit"]}',
                         'p_id': f'https://w3id.org/fst/resource/{row["uuid"]}'
             }

            # TODO: Hardcoded edge case, is there a better way to handle
            # Add "abs/rel" at the end of the measurement_range in case of pressure sensors.
            if sheet == 'Druck':
                absolute_relative_string = ''
                if str(row["absolut/ relativ"]) != 'nan':
                    absolute_relative_string = row["absolut/ relativ"]

                data_dict['measurement_range'] = f'{data_dict["measurement_range"]} ({absolute_relative_string})'

            # Name the file after the uuid.
            qr_code_file_path: Path = Path(path_for_generated_qrcode_files / f'{row["uuid"]}.svg')
            label_file_path: Path = Path(path_for_generated_label_files / f'{row["uuid"]}.pdf')

            # Generate the QR code and the QR code label.
            utilities.generate_QR_code(data_dict['p_id'], qr_code_file_path)
            utilities.generate_pID_QR_code_label(label_file_path, qr_code_file_path, data_dict)


    p_ID_sensor_template = SUPPORTED_TEMPLATES['B7651']
    utilities.place_labels_on_DINA4_template(
                            path_for_generated_files= path_for_generated_files,
                            path_for_generated_label_files= path_for_generated_label_files,
                            row_max_label_count= p_ID_sensor_template.ROW_MAX_LABEL_COUNT,
                            column_max_label_count= p_ID_sensor_template.COLUMN_MAX_LABEL_COUNT,
                            measured_start_position= p_ID_sensor_template.MEASURED_START_POSITION,
                            measured_x_distance_per_step= p_ID_sensor_template.MEASURED_x_DISTANCE_PER_STEP,
                            measured_y_distance_per_step= p_ID_sensor_template.MEASURED_y_DISTANCE_PER_STEP,
                            target_label_size= (3.35 * cm, 1.5 * cm),
                            start_position_number=label_start_position_number)


def generate_label_sites_from_excel_sheets(path_for_generated_files: [str, Path],
                                           path_to_text_excel_sheet: [str, Path],
                                           supported_template: SupportedTemplate,
                                           label_start_position_number: int = 1):

    # Check if the template is supported.
    found_supported_template_flag = 0
    for key in SUPPORTED_TEMPLATES.keys():
        if supported_template is SUPPORTED_TEMPLATES[key]:
            found_supported_template_flag = 1
            break

    if found_supported_template_flag == 0:
        raise NotImplementedError(f"Your provided Template isn't present in the supported ones.")

    qr_codes_directory_path: Path = Path(f'{path_for_generated_files}/_QR_codes/')
    labels_directory_path: Path = Path(f'{path_for_generated_files}/labels/')

    # Create the subdirectories if not already present.
    try:
        labels_directory_path.mkdir(parents=True)
    except FileExistsError:
        pass

    try:
        qr_codes_directory_path.mkdir(parents=True)
    except FileExistsError:
        pass

    # Load the Excel sheet.
    df = pd.read_excel(f'{Path(path_to_text_excel_sheet)}', sheet_name='Sheet1')
    data_dict = df.to_dict(orient='records')
    data_dict_without_doubles = []
    for item in data_dict:
        if item in data_dict_without_doubles:
            continue
        else:
            data_dict_without_doubles.append(item)

    # Generate a QR-Code and label for every line in the Excel table.
    for item in data_dict_without_doubles:
        counter = 0
        while True:
            try:
                data_dict.remove(item)
            except ValueError:
                break

            input_text = item['ID']
            heading = item['heading']
            if '"' == heading[0] and '"' == heading[-1]:
                heading = heading.replace('"', '')

            # TODO: Is a parsing function viable to have more control over the formatting?
            file_name = f"{heading}_{counter}"
            # FIXME: TODO: That 'heading' fields can contain a lot of special characters that are forbidden in file
            #  names. The software throws a weird error in this case. So a parsing function that checks the content
            #  of the 'heading' field and parses it into a acceptable file name needs to be written or it should be
            #  implemented that the files of the single labels follow a standard naming schema.
            if '<br/>' in file_name\
                    or '/' in file_name:
                file_name = file_name.replace('<br/>', '').replace(':', '').replace(',', '').replace('/', '').replace('</b>', '').replace('<b>', '')

            utilities.generate_text_QR_code_label(input_text= input_text,
                                                  heading_text= heading,
                                                  label_size= supported_template.RECOMMENDED_MAX_LABEL_PRINT_SIZE,
                                                  file_name= file_name,
                                                  qr_code_directory_path= qr_codes_directory_path,
                                                  label_directory_path= labels_directory_path)

            counter = counter + 1


    # Place the created labels on the site.
    utilities.place_labels_on_DINA4_template(
                            path_for_generated_files= path_for_generated_files,
                            path_for_generated_label_files= labels_directory_path,
                            row_max_label_count= supported_template.ROW_MAX_LABEL_COUNT,
                            column_max_label_count= supported_template.COLUMN_MAX_LABEL_COUNT,
                            measured_start_position= supported_template.MEASURED_START_POSITION,
                            measured_x_distance_per_step= supported_template.MEASURED_x_DISTANCE_PER_STEP,
                            measured_y_distance_per_step= supported_template.MEASURED_y_DISTANCE_PER_STEP,
                            target_label_size= supported_template.RECOMMENDED_MAX_LABEL_PRINT_SIZE,
                            start_position_number=label_start_position_number)

