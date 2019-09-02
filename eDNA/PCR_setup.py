## Description of procedure ##
#
#
#	1. Adding MM_Fw1 to column 1-3 in setup plate
#   2. Adding MM_Fw2 to column 4-6 in setup plate
#   3. Adding MM_Fw3 to column 7-9 in setup plate
#   4. Adding MM_Fw4 to column 10-12 in setup plate

#   5. Add Re1-Re24 to column 1-3 in setup plate
#   6. Add Re1-Re24 to column 4-6 in setup plate
#   7. Add Re1-Re24 to column 7-9 in setup plate
#   8. Add Re1-Re24 to column 10-12 in setup plate


### Procedure ###


######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'eDNA PCR setup',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0-optimized',
    'date': '2019/09/02',
    'description': 'Automation of Metabarcoding setup for 96 samples',
}


#### LABWARE SETUP ####
plate_name = 'chill_rack_2ml'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(6, 4),                    # specify amount of (columns, rows)
        spacing=(18, 18),               # distances (mm) between each (column, row)
        diameter=10,                     # diameter (mm) of each well on the plate
        depth=74,                       # depth (mm) of each well on the plate
        volume=2000)

Re_plate = labware.load('biorad-hardshell-96-PCR', '4')
Reagents = labware.load('chill_rack_2ml', '7')
temp_deck = modules.load('tempdeck', '10')
setup_plate = labware.load('biorad-hardshell-96-PCR', '10', share=True)
DNA_plate = labware.load('biorad-hardshell-96-PCR', '11')

tipracks_10_1 = labware.load('tiprack-200ul', '1', share=True)
tipracks_10_2 = labware.load('tiprack-10ul', '2', share=True)
tipracks_10_3 = labware.load('tiprack-10ul', '3', share=True)

#### PIPETTE SETUP ####
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=([tipracks_10_1, tipracks_10_2,tipracks_10_3]))

#### REAGENT SETUP
MM_Fw1 = Reagents.wells('A1')
MM_Fw2 = Reagents.wells('B1')
MM_Fw3 = Reagents.wells('C1')
MM_Fw4 = Reagents.wells('D1')

Re1_8 = Re_plate.wells('A1')
Re9_16 = Re_plate.wells('A2')
Re17_24 = Re_plate.wells('A3')


#### RXN SETUP - Can be changed for other setups

RXN_vol = 20
DNA_vol = 1
Re_vol = 2

MM_vol = RXN_vol - DNA_vol - Re_vol

if MM_vol < 10:
    MM_vol = MM_vol
else:
    MM_vol = MM_vol/2
### PROTOCOL ###

### Engage tempdeck at 10°C
temp_deck.set_temperature(10)
temp_deck.wait_for_temp()

### Adding MM_Fw1 to Coloumn 1-3
samples = [setup_plate.wells('A1'), setup_plate.wells('A2'), setup_plate.wells('A3')]
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, MM_Fw1.bottom(4))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(MM_vol, MM_Fw1.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.aspirate(MM_vol, MM_Fw1.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.delay(seconds=2)
    m10.move_to(target.bottom(5))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.return_tip()

### Adding MM_Fw2 to Coloumn 4-6
samples = [setup_plate.wells('A4'), setup_plate.wells('A5'), setup_plate.wells('A6')]
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, MM_Fw2.bottom(4))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(MM_vol, MM_Fw2.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.aspirate(MM_vol, MM_Fw2.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.delay(seconds=2)
    m10.move_to(target.bottom(5))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.return_tip()

### Adding MM_Fw2 to Coloumn 7-9
samples = [setup_plate.wells('A7'), setup_plate.wells('A8'), setup_plate.wells('A9')]
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, MM_Fw3.bottom(4))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(MM_vol, MM_Fw3.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.aspirate(MM_vol, MM_Fw3.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.delay(seconds=2)
    m10.move_to(target.bottom(5))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.return_tip()

### Adding MM_Fw2 to Coloumn 10-12
samples = [setup_plate.wells('A10'), setup_plate.wells('A11'), setup_plate.wells('A12')]
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, MM_Fw4.bottom(4))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(MM_vol, MM_Fw4.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.aspirate(MM_vol, MM_Fw4.bottom(1))
    m10.dispense(MM_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.delay(seconds=2)
    m10.move_to(target.bottom(5))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.return_tip()



### Adding Re_1-8 to Coloumn 1,4,7,10
samples = [setup_plate.wells('A1'), setup_plate.wells('A4'), setup_plate.wells('A7'), setup_plate.wells('A10')]
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Re1_8.bottom(2))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(Re_vol, Re1_8.bottom(1))
    m10.dispense(Re_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.mix(3, 10, target.bottom(2))
    m10.delay(seconds=2)
    m10.move_to(target.bottom(5))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.return_tip()

### Adding Re_9-16 to Coloumn 2,5,8,11
samples = [setup_plate.wells('A2'), setup_plate.wells('A5'), setup_plate.wells('A8'), setup_plate.wells('A11')]
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Re9_16.bottom(2))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(Re_vol, Re9_16.bottom(1))
    m10.dispense(Re_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.mix(3, 10, target.bottom(2))
    m10.delay(seconds=2)
    m10.move_to(target.bottom(5))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.return_tip()


### Adding Re_17-24 to Coloumn 3,6,9,12
samples = [setup_plate.wells('A3'), setup_plate.wells('A6'), setup_plate.wells('A9'), setup_plate.wells('A12')]
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Re17_24.bottom(2))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(Re_vol, Re17_24.bottom(1))
    m10.dispense(Re_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.mix(3, 10, target.bottom(2))
    m10.delay(seconds=2)
    m10.move_to(target.bottom(5))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.return_tip()

### Transfer DNA to SETUP plate A1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A1').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A1').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A1').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A1').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A1').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A2').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A2').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A2').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A2').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A2').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A3').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A3').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A3').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A3').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A3').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A4').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A4').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A4').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A4').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A4').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A5').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A5').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A5').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A5').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A5').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A6').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A6').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A6').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A6').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A6').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A7').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A7').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A7').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A7').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A7').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A8').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A8').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A8').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A8').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A8').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A9').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A9').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A9').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A9').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A9').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A10').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A10').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A10').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A10').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A10').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A11').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A11').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A11').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A11').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A11').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer DNA to SETUP plate A12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, DNA_plate.wells('A12').bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(DNA_vol, DNA_plate.wells('A12').bottom(2))
m300.dispense(DNA_vol, setup_plate.wells('A12').bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 10, setup_plate.wells('A12').bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(setup_plate.wells('A12').top(-5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()
