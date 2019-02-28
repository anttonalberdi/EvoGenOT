metadata = {
    'protocolName': '1.5/2ml to 96-well plate transfer',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/02/26',
    'validation_date': 'XXXXX',
    'description': 'Protocol for transferring liquids from 1.5/2ml to 96-well plate transfer',
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
with open("/root/csv/2ml_to_96plate_map.csv", "r") as csvfile:
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
ice_rack1 = labware.load('PCR-strip-tall', '9', share=True)

#### TIP RACKS ####
tiprack_200 = labware.load('labsolute-tiprack-200µl', '6')

#### PIPETTES ####
s50 = instruments.P50_Single(mount='left', tip_racks=[tiprack_200],  min_volume=3)

#### LIQUID HANDLING ####
if "1" in racklist:
    positions=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "1"])]
    wells=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "1"])]
    volumes=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "1"])]
    s50.transfer(volumes, tube_rack1.wells(positions), ice_rack1.wells(wells), new_tip='always')
if "2" in racklist:
    positions=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "2"])]
    wells=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "2"])]
    volumes=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "2"])]
    s50.transfer(volumes, tube_rack2.wells(positions), ice_rack1.wells(wells), new_tip='always')
if "3" in racklist:
    positions=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "3"])]
    wells=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "3"])]
    volumes=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "3"])]
    s50.transfer(volumes, tube_rack3.wells(positions), ice_rack1.wells(wells), new_tip='always')
if "4" in racklist:
    positions=[positionlist[i] for i in ([i for i,x in enumerate(racklist) if x == "4"])]
    wells=[welllist[i] for i in ([i for i,x in enumerate(racklist) if x == "4"])]
    volumes=[volumelist[i] for i in ([i for i,x in enumerate(racklist) if x == "4"])]
    s50.transfer(volumes, tube_rack4.wells(positions), ice_rack1.wells(wells), new_tip='always')
