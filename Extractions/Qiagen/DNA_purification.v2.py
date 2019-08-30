####### IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

# metadata
metadata = {
    'protocolName': 'DNA Purification',
    'author': 'Name <lassenyholm@gmail.com>',
    'description': 'DNA purification of PowerSoil/Fecal extracts (C1 and bead beating)',
}

### CUSTOM LABWARE ###

plate_name = 'One-Column-reservoir'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(1, 1),                    # specify amount of (wells, rows)
        spacing=(0, 0),               # distances (mm) between each (column, row)
        diameter=81,                     # diameter (mm) of each well on the plate
        depth=35,                       # depth (mm) of each well on the plate
        volume=350000)

plate_name = '1ml_PCR' #Used on the magdeck together with adaptor
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (wells, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)



### LABWARE SETUP ###

mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('1ml_PCR', '7', share=True)
trough = labware.load('trough-12row', '2')
Trash = labware.load('One-Column-reservoir','9')
elution_plate = labware.load('biorad-hardshell-96-PCR','1')


tipracks_200_1 = labware.load('tiprack-200ul', '4', share=True)
tipracks_200_2 = labware.load('tiprack-200ul', '5', share=True)
tipracks_200_3 = labware.load('tiprack-200ul', '6', share=True)
tipracks_1000_1 = labware.load('tiprack-1000ul', '10', share=True)
tipracks_1000_2 = labware.load('tiprack-1000ul', '11', share=True)



#### PIPETTE SETUP ####

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=300,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=(tipracks_200_1,tipracks_200_2,tipracks_200_3))

m1000 = instruments.P1000_Single(
    mount='left',
    min_volume=300,
    max_volume=1000,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=(tipracks_1000_1, tipracks_1000_2))

###  PURIFICATION REAGENTS SETUP ###
SPRI_beads = trough.wells('A1')
EtOH1 = trough.wells('A4')
EtOH2 = trough.wells('A5')
EtOH3 = trough.wells('A6')
EtOH4 = trough.wells('A7')
Elution_buffer = trough.wells('A12')
Liquid_trash = Trash.wells('A1')

sample_vol = 200
bead_vol = sample_vol
EtOH_vol = 200
Supernatant_vol = 500
elution_vol = 30

#### Sample SETUP

SA1 = sample_plate.wells('A1')
SA2 = sample_plate.wells('A3')
SA3 = sample_plate.wells('A5')
SA4 = sample_plate.wells('A7')
SA5 = sample_plate.wells('A9')
SA6 = sample_plate.wells('A11')

EA1 = elution_plate.wells('A1')
EA2 = elution_plate.wells('A3')
EA3 = elution_plate.wells('A5')
EA4 = elution_plate.wells('A7')
EA5 = elution_plate.wells('A9')
EA6 = elution_plate.wells('A11')


#### PROTOCOL ####

### Beads addition ###
mag_deck.disengage()

### Transfer beads to SA1
#m300.set_flow_rate(aspirate=100, dispense=150)
#m300.pick_up_tip(tipracks_200_1.wells('A1'))
#m300.move_to(SPRI_beads.top(-16))
#m300.mix(10, 200, SPRI_beads.top(-35))
#max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.set_flow_rate(aspirate=25, dispense=25)
#m300.aspirate(bead_vol, SPRI_beads.top(-35))
#m300.dispense(bead_vol, SA1.top(-4))
#m300.set_flow_rate(aspirate=100, dispense=100)
#m300.mix(5, bead_vol, SA1.bottom(5))
#m300.delay(seconds=5)
#m300.set_flow_rate(aspirate=130, dispense=130)
#m300.move_to(SA1.top(-10))
#m300.blow_out()
#max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.drop_tip()

### Transfer beads to SA2
#m300.set_flow_rate(aspirate=100, dispense=150)
#m300.pick_up_tip(tipracks_200_1.wells('A2')) # Slow down head speed 0.5X for bead handling
#m300.move_to(SPRI_beads.top(-16))
#m300.mix(10, 200, SPRI_beads.top(-35))
#max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.set_flow_rate(aspirate=25, dispense=25)
#m300.aspirate(bead_vol, SPRI_beads.top(-35))
#m300.dispense(bead_vol, SA2.top(-4))
#m300.set_flow_rate(aspirate=100, dispense=100)
#m300.mix(5, bead_vol, SA2.bottom(5))
#m300.delay(seconds=5)
#m300.set_flow_rate(aspirate=130, dispense=130)
#m300.move_to(SA2.top(-10))
#m300.blow_out()
#max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.drop_tip()

### Transfer beads to SA3
#m300.set_flow_rate(aspirate=100, dispense=150)
#m300.pick_up_tip(tipracks_200_1.wells('A3')) # Slow down head speed 0.5X for bead handling
#m300.move_to(SPRI_beads.top(-16))
#m300.mix(10, 200, SPRI_beads.top(-35))
#max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.set_flow_rate(aspirate=25, dispense=25)
#m300.aspirate(bead_vol, SPRI_beads.top(-35))
#m300.dispense(bead_vol, SA3.top(-4))
#m300.set_flow_rate(aspirate=100, dispense=100)
#m300.mix(5, bead_vol, SA3.bottom(5))
#m300.delay(seconds=5)
#m300.set_flow_rate(aspirate=130, dispense=130)
#m300.move_to(SA3.top(-10))
#m300.blow_out()
#max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.drop_tip()

### Transfer beads to SA4
#m300.set_flow_rate(aspirate=100, dispense=150)
#m300.pick_up_tip(tipracks_200_1.wells('A4')) # Slow down head speed 0.5X for bead handling
#m300.move_to(SPRI_beads.top(-16))
#m300.mix(10, 200, SPRI_beads.top(-35))
#max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.set_flow_rate(aspirate=25, dispense=25)
#m300.aspirate(bead_vol, SPRI_beads.top(-35))
#m300.dispense(bead_vol, SA4.top(-4))
#m300.set_flow_rate(aspirate=100, dispense=100)
#m300.mix(5, bead_vol, SA4.bottom(5))
#m300.delay(seconds=5)
#m300.set_flow_rate(aspirate=130, dispense=130)
#m300.move_to(SA4.top(-10))
#m300.blow_out()
#max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.drop_tip()

### Transfer beads to SA5
#m300.set_flow_rate(aspirate=100, dispense=150)
#m300.pick_up_tip(tipracks_200_1.wells('A5')) # Slow down head speed 0.5X for bead handling
#m300.move_to(SPRI_beads.top(-16))
#m300.mix(10, 200, SPRI_beads.top(-35))
#max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.set_flow_rate(aspirate=25, dispense=25)
#m300.aspirate(bead_vol, SPRI_beads.top(-35))
##m300.dispense(bead_vol, SA5.top(-4))
#m300.set_flow_rate(aspirate=100, dispense=100)
#m300.mix(5, bead_vol, SA5.bottom(5))
#m300.delay(seconds=5)
#m300.set_flow_rate(aspirate=130, dispense=130)
#m300.move_to(SA5.top(-10))
#m300.blow_out()
#max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.drop_tip()

### Transfer beads to SA6
##m300.set_flow_rate(aspirate=100, dispense=150)
#m300.pick_up_tip(tipracks_200_1.wells('A6')) # Slow down head speed 0.5X for bead handling
#m300.move_to(SPRI_beads.top(-16))
#m300.mix(10, 200, SPRI_beads.top(-35))
#max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.set_flow_rate(aspirate=25, dispense=25)
#m300.aspirate(bead_vol, SPRI_beads.top(-35))
#m300.dispense(bead_vol, SA6.top(-4))
#m300.set_flow_rate(aspirate=100, dispense=100)
##m300.mix(5, bead_vol, SA6.bottom(5))
#m300.delay(seconds=5)
#m300.set_flow_rate(aspirate=130, dispense=130)
#m300.move_to(SA6.top(-10))
#m300.blow_out()
#max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
#robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
#m300.drop_tip()



#m300.delay(minutes=10)
mag_deck.engage(height=33)
#m300.delay(minutes=10)



### REMOVING SUPERNATANT ###

#1. Remove blowout
#2. Make it do the entire column



### remove supernatant from SA1
m1000.set_flow_rate(aspirate=100, dispense=100)
m1000.pick_up_tip(tipracks_1000_1.cols('1'))
m1000.transfer(Supernatant_vol, SA1.bottom(1), Trash.wells('A1').top(-5))
#m1000.transfer(Supernatant_vol, plate.cols('1'), plate.cols('2'))
#m1000.dispense(Supernatant_vol, Trash.wells('A1').top(-5))
#m1000.drop_tip()

### remove supernatant from SA2
m1000.set_flow_rate(aspirate=100, dispense=100)
m1000.pick_up_tip(tipracks_1000_1.wells())
m1000.transfer(Supernatant_vol, SA2.bottom(1), Trash.wells('A1').top(-5))
#m1000.set_flow_rate(aspirate=100, dispense=100)
#m1000.pick_up_tip(tipracks_1000_1.columns('2'))
#m1000.aspirate(Supernatant_vol, SA2.bottom(1))
#m1000.transfer(Supernatant_vol, SA2.bottom(1), Trash.wells('A1').top(-5))
#m1000.dispense(Supernatant_vol, Trash.wells('A1').top(-5))
#m1000.drop_tip()


### remove supernatant from SA3
m1000.set_flow_rate(aspirate=100, dispense=100)
m1000.pick_up_tip(tipracks_1000_1.wells())
m1000.transfer(Supernatant_vol, SA3.bottom(1), Trash.wells('A1').top(-5))
#m1000.set_flow_rate(aspirate=100, dispense=100)
#m1000.pick_up_tip(tipracks_1000_1.columns('3'))
#m1000.aspirate(Supernatant_vol, SA3.bottom(1))
#m1000.transfer(Supernatant_vol, SA3.bottom(1), Trash.wells('A1').top(-5))

#m1000.dispense(Supernatant_vol, Trash.wells('A1').top(-5))
#m1000.drop_tip()


### remove supernatant from SA4
m1000.set_flow_rate(aspirate=100, dispense=100)
m1000.pick_up_tip(tipracks_1000_1.wells())
m1000.transfer(Supernatant_vol, SA4.bottom(1), Trash.wells('A1').top(-5))
#m1000.set_flow_rate(aspirate=100, dispense=100)
#m1000.pick_up_tip(tipracks_1000_1.columns('4'))
#m1000.aspirate(Supernatant_vol, SA4.bottom(1))
#m1000.transfer(Supernatant_vol, SA4.bottom(1), Trash.wells('A1').top(-5))

#m1000.dispense(Supernatant_vol, Trash.wells('A1').top(-5))
#m1000.drop_tip()


### remove supernatant from SA5
m1000.set_flow_rate(aspirate=100, dispense=100)
m1000.pick_up_tip(tipracks_1000_1.wells())
m1000.transfer(Supernatant_vol, SA5.bottom(1), Trash.wells('A1').top(-5))
#m1000.set_flow_rate(aspirate=100, dispense=100)
#m1000.pick_up_tip(tipracks_1000_1.columns('5'))
#m1000.aspirate(Supernatant_vol, SA5.bottom(1))
#m1000.transfer(Supernatant_vol, SA5.bottom(1), Trash.wells('A1').top(-5))

#m1000.dispense(Supernatant_vol, Trash.wells('A1').top(-5))
#m1000.drop_tip()


### remove supernatant from SA6
m1000.set_flow_rate(aspirate=100, dispense=100)
m1000.pick_up_tip(tipracks_1000_1.wells())
m1000.transfer(Supernatant_vol, SA6.bottom(1), Trash.wells('A1').top(-5))
#m1000.set_flow_rate(aspirate=100, dispense=100)
#m1000.pick_up_tip(tipracks_1000_1.columns('6'))
#m1000.aspirate(Supernatant_vol, SA6.bottom(1))
#m1000.transfer(Supernatant_vol, SA6.bottom(1), Trash.wells('A1').top(-5))

#m1000.dispense(Supernatant_vol, Trash.wells('A1').top(-5))
#m1000.drop_tip()

## Wash with EtOH1 ####

#1. Add blow out or delay when done washing
#2. Remove delay while submerged and add it outside the liquid

### Transfer EtOH1 to SA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_1.wells('A7'))
m300.move_to(EtOH1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(EtOH_vol, EtOH1.top(-35))
m300.dispense(EtOH_vol, SA1.top(-3))
m300.aspirate(EtOH_vol, EtOH1.top(-35))
m300.dispense(EtOH_vol, SA1.top(-3))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, EtOH_vol, SA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA1.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()


### Transfer EtOH1 to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_1.wells('A8'))
m300.move_to(EtOH1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(EtOH_vol, EtOH1.top(-35))
m300.dispense(EtOH_vol, SA2.top(-3))
m300.aspirate(EtOH_vol, EtOH1.top(-35))
m300.dispense(EtOH_vol, SA2.top(-3))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, EtOH_vol, SA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA2.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer EtOH1 to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_1.wells('A9'))
m300.move_to(EtOH1.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(EtOH_vol, EtOH1.top(-35))
m300.dispense(EtOH_vol, SA3.top(-3))
m300.aspirate(EtOH_vol, EtOH1.top(-35))
m300.dispense(EtOH_vol, SA3.top(-3))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, EtOH_vol, SA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA3.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer EtOH1 to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_1.wells('A10'))
m300.move_to(EtOH2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(EtOH_vol, EtOH2.top(-35))
m300.dispense(EtOH_vol, SA4.top(-3))
m300.aspirate(EtOH_vol, EtOH2.top(-35))
m300.dispense(EtOH_vol, SA4.top(-3))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, EtOH_vol, SA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA4.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer EtOH1 to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_1.wells('A11'))
m300.move_to(EtOH2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(EtOH_vol, EtOH2.top(-35))
m300.dispense(EtOH_vol, SA5.top(-3))
m300.aspirate(EtOH_vol, EtOH2.top(-35))
m300.dispense(EtOH_vol, SA5.top(-3))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, EtOH_vol, SA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA5.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer EtOH1 to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip(tipracks_200_1.wells('A12'))
m300.move_to(EtOH2.top(-16))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (100), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(EtOH_vol, EtOH2.top(-35))
m300.dispense(EtOH_vol, SA6.top(-3))
m300.aspirate(EtOH_vol, EtOH2.top(-35))
m300.dispense(EtOH_vol, SA6.top(-3))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, EtOH_vol, SA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(SA6.top(-10))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()
