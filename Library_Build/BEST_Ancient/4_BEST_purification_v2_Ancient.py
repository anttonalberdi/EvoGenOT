#######################################
### BEST Library build Purification ###
#######################################

## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Ensure samples are room temperature and place libraries in magnetic module
# 	2. Ensure SPRI beads are room temperature
#   3. Make freshly made 80% Ethanol for purification
#   4. Distribute:
#                   SPRI beads to Column 1,
#                   Ethanol to Column 2 and 3
#                   Elution Buffer to Column 12
#
# Procedure
#
#		Purification
# 	1.	Distribute 1.5x beads to library and mixes
#	2.	Removes supernatant and adds ethanol for washing, washing will be processed twice
#   3.  Beads will air dry for 4 minutes and 35µl elution buffer will be added
#	4.	Elutes will incubate for 15 minutes at room temperature and be eluted to a new plate in slot 1
#
#	Good Luck!
#
######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'BEST_Purification',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/07/04',
    'description': 'Purification procedure of Automated single tube library preperation after Carøe et al. 2017',
}
#### LOADING CUSTOM LABWARE ####

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
trough = labware.load('trough-12row', '10')
Trash = labware.load('One-Column-reservoir','8')
mag_deck = modules.load('magdeck', '7')
mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)
elution_plate = labware.load('biorad-hardshell-96-PCR','1')


tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
                for slot in ['3','4','5','6']]


#### PIPETTE SETUP ####

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)


## Purification reagents SETUP
SPRI_beads = trough.wells('A1')
EtOH1 = trough.wells('A2')
EtOH2 = trough.wells('A3')
Elution_buffer = trough.wells('A12')

Liquid_trash = Trash.wells('A1')

## Sample Setup
sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in mag_plate.cols()[:col_num]]
samples_top = [well.top() for well in mag_plate.rows(0)[:col_num]]

SA1 = mag_plate.wells('A1')
SA2 = mag_plate.wells('A2')
SA3 = mag_plate.wells('A3')
SA4 = mag_plate.wells('A4')
SA5 = mag_plate.wells('A5')
SA6 = mag_plate.wells('A6')
SA7 = mag_plate.wells('A7')
SA8 = mag_plate.wells('A8')
SA9 = mag_plate.wells('A9')
SA10 = mag_plate.wells('A10')
SA11 = mag_plate.wells('A11')
SA12 = mag_plate.wells('A12')

sample_vol = 50
bead_vol = 1.5*sample_vol
EtOH_vol = 160
EtOH_vol2 = 150
elution_vol = 35

robot.comment("Yay! \ Purification begins!")

### Beads addition
mag_deck.disengage()

for target in samples:
    m300.set_flow_rate(aspirate=180, dispense=180)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, 200, SPRI_beads)
    max_speed_per_axis = {'x': (100), 'y': (100), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=25, dispense=25)
    m300.aspirate(bead_vol, SPRI_beads)
    m300.move_to(target.bottom())
    m300.dispense(bead_vol,target.bottom(4))
    m300.set_flow_rate(aspirate=30, dispense=30)
    m300.mix(5, 100, target.bottom(4))
    m300.delay(seconds=5)
    m300.move_to(target.top(-4))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

robot.comment("Incubating the beads and PCR products at room temperature \
for 5 minutes. Protocol will resume automatically.")
m300.delay(minutes=5)
mag_deck.engage(height=16)
m300.delay(minutes=2)

### Resets head speed for futher processing
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)

### Remove supernatant
m300.transfer(180, SA1.bottom(), Liquid_trash.top(-5), blow_out=True,new_tip='always')
m300.transfer(180, SA2.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA3.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA4.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA5.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA6.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA7.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA8.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA9.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA10.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA11.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA12.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')

### Wash with EtOH1
mag_deck.disengage()
for target in samples:
    m300.set_flow_rate(aspirate=180, dispense=180)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (75), 'a': (75), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=40, dispense=40)
    m300.transfer(EtOH_vol, EtOH1, target.bottom(6), air_gap=0, new_tip='never')
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.mix(3, 100, target.bottom(6))
    m300.delay(seconds=5)
    m300.move_to(target.top(-3))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

### Resets head speed for futher processing
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)

mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(200, SA1.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA2.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA3.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA4.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA5.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA6.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA7.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA8.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA9.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA10.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA11.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA12.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)

##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process and empty trash box")
m300.reset()

### Wash with EtOH2
mag_deck.disengage()

for target in samples:
    m300.set_flow_rate(aspirate=180, dispense=180)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (75), 'a': (75), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=40, dispense=40)
    m300.transfer(EtOH_vol2, EtOH2, target.bottom(6), air_gap=0, new_tip='never')
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.mix(3, 100, target.bottom(6))
    m300.delay(seconds=5)
    m300.move_to(target.top(-3))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

### Resets head speed for futher processing
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)

mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(200, SA1.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA2.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA3.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA4.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA5.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA6.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA7.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA8.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA9.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA10.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA11.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA12.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)

## Dry beads before elution
m300.delay(minutes=4)

## Elution of DNA

for target in samples:
    m300.set_flow_rate(aspirate=180, dispense=180)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (75), 'a': (75), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=40, dispense=40)
    m300.transfer(elution_vol, Elution_buffer, target.bottom(2), air_gap=0, new_tip='never')
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.mix(3, 100, target.bottom(6))
    m300.delay(seconds=5)
    m300.move_to(target.top(-3))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

### Resets head speed for futher processing
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (50), 'a': (50), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)

### Incubate elutes for 15 minutes at room temperature
m300.delay(minutes=15)

### Transfer elutes to new plates.
m300.transfer(35, SA1.bottom(1), elution_plate('A1'), new_tip='always', blow_out=True)
m300.transfer(35, SA2.bottom(1), elution_plate('A2'), new_tip='always', blow_out=True)
m300.transfer(35, SA3.bottom(1), elution_plate('A3'), new_tip='always', blow_out=True)
m300.transfer(35, SA4.bottom(1), elution_plate('A4'), new_tip='always', blow_out=True)
m300.transfer(35, SA5.bottom(1), elution_plate('A5'), new_tip='always', blow_out=True)
m300.transfer(35, SA6.bottom(1), elution_plate('A6'), new_tip='always', blow_out=True)
m300.transfer(35, SA7.bottom(1), elution_plate('A7'), new_tip='always', blow_out=True)
m300.transfer(35, SA8.bottom(1), elution_plate('A8'), new_tip='always', blow_out=True)
m300.transfer(35, SA9.bottom(1), elution_plate('A9'), new_tip='always', blow_out=True)
m300.transfer(35, SA10.bottom(1), elution_plate('A10'), new_tip='always', blow_out=True)
m300.transfer(35, SA11.bottom(1), elution_plate('A11'), new_tip='always', blow_out=True)
m300.transfer(35, SA12.bottom(1), elution_plate('A12'), new_tip='always', blow_out=True)
mag_deck.disengage()

robot.pause("Yay! \ Purification has finished \ Please store purified libraries as -20°C \ Press resume when finished.")
