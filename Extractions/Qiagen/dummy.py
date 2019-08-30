

####### IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####


metadata = {
    'protocolName': 'Dummy protocol',
    'author': 'Lasse Nyholm Jessen <lassenyholm@gmail.com>',
    'version': '1.0-optimized',
    'SAte': '2019/08/30',
    'description': 'Dummy protocol',
}

#### LABWARE SETUP ####
reagent_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '9')
reagent_rack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '3')





tiprack_10 = labware.load('tiprack-10µl', '2')

m10 = instruments.P10_Multi(mount='right', tip_racks=[tiprack_10])


m10.transfer(10, reagent_rack(A1), reagent_rack1(A1))
