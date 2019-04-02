metadata = {
    'protocolName': '96-well plate to 1.5/2 ml epp transfer',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/04/02',
    'validation_date': '2019/XX/XX',
    'description': 'Protocol for transferring liquids from a 96-well plate to 1.5/2ml Eppendorf tubes',
}

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
with open("/root/csv/amplicon_pooling_v1_map.csv", "r") as csvfile:
    transfermap = csv.reader(csvfile, delimiter=',')
    for i in transfermap:
        welllist.append(i[0])
        tubelist.append(i[1])
        volumelist.append(i[2])

#Remove headers
welllist.pop(0)
tubelist.pop(0)
volumelist.pop(0)

#### MODULES ####

#Pooling tubes
tube_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '2', share=True)
#Pools 1-6 in A1-A6
#Pools 7-12 in B1-B6
#Pooling tubes should ideally contain 10-20ul of water

#Plate
PCR_plate = labware.load('96-PCR-flat', '9', share=True)

#### TIP RACKS ####
tiprack_10 = labware.load('labsolute-tiprack-10µl', '6')

#### PIPETTES ####
s10 = instruments.P10_Single(mount='left', tip_racks=[tiprack_10])

#### LIQUID HANDLING ####
if "1" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "1"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "1"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('A1'), blow_out=True, touch_tip=True, new_tip='always')
if "2" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "2"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "2"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('A2'), blow_out=True, touch_tip=True, new_tip='always')
if "3" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "3"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "3"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('A3'), blow_out=True, touch_tip=True, new_tip='always')
if "4" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "4"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "4"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('A4'), blow_out=True, touch_tip=True, new_tip='always')
if "5" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "5"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "5"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('A5'), blow_out=True, touch_tip=True, new_tip='always')
if "6" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == '6'])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "6"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('A6'), blow_out=True, touch_tip=True, new_tip='always')
if "7" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "7"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "7"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('B1'), blow_out=True, touch_tip=True, new_tip='always')
if "8" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "8"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "8"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('B2'), blow_out=True, touch_tip=True, new_tip='always')
if "9" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "9"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "9"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('B3'), blow_out=True, touch_tip=True, new_tip='always')
if "10" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "10"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "10"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('B4'), blow_out=True, touch_tip=True, new_tip='always')
if "11" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == "11"])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "11"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('B5'), blow_out=True, touch_tip=True, new_tip='always')
if "12" in tubelist:
    wellsubset=[welllist[i] for i in ([i for i,x in enumerate(tubelist) if x == '12'])]
    volumesubset=[volumelist[i] for i in ([i for i,x in enumerate(tubelist) if x == "12"])]
    s10.transfer(volumesubset, PCR_plate.wells(wellsubset), tube_rack.wells('B6'), blow_out=True, touch_tip=True, new_tip='always')
