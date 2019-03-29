4metadata = {
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
tube_rack = labware.load('tube-rack-15_50ml', 7)

#Plate
buffer_plate = labware.load('96-deep-well', 8)

#### TIP RACKS ####
tiprack_1000 = labware.load('labsolute-tiprack-1000µl', '11')

#### PIPETTES ####
s1000 = instruments.P1000_Single(mount='left', tip_racks=[tiprack_1000])

#### LIQUID HANDLING ####
s1000.transfer(1000, tube_rack.wells('A3'), buffer_plate.rows('1'), blow_out=True, touch_tip=True)
s1000.transfer(1000, tube_rack.wells('A4'), buffer_plate.rows('2'), blow_out=True, touch_tip=True)
s1000.transfer(1000, tube_rack.wells('B3'), buffer_plate.rows('3'), blow_out=True, touch_tip=True)
s1000.transfer(1000, tube_rack.wells('B4'), buffer_plate.rows('4'), blow_out=True, touch_tip=True)
