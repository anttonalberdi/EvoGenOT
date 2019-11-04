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
    'protocolName': 'D-Rex Inital Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0-optimized',
    'date': '2019/08/15',
    'description': 'Automation of D-Rex RNA and DNA seperation for extraction protocol of stool samples in SHIELD',
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
trough = labware.load('trough-12row', '9')
RNA_plate = labware.load('1ml_PCR', '1')
mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('1ml_magPCR', '7', share=True)

tipracks_200_1 = labware.load('tiprack-200ul', '4', share=True)

#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=[tipracks_200_1])

#### REAGENT SETUP
Binding_buffer1 = trough.wells('A1')			# Buffer B			# Buffer B
EtOH_Bind1 = trough.wells('A3')
BufferC_1 = trough.wells('A9')

#### Plate SETUP
SA1 = sample_plate.wells('A7')
SA2 = sample_plate.wells('A8')
SA3 = sample_plate.wells('A9')


RA1 = RNA_plate.wells('A7')
RA2 = RNA_plate.wells('A8')
RA3 = RNA_plate.wells('A9')


#### VOLUME SETUP
Sample_vol = 200
Binding_buffer_vol = Sample_vol*1
EtOH_buffer_vol = 175
BufferC_vol = 0.9*Sample_vol

#### PROTOCOL ####


## add beads and sample binding buffer to DNA/sample plate

mag_deck.disengage()
### Transfer buffer B and beads to SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Binding_buffer1.bottom(2))
m300.mix(3, Binding_buffer_vol, Binding_buffer1.bottom(3))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(3))
m300.move_to(SA1.bottom(1))
m300.dispense(Binding_buffer_vol, SA1.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA1.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer buffer B and beads to SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer1.bottom(3))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (40), 'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(2))
m300.move_to(SA2.bottom(1))
m300.dispense(Binding_buffer_vol, SA2.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA2.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer buffer B and beads to SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, Binding_buffer_vol, Binding_buffer1.bottom(1))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.move_to(SA3.bottom(1))
m300.dispense(Binding_buffer_vol, SA3.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Binding_buffer_vol, SA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA3.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()


## add beads and EtOH binding buffer to RNA plate
mag_deck.disengage()

#Pick up tip
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling

# Adding beads + ethanol to RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(EtOH_Bind1.bottom(2))
m300.mix(5, 200, EtOH_Bind1.bottom(4))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(4))
m300.dispense(EtOH_buffer_vol, RA1.bottom(4))
m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(4))
m300.dispense(EtOH_buffer_vol, RA1.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA1.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)

# Adding beads + ethanol to RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 200, EtOH_Bind1.bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(2))
m300.dispense(EtOH_buffer_vol, RA2.bottom(4))
m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(2))
m300.dispense(EtOH_buffer_vol, RA2.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA2.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)

# Adding beads + ethanol to RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 200, EtOH_Bind1.bottom(1))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(1))
m300.dispense(EtOH_buffer_vol, RA3.bottom(4))
m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(1))
m300.dispense(EtOH_buffer_vol, RA3.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(RA3.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)

#Dropping tip after aliquoting beads and Ethanol
m300.drop_tip()

## Incubate beads
m300.delay(minutes=5)

## Transfer supernatant
mag_deck.engage(height=34)
m300.delay(minutes=5)

#Transfer supernatant to RA1
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(165, SA1.bottom(2))
m300.dispense(165, RA1.top(-5))
m300.move_to(RA1.top(-2))
m300.blow_out()
m300.aspirate(165, SA1.bottom(2))
m300.dispense(165, RA1.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 200, RA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=150, dispense=150)
m300.move_to(RA1.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#Transfer supernatant to RA2
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(165, SA2.bottom(2))
m300.dispense(165, RA2.top(-5))
m300.move_to(RA2.top(-2))
m300.blow_out()
m300.aspirate(165, SA2.bottom(2))
m300.dispense(165, RA2.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 200, RA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=150, dispense=150)
m300.move_to(RA2.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

#Transfer supernatant to RA3
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(165, SA3.bottom(2))
m300.dispense(165, RA3.top(-5))
m300.move_to(RA3.top(-2))
m300.blow_out()
m300.aspirate(165, SA3.bottom(2))
m300.dispense(165, RA3.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(3, 200, RA3.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=150, dispense=150)
m300.move_to(RA3.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()


#### Adding BufferC to beads with DNA

mag_deck.disengage()

### Transfer buffer C to SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down  speed 0.5X for bead handling
m300.move_to(BufferC_1.bottom(3))
m300.mix(3, BufferC_vol, BufferC_1.bottom(4))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(SA1.bottom(1))
m300.dispense(BufferC_vol, SA1.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(8, BufferC_vol, SA1.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA1.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer buffer C to SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1.bottom(2))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.move_to(BufferC_1.top(-8))
m300.aspirate(BufferC_vol, BufferC_1.bottom(5))
m300.move_to(SA2.bottom(1))
m300.dispense(BufferC_vol, SA2.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(8, BufferC_vol, SA2.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA2.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()

### Transfer buffer C to SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, BufferC_vol, BufferC_1.bottom(1))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.move_to(BufferC_1.bottom(1))
m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
m300.move_to(SA3.bottom(1))
m300.dispense(BufferC_vol, SA3.bottom(4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(8, BufferC_vol, SA3.bottom(2))
m300.delay(seconds=2)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA3.bottom(5))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.return_tip()


robot.home()
############################
###### Job's is done! ######
############################
