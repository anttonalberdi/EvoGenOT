metadata = {
    'protocolName': 'Foil puncturing test',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/05/07',
    'validation_date': 'XXX',
    'description': 'Foil puncturing test',
}

#### LIBRARIES ####

import csv
#Opentrons presets
from opentrons import labware, instruments, modules, robot
#Custom presets
import os,sys
sys.path.append("/root")
import custom_labware

#### MODULES ####

#PCR plate
pcr_plate = labware.load('96-PCR-tall', '2', share=True)

#### TIP RACKS ####
tiprack_10 = labware.load('labsolute-tiprack-10µl', '3')

#### PIPETTES ####
s10 = instruments.P10_Single(mount='left', tip_racks=[tiprack_10])
m10 = instruments.P10_Multi(mount='right', tip_racks=[tiprack_10])

m10.transfer(2, pcr_plate.wells('A1'), pcr_plate.wells('A4'), new_tip='always')
m10.transfer(2, pcr_plate.wells('A2'), pcr_plate.wells('A12'), new_tip='always')
s10.transfer(2, pcr_plate.wells('A6'), pcr_plate.wells('H6'), new_tip='always')
