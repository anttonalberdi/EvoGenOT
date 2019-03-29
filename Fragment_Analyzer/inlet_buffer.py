metadata = {
    'protocolName': 'Inlet buffer 96-well plate preparation',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/03/19',
    'validation_date': '',
    'description': '',
}

#### CHANGELOG  ####

#2018/03/11, Antton - Blow out added to the transfer to plate

#### LIBRARIES ####

#Opentrons presets
from opentrons import labware, instruments, modules, robot
#Custom presets
import os,sys
sys.path.append("/root")
import custom_labware

#### MODULES ####

#Source tubes (only load if mentioned in the map file)
tube_rack = labware.load('opentrons-tuberack-50ml', 10)
#calibrate 2-3 mm above the tube top

#Plate
buffer_plate1 = labware.load('96-PCR-flat', 7)
buffer_plate2 = labware.load('96-PCR-flat', 8)
buffer_plate3 = labware.load('96-PCR-flat', 9)

#### TIP RACKS ####
tiprack_1000 = labware.load('labsolute-tiprack-1000µl', '11')
#At least 6 tips (A1-F1)

#### PIPETTES ####
s1000 = instruments.P1000_Single(mount='left', tip_racks=[tiprack_1000])

#### LIQUID HANDLING ####

#Plate 1
s1000.transfer(1000, tube_rack.wells('A1'), buffer_plate1.rows('A','B'), blow_out=True)
s1000.transfer(1000, tube_rack.wells('B1'), buffer_plate1.rows('C','D'), blow_out=True)

#Plate 2
s1000.transfer(1000, tube_rack.wells('A2'), buffer_plate1.rows('A','B'), blow_out=True)
s1000.transfer(1000, tube_rack.wells('B2'), buffer_plate1.rows('C','D'), blow_out=True)

#Plate 3
s1000.transfer(1000, tube_rack.wells('A3'), buffer_plate1.rows('A','B'), blow_out=True)
s1000.transfer(1000, tube_rack.wells('B3'), buffer_plate1.rows('C','D'), blow_out=True)
