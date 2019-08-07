## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Bead beat samples at maximum speed for 5 minutes
# 	2. Spin down samples 10.000 rpm for 1 minute
#	3. Transfer 200µl lysed sample to a deep well plate

### Procedure ###


######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'Extraction_DNA_RNA',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of D-Rex DNA protocol for stool samples in SHIELD',
}

### Custom LABWARE load
plate_name = '1ml_PCR'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

plate_name = 'One-Column-reservoir'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(1, 1),                    # specify amount of (columns, rows)
        spacing=(0, 0),               # distances (mm) between each (column, row)
        diameter=81,                     # diameter (mm) of each well on the plate
        depth=35,                       # depth (mm) of each well on the plate
        volume=350000)

#### LABWARE SETUP ####
elution_plate_DNA = labware.load('biorad-hardshell-96-PCR', '1')
trough = labware.load('trough-12row', '9')
trash_box = labware.load('One-Column-reservoir', '8')
mag_deck = modules.load('magdeck', '7')
DNA_plate = labware.load('1ml_PCR', '7', share=True)
tipracks_200 = [labware.load('tiprack-200ul', slot)
               for slot in ['2','3','4','5','6']]



#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)

#### REAGENT SETUP

Liquid_trash = trash_box.wells('A1')


BufferC_1 = trough.wells('A10')
BufferC_2 = trough.wells('A11')
EtOH1 = trough.wells('A5')
EtOH2 = trough.wells('A6')
Elution_buffer = trough.wells('A12')


#### VOLUME SETUP


Sample_vol = 200
Sample_buffer_vol = 2.5*Sample_vol
BufferC_vol = 0.9*Sample_vol
Wash_1_vol = Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50

#### Plate SETUP
DA1 = DNA_plate.wells('A1')
DA2 = DNA_plate.wells('A2')
DA3 = DNA_plate.wells('A3')
DA4 = DNA_plate.wells('A4')
DA5 = DNA_plate.wells('A5')
DA6 = DNA_plate.wells('A6')
DA7 = DNA_plate.wells('A7')
DA8 = DNA_plate.wells('A8')
DA9 = DNA_plate.wells('A9')
DA10 = DNA_plate.wells('A10')
DA11 = DNA_plate.wells('A11')
DA12 = DNA_plate.wells('A12')

sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in DNA_plate.cols()[:col_num]]


#### PROTOCOL ####
mag_deck.disengage()
mag_deck.engage(height=25)
m300.delay(seconds=30)
mag_deck.engage(height=35)
m300.delay(seconds=30)
mag_deck.engage(height=45)
m300.delay(seconds=30)
