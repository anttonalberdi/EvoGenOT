###################################
### HOLOFOOD BEST library build ###
###################################

## Description of procedure ##

# BEFORE PROTOCOL BEGINS
#
    # Ligation step mastex mix reagents and volumes:
    #                           1X      96(+10)X
    # PEG 4000 50%              4.5     477
    # T4 DNA ligase buffer      0.75    79.5
    # T4 DNA ligase             0.75    79.5
    # Mix                       6       636
    # Sample                    30 (24.15 + ER-master mix (5.85))
    #Total                      36 (+ 1 ul BGI adaptors)
    #
# 1) Distribute 19.9 ul (1.5 ul for each well) of BGI Adaptor to Column 5 (BGI_adaptor) of chill_rack_96
#
# 2) Pre-mix buffers in 1.5 ml tube and distribute to Column 6 (Lig_mastermix) of chill_rack_96
#       PEG 4000 50%            477
#       T4 DNA ligase buffer    79.5
#       For each well           69.6
#
# 3) Pre-mix enzymes in 1.5 ml tube and distribute to Column 2 (Enzyme_Lig) of chill_rack_96
#       T4 DNA ligase           79.5
#       For each well           9.9
#
# ROBOT PROTOCOL BEGINS
#
# 4) Transfer 1.5 ul of BGI adaptors to each well in the sample plate and mix thoroughly
#
# 5) Transfer 69.6 ul from Column 6 to Column 2 and mix
#
# 6) Distribute 6 ul to each well in the sample plate and mix thoroughly
#
# ROBOT PROTOCOL ENDS
#
# 7) Cover the plate with thin aluminium seal
#
# 8) Incubate the plate 30 min 20ºC, 15 min 65ºC



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
MM_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
# trough = labware.load('trough-12row', '2')
# Trash = labware.load('One-Column-reservoir','3')
temp_deck2 = modules.load('tempdeck', '10')
temp_plate = labware.load('1ml_Covaris', '10', share=True)
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
Lig_vol = 6
#Fill_vol = 7.5
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
    m10.aspirate(1,BGI_adapter.bottom(1))
    m10.move_to(target.bottom())
    m10.dispense(1, target.bottom(3))
    m10.set_flow_rate(aspirate=50, dispense=50)
    m10.mix(3, 10, target.bottom(3))
    m10.delay(seconds=3)
    m10.set_flow_rate(aspirate=180, dispense=180)
    m10.move_to(target.top(-4))
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
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m10.drop_tip()

temp_deck_1.deactivate()
temp_deck_2.deactivate()
robot.comment("Yay! \ Please incubate in PCR machine \ at 20°C for 30 minutes, followed by 15 minutes at 65°C. \ Press resume when finished.")
