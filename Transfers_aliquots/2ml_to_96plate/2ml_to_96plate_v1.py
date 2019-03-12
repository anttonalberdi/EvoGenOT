metadata = {
    'protocolName': '1.5/2ml to 96-well plate transfer',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/02/26',
    'validation_date': '2019/02/28',
    'description': 'Protocol for transferring liquids from 1.5/2ml to 96-well plate transfer',
}

#### CHANGELOG  ####

#2018/03/11, Antton - Blow out added to the transfer to plate

#### LIBRARIES ####

import csv
#Opentrons presets
from opentrons import labware, instruments, modules, robot
#Custom presets
import os,sys
sys.path.append("/root")
import custom_labware

#### INPUT FILES ####

#Load data files
racklist=[]
positionlist=[]
welllist=[]
volumelist=[]
with open("/root/csv/2ml_to_96plate_v1_map.csv", "r") as csvfile:
    transfermap = csv.reader(csvfile, delimiter=',')
    for i in transfermap:
        racklist.append(i[1])
        positionlist.append(i[2])
        welllist.append(i[3])
        volumelist.append(i[4])

racklist.pop(0)
positionlist.pop(0)
welllist.pop(0)
volumelist.pop(0)

#### MODULES ####

#Source tubes (only load if mentioned in the map file)
if "1" in racklist:
    tube_rack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '2', share=True)
if "2" in racklist:
    tube_rack2 = labware.load('opentrons-tuberack-2ml-eppendorf', '5', share=True)
if "3" in racklist:
    tube_rack3 = labware.load('opentrons-tuberack-2ml-eppendorf', '8', share=True)
if "4" in racklist:
    tube_rack4 = labware.load('opentrons-tuberack-2ml-eppendorf', '11', share=True)

#Plate
PCR_plate1 = labware.load('96-PCR-flat', '9', share=True)

#### TIP RACKS ####
tiprack_10 = labware.load('labsolute-tiprack-10µl', '6')

#### PIPETTES ####
s10 = instruments.P10_Single(mount='left', tip_racks=[tiprack_10])

#### LIQUID HANDLING ####
if "1" in racklist:
    positionsubset=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "1"])]
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "1"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "1"])]
    s10.transfer(volumesubset, tube_rack1.wells(positionsubset), PCR_plate1.wells(wellsubset), blow_out=True, touch_tip=True, new_tip='always')
if "2" in racklist:
    positionsubset=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "2"])]
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "2"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "2"])]
    s10.transfer(volumesubset, tube_rack2.wells(positionsubset), PCR_plate1.wells(wellsubset), blow_out=True, touch_tip=True, new_tip='always')
if "3" in racklist:
    positionsubset=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "3"])]
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "3"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "3"])]
    s10.transfer(volumesubset, tube_rack3.wells(positionsubset), PCR_plate1.wells(wellsubset), blow_out=True, touch_tip=True, new_tip='always')
if "4" in racklist:
    positionsubset=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "4"])]
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "4"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "4"])]
    s10.transfer(volumesubset, tube_rack4.wells(positionsubset), PCR_plate1.wells(wellsubset), blow_out=True, touch_tip=True, new_tip='always')
