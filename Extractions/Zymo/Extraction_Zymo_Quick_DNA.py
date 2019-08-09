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

plate_name = '1ml_PCR'
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
trash_box = labware.load('One-Colum-reservoir', '8')
mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('1ml_PCR', '7', share=True)

tipracks_300_1 = labware.load('tiprack-200ul', '1', share=True)
tipracks_300_2 = labware.load('tiprack-200ul', '2', share=True)
tipracks_300_3 = labware.load('tiprack-200ul', '3', share=True)


tipracks_1000 = [labware.load('tiprack-1000ul', slot, share=True)
               for slot in ['6']]

#### PIPETTE SETUP ####

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=300,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_300_1,tipracks_300_2,tipracks_300_3)

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
Elution_vol = 55


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
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer1.top(-16))
m300.mix(3, Binding_buffer_vol, Binding_buffer1.top(-12))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
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

### Transfer Binding buffer and beads to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer1.bottom())
m300.mix(3, Binding_buffer_vol, Binding_buffer1.bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(2))
m300.dispense(Binding_buffer_vol, SA2.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(2))
m300.dispense(Binding_buffer_vol, SA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA2.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer1.bottom(1))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.dispense(Binding_buffer_vol, SA3.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.dispense(Binding_buffer_vol, SA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA3.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer1.bottom(1))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom())
m300.dispense(Binding_buffer_vol, SA4.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom())
m300.dispense(Binding_buffer_vol, SA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA4.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer2.top(-16))
m300.mix(3, Binding_buffer_vol, Binding_buffer2.top(-12))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.top(-12))
m300.dispense(Binding_buffer_vol, SA5.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer2.top(-16))
m300.dispense(Binding_buffer_vol, SA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA5.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer2.bottom())
m300.mix(3, Binding_buffer_vol, Binding_buffer2.bottom(4))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(2))
m300.dispense(Binding_buffer_vol, SA6.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(2))
m300.dispense(Binding_buffer_vol, SA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer2.bottom(4))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.dispense(Binding_buffer_vol, SA7.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.dispense(Binding_buffer_vol, SA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer2.bottom(1))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom())
m300.dispense(Binding_buffer_vol, SA8.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom())
m300.dispense(Binding_buffer_vol, SA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA8.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer3.top(-16))
m300.mix(3, Binding_buffer_vol, Binding_buffer3.top(-12))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer3.top(-12))
m300.dispense(Binding_buffer_vol, SA9.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer3.top(-16))
m300.dispense(Binding_buffer_vol, SA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA9.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer3.bottom())
m300.mix(3, Binding_buffer_vol, Binding_buffer3.bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer3.bottom(2))
m300.dispense(Binding_buffer_vol, SA10.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer3.bottom(2))
m300.dispense(Binding_buffer_vol, SA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA10.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer3.bottom(1))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer3.bottom(1))
m300.dispense(Binding_buffer_vol, SA11.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer3.bottom(1))
m300.dispense(Binding_buffer_vol, SA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA11.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Binding buffer and beads to SA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer3.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer3.bottom())
m300.dispense(Binding_buffer_vol, SA12.top(-4))
m300.aspirate(Binding_buffer_vol, Binding_buffer3.bottom())
m300.dispense(Binding_buffer_vol, SA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA12.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA12.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

robot.pause("Distribution of binding buffer is done. Incubate samples in 20 minutes on rotator to ensure proper binding. Press resume to continue process after incubation")

### Remove supernatant
mag_deck.engage(heigth=34)
m300.delay(minutes=3)

### remove supernatant from SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A1'))
m300.aspirate(Binding_buffer_vol, SA1.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA1.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A2'))
m300.aspirate(Binding_buffer_vol, SA2.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA2.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A3'))
m300.aspirate(Binding_buffer_vol, SA3.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA3.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A4'))
m300.aspirate(Binding_buffer_vol, SA4.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA4.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A5'))
m300.aspirate(Binding_buffer_vol, SA5.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA5.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A6'))
m300.aspirate(Binding_buffer_vol, SA6.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA6.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A7'))
m300.aspirate(Binding_buffer_vol, SA7.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA7.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A8'))
m300.aspirate(Binding_buffer_vol, SA8.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA8.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A9'))
m300.aspirate(Binding_buffer_vol, SA9.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA9.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A10'))
m300.aspirate(Binding_buffer_vol, SA10.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA10.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A11'))
m300.aspirate(Binding_buffer_vol, SA11.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA11.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A12'))
m300.aspirate(Binding_buffer_vol, SA12.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Binding_buffer_vol, SA12.bottom(1))
m300.dispense(Binding_buffer_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### Wash with wash-buffer
### Transfer Wash 1 to SA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Wash_1_1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_1.top(-12))
m300.dispense(Wash_vol, SA1.top(-4))
m300.aspirate(Wash_vol, Wash_1_1.top(-16))
m300.dispense(Wash_vol, SA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA1.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Wash_1_1.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_1.bottom(2))
m300.dispense(Wash_vol, SA2.top(-4))
m300.aspirate(Wash_vol, Wash_1_1.bottom(2))
m300.dispense(Wash_vol, SA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA2.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_1.bottom(1))
m300.dispense(Wash_vol, SA3.top(-4))
m300.aspirate(Wash_vol, Wash_1_1.bottom(1))
m300.dispense(Wash_vol, SA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA3.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_1.bottom())
m300.dispense(Wash_vol, SA4.top(-4))
m300.aspirate(Wash_vol, Wash_1_1.bottom())
m300.dispense(Wash_vol, SA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA4.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
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

### Transfer Wash 1 to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_1.bottom())
m300.dispense(Wash_vol, SA5.top(-4))
m300.aspirate(Wash_vol, Wash_1_1.bottom())
m300.dispense(Wash_vol, SA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA5.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Wash_1_1.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_1.bottom())
m300.dispense(Wash_vol, SA6.top(-4))
m300.aspirate(Wash_vol, Wash_1_1.bottom())
m300.dispense(Wash_vol, SA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Start taking wash buffer from Wash_1_2
### Transfer Wash 1 to SA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Wash_vol, Wash_1_2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_2.top(-12))
m300.dispense(Wash_vol, SA7.top(-4))
m300.aspirate(Wash_vol, Wash_1_2.top(-16))
m300.dispense(Wash_vol, SA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handlingSA9
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_2.bottom())
m300.dispense(Wash_vol, SA8.top(-4))
m300.aspirate(Wash_vol, Wash_1_2.bottom())
m300.dispense(Wash_vol, SA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA8.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_2.bottom())
m300.dispense(Wash_vol, SA9.top(-4))
m300.aspirate(Wash_vol, Wash_1_2.bottom())
m300.dispense(Wash_vol, SA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA9.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_2.top(-12))
m300.dispense(Wash_vol, SA10.top(-4))
m300.aspirate(Wash_vol, Wash_1_2.top(-16))
m300.dispense(Wash_vol, SA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA10.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, Wash_backup.top(-28))
p1000.dispense(800, Wash_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-32))
p1000.dispense(800, Wash_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-36))
p1000.dispense(800, Wash_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-40))
p1000.dispense(800, Wash_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_1_2.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Wash 1 to SA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_2.top(-12))
m300.dispense(Wash_vol, SA11.top(-4))
m300.aspirate(Wash_vol, Wash_1_2.top(-16))
m300.dispense(Wash_vol, SA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA11.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 1 to SA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_1_2.top(-12))
m300.dispense(Wash_vol, SA12.top(-4))
m300.aspirate(Wash_vol, Wash_1_2.top(-16))
m300.dispense(Wash_vol, SA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA12.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA12.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Remove wash supernatant
mag_deck.engage(heigth=34)
m300.delay(minutes=1)
### remove supernatant from SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A1'))
m300.aspirate(Wash_vol, SA1.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA1.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A2'))
m300.aspirate(Wash_vol, SA2.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA2.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A3'))
m300.aspirate(Wash_vol, SA3.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA3.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A4'))
m300.aspirate(Wash_vol, SA4.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA4.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A5'))
m300.aspirate(Wash_vol, SA5.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA5.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A6'))
m300.aspirate(Wash_vol, SA6.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA6.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A7'))
m300.aspirate(Wash_vol, SA7.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA7.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A8'))
m300.aspirate(Wash_vol, SA8.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA8.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A9'))
m300.aspirate(Wash_vol, SA9.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA9.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A10'))
m300.aspirate(Wash_vol, SA10.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA10.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A11'))
m300.aspirate(Wash_vol, SA11.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA11.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A12'))
m300.aspirate(Wash_vol, SA12.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA12.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### Transfer Wash 2 to SA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Wash_2_1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_1.top(-12))
m300.dispense(Wash_vol, SA1.top(-4))
m300.aspirate(Wash_vol, Wash_2_1.top(-16))
m300.dispense(Wash_vol, SA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA1.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Wash_2_1.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_1.bottom(2))
m300.dispense(Wash_vol, SA2.top(-4))
m300.aspirate(Wash_vol, Wash_2_1.bottom(2))
m300.dispense(Wash_vol, SA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA2.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_1.bottom(1))
m300.dispense(Wash_vol, SA3.top(-4))
m300.aspirate(Wash_vol, Wash_2_1.bottom(1))
m300.dispense(Wash_vol, SA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA3.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_1.bottom())
m300.dispense(Wash_vol, SA4.top(-4))
m300.aspirate(Wash_vol, Wash_2_1.bottom())
m300.dispense(Wash_vol, SA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA4.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, Wash_backup.top(-12))
p1000.dispense(800, Wash_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-16))
p1000.dispense(800, Wash_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-20))
p1000.dispense(800, Wash_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-24))
p1000.dispense(800, Wash_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_1.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Wash 2 to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_1.bottom())
m300.dispense(Wash_vol, SA5.top(-4))
m300.aspirate(Wash_vol, Wash_2_1.bottom())
m300.dispense(Wash_vol, SA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA5.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_1.bottom())
m300.dispense(Wash_vol, SA6.top(-4))
m300.aspirate(Wash_vol, Wash_2_1.bottom())
m300.dispense(Wash_vol, SA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Start taking wash buffer from Wash_2_2

### Transfer Wash 2 to SA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Wash_2_2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_2.top(-12))
m300.dispense(Wash_vol, SA7.top(-4))
m300.aspirate(Wash_vol, Wash_2_2.top(-16))
m300.dispense(Wash_vol, SA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handlingSA9
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_2.bottom())
m300.dispense(Wash_vol, SA8.top(-4))
m300.aspirate(Wash_vol, Wash_2_2.bottom())
m300.dispense(Wash_vol, SA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA8.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_2.bottom())
m300.dispense(Wash_vol, SA9.top(-4))
m300.aspirate(Wash_vol, Wash_2_2.bottom())
m300.dispense(Wash_vol, SA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA9.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_2.top(-12))
m300.dispense(Wash_vol, SA10.top(-4))
m300.aspirate(Wash_vol, Wash_2_2.top(-16))
m300.dispense(Wash_vol, SA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA10.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, Wash_backup.top(-28))
p1000.dispense(800, Wash_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-32))
p1000.dispense(800, Wash_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-36))
p1000.dispense(800, Wash_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Wash_backup.top(-40))
p1000.dispense(800, Wash_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Wash_2_2.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Wash 2 to SA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_2.top(-12))
m300.dispense(Wash_vol, SA11.top(-4))
m300.aspirate(Wash_vol, Wash_2_2.top(-16))
m300.dispense(Wash_vol, SA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA11.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Wash 2 to SA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Wash_vol, Wash_2_2.top(-12))
m300.dispense(Wash_vol, SA12.top(-4))
m300.aspirate(Wash_vol, Wash_2_2.top(-16))
m300.dispense(Wash_vol, SA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_vol, SA12.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA12.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Remove wash supernatant
mag_deck.engage(heigth=34)
m300.delay(minutes=1)
m300.set_flow_rate(aspirate=130, dispense=300)
### remove supernatant from SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A1'))
m300.aspirate(Wash_vol, SA1.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA1.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A2'))
m300.aspirate(Wash_vol, SA2.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA2.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A3'))
m300.aspirate(Wash_vol, SA3.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA3.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A4'))
m300.aspirate(Wash_vol, SA4.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA4.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A5'))
m300.aspirate(Wash_vol, SA5.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA5.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A6'))
m300.aspirate(Wash_vol, SA6.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA6.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A7'))
m300.aspirate(Wash_vol, SA7.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA7.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A8'))
m300.aspirate(Wash_vol, SA8.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA8.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A9'))
m300.aspirate(Wash_vol, SA9.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA9.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A10'))
m300.aspirate(Wash_vol, SA10.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA10.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A11'))
m300.aspirate(Wash_vol, SA11.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA11.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_3.wells('A12'))
m300.aspirate(Wash_vol, SA12.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Wash_vol, SA12.bottom(1))
m300.dispense(Wash_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

#_-_-_-_-_-_-_-##Reset tipracks for more tips##_-_-_-_-_-_-_-_-_-#
##Reset tipracks for more tips##
robot.pause("Please fill up tips before continuing process")
m300.reset()
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#


### Transfer Ethanol 1 to SA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Ethanol_1_1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_1.top(-12))
m300.dispense(Ethanol_vol, SA1.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_1.top(-16))
m300.dispense(Ethanol_vol, SA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA1.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Ethanol_1_1.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom(2))
m300.dispense(Ethanol_vol, SA2.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom(2))
m300.dispense(Ethanol_vol, SA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA2.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom(1))
m300.dispense(Ethanol_vol, SA3.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom(1))
m300.dispense(Ethanol_vol, SA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA3.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom())
m300.dispense(Ethanol_vol, SA4.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom())
m300.dispense(Ethanol_vol, SA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA4.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, Ethanol_backup.top(-12))
p1000.dispense(800, Ethanol_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-16))
p1000.dispense(800, Ethanol_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-20))
p1000.dispense(800, Ethanol_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-24))
p1000.dispense(800, Ethanol_1_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_1.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Ethanol 1 to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom())
m300.dispense(Ethanol_vol, SA5.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom())
m300.dispense(Ethanol_vol, SA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA5.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom())
m300.dispense(Ethanol_vol, SA6.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_1.bottom())
m300.dispense(Ethanol_vol, SA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Start taking Ethanol buffer from Ethanol_1_2

### Transfer Ethanol 1 to SA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Ethanol_1_2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-12))
m300.dispense(Ethanol_vol, SA7.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-16))
m300.dispense(Ethanol_vol, SA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handlingSA9
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_2.bottom())
m300.dispense(Ethanol_vol, SA8.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_2.bottom())
m300.dispense(Ethanol_vol, SA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA8.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_2.bottom())
m300.dispense(Ethanol_vol, SA9.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_2.bottom())
m300.dispense(Ethanol_vol, SA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA9.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-12))
m300.dispense(Ethanol_vol, SA10.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-16))
m300.dispense(Ethanol_vol, SA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA10.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, Ethanol_backup.top(-28))
p1000.dispense(800, Ethanol_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-32))
p1000.dispense(800, Ethanol_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-36))
p1000.dispense(800, Ethanol_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-40))
p1000.dispense(800, Ethanol_1_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_1_2.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Ethanol 1 to SA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-12))
m300.dispense(Ethanol_vol, SA11.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-16))
m300.dispense(Ethanol_vol, SA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA11.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 1 to SA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-12))
m300.dispense(Ethanol_vol, SA12.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_1_2.top(-16))
m300.dispense(Ethanol_vol, SA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA12.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA12.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Remove ethanol supernatant
mag_deck.engage(heigth=34)
m300.delay(minutes=1)
### remove supernatant from SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A1'))
m300.aspirate(Ethanol_vol, SA1.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA1.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A2'))
m300.aspirate(Ethanol_vol, SA2.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA2.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A3'))
m300.aspirate(Ethanol_vol, SA3.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA3.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A4'))
m300.aspirate(Ethanol_vol, SA4.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA4.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A5'))
m300.aspirate(Ethanol_vol, SA5.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA5.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A6'))
m300.aspirate(Ethanol_vol, SA6.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA6.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A7'))
m300.aspirate(Ethanol_vol, SA7.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA7.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A8'))
m300.aspirate(Ethanol_vol, SA8.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA8.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A9'))
m300.aspirate(Ethanol_vol, SA9.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA9.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A10'))
m300.aspirate(Ethanol_vol, SA10.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA10.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A11'))
m300.aspirate(Ethanol_vol, SA11.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA11.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_1.wells('A12'))
m300.aspirate(Ethanol_vol, SA12.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA12.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### Transfer Ethanol 2 to SA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Ethanol_2_1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_1.top(-12))
m300.dispense(Ethanol_vol, SA1.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_1.top(-16))
m300.dispense(Ethanol_vol, SA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA1.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Ethanol_2_1.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom(2))
m300.dispense(Ethanol_vol, SA2.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom(2))
m300.dispense(Ethanol_vol, SA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA2.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom(1))
m300.dispense(Ethanol_vol, SA3.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom(1))
m300.dispense(Ethanol_vol, SA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA3.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom())
m300.dispense(Ethanol_vol, SA4.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom())
m300.dispense(Ethanol_vol, SA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA4.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, Ethanol_backup.top(-12))
p1000.dispense(800, Ethanol_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-16))
p1000.dispense(800, Ethanol_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-20))
p1000.dispense(800, Ethanol_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_1.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-24))
p1000.dispense(800, Ethanol_2_1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_1.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Ethanol 2 to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom())
m300.dispense(Ethanol_vol, SA5.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom())
m300.dispense(Ethanol_vol, SA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA5.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom())
m300.dispense(Ethanol_vol, SA6.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_1.bottom())
m300.dispense(Ethanol_vol, SA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Start taking Ethanol buffer from Ethanol_2_2

### Transfer Ethanol 2 to SA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Ethanol_2_2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-12))
m300.dispense(Ethanol_vol, SA7.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-16))
m300.dispense(Ethanol_vol, SA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handlingSA9
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_2.bottom())
m300.dispense(Ethanol_vol, SA8.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_2.bottom())
m300.dispense(Ethanol_vol, SA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA8.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_2.bottom())
m300.dispense(Ethanol_vol, SA9.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_2.bottom())
m300.dispense(Ethanol_vol, SA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA9.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-12))
m300.dispense(Ethanol_vol, SA10.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-16))
m300.dispense(Ethanol_vol, SA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA10.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, Ethanol_backup.top(-28))
p1000.dispense(800, Ethanol_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-32))
p1000.dispense(800, Ethanol_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-36))
p1000.dispense(800, Ethanol_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_2.top(-4))
p1000.blow_out()
p1000.aspirate(800, Ethanol_backup.top(-40))
p1000.dispense(800, Ethanol_2_2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(Ethanol_2_2.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Ethanol 2 to SA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-12))
m300.dispense(Ethanol_vol, SA11.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-16))
m300.dispense(Ethanol_vol, SA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA11.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Ethanol 2 to SA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-12))
m300.dispense(Ethanol_vol, SA12.top(-4))
m300.aspirate(Ethanol_vol, Ethanol_2_2.top(-16))
m300.dispense(Ethanol_vol, SA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Ethanol_vol, SA12.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA12.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Remove ethanol supernatant
mag_deck.engage(heigth=34)
m300.delay(minutes=1)
m300.set_flow_rate(aspirate=130, dispense=300)
### remove supernatant from SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A1'))
m300.aspirate(Ethanol_vol, SA1.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA1.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A2'))
m300.aspirate(Ethanol_vol, SA2.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA2.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A3'))
m300.aspirate(Ethanol_vol, SA3.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA3.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A4'))
m300.aspirate(Ethanol_vol, SA4.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA4.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A5'))
m300.aspirate(Ethanol_vol, SA5.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA5.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A6'))
m300.aspirate(Ethanol_vol, SA6.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA6.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A7'))
m300.aspirate(Ethanol_vol, SA7.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA7.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A8'))
m300.aspirate(Ethanol_vol, SA8.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA8.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A9'))
m300.aspirate(Ethanol_vol, SA9.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA9.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A10'))
m300.aspirate(Ethanol_vol, SA10.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA10.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A11'))
m300.aspirate(Ethanol_vol, SA11.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA11.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from SA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_300_2.wells('A12'))
m300.aspirate(Ethanol_vol, SA12.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(Ethanol_vol, SA12.bottom(1))
m300.dispense(Ethanol_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

## Drying beads
m300.delay(minutes=5)

### Transfer Elution buffer and beads to SA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Elution_buffer.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.top(-12))
m300.dispense(Elution_buffer_vol, SA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA1.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Elution_buffer.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.top(-16))
m300.dispense(Elution_buffer_vol, SA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA2.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom(1))
m300.dispense(Elution_buffer_vol, SA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA3.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA4.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA4.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA5.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA5.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA6.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA7.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA7.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA8.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA8.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA9.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA9.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Elution_buffer.bottom())
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA10.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA10.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA11.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA11.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer Elution buffer and beads to SA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, Elution_buffer.bottom())
m300.dispense(Elution_buffer_vol, SA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Elution_buffer_vol, SA12.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA12.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()


### Incubating beads with elution buffer
m300.delay(minutes=10)

mag_deck.engage(heigth=34)
m300.delay(minutes=2)

### Transfer Elution buffer to EA1
m300.pick_up_tip(tipracks_300_2.wells('A1'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA1.bottom())
m300.dispense(Elution_buffer_vol, EA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA2
m300.pick_up_tip(tipracks_300_2.wells('A2'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA2.bottom())
m300.dispense(Elution_buffer_vol, EA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA3
m300.pick_up_tip(tipracks_300_2.wells('A3'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA3.bottom())
m300.dispense(Elution_buffer_vol, EA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA3.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA4
m300.pick_up_tip(tipracks_300_2.wells('A4'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA4.bottom())
m300.dispense(Elution_buffer_vol, EA4.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA4.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA5
m300.pick_up_tip(tipracks_300_2.wells('A5'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA5.bottom())
m300.dispense(Elution_buffer_vol, EA5.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA5.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA6
m300.pick_up_tip(tipracks_300_2.wells('A6'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA6.bottom())
m300.dispense(Elution_buffer_vol, EA6.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA6.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA7
m300.pick_up_tip(tipracks_300_2.wells('A7'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA7.bottom())
m300.dispense(Elution_buffer_vol, EA7.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA7.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA8
m300.pick_up_tip(tipracks_300_2.wells('A8'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA8.bottom())
m300.dispense(Elution_buffer_vol, EA8.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA8.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA9
m300.pick_up_tip(tipracks_300_2.wells('A9'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA9.bottom())
m300.dispense(Elution_buffer_vol, EA9.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA9.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA10
m300.pick_up_tip(tipracks_300_2.wells('A10'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA10.bottom())
m300.dispense(Elution_buffer_vol, EA10.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA10.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA11
m300.pick_up_tip(tipracks_300_2.wells('A11'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA11.bottom())
m300.dispense(Elution_buffer_vol, EA11.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA11.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA12
m300.pick_up_tip(tipracks_300_2.wells('A12'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, SA12.bottom())
m300.dispense(Elution_buffer_vol, EA12.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(EA12.top(-10))
m300.blow_out()
m300.return_tip()

mag_deck.disengage()
