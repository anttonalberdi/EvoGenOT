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
## transfer respuspended supernatant to DNA plate
mag_deck.engage(height=18)
m300.delay(minutes=2)

#### Wash beads with BufferC
mag_deck.disengage()
### Transfer buffer C and beads to DA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down  speed 0.5X for bead handling
m300.move_to(BufferC_1.top(-16))
m300.mix(3, BufferC_vol, BufferC_1.top(-12))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(BufferC_vol, BufferC_1.top(-12))
m300.move_to(DA1.bottom(1))
m300.dispense(BufferC_vol, DA1.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA1.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(BufferC_1.top(-20))
m300.mix(3, BufferC_vol, BufferC_1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.top(-8))
m300.aspirate(BufferC_vol, BufferC_1.top(-16))
m300.move_to(DA2.bottom(1))
m300.dispense(BufferC_vol, DA2.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA2.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.bottom())
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(DA3.bottom(1))
m300.dispense(BufferC_vol, DA3.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA3.bottom(2))
m300.delay(seconds=2)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA3.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.bottom())
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(DA4.bottom(1))
m300.dispense(BufferC_vol, DA4.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA4.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA4.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_1.bottom())
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(DA5.bottom(1))
m300.dispense(BufferC_vol, DA5.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA5.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA5.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(BufferC_vol, BufferC_1.bottom(1))
m300.move_to(DA6.bottom(1))
m300.dispense(BufferC_vol, DA6.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA6.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA6.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(DA7.bottom(1))
m300.dispense(BufferC_vol, DA7.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA7.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA7.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(DA8.bottom(1))
m300.dispense(BufferC_vol, DA8.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA8.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA8.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(DA9.bottom(1))
m300.dispense(BufferC_vol, DA9.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA9.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA9.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(DA10.bottom(1))
m300.dispense(BufferC_vol, DA10.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA10.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA10.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(DA11.bottom(1))
m300.dispense(BufferC_vol, DA11.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA11.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA11.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer C and beads to DA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.move_to(BufferC_2.bottom())
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(DA12.bottom(1))
m300.dispense(BufferC_vol, DA12.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, BufferC_vol, DA12.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA12.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

mag_deck.engage(height=18)
m300.delay(minutes=2)

## Remove Buffer C
m300.transfer(250, DA1.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA2.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA3.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA4.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA5.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA6.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA7.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA8.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA9.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA10.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA11.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA12.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)

#### Wash beads with EtOH1
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH1, [wells.top(-3) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=18)
m300.delay(minutes=2)

m300.transfer(180, DA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(180, DA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process")
m300.reset()

#### Wash beads with EtOH2
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH2, [wells.top(-3) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=18)
m300.delay(minutes=2)

m300.transfer(250, DA1.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA3.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA2.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA4.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA5.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA6.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA7.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA9.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA8.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA10.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA11.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA12.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)

#### Dry beads before elution
m300.delay(minutes=2)

## Elution
mag_deck.disengage()
for target in samples: # Slow down head speed 0.5X for bead handling
    m300.pick_up_tip()
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
    m300.dispense(Elution_vol, target.bottom(1))
    m300.mix(5, 30, target.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(target.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

m300.delay(minutes=5)

mag_deck.engage(height=18)
m300.delay(minutes=5)
m300.transfer(Elution_vol, DA1.bottom(), elution_plate_DNA.wells('A1'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA3.bottom(), elution_plate_DNA.wells('A3'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA2.bottom(), elution_plate_DNA.wells('A2'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA4.bottom(), elution_plate_DNA.wells('A4'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA5.bottom(), elution_plate_DNA.wells('A5'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA7.bottom(), elution_plate_DNA.wells('A7'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA6.bottom(), elution_plate_DNA.wells('A6'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA8.bottom(), elution_plate_DNA.wells('A8'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA9.bottom(), elution_plate_DNA.wells('A9'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA10.bottom(), elution_plate_DNA.wells('A10'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA11.bottom(), elution_plate_DNA.wells('A11'), new_tip='always',  blow_out =True, air_gap=30)
m300.transfer(Elution_vol, DA12.bottom(), elution_plate_DNA.wells('A12'), new_tip='always',  blow_out =True, air_gap=30)
mag_deck.disengage()
