## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Bead beat samples at maximum speed for 5 minutes
# 	2. Spin down samples 10.000 rpm for 1 minute
#	3. Transfer 200µl lysed sample to a deep well plate

### Procedure ###
#
#	https://files.zymoresearch.com/protocols/_r2130_r2131_quick-dna_rna_magbead.pdf
#	Purification of DNA (p. 6)
#

######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'Extraction_Quick_DNA',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of Zymo Quick DNA protocol for stool samples in SHIELD',
}
#Custom LABWARE load
plate_name = 'One-Column-reservoir'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(1, 1),                    # specify amount of (columns, rows)
        spacing=(0, 0),               # distances (mm) between each (column, row)
        diameter=81,                     # diameter (mm) of each well on the plate
        depth=35,                       # depth (mm) of each well on the plate
        volume=350000)

plate_name = '1ml_magPCR'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

#### LABWARE SETUP ####
elution_plate = labware.load('96-flat', '4')
trough = labware.load('trough-12row', '9')
backup = labware.load('opentrons-tuberack-50ml', '5')
trash_box = labware.load('One-Column-reservoir', '8')
mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('1ml_magPCR', '7', share=True)

tipracks_300_1 = labware.load('tiprack-200ul', '2', share=True)
tipracks_300_2 = labware.load('tiprack-200ul', '3', share=True)
tipracks_300_3 = labware.load('tiprack-200ul', '4', share=True)


tipracks_1000 = labware.load('tiprack-1000ul', '1', share=True)

#### PIPETTE SETUP ####

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=300,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=[tipracks_300_1, tipracks_300_2, tipracks_300_3])

p1000 = instruments.P1000_Single(
    mount='left',
    aspirate_flow_rate=500,
    dispense_flow_rate=500,
    tip_racks=tipracks_1000)

#### REAGENT SETUP
Binding_buffer1 = trough.wells('A1')
Binding_buffer2 = trough.wells('A2')
Binding_buffer3 = trough.wells('A3')

Wash_1_1 = trough.wells('A4')
Wash_1_2 = trough.wells('A5')
Wash_2_1 = trough.wells('A6')
Wash_2_2 = trough.wells('A7')

Ethanol_1_1 = trough.wells('A8')
Ethanol_1_2 = trough.wells('A9')
Ethanol_2_1 = trough.wells('A10')
Ethanol_2_2 = trough.wells('A11')

Elution_buffer = trough.wells('A12')

#### Backup liquids
Wash_backup = backup.wells('A1')
Ethanol_backup = backup.wells('A2')

## Liquid trash
Liquid_trash = trash_box.wells('A1')

#### VOLUME SETUP
Sample_vol = 200
Binding_buffer_vol = 250 # add binding_buffer and beads together 470µl buffer to 30µl beads per sample = total of 500 per sample
EtOH_vol = 1.25*Sample_vol
Wash_vol = 1.25*Sample_vol
Elution_buffer_vol = 55


#### Sample SETUP
SA1 = sample_plate.wells('A1')
SA2 = sample_plate.wells('A2')
SA3 = sample_plate.wells('A3')
SA4 = sample_plate.wells('A4')
SA5 = sample_plate.wells('A5')
SA6 = sample_plate.wells('A6')
SA7 = sample_plate.wells('A7')
SA8 = sample_plate.wells('A8')
SA9 = sample_plate.wells('A9')
SA10 = sample_plate.wells('A10')
SA11 = sample_plate.wells('A11')
SA12 = sample_plate.wells('A12')

EA1 = elution_plate.wells('A1')
EA2 = elution_plate.wells('A2')
EA3 = elution_plate.wells('A3')
EA4 = elution_plate.wells('A4')
EA5 = elution_plate.wells('A5')
EA6 = elution_plate.wells('A6')
EA7 = elution_plate.wells('A7')
EA8 = elution_plate.wells('A8')
EA9 = elution_plate.wells('A9')
EA10 = elution_plate.wells('A10')
EA11 = elution_plate.wells('A11')
EA12 = elution_plate.wells('A12')

#### PROTOCOL ####
## add beads and sample buffer
mag_deck.disengage()

### Transfer Binding buffer and beads to SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer1.top(-16))
m300.mix(3, Binding_buffer_vol, Binding_buffer1.top(-12))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.top(-12))
m300.dispense(Binding_buffer_vol, SA1.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer1.top(-16))
m300.dispense(Binding_buffer_vol, SA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA1.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip(tipracks_1000.wells('A1'))
p1000.aspirate(800, Wash_backup.top(-12))
p1000.dispense(800, Wash_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-16))
p1000.dispense(800, Wash_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-20))
p1000.dispense(800, Wash_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-24))
p1000.dispense(800, Wash_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_1.top(-4))
p1000.blow_out()
p1000.drop_tip()
