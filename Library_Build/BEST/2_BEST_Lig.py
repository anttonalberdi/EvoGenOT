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
#	  2.	Adds 91µl of Ligase MM to Enzyme strip (7µl * 13 columns)
#   3.  Distribute 8µl of Enzyme-Lig_MM to each well
#	  4.	Incubate in PCR at 20°C for 30 min, and at 65°C for 15 min

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
    'description': 'Adapter ligation procedure of Automated single tube library preperation after Carøe et al. 2017',
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



temp_deck1 = modules.load('tempdeck', '4')
MM_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
# trough = labware.load('trough-12row', '2')
# Trash = labware.load('One-Column-reservoir','3')
temp_deck2 = modules.load('tempdeck', '10')
temp_plate = labware.load('biorad-hardshell-96-PCR', '10', share=True)
#mag_deck = modules.load('magdeck', '7')
#mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

tipracks_10 = [labware.load('tiprack-10ul', slot, share=True)
               for slot in ['8','5']]

tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
                for slot in ['9']]


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
# Enzyme_ER = MM_plate.wells('A1')
Enzyme_Lig = MM_plate.wells('A2')
# Enzyme_Fill = MM_plate.wells('A3')

## Reagent SETUP
# ER_mastermix = MM_plate.wells('A4')
BGI_adapter = MM_plate.wells('A5')
Lig_mastermix = MM_plate.wells('A6')
# Fill_mastermix = MM_plate.wells('A7')

## Purification reagents SETUP
# SPRI_beads = trough.wells('A8')
# ethanol = trough.wells('A9')
# elution_buffer = trough.wells('A10')
# Liquid_trash = Trash.wells('A1')

## Sample Setup
sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in temp_plate.cols()[:col_num]]

## Volume setup
#ER_vol = 5.85
Lig_vol = 8
#Fill_vol = 10
#MM_dist_ER = ER_vol * col_num
MM_dist_Lig = Lig_vol * col_num
#MM_dist_Fill = Fill_vol * col_num

"""
Ligase
"""
robot.comment("Yay! \ Ligase begins.")

temp_deck_1.set_temperature(10)
temp_deck_2.set_temperature(10)

temp_deck_1.wait_for_temp()
temp_deck_2.wait_for_temp()


### Addition of Adapters

for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.move_to(BGI_adapter.bottom())
    m10.mix(3, 5, BGI_adapter.bottom(4))
    max_speed_per_axis = {'x': (400), 'y': (400), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.aspirate(2,BGI_adapter.bottom(1))
    m10.move_to(target.bottom())
    m10.dispense(2, target.bottom(3))
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.mix(3, 10, target.bottom(3))
    m10.delay(seconds=3)
    m10.set_flow_rate(aspirate=180, dispense=180)
    m10.move_to(target.top(-4))
    m10.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.drop_tip()


### Addition of End repair mastermix to enzymes
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(Lig_mastermix.bottom())
m300.mix(3, 50, Lig_mastermix.bottom(4))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(MM_dist_Lig,Lig_mastermix.bottom(1))
m300.move_to(Enzyme_Lig.bottom())
m300.dispense(MM_dist_Lig, Enzyme_Lig.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 30, Enzyme_Lig.bottom(4))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=180, dispense=180)
m300.move_to(Enzyme_Lig.top(-4))
m300.blow_out()
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Addition of End repair mastermix to libraries
for target in samples:
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_Lig)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.transfer(Lig_vol, Enzyme_Lig.bottom(1), target.bottom(2), air_gap=0, new_tip='never')
    m10.set_flow_rate(aspirate=40, dispense=40)
    m10.mix(5, 10, target.bottom(6))
    m10.delay(seconds=5)
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.move_to(target.top(-4))
    m10.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.drop_tip()

temp_deck_1.deactivate()
temp_deck_2.deactivate()
robot.comment("Yay! \ Please incubate in PCR machine \ at 20°C for 30 minutes, followed by 15 minutes at 65°C. \ Press resume when finished.")
