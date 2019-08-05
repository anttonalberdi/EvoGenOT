## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Bead beat samples at maximum speed for 5 minutes (If needed do Proteinase K for digestion of tissue)
# 	2. Spin down samples 10.000 rpm for 1 minute
#	3. Transfer 200µl lysed sample to a deep well plate

### Procedure ###


######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'D-Rex RNA Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of D-Rex RNA protocol for stool samples in SHIELD',
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
elution_plate_RNA = labware.load('biorad-hardshell-96-PCR', '1')
trough = labware.load('trough-12row', '9')
mag_deck = modules.load('magdeck', '7')
RNA_plate = labware.load('1ml_PCR', '7', share=True)
trash_box = labware.load('One-Column-reservoir', '8')

tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
               for slot in ['3','4','5','6']]



#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)

#### REAGENT SETUP

EtOH1 = trough.wells('A5')
EtOH2 = trough.wells('A6')
EtOH3 = trough.wells('A7')
EtOH4 = trough.wells('A8')
DNase = trough.wells('A9')
BufferC_1 = trough.wells('A10')
BufferC_2 = trough.wells('A11')
Elution_buffer = trough.wells('A12')

Liquid_trash = trash_box.wells('A1')
#### Plate SETUP for Purification

RA1 = RNA_plate.wells('A1')
RA2 = RNA_plate.wells('A2')
RA3 = RNA_plate.wells('A3')
RA4 = RNA_plate.wells('A4')
RA5 = RNA_plate.wells('A5')
RA6 = RNA_plate.wells('A6')
RA7 = RNA_plate.wells('A7')
RA8 = RNA_plate.wells('A8')
RA9 = RNA_plate.wells('A9')
RA10 = RNA_plate.wells('A10')
RA11 = RNA_plate.wells('A11')
RA12 = RNA_plate.wells('A12')
#### VOLUME SETUP


Sample_vol = 200
EtOH_vol = 2.0*Sample_vol
Wash_1_vol = 1.0*Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50

BufferC_vol = 0.9*Sample_vol

#### PROTOCOL ####
## Dry beads before DNase treatment
mag_deck.disengage()

sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in RNA_plate.cols()[:col_num]]

## Buffer C rebind
### Transfer buffer C and beads to RA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down  speed 0.5X for bead handling
m300.move_to(BufferC_2.top(-10))
m300.mix(3, BufferC_vol, BufferC_2.top(-8))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(BufferC_vol, BufferC_2.top(-8))
m300.move_to(RA1.bottom())
m300.dispense(BufferC_vol, RA1.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, RA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA1.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()
