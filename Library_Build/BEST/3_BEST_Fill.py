##########################
### BEST Library build ###
##########################

## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Mix mastermix of End-repair, Ligase and Fill-in according to BEST-sheet and sample size.
#				NOTE! This procedure is for full plates
# 	2. Thaw samples in fridge and place them in a slot 2 in a chilling rack.
#
# Procedure
#
#		BEST
# 	1.	Distribute 2µl Adapters mix into temp_deck
#	  2.	Adds 110µl of Fill MM to Enzyme strip (8.4µl * 13 columns)
#   3.  Distribute 10µl of Enzyme-Fill_MM to each well
#	  4.	Incubate in PCR at 65°C for 15 min, and at 80°C for 15 min

#
#	Good Luck!
#
#
######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import tempdeck

#### METADATA ####

metadata = {
    'protocolName': 'BEST_Lib_build_96_sample',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/07/04',
    'description': 'Fill in procedure of Automated single tube library preperation after Carøe et al. 2017',
}
#### LOADING CUSTOM LABWARE ####
plate_name = 'chill_rack_96'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(12, 12),               # distances (mm) between each (column, row)
        diameter=6.4,                     # diameter (mm) of each well on the plate
        depth=15,                       # depth (mm) of each well on the plate
        volume=200)

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
temp_deck_1 = tempdeck.TempDeck()
temp_deck_2 = tempdeck.TempDeck()

temp_deck_1._port = '/dev/ttyACM0'
temp_deck_2._port = '/dev/ttyACM1'


if not robot.is_simulating():
	temp_deck_1.connect()
	temp_deck_2.connect()



temp_deck1 = modules.load('tempdeck', '7')
Cold_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)
# trough = labware.load('trough-12row', '2')
# Trash = labware.load('One-Column-reservoir','3')
temp_deck2 = modules.load('tempdeck', '10')
temp_plate = labware.load('biorad-hardshell-96-PCR', '10', share=True)
#mag_deck = modules.load('magdeck', '7')
#mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

tipracks_10 = [labware.load('tiprack-10ul', slot, share=True)
               for slot in ['8','5', '4']]

tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
                for slot in ['9', '11']]


#### PIPETTE SETUP ####
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_10)

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)

## Enzyme SETUP
# Enzyme_ER = Cold_plate.wells('A1')
# Enzyme_Lig = Cold_plate.wells('A2')
Enzyme_Fill = Cold_plate.wells('A3')

## Reagent SETUP
# ER_mastermix = Cold_plate.wells('A4')
# BGI_adapter = Cold_plate.wells('A5')
# Lig_mastermix = Cold_plate.wells('A6')
Fill_mastermix = Cold_plate.wells('A7')

## Purification reagents SETUP
# SPRI_beads = trough.wells('A8')
# ethanol = trough.wells('A9')
# elution_buffer = trough.wells('A10')
# Liquid_trash = Trash.wells('A1')

## Sample Setup
sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in temp_plate.cols()[:col_num]]

SA1 = temp_plate.wells('A1')
SA2 = temp_plate.wells('A2')
SA3 = temp_plate.wells('A3')
SA4 = temp_plate.wells('A4')
SA5 = temp_plate.wells('A5')
SA6 = temp_plate.wells('A6')
SA7 = temp_plate.wells('A7')
SA8 = temp_plate.wells('A8')
SA9 = temp_plate.wells('A9')
SA10 = temp_plate.wells('A10')
SA11 = temp_plate.wells('A11')
SA12 = temp_plate.wells('A12')

## Volume setup
#ER_vol = 5.85
#Lig_vol = 8
Fill_vol = 10
#MM_dist_ER = ER_vol * col_num
#MM_dist_Lig = Lig_vol * col_num
MM_dist_Fill = Fill_vol * col_num

"""
Fill in
"""
robot.comment("Yay! \ Blund-end Repair begins.")

cold_block.set_temperature(10)
temp_deck.set_temperature(10)
temp_deck.wait_for_temp()

### Addition of Fill in mastermix to enzymes
m300.start_at_tip(tipracks_200.well('A3'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.mix(3, 50, Fill_mastermix)
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.transfer(MM_dist_Fill, Fill_mastermix, Enzyme_Fill.bottom(2), air_gap=1, new_tip='never')
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 30, Enzyme_ER.bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=180, dispense=180)
m300.move_to(Enzyme_ER.top(-1))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Addition of Fill in mastermix to to libraries
for target in samples:
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_Fill.bottom(4))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.transfer(Fill_vol, Enzyme_Fill, target.bottom(3), air_gap=2, new_tip='never')
    m10.set_flow_rate(aspirate=20, dispense=20)
    m10.mix(2, 10, target.bottom(6))
    m10.delay(seconds=3)
    m10.touch_tip(v_offset=-2)
    m10.move_to(target.top(-4))
    m10.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.drop_tip()

temp_deck_1.deactivate()
temp_deck_2.deactivate()
robot.comment("Yay! \ Please incubate in PCR machine \ at 65°C for 15 minutes, followed by 15 minutes at 80°C. \ Press resume when finished.")
