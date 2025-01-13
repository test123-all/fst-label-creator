<!-- heading declaration and main RDFa data declaration in HTML-->
<div xmlns:schema="https://schema.org/" typeof="schema:SoftwareSourceCode" id="software-1">
   <h1 property="schema:name">FST Label Creator</h1>
   <meta property="schema:codeRepository" content="https://github.com/test123-all/fst-label-creator">
   <meta property="schema:codeSampleType" content="full solution">
   <meta property="schema:license" content="https://www.gnu.org/licenses/lgpl-3.0.html">
   <meta property="schema:programmingLanguage" content="Python">
   <h2>Introduction:</h2>
   <p property="schema:description">
      This is the repository of the FST Label Creator software/python package. The goal of this software is to provide
      user friendly functions to generate labels that contain a QR-Code and some text/loaded data. In more detail this
      can be used to generate persistent identifier (p_ID) labels where the QR-Code points to a p_ID URL like 
      <a href="https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8">https://w3id.org/fst/resource/0184ebd9-988b-7bba-8203-06be5cf6bbb8</a>
      and the text displays information about the referenced object.
      <br>
      This software also supports placing those labels onto a DIN A4 PDF site template, to be able to print the .pdf 
      sites, and therefore your own labels. Also bulk creation and placing with data read out of Excel tables is
      supported. <br>
      Currently this software only supports the bulk creation of sensor p_ID labels and normal text labels 
      where the text gets encoded inside the QR code instead of the p_ID URL with data read out of Excel tables.
      For visible examples for the different label models please have a look at the 'How to use this package?'-section.
      Examples for full .pdf pages with placed labels and a test fit background can be found behind the following
      hyperlinks: <br>
      <ol>
         <li>
             <a href="SUPPORTED_TEMPLATES/test_fit_template_AveryB7651.png">p_ID sensor labels full page test fit</a>
         </li>
         <li>
             <a href="SUPPORTED_TEMPLATES/test_fit_template_AveryL6009.png">labels with heading full page test fit</a>
         </li>
      </ol>
   </p>
</div>

<b>DISCLAIMER:</b> <br>
This software in its current version is in an early proof of concept phase and used in the 
https://preprints.inggrid.org/repository/view/40/ paper and contributed to the results mentioned in the paper.<br>
<br>
Since this software is in an early proof of concept phase it is not commented out comprehensively yet,
the functional segregation isn't good and in conclusion the function and variable names might be subject to 
significant change in the future. Therefore, the backwards compatibility of the API won't be granted for now. <br>
<br>
Please note that we are no longer able to provide an exact time span for the refactoring work at this time, as the 
German government has recently reduced funding for scientific purposes overall, leaving the future of all sciences 
somewhat uncertain. Thank you very much for your understanding.

Furthermore, the persistent ID namespace (https://w3id.org/fst/resource/) for the sensor labels is currently hardcoded
into the script_functions.py file and therefore your generated sensor labels will point only to this persistent ID 
namespace. A '#TODO' to remove this limitation and give different users more liberties is already added.

## Installation Instructions:
### Introduction (all platforms):
You need to have python3 (>3.10 https://www.python.org/) and inkscape (https://inkscape.org/) installed. <br>
Also it is recommended, for development explicitily needed, to use the python package manager poetry (https://python-poetry.org/). <br>

If you are just a user of the library you can get along with the "venv" program, that gets shipped together with python.
Therefore, you don't need to download and install poetry just to use this software.
For installation introductions on windows with venv please have a look at the next subsection.

### On Windows with venv:
Introductions:

0. Please make sure, as already mentioned, you have python3 (>3.10 https://www.python.org/) and inkscape (https://inkscape.org/) installed.
1. Also, please make sure to add Inkscape to your windows PATH. To do this please run ```cmd``` as administrator and run the command 
    ```
    setx /M "%PATH%;<<path_to_your_incscape_installation>>"
    ```
    with your Inkscape path. For example:
    ```
    setx /M "%PATH%;C:\Program Files\Inkscape\bin\"
    ```
    . After that please make sure to **restart your computer** and run ```inkscape -V``` in the command line. That should run successfully and return something like 
    ``` cmd
    C:\Users\sebastian>inkscape -V
    Inkscape 1.2.1 (9c6d41e410, 2022-07-14)
    ```
    . If you don't have administrator rights on your computer please contact your administrator or search on the internet on how to set the user environment variables.
2. Clone or download this FST Label Creator git-repository
3. Please navigate with your command line program inside the folder where this README.md is located (for example with `cd C:\Users\Neumeier\Desktop\fst-label-creator`)
4. Inside this folder run with the Windows command line "cmd" the command `py -m venv env`. (This will create a virtual environment, that won't mess up your system python installation)
5. Next run the command `.\env\Scripts\activate` to activate that environment
6. After setting up the virtual environment you are ready to install the neccessary packages with the command `py -m pip install qrcode reportlab svglib pandas openpyxl`
7. Next you are able to run the scripts with for example `python .\main.py`

8. At the end please deactivate the virtual environment with `.\env\Scripts\deactivate`


## How to use this package?:
1. Please make sure you followed the installation intructions properly.
The example Excel sheets can be found inside the `./tests/` directory.

2. Next create a `test.py` Python file inside this folder.

3.
- If you want to bulk create labels with a heading, like this,
<img src="doc/example_text_label_your_heading.png"  width="300">

from an Excel sheet use the following code and please adjust the used paths accordingly:

```python
from pathlib import Path

from fstlabelcreator import script_functions

# Set the paths
path_for_generated_files: Path = Path(f'./_generated')
path_for_generated_files_text_label_from_excel_sheet: Path = Path(f'{path_for_generated_files}/text_label_from_excel_sheet')
path_to_text_excel_sheet: Path = Path(f'./id_list.xlsx')

script_functions.generate_label_sites_from_excel_sheets(path_for_generated_files= path_for_generated_files_text_label_from_excel_sheet,
                                                        path_to_text_excel_sheet= path_to_text_excel_sheet,
                                                        supported_template= script_functions.SUPPORTED_TEMPLATES['L6011'])
```
- If you want to bulk create PID labels for sensors, like this,
<img src="doc/example_pid_label_0184ebd9-988b-7bba-8203-06be5cf6bbb8.png"  width="300">

from an Excel sheet please use the following code and adjust the used paths accordingly:

```python
from pathlib import Path

from fstlabelcreator import script_functions

# Set the paths
path_for_generated_files: Path = Path(f'./_generated')
path_for_generated_files_pID_label_from_excel_sheet: Path = Path(f'{path_for_generated_files}/pID_label_from_excel_sheet')
path_to_sensor_excel_sheet: Path = Path(f'./info_Messtechnik_Uebersicht_FST_Wetterich.xlsx')

script_functions.generate_sensor_pID_label_sites_from_excel_sheets(path_for_generated_files= path_for_generated_files_pID_label_from_excel_sheet,
                                                                   path_to_sensor_excel_sheet= path_to_sensor_excel_sheet,
                                                                   responsible_WiMi= 'Rexer')
```

## Supported Templates:
Currently supported are the following templates:
- #TODO: Check whether AveryZweckform uses the same template on every different product range with the same number of labels on each DIN A4 page (for example 65, 27, 48 and so on)
1. <b> 'B7651'</b>: AveryZweckform B7651-? Ultra-Resistente Etiketten 38mmx21mm (65 labels per DIN A4 page)
2. <b> 'L6011'</b>: AveryZweckform L6011-? Typenschild-Etiketten 63.5mmx29.6mm (27 labels per DIN A4 page)
3. <b> 'L6009'</b>: AveryZweckform L6009-? Typenschild-Etiketten 45.7mmx21.2mm (48 labels per DIN A4 page)

## Possible Improvements:
The following list includes possible improvements that have been identified up to this version:
1. TODO: Search for additional possible use cases and functions followed by a reevaluation of the current software.
2. TODO: After this restructuring and extensive refactoring of the existing code (add docstrings to the 
refactored functions, test case clean up and documentation).
3. For example: Implement a rdf library to be able to load rdf data that can be used on the labels. Maybe add also
function that sorts different information by the order of given rdf tags.  This also could be a type of "template function"
4. For example: The sensor template could be generatable with an Ontology and an RDF Query based on a standard label 
template with line positions and rules. Which should be calculable by the label size and other rule[s] like the
distance from which a normal user should be able to read the label. Also handle edge cases that everything fits
well and add output with suggestions if it doesn't. Combined that would make it really easy for the user to
5. A function that fits the pid template on different given or label sizes. On larger objects bigger labels with bigger
text could be needed to be able to find and read the text from a bigger distance.
6. Write a CLI for the program
7. Add a CI/CD testing pipeline for this repository on GitHub (please choose a docker image where you can install
inkscape) and extend the tests
8. Sphinx documentation generator, through CI/CD of this package.
9. Add a function that automatically test fits a generated site on the used template .pdf/.png ()
10. Add additional label sizes to the supported_templates / Add a contributing guide on how other people can add a new
template and what they need to provide for it to be accepted.
11. Improve the outputs off the software, maybe add the logging module that prints the output properly.
The placement of the labels should still be displayed e.g. "Place label xy on site_z at (...)", "Starting new site" "Generate QR-Code ...", ..
12. Add a table of contents to this README.md and properly structure it.
13. Add a contributing file and split it in one part for contributing/refactoring code and one for contributing sizes
for new templates that should get supported
14. If a CI/CD pipeline is added for this repository and even more URLs should be used in the documentation add a URL
checker to check this URLS if they still resolve properly
15. Is a parsing function viable to have more control over the formatting?
16. The ```generate_QR_code(...)```-function outputs a svg file without .svg ending. The user has to set it by
herself/himself. Since it is always .svg, set it in the code and check the input from the user.
Throw a warning/error (might be a subject for discussion) if the user uses an unresolveable '.' and probably tries to
force a file format. Unresolveable means: The '.' and '..' are also used to navigate the directory structure and if
they can't be resolved into a correct directory path it probably is a user error or the '.' of the file format.
17. Add use cases as examples to this repository.
18. Move the supported templates inside their own file(s) or even directory.
19. Add a section that describes the used Excel sheet format conventions in more detail, that the users know how to use
and modify them.


## Current To-Do List:
1. test the path of inkscape on a Windows machine.
2. Take a look at the incskape bug.
3. Convert the use of pandas to load the Excel sheets to openpyxl as it is used in the background anyway to be able to
drop pandas as dependency.
4. Implement a function that creates directories recurseviely if they shouldn't exist when the user references a save-to
location.
5. Make the currently hardcoded persistent namespace (`https://w3id.org/fst/resource/`) inside the 
`script_functions.py` file a function argument. That will enable users outside the FST to also generate their own
sensor labels.
6. The 'generate_label_sites_from_excel_sheets(...)' function takes the content of the 'heading' column as file name.
That fields can contain a lot of special characters that are forbidden in file names. The software throws a weird error
in this case. So a parsing function that checks the content of the 'heading' field and parses it into an acceptable
file name needs to be written, or it should be implemented that the files of the single labels follow a standard
naming schema.

## Dependencies:
This python package uses the following third party python packages and software as dependency:
- qrcode _ BSD License, Other/Proprietary License (BSD) (https://pypi.org/project/qrcode/ [Last Access at 12th January 2025])
- reportlab open source version _ BSD License (BSD license (see license.txt for details) (https://pypi.org/project/reportlab/ [Last Access at 12th January 2025], https://docs.reportlab.com/reportlab/userguide/ch1_intro/ [Last Access at 03th October 2023])
- svglib _ GNU Lesser General Public License v3 (LGPLv3) (LGPL 3) (https://pypi.org/project/svglib/ [Last Access at 12th January 2025])
- pandas + openpyxl (to load the data of the Excel sheets) _ BSD License (BSD 3-Clause License Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and...) (https://pypi.org/project/openpyxl/ [Last Access at 12th January 2025]) 
- Inkscape _ GNU General Public License, version 2 (https://inkscape.org/ [Last Access at 12th January 2025])

Since Inkscape is only used as an external tool, the current license choice is LGPLv3.
This might change in the future during the restructuring and refactoring process if we find open-source software 
packages with less restrictive licenses or are able to replace them with self-written code.


<!-- maintainer- and creator- RDFa data declaration in HTML-->
<div xmlns:schema="https://schema.org/" about="#software-1">
    <h2>Current Maintainer[s]:</h2>
    <div typeof="schema:Person">
        <strong property="schema:givenName">Sebastian</strong>
        <strong property="schema:familyName">Neumeier</strong>
        <strong>(<a href="https://orcid.org/0000-0001-9533-9004" property="schema:identifier">https://orcid.org/0000-0001-9533-9004</a>)</strong>
        <span property="schema:email">sebastian.neumeieratstud.tu-darmstadt.de</span>
    </div>
    <h2>Authors:</h2>
    <p xmlns:dcterms="http://purl.org/dc/terms/">The first running version of this software was originally created in 
         <span property="dcterms:date" content="2023-10-01">October 2023</span>
     by:
    </p>
    <div typeof="schema:Person">
        <strong property="schema:givenName">Sebastian</strong>
        <strong property="schema:familyName">Neumeier</strong>
        <strong>(<a href="https://orcid.org/0000-0001-9533-9004" property="schema:identifier">https://orcid.org/0000-0001-9533-9004</a>)</strong>
        , <span property="schema:affiliation">
            Chair of Fluid Systems at Technical University of Darmstadt 
            (<a href="https://ror.org/05n911h24">https://ror.org/05n911h24</a>)
        </span>
        : <span property="schema:role">Conceptualization, Implementation, Documentation</span>.
    </div>
    <div typeof="schema:Person">
        <strong property="schema:givenName">Manuel</strong>
        <strong property="schema:familyName">Rexer</strong>
        <strong>(<a href="https://orcid.org/0000-0003-0559-1156" property="schema:identifier">https://orcid.org/0000-0003-0559-1156</a>)</strong>
        , <span property="schema:affiliation">
            Chair of Fluid Systems at Technical University of Darmstadt 
            (<a href="https://ror.org/05n911h24">https://ror.org/05n911h24</a>)
        </span>
        : <span property="schema:role">Project Manager, Provider of the Use Cases, Supervision</span>.
    </div>
</div>

## Additional Ressources:
This software is somehow connected to the following paper[s] or contributed to the results of the following papers:
<ol>
   <li>
       <div>
           <strong>
               <span property="schema:name">How to Make Bespoke Experiments FAIR: Modular Dynamic Semantic Digital Twin and Open Source Information Infrastructure</span>
               <span>(</span>
               <a property="schema:relatedLink" href="https://preprints.inggrid.org/repository/view/40/" typeof="schema:Article"> 
                   <span>https://preprints.inggrid.org/repository/view/40/</span>
               </a>
               <span>)</span>
           </strong>
           <span>(January 2025, currently only available as a preprint.)</span>
       </div>
   </li>
</ol>

