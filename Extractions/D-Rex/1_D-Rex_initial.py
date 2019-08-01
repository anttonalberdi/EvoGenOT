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
    'version': '1.0',
    'date': '2019/03/28',
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

#### LABWARE SETUP ####
trough = labware.load('trough-12row', '2')
RNA_plate = labware.load('1ml_PCR', '1')
mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('1ml_PCR', '7', share=True)

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
Binding_buffer1 = trough.wells('A1')
Binding_buffer2 = trough.wells('A2')			# Buffer B			# Buffer B
EtOH_Bind1 = trough.wells('A3')
EtOH_Bind2 = trough.wells('A4')

#### Plate SETUP
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
Binding_buffer_vol = Sample_vol*1
EtOH_buffer_vol = 350


#### PROTOCOL ####


## add beads and sample binding buffer to DNA/sample plate


mag_deck.disengage()
m300.distribute(Binding_buffer_vol, Binding_buffer1, [wells.top(-4) for wells in sample_plate.wells('A1','A2','A3','A4','A5','A6')], new_tip='always', mix_before=(3,200), blow_out =True)
m300.distribute(Binding_buffer_vol, Binding_buffer2, [wells.top(-4) for wells in sample_plate.wells('A8','A9','A10','A11','A12')], new_tip='always', mix_before=(3,200), blow_out =True)

### Transfer buffer B and beads to SA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.move_to(SA1.bottom(1))
m300.dispense(Binding_buffer_vol, SA1.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA1.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA1.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.move_to(SA2.bottom(1))
m300.dispense(Binding_buffer_vol, SA2.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA2.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA2.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.move_to(SA3.bottom(1))
m300.dispense(Binding_buffer_vol, SA3.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA3.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA3.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.move_to(SA4.bottom(1))
m300.dispense(Binding_buffer_vol, SA4.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA4.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA4.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.move_to(SA5.bottom(1))
m300.dispense(Binding_buffer_vol, SA5.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA5.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA5.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer1)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(1))
m300.move_to(SA6.bottom(1))
m300.dispense(Binding_buffer_vol, SA6.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA6.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA6.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.move_to(SA7.bottom(1))
m300.dispense(Binding_buffer_vol, SA7.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA7.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA7.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.move_to(SA8.bottom(1))
m300.dispense(Binding_buffer_vol, SA8.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA8.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA8.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.move_to(SA9.bottom(1))
m300.dispense(Binding_buffer_vol, SA9.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA9.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA9.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.move_to(SA10.bottom(1))
m300.dispense(Binding_buffer_vol, SA10.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA10.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA10.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.move_to(SA11.bottom(1))
m300.dispense(Binding_buffer_vol, SA11.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA11.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA11.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Transfer buffer B and beads to SA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 10, Binding_buffer2)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(1))
m300.move_to(SA12.bottom(1))
m300.dispense(Binding_buffer_vol, SA12.bottom(3))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 10, SA12.bottom(6))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=100, dispense=100)
m300.move_to(SA12.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

## add beads and EtOH binding buffer to RNA plate
mag_deck.disengage()
m300.set_flow_rate(aspirate=100, dispense=200)
m300.distribute(EtOH_buffer_vol, EtOH_Bind1, RNA_plate.cols('1','2','3','4','5','6'), new_tip='once', blow_out =True)
m300.distribute(EtOH_buffer_vol, EtOH_Bind2, RNA_plate.cols('7','8','9','10','11','12'), new_tip='once', blow_out =True)

## Incubate beads
m300.delay(minutes=5)


## Transfer supernatant
mag_deck.engage(height=16)
m300.delay(minutes=5)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.transfer(165, SA1.bottom(2), RA1.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA1.bottom(2), RA1.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA2.bottom(2), RA2.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA2.bottom(2), RA2.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA3.bottom(2), RA3.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA3.bottom(2), RA3.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA4.bottom(2), RA4.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA4.bottom(2), RA4.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA5.bottom(2), RA5.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA5.bottom(2), RA5.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA6.bottom(2), RA6.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA6.bottom(2), RA6.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA7.bottom(2), RA7.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA7.bottom(2), RA7.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA8.bottom(2), RA8.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA8.bottom(2), RA8.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA9.bottom(2), RA9.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA9.bottom(2), RA9.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA10.bottom(2), RA10.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA10.bottom(2), RA10.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA11.bottom(2), RA11.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA11.bottom(2), RA11.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)

m300.transfer(165, SA12.bottom(2), RA12.top(-4), new_tip='once',  blow_out =True)
m300.transfer(165, SA12.bottom(2), RA12.bottom(2), mix_after=(5,200), new_tip='once',  blow_out =True)



mag_deck.disengage()
robot.pause("Transfer DNA plate to fridge with cover-foil")
