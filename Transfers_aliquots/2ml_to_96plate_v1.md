# Transferring from 1.5/2ml tubes to a PCR plate

This protocol transfers volumes between 3 and 50 ul from 1.5/2ml tubes (max 96 tubes) to a PCR plate.

## 1) Prepare the mapping file
The protocol requires a mapping file (2ml_to_96plate_v1_map.csv) that specifies the relation between the 1.5/2ml tubes and the PCR plate. A template is available: 2ml_to_96plate_v1_map_template.csv. The structure of the mapping file is as follows:

|Sample|Rack|Position|Well|Volume|
|.....|.....|.....|.....|.....|.....|


Download this template, edit it and upload it to github with the file name 2ml_to_96plate_v1_map.csv. This will overwrite the 2ml_to_96plate_v1_map.csv document. Make sure you do not overwrite the 2ml_to_96plate_v1_map_template.csv file. 
