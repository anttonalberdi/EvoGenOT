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
#from opentrons import labware, instruments, modules, robot

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
cold_block = labware.load('chill_rack_96', '1')
Cold_plate = labware.load('96-flat', '1', share=True)
# trough = labware.load('trough-12row', '2')
# Trash = labware.load('One-Column-reservoir','3')
temp_deck = modules.load('tempdeck', '10')
temp_plate = labware.load('96-flat', '10', share=True)
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

"""
Blund end repair
"""
robot.comment("Yay! \ Blund-end Repair begins.")

temp_deck.set_temperature(6)
temp_deck.wait_for_temp()

### Addition of Fill in mastermix to enzymes

m300.transfer(110, Fill_mastermix, Enzyme_Fill.bottom(2), mix_after=(5,30), blow_out=True)

### Addition of Fill in mastermix to to libraries
m10.transfer(10, Enzyme_Fill.bottom(1), SA1.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA2.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA3.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA4.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA5.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA6.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA7.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA8.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA9.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA10.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA11.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)
m10.transfer(10, Enzyme_Fill.bottom(1), SA12.bottom(2),mix_after=(3,8) , new_tip='always',  blow_out =True)

robot.pause("Yay! \ Please incubate in PCR machine \ at 65°C for 15 minutes, followed by 15 minutes at 80°C. \ Press resume when finished.")
