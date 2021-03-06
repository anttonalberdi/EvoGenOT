# Transferring liquid from 1.5/2ml tubes to a PCR plate

This protocol transfers volumes between 3 and 50 ul from 1.5/2ml tubes (max 96 tubes) to a PCR plate.

## 1) Prepare the mapping file
The protocol requires a mapping file (2ml_to_96plate_v1_map.csv) that specifies the relation between the 1.5/2ml tubes and the PCR plate. A template is available: 2ml_to_96plate_v1_map_template.csv. The structure of the mapping file is as follows:

|Sample|Rack|Position|Well|Volume|
|------|----|--------|----|------|
|Sample1name|1|A1|A1|5|
|Sample2name|1|A2|B1|5|

* Sample: the sample name column is not actually used in the protocol, it is just for identification purposes.
* Rack: specifies in which of the 4 possible racks the source tube is located (1-4).
* Position: specifies the coordinate of the tube within the specified rack (A1-D6).
* Well: specifies the coordinate of the well in the PCR plate (A1-H12)
* Volume: specifies the volume to be transferred in ul.

You can specify any relation between 1.5/2ml tubes and PCR plate wells. For instance, if you require one sample to be distributed to multiple PCR plate wells, just use the same source coordinates (rack and position) with different PCR plate well coordinates. The columns must be comma-separated.

Download the template csv file, edit it and upload it to github with the file name 2ml_to_96plate_v1_map.csv. This will overwrite the existing document with the same name. Make sure you do not overwrite the 2ml_to_96plate_v1_map_template.csv file. 

## 2) Download the mapping file and transfer to the OT2 robot
Bla bla

## 3) Load the protocol in the OT2 app

## 4) Check and calibrate pipette

## 5) Place and calibrate labware

## 6) Doublecheck the operations in the OT2 app

## 7) Run the protocol
