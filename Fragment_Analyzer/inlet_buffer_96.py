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
