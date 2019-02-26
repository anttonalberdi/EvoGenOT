metadata = {
    'protocolName': '1.5/2ml to 96-well plate transfer',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/02/26',
    'validation_date': 'XXXXX',
    'description': 'Protocol for transferring liquids from 1.5/2ml to 96-well plate transfer',
}

#### LIBRARIES ####
#Pandas for handling csv files
import pandas as pd
#Opentrons presets
from opentrons import labware, instruments, modules, robot
#Custom presets
import os
os.system("python custom_labware.py")

#### INPUT FILES ####

#Load data files
transfermap = pd.read_csv("/Users/jpl786/github/EvoGenOT/Transfers_aliquots/2ml_to_96plate_map.csv")


#### MODULES ####

#Source tubes (only load if mentioned in the map file)
if 1 in transfermap.Rack.tolist():
    tube_rack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '2', share=True)
if 2 in transfermap.Rack.tolist():
    tube_rack2 = labware.load('opentrons-tuberack-2ml-eppendorf', '5', share=True)
if 3 in transfermap.Rack.tolist():
    tube_rack3 = labware.load('opentrons-tuberack-2ml-eppendorf', '8', share=True)
if 4 in transfermap.Rack.tolist():
    tube_rack4 = labware.load('opentrons-tuberack-2ml-eppendorf', '11', share=True)

#Plate
ice_rack1 = labware.load('PCR-strip-tall', '9', share=True)

#### TIP RACKS ####
tiprack_10 = labware.load('labsolute-tiprack-10µl', '6')

#### PIPETTES ####
s10 = instruments.P10_Single(mount='left', tip_racks=[tiprack_10])

#### LIQUID HANDLING ####
if 1 in transfermap.Rack.tolist():
    transfermap_rack1 = transfermap[transfermap['Rack'] == 1]
    s10.transfer(transfermap_rack1.Volume.tolist(), tube_rack1.wells(transfermap_rack1.Position.tolist()), ice_rack1.wells(transfermap_rack1.Well.tolist()), new_tip='always')
if 2 in transfermap.Rack.tolist():
    transfermap_rack2 = transfermap[transfermap['Rack'] == 2]
    s10.transfer(transfermap_rack2.Volume.tolist(), tube_rack2.wells(transfermap_rack2.Position.tolist()), ice_rack1.wells(transfermap_rack2.Well.tolist()), new_tip='always')
if 3 in transfermap.Rack.tolist():
    transfermap_rack3 = transfermap[transfermap['Rack'] == 3]
    s10.transfer(transfermap_rack3.Volume.tolist(), tube_rack3.wells(transfermap_rack3.Position.tolist()), ice_rack1.wells(transfermap_rack3.Well.tolist()), new_tip='always')
if 4 in transfermap.Rack.tolist():
    transfermap_rack3 = transfermap[transfermap['Rack'] == 3]
    s10.transfer(transfermap_rack3.Volume.tolist(), tube_rack4.wells(transfermap_rack4.Position.tolist()), ice_rack1.wells(transfermap_rack4.Well.tolist()), new_tip='always')
