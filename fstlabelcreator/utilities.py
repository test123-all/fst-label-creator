import os
import sys
from pathlib import Path
import copy
import subprocess


import qrcode
import qrcode.image.svg

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.graphics import renderPDF
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from svglib.svglib import svg2rlg

# TODO: This document still needs to be commented sufficiently.

def generate_QR_code(qr_code_data : str, qr_code_file_path: [str, Path]):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        image_factory=qrcode.image.svg.SvgPathImage
    )

    qr.add_data(qr_code_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_code_file_path: Path = Path(qr_code_file_path)
    img.save(f'{qr_code_file_path}')


def generate_pID_QR_code_label(label_file_path:[str,Path], qr_code_file_path:[str,Path], data_dict: dict):
    # LABEL_SIZE = (3.5 * cm, 1.5 * cm)
    LABEL_SIZE = (3.35 * cm, 1.5 * cm)
    PADDING_FACTOR = 47 / 626  # measured

    # Create pdf canvas.
    canvas = Canvas(f'{label_file_path}', pagesize=LABEL_SIZE)

    # Create a drawing object of the QR Code and add it to the canvas.
    qr_code__drawing = svg2rlg(qr_code_file_path)
    # The QR-Code should be 1.5cm x 1.5cm, x and y should be equal
    target_qr_code_length_in_points = LABEL_SIZE[1]
    scaling_factor = (target_qr_code_length_in_points)/qr_code__drawing.height
    qr_code__drawing.scale(scaling_factor, scaling_factor) # scaling factor is equal for x and y since rectangular
    renderPDF.draw(qr_code__drawing, canvas, 0, 0)

    # Get example styles for the text
    stylesheet = getSampleStyleSheet()
    normal_style = copy.deepcopy(stylesheet['Normal'])
    pid_normal_style = copy.deepcopy(stylesheet['Normal'])
    heading_style = stylesheet['Heading1']

    MEASURED_DIVISION_FACTOR = 2.9
    normal_style.fontSize = normal_style.fontSize / MEASURED_DIVISION_FACTOR
    normal_style.leading = normal_style.leading / MEASURED_DIVISION_FACTOR

    pid_normal_style.fontSize = pid_normal_style.fontSize / MEASURED_DIVISION_FACTOR
    pid_normal_style.leading = pid_normal_style.leading / MEASURED_DIVISION_FACTOR
    pid_normal_style.fontSize = pid_normal_style.fontSize - 0.5 #measured

    # normal_style.underlineGap = normal_style.fontSize / 5

    # # heading_paragraph = Paragraph(df["heading"][i], heading_style, bulletText=None, frags=None, caseSensitive=1,
    # #                               encoding='utf8')
    # w_heading, h_heading = heading_paragraph.wrap(
    #     (drawing.height * 1.5) - (drawing.height * percentual_padding) / 2,
    #     drawing.height)
    # heading_paragraph.drawOn(canvas,
    #                          drawing.height * 1,
    #                          drawing.height - h_heading - (drawing.height * percentual_padding))

    if 'V' in data_dict["output_range"]:
        input_text = (f'<b>{data_dict["internal_id"]} </b><br/>'
                      f'{data_dict["product_name"]} <br/>'
                      f'measm. range: &nbsp; {data_dict["measurement_range"]} <br/>'
                      f'volt. range: &nbsp; {data_dict["output_range"]} <br/>'
                      )
    elif 'A' in data_dict["output_range"]:
        input_text = (f'<b>{data_dict["internal_id"]} </b><br/>'
                      f'{data_dict["product_name"]} <br/>'
                      f'measm. range: &nbsp; {data_dict["measurement_range"]} <br/>'
                      f'amper. range: &nbsp; {data_dict["output_range"]} <br/>'
                      )
    else:
        raise Exception(f"The used unit in {data_dict['output_range']} isn't supported yet. Please contact the maintainers.")

    text_paragraph = Paragraph(input_text, normal_style, bulletText=None, frags=None, caseSensitive=1,
                               encoding='utf8')
    padding_length_in_points = LABEL_SIZE[1] * PADDING_FACTOR
    w_text, h_text = text_paragraph.wrap(LABEL_SIZE[0] - LABEL_SIZE[1] - padding_length_in_points/2,
                                         LABEL_SIZE[1] - 2*padding_length_in_points)
    text_paragraph.drawOn(canvas,
                          LABEL_SIZE[1] * 1,
                          LABEL_SIZE[1] - padding_length_in_points - normal_style.fontSize/4 - h_text)


    pid_url_text = f'p_ID: {data_dict["p_id"]}'
    pID_url_paragraph = Paragraph(pid_url_text, pid_normal_style, bulletText=None, frags=None, caseSensitive=1,
                               encoding='utf8')

    # TODO: the wrapping isn't that easy with twol paragraphs
    w_pid_url_text, h_pid_url_text = pID_url_paragraph.wrap(LABEL_SIZE[0] - LABEL_SIZE[1] - padding_length_in_points / 2,
                                         LABEL_SIZE[1] - 2 * padding_length_in_points)
    pID_url_paragraph.drawOn(canvas,
                          LABEL_SIZE[1] * 1,
                          padding_length_in_points + normal_style.fontSize / 4)#LABEL_SIZE[1] - padding_length_in_points - normal_style.fontSize / 4 - h_text - h_pid_url_text)

    canvas.save()


def place_labels_on_DINA4_template(path_for_generated_files: [str, Path],
                                   path_for_generated_label_files: [str, Path],
                                   row_max_label_count: int,
                                   column_max_label_count: int,
                                   measured_start_position: tuple,
                                   measured_x_distance_per_step: float,
                                   measured_y_distance_per_step: float,
                                   target_label_size: tuple,
                                   start_position_number: int = 1):
    cwd = Path.cwd()
    resolved_path = path_for_generated_label_files.resolve()
    os.chdir(str(resolved_path))

    # Convert the label pdf to svg
    
    if not(sys.platform.startswith('linux') or sys.platform.startswith('win32')):
        # TODO: FIXME: Find a better error message
        raise Warning(f"You are running the FST Label Creator on the platform '{sys.platform}', that isn't tested yet. Please write the maintainers an email and share your findings with them to improve this software product. Thank You.")

    for item in resolved_path.glob('*.pdf'):
        subprocess.run(['inkscape', '--export-type=svg', f'--export-filename={item.stem}.svg', f'{item.stem}.pdf'])
    os.chdir(str(cwd))

    # Als erstes DNAA4 Seite erstellen und dann anordnen
    DINA4_SITE_SIZE = (21.0 * cm, 29.7 * cm)
    PADDING_FACTOR = 47 / 626  # measured

    # Create pdf canvas.
    print(len(list(resolved_path.glob('*.svg'))))
    # Die Liste soll von oben nach unten und von Links nach rechts angeordnet werden, 65 gehen auf eine Seite, 5 pro Reihe bei 13 Reihen
    row_position_counter: int = 1
    column_position_counter: int = 1
    seiten_counter: int = 1

    # Set the label row_position_counter and column_position_counter accordingly top the position that the labels should
    # start on the side.
    MAXIMUM_AMOUNT_OF_LABELS = row_max_label_count * column_max_label_count
    if start_position_number > MAXIMUM_AMOUNT_OF_LABELS:
        # TODO: Find a better suiting exception.
        raise Exception(f'The following label start position was declared: {start_position_number}\n'
                        f'But the chosen label template only contains: {MAXIMUM_AMOUNT_OF_LABELS} labels.\n'
                        f'Please make sure that the start_position_number of the first label is smaller than the '
                        f'amount of labels of the template that it will be possible to place labels.')

    # Calculate the start label position.
    for _ in range(start_position_number - 1):
        if column_position_counter > column_max_label_count:
            column_position_counter = 1
            row_position_counter += 1

        column_position_counter += 1

    # Create the canvas and sort the label names that they will be printed on the page in order.
    canvas = Canvas(f'{path_for_generated_files}/seite{seiten_counter}.pdf', pagesize=DINA4_SITE_SIZE)
    converted_svg_labels_list: list = list(resolved_path.glob('*.svg'))
    converted_svg_labels_list.sort()

    for item in converted_svg_labels_list:
        # Calculate position
        position_x = measured_start_position[0] + (column_position_counter - 1) * measured_x_distance_per_step
        position_y = measured_start_position[1] + (row_position_counter - 1) * measured_y_distance_per_step
        print(f'{position_x, position_y}')
        # Create a drawing object of the QR Code and add it to the canvas.
        label__drawing = svg2rlg(str(item))
        scaling_factor_x = target_label_size[0] / label__drawing.width
        scaling_factor_y = target_label_size[1] / label__drawing.height
        print(scaling_factor_x)
        label__drawing.scale(scaling_factor_x, scaling_factor_y)

        if not round(label__drawing.width / label__drawing.height, 4) == round(
                target_label_size[0] / target_label_size[1], 4):
            Warning(
                f"The Label at position ({position_x}, {position_y}) doesn't has the expected size and therefore gets squished to fit the space")

        renderPDF.draw(label__drawing, canvas, position_x, position_y)

        column_position_counter += 1

        if column_position_counter > column_max_label_count:
            column_position_counter = 1
            row_position_counter += 1

        if row_position_counter > row_max_label_count:
            seiten_counter += 1
            canvas.save()
            # Create new canvas for the next iteration
            canvas = Canvas(f'{path_for_generated_files}/seite{seiten_counter}.pdf', pagesize=DINA4_SITE_SIZE)
            print('Neuuee Seite! :D')
            row_position_counter = 1

    canvas.save()


def generate_text_QR_code_label(input_text: str,
                                heading_text: str,
                                label_size: tuple,
                                file_name: str,
                                qr_code_directoy_path: [str,Path],
                                label_directory_path: [str,Path]):
    try:
        Path(qr_code_directoy_path).mkdir()
    except FileExistsError:
        pass

    try:
        Path(label_directory_path).mkdir()
    except FileExistsError:
        pass

    MEASURED_PADDING_FACTOR = 47 / 626  # measured
    qr_code_file_path: Path = Path(qr_code_directoy_path) / f'{file_name}.svg'
    label_file_path: Path = Path(label_directory_path) / f'{file_name}.pdf'
    label_width_in_points = label_size[0] * cm
    label_height_in_points = label_size[1] * cm

    # Create QR-Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        image_factory=qrcode.image.svg.SvgPathImage
    )

    qr.add_data(input_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(str(qr_code_file_path.resolve()))

    canvas = Canvas(str(label_file_path.resolve()), pagesize=(label_size[0] * cm, label_size[1] * cm))
    drawing = svg2rlg(str(qr_code_file_path.resolve()))
    scale_factor_drawing = label_height_in_points / drawing.height
    drawing.scale(scale_factor_drawing, scale_factor_drawing)
    # Since the drawing.widht and .height are always the old value and and scaling value changes the values
    # need to be calculated
    scaled_drawing_width_in_points = drawing.width * scale_factor_drawing
    scaled_drawing_height_in_points = drawing.height * scale_factor_drawing

    renderPDF.draw(drawing, canvas, 0, 0)
    stylesheet = getSampleStyleSheet()
    normal_style = stylesheet['Normal']
    heading_style = stylesheet['Heading1']

    LINE_COUNT = 15
    new_fontsize = label_height_in_points / LINE_COUNT
    fontsize_factor =  new_fontsize / normal_style.fontSize

    normal_style.fontSize = normal_style.fontSize * fontsize_factor
    normal_style.leading = normal_style.leading * fontsize_factor
    heading_style.fontSize = heading_style.fontSize * fontsize_factor
    heading_style.leading = heading_style.leading * fontsize_factor

    heading_paragraph = Paragraph(heading_text, heading_style, bulletText=None, frags=None, caseSensitive=1,
                                  encoding='utf8')
    text_width = label_width_in_points - scaled_drawing_width_in_points - (scaled_drawing_height_in_points * MEASURED_PADDING_FACTOR) / 2
    text_height = label_width_in_points - (scaled_drawing_height_in_points * MEASURED_PADDING_FACTOR)
    w_heading, h_heading = heading_paragraph.wrap(text_width, text_height)
    heading_paragraph.drawOn(canvas,
                             scaled_drawing_width_in_points,
                             label_height_in_points - (scaled_drawing_height_in_points * MEASURED_PADDING_FACTOR) - h_heading)

    text_paragraph = Paragraph(input_text, normal_style, bulletText=None, frags=None, caseSensitive=1, encoding='utf8')
    w_text, h_text = text_paragraph.wrap(text_width, text_height)
    text_paragraph.drawOn(canvas,
                          scaled_drawing_width_in_points,
                          label_height_in_points - (scaled_drawing_height_in_points * MEASURED_PADDING_FACTOR) - h_heading - h_text)

    canvas.save()

