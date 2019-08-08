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
plate_name = '1ml_magPCR'
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
RNA_plate = labware.load('1ml_magPCR', '7', share=True)
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

## Remove supernatant
mag_deck.engage(height=34)
m300.delay(minutes=3)
m300.transfer(700, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

## Ethanol Wash 1
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH1, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=34)
m300.delay(minutes=2)

m300.transfer(Wash_1_vol, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)


## Ethanol Wash 2
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH2, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=34)
m300.delay(minutes=2)
m300.transfer(250, RA1.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA2.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA3.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA4.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA5.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA6.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA7.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA8.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA9.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA10.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA11.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA12.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

## Dry beads before DNase treatment
mag_deck.disengage()
m300.delay(minutes=1)

sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in RNA_plate.cols()[:col_num]]

m300.pick_up_tip()
for target in samples: # Slow down head speed 0.5X for bead handling
    m300.mix(2, 30, DNase)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(30, DNase.bottom(1))
    m300.dispense(30, target.top(-10))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(target.top(-8))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

#incubating samples with DNase
m300.delay(minutes=10)
##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process")
m300.reset()

## Buffer C rebind
### Transfer buffer C and beads to RA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down  speed 0.5X for bead handling
m300.move_to(BufferC_1.top(-16))
m300.mix(3, BufferC_vol, BufferC_1.top(-12))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.top(-8)
m300.aspirate(BufferC_vol, BufferC_1.top(-12))
m300.move_to(RA1.bottom(2))
m300.dispense(BufferC_vol, RA1.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA1.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(BufferC_1.top(-20))
m300.mix(3, BufferC_vol, BufferC_1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(BufferC_vol, BufferC_1.top(-16))
m300.move_to(RA2.bottom(2))
m300.dispense(BufferC_vol, RA2.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA2.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.bottom())
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(RA3.bottom(2))
m300.dispense(BufferC_vol, RA3.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA3.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.bottom())
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(RA4.bottom(2))
m300.dispense(BufferC_vol, RA4.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA4.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA4.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.bottom())
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(RA5.bottom(2))
m300.dispense(BufferC_vol, RA5.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA5.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA5.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.bottom())
m300.aspirate(BufferC_vol, BufferC_1.bottom(1))
m300.move_to(RA6.bottom(2))
m300.dispense(BufferC_vol, RA6.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA6.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA6.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(BufferC_2.top(-16))
m300.mix(3, BufferC_vol, BufferC_2.top(-12))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(BufferC_vol, BufferC_2.top(-12))
m300.move_to(RA7.bottom(2))
m300.dispense(BufferC_vol, RA7.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA7.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA7.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(BufferC_2.top(-20))
m300.mix(3, BufferC_vol, BufferC_2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(BufferC_vol, BufferC_2.top(-16))
m300.move_to(RA8.bottom(2))
m300.dispense(BufferC_vol, RA8.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA8.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA8.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(RA9.bottom(2))
m300.dispense(BufferC_vol, RA9.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA9.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA9.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(RA10.bottom(2))
m300.dispense(BufferC_vol, RA10.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA10.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA10.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(RA11.bottom(2))
m300.dispense(BufferC_vol, RA11.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA11.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA11.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to RA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(RA12.bottom(2))
m300.dispense(BufferC_vol, RA12.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, BufferC_vol, RA12.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA12.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

m300.delay(minutes=5)
mag_deck.engage(height=34)
m300.delay(minutes=1)

m300.transfer(250, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)

## Ethanol Wash 3
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH3, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=34)
m300.delay(minutes=2)

m300.transfer(200, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

## Ethanol Wash 4
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH4, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=34)

##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process")
m300.reset()

## Ethanol Wash 4 - continued
m300.delay(minutes=2)
m300.transfer(250, RA1.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA3.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA2.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA4.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA5.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA6.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA7.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA8.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA9.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA10.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA11.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, RA12.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)



## Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)

## Elution
mag_deck.disengage()
for target in samples: # Slow down head speed 0.5X for bead handling
    m300.pick_up_tip()
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
    m300.dispense(Elution_vol, target.bottom(1))
    m300.mix(5, 30, target.bottom(3))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(target.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

m300.delay(minutes=10)
mag_deck.engage(height=34)
m300.delay(minutes=2)

m300.transfer(Elution_vol, RA1.bottom(), elution_plate_RNA.wells('A1'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA2.bottom(), elution_plate_RNA.wells('A2'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA3.bottom(), elution_plate_RNA.wells('A3'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA4.bottom(), elution_plate_RNA.wells('A4'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA5.bottom(), elution_plate_RNA.wells('A5'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA6.bottom(), elution_plate_RNA.wells('A6'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA7.bottom(), elution_plate_RNA.wells('A7'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA8.bottom(), elution_plate_RNA.wells('A8'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA9.bottom(), elution_plate_RNA.wells('A9'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA10.bottom(), elution_plate_RNA.wells('A10'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA11.bottom(), elution_plate_RNA.wells('A11'), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, RA12.bottom(), elution_plate_RNA.wells('A12'), new_tip='once',  blow_out =True, air_gap=30)
mag_deck.disengage()
