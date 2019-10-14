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
elution_plate_DNA = labware.load('biorad-hardshell-96-PCR', '1')
trough = labware.load('trough-12row', '9')
trash_box = labware.load('One-Column-reservoir', '8')
mag_deck = modules.load('magdeck', '7')
DNA_plate = labware.load('1ml_magPCR', '7', share=True)


tipracks_200_1 = labware.load('tiprack-200ul', '2', share=True)
tipracks_200_2 = labware.load('tiprack-200ul', '3', share=True)




#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=[tipracks_200_1, tipracks_200_2])

#### REAGENT SETUP

Liquid_trash = trash_box.wells('A1')

EtOH1 = trough.wells('A4')
EtOH2 = trough.wells('A5')
Elution_buffer = trough.wells('A12')

#### VOLUME SETUP
Sample_vol = 200
Sample_buffer_vol = 2.5*Sample_vol
BufferC_vol = 0.9*Sample_vol
Wash_1_vol = Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50

#### Plate SETUP
DA1 = DNA_plate.wells('A4')
DA2 = DNA_plate.wells('A5')
DA3 = DNA_plate.wells('A6')

sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in DNA_plate.cols()[:col_num]]

#### PROTOCOL ####
mag_deck.engage(height=34)
m300.delay(minutes=2)

## Remove Buffer C
m300.transfer(250, DA1.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA2.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA3.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)


mag_deck.disengage()

### Wash 1 with Ethanol, using tiprack 2
### Transfer Wash 1 to DA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A4')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, DA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to DA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A5')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, DA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to DA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A6')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, DA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA3.top(-10))
m300.blow_out()
m300.return_tip()

m300.delay(seconds=30)
mag_deck.engage(height=34)
m300.delay(minutes=2)

### Remove supernatant, by re-using tiprack 2
### remove supernatant from DA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A4'))
m300.aspirate(Wash_1_vol, DA1.bottom())
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from DA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A5'))
m300.aspirate(Wash_1_vol, DA2.bottom())
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from DA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A6'))
m300.aspirate(Wash_1_vol, DA3.bottom())
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

mag_deck.disengage()

## Ethanol Wash 2, by using tiprack 3
### Transfer Wash 2 to DA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A7')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, DA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 2 to DA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A8')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, DA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 2 to DA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A9')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, DA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA3.top(-10))
m300.blow_out()
m300.return_tip()

m300.delay(seconds=30)
mag_deck.engage(height=34)
m300.delay(minutes=2)

### Remove supernatant, by using re-using tiprack 3

### remove supernatant from DA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A7'))
m300.aspirate(Wash_2_vol, DA1.bottom())
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from DA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A8'))
m300.aspirate(Wash_2_vol, DA2.bottom())
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from DA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A9'))
m300.aspirate(Wash_2_vol, DA3.bottom())
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

m300.delay(minutes=2)
#### Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)

## Elution
mag_deck.disengage()

m300.pick_up_tip(tipracks_200_1.wells('A10'))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
m300.dispense(Elution_vol, DA1.bottom(2))
m300.mix(5,50,DA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA1.bottom(8))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.pick_up_tip(tipracks_200_1.wells('A11'))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
m300.dispense(Elution_vol, DA2.bottom(2))
m300.mix(5,50,DA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA2.bottom(8))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.pick_up_tip(tipracks_200_1.wells('A12'))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
m300.dispense(Elution_vol, DA1.bottom(2))
m300.mix(5,50,DA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(DA3.bottom(8))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.delay(minutes=5)

mag_deck.engage(height=34)
m300.delay(minutes=3)

### Transfer Elution buffer to elution_plate A1
m300.pick_up_tip(tipracks_200_2.wells('A1'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, DA1.bottom(1))
m300.dispense(Elution_vol, elution_plate_DNA.wells('A1').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_DNA.wells('A1').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A2
m300.pick_up_tip(tipracks_200_2.wells('A2'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, DA2.bottom(1))
m300.dispense(Elution_vol, elution_plate_DNA.wells('A2').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_DNA.wells('A2').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A3
m300.pick_up_tip(tipracks_200_2.wells('A3'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, DA3.bottom(1))
m300.dispense(Elution_vol, elution_plate_DNA.wells('A3').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_DNA.wells('A3').top(-10))
m300.blow_out()
m300.drop_tip()

mag_deck.disengage()
