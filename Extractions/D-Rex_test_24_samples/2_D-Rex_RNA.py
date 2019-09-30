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
    'version': '1.0-optimized',
    'date': '2019/08/15',
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

tipracks_200_1 = labware.load('tiprack-200ul', '2', share=True)
tipracks_200_2 = labware.load('tiprack-200ul', '3', share=True)
tipracks_200_3 = labware.load('tiprack-200ul', '4', share=True)

#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=([tipracks_200_1, tipracks_200_2, tipracks_200_3]))


#### REAGENT SETUP
EtOH1 = trough.wells('A4')
EtOH2 = trough.wells('A5')
EtOH3 = trough.wells('A6')
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

#### VOLUME SETUP
Sample_vol = 200
EtOH_vol = 2.0*Sample_vol
Wash_1_vol = 1.0*Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 100
BufferC_vol = 0.9*Sample_vol


#### PROTOCOL ####
## Remove supernatant, using tiprack 1
mag_deck.engage(height=34)
m300.delay(minutes=3)
m300.transfer(700, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
mag_deck.disengage()

### Wash 1 with Ethanol, using tiprack 2
### Transfer Wash 1 to RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A4')) # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH1.bottom(2))
m300.aspirate(Wash_1_vol, EtOH1.bottom(2))
m300.dispense(Wash_1_vol, RA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA1.bottom(4))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A5')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(2))
m300.dispense(Wash_1_vol, RA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA2.bottom(4))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A6')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA3.bottom(4))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA3.top(-10))
m300.blow_out()
m300.return_tip()


mag_deck.engage(height=34)
m300.delay(minutes=2)

### Remove supernatant, by re-using tiprack 2

### remove supernatant from RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A4'))
m300.aspirate(Wash_1_vol, RA1.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A5'))
m300.aspirate(Wash_1_vol, RA2.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A6'))
m300.aspirate(Wash_1_vol, RA3.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()


mag_deck.disengage()

## Ethanol Wash 2, by using tiprack 3
### Transfer Wash 2 to RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A7')) # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH2.bottom(2))
m300.aspirate(Wash_2_vol, EtOH2.bottom(2))
m300.dispense(Wash_2_vol, RA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA1.bottom(4))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A8')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(2))
m300.dispense(Wash_2_vol, RA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA2.bottom(4))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 2 to RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A9')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA3.bottom(4))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA3.top(-10))
m300.blow_out()
m300.return_tip()


mag_deck.engage(height=34)
m300.delay(minutes=2)

### Remove supernatant, by using re-using tiprack 3
mag_deck.engage(height=34)
m300.delay(minutes=2)

### remove supernatant from RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A7'))
m300.aspirate(Wash_2_vol, RA1.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A8'))
m300.aspirate(Wash_2_vol, RA2.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A9'))
m300.aspirate(Wash_2_vol, RA3.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()


## Dry beads before DNase treatment
mag_deck.disengage()
m300.delay(minutes=1)

### Adding DNAse, by using tiprack 4
m300.pick_up_tip(tipracks_200_1.wells('A10'))
m300.mix(2, 30, DNase)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(30, DNase.bottom(1))
m300.dispense(30, RA1.top(-10))
m300.mix(3,100,RA1.bottom(2)
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA1.top(-8))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.pick_up_tip(tipracks_200_1.wells('A11'))
m300.mix(2, 30, DNase)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(30, DNase.bottom(1))
m300.dispense(30, RA2.top(-10))
m300.mix(3,100,RA2.bottom(2)
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA2.top(-8))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.pick_up_tip(tipracks_200_1.wells('A12'))
m300.mix(2, 30, DNase)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(30, DNase.bottom(1))
m300.dispense(30, RA3.top(-10))
m300.mix(3,100,RA3.bottom(2)
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA3.top(-8))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#incubating samples with DNase
robot.pause("Please cover the plate with film and incubate 10 min 25°C at 1300 rpm. Please fill up tips before continuing process")
##Reset tipracks for more tips
m300.reset()


### Buffer C rebind, by using tiprack 1
### Transfer buffer C and beads to RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A1'))
m300.move_to(BufferC_2.bottom(2))
m300.mix(3, BufferC_vol, BufferC_2.bottom(4))
max_speed_per_axis = {'x':(300), 'y':(300), 'z': (50), 'a': (20), 'b': (20), 'c': 20}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(RA1.bottom(1))
m300.dispense(BufferC_vol, RA1.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(8, BufferC_vol, RA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA1.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()


### Transfer buffer C and beads to RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A2')) # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2.bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(RA2.bottom(1))
m300.dispense(BufferC_vol, RA2.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(8, BufferC_vol, RA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA2.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer buffer C and beads to RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A3')) # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_2.bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
m300.move_to(RA3.bottom(1))
m300.dispense(BufferC_vol, RA3.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(8, BufferC_vol, RA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA3.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.delay(minutes=5)
mag_deck.engage(height=34)
m300.delay(minutes=1)

### Remove supernatant by re-using tiprack 2
### remove supernatant from RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A1'))
m300.aspirate(125, RA1.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(125, RA1.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A2'))
m300.aspirate(125, RA2.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(125, RA2.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A3'))
m300.aspirate(125, RA3.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(125, RA3.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()


## Ethanol Wash 3, using tiprack 2
mag_deck.disengage()

### Transfer Wash 3 to RA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_2.wells('A4')) # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH3.bottom(2))
m300.aspirate(Wash_1_vol, EtOH3.bottom(4))
m300.dispense(Wash_1_vol, RA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 3 to RA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_2.wells('A5')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH3.bottom(2))
m300.dispense(Wash_1_vol, RA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 3 to RA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_2.wells('A6')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH3.bottom(2))
m300.dispense(Wash_1_vol, RA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA3.top(-10))
m300.blow_out()
m300.return_tip()

mag_deck.engage(height=34)
m300.delay(minutes=2)

## Remove supernatant, by re-using tiprack 2
### remove supernatant from RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A4'))
m300.aspirate(Wash_1_vol, RA1.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A5'))
m300.aspirate(Wash_1_vol, RA2.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A6'))
m300.aspirate(Wash_1_vol, RA3.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

## Ethanol Wash 4, by using tiprack 3
mag_deck.disengage()

### Transfer Wash 4 to RA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_2.wells('A7')) # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH4.bottom(2))
m300.aspirate(Wash_2_vol, EtOH4.bottom(3))
m300.dispense(Wash_2_vol, RA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 4 to RA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_2.wells('A8')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH4.bottom(2))
m300.dispense(Wash_2_vol, RA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 4 to RA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_2.wells('A9')) # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH4.bottom(2))
m300.dispense(Wash_2_vol, RA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA3.top(-10))
m300.blow_out()
m300.return_tip()

mag_deck.engage(height=34)
m300.delay(minutes=2)

## Remove supernatant, by re-using tiprack 3
### remove supernatant from RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A7'))
m300.aspirate(125, RA1.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(125, RA1.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A8'))
m300.aspirate(125, RA2.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(125, RA2.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A9'))
m300.aspirate(125, RA3.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.aspirate(125, RA3.bottom(1))
m300.dispense(125, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

## Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)
m300.delay(minutes=2)
## Elution
mag_deck.disengage()

m300.pick_up_tip(tipracks_200_2.wells('A10'))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
m300.dispense(Elution_vol, RA1.bottom(4))
m300.mix(5,50,RA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA1.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.pick_up_tip(tipracks_200_2.wells('A11'))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
m300.dispense(Elution_vol, RA2.bottom(4))
m300.mix(5,50,RA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA2.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

m300.pick_up_tip(tipracks_200_2.wells('A12'))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
m300.dispense(Elution_vol, RA3.bottom(4))
m300.mix(5,50,RA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA3.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()


robot.pause("Please cover the plate with film and incubate 5 min 25°C at 1500 rpm")
mag_deck.engage(height=34)
m300.delay(minutes=2)

### Transfer Elution buffer to elution_plate A1
m300.pick_up_tip(tipracks_200_3.wells('A1'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, RA1.bottom())
m300.dispense(Elution_vol, elution_plate_RNA.wells('A1').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A1').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to EA2
m300.pick_up_tip(tipracks_200_3.wells('A2'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, RA2.bottom())
m300.dispense(Elution_vol, elution_plate_RNA.wells('A2').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A2').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to EA3
m300.pick_up_tip(tipracks_200_3.wells('A3'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_vol, RA3.bottom())
m300.dispense(Elution_vol, elution_plate_RNA.wells('A3').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A3').top(-10))
m300.blow_out()
m300.drop_tip()

mag_deck.disengage()
