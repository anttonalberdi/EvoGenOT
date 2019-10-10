##########################
### BEST Library build ###
##########################

## Description of procedure
#
#                           x1          x96(+10) #the extra amount shoud be optimised based on robot behavior
# T4 DNA ligase buffer	    4           424
# Reaction enhancer	        2.2         233.2
# T4 PNK	                1           106
# T4 polymerase	            0.4         42.4
# dNTP 25 mM	            0.4         42.4
# Mix                       8           848
# Sample                    32
# Total                     40
#
# 1) Pre-mix buffers in 1.5ml tube and distribute to strip tubes (B-Str) #Should be done before and keep frozen
#      T4 DNA ligase buffer	 424
#      Reaction enhancer     233.2
#      dNTP 25 mM	         42.4
#      Total                 699.6
#      For each well         87.45
#
# 2) Pre-mix enzymes in 1.5ml tube and distribute to strip tubes (E-Str) #Should be done before and keep frozen
#       T4 PNK	             106
#       T4 polymerase	     42.4
#       Total                148.4
#       For each well        18.55
#
# 3) Place B-Str in Column 1 of chill_rack_96 and E-Str in Column 3 of chill_rack_96 #Open the leads just before starting the protocol
#
# 4) Place the plate (biorad-hardshell-96-PCR) with the 96 samples in the tempdeck. NEED TO DECIDE ON THE FOIL! X-CROSSED?
#
# ROBOT PROTOCOL BEGINS
#
# 5) Transfer 87.45 ul from B-Str to E-Str (total should be around 77 ul) and mix well
#
# 6) Distribute 8 ul to each column in the plate and mix thoroughly (each well should have ca 30 ul and there should be around 7ul spare mix in the strip-tube)
#
# ROBOT PROTOCOL ENDS
#
# 7) Seal the plate with thin aluminium foil
#
# 8) Incubate the plate 30 min 20 ºC, 30 min 65 ºC
#
###########
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
    'description': 'End Repair of Automated single tube library preperation after Carøe et al. 2017',
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

plate_name = '1ml_Covaris'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=5.2,                     # diameter (mm) of each well on the plate
        depth=18.6,                       # depth (mm) of each well on the plate
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
temp_deck_1 = tempdeck.TempDeck()
temp_deck_2 = tempdeck.TempDeck()

temp_deck_1._port = '/dev/ttyACM0'
temp_deck_2._port = '/dev/ttyACM1'


if not robot.is_simulating():
	temp_deck_1.connect()
	temp_deck_2.connect()



temp_deck1 = modules.load('tempdeck', '4')
Cold_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
# trough = labware.load('trough-12row', '2')
# Trash = labware.load('One-Column-reservoir','3')
temp_deck2 = modules.load('tempdeck', '10')
temp_plate = labware.load('1ml_Covaris', '10', share=True)
#mag_deck = modules.load('magdeck', '7')
#mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

tipracks_10 = [labware.load('tiprack-10ul', slot, share=True)
               for slot in ['8','5']]

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
Enzyme_ER = Cold_plate.wells('A1')
# Enzyme_Lig = Cold_plate.wells('A2')
# Enzyme_Fill = Cold_plate.wells('A3')

## Reagent SETUP
ER_mastermix = Cold_plate.wells('A4')
# BGI_adapter = Cold_plate.wells('A5')
# Lig_mastermix = Cold_plate.wells('A6')
# Fill_mastermix = Cold_plate.wells('A7')

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
ER_vol = 8
#Lig_vol = 8
#Fill_vol = 10
MM_dist_ER = ER_vol * col_num
#MM_dist_Lig = Lig_vol * col_num
#MM_dist_Fill = Fill_vol * col_num



"""
Blund end repair
"""
robot.comment("Yay! \ Blund-end Repair begins.")

temp_deck_1.set_temperature(10)
temp_deck_2.set_temperature(10)

temp_deck_1.wait_for_temp()
temp_deck_2.wait_for_temp()

### Addition of End repair mastermix to enzymes

m300.set_flow_rate(aspirate=180, dispense=180)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(ER_mastermix.bottom())
m300.mix(3, 50, ER_mastermix.bottom(4))
max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (20), 'b': (20), 'c': (20)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(MM_dist_ER,ER_mastermix.bottom(1))
m300.move_to(Enzyme_ER.bottom())
m300.dispense(MM_dist_ER,Enzyme_ER.bottom(4))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.mix(5, 30, Enzyme_ER.bottom(4))
m300.delay(seconds=5)
m300.move_to(Enzyme_ER.top(-4))
max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

### Addition of End repair mastermix to libraries

for target in samples:
    m10.set_flow_rate(aspirate=180, dispense=180)
    m10.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.set_flow_rate(aspirate=25, dispense=25)
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(target.bottom())
    m10.dispense(ER_vol, target.bottom(3))
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.mix(5, 10, target.bottom(2))
    m10.delay(seconds=5)
    m10.set_flow_rate(aspirate=100, dispense=100)
    m10.move_to(target.top(-4))
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.drop_tip()


robot.pause("Yay! \ Please incubate in PCR machine \ at 20°C for 30 minutes, followed by 30 minutes at 65°C. \ Press resume when finished.")

temp_deck_1.deactivate()
temp_deck_2.deactivate()
