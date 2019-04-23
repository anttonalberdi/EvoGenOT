# Transferring liquid from 96 well plate to 1.5/2ml tubes

This protocol transfers volumes between 1 and 10 ul from a 96 well PCR plate to 1.5/2ml tubes.

## 1) Prepare the mapping file
The protocol requires a mapping file (amplicon_pooling_v1_map.csv) that specifies the relation between the PCR plate and the 1.5/2ml tubes. A template is available: amplicon_pooling_v1_map_template.csv. The structure of the mapping file is as follows:

|Well|Pool|Volume|
|------|----|--------|
|A1|1|5.23|
|A2|1|1.34|

* Well: specifies the coordinate of the well in the PCR plate (A1-H12)
* Pool: specifies the pool tube (e.g. 1,2,3). The script will automatically change to coordinates (e.g. A1, A2)
* Volume: specifies the volume to be transferred in ul (needs to be between 1 and 10 ul).

Download the template csv file, edit it and upload it to github with the file name amplicon_pooling_v1_map.csv. This will overwrite the existing document with the same name. Make sure you do not overwrite the amplicon_pooling_v1_map_template.csv file. The columns must be comma-separated.

## 2) Download the mapping file and transfer to the OT2 robot
Bla bla

## 3) Load the protocol in the OT2 app

## 4) Check and calibrate pipette

## 5) Place and calibrate labware

## 6) Doublecheck the operations in the OT2 app

## 7) Run the protocol
