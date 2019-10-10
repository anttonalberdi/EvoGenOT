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
# 	1.	Distribute 8µl End-Repair mix into temp_deck
#	2.	Add 32 µl sample into temp_deck
#	3.	Incubate in PCR at 20°C for 30 min, and at 65°C for 30 min
#
#	4.	Add 2µl of (5µM - 20µM) adaptor to a new plate
#	5.	Transfer ER-sample to adapters and mix
#	6.	Add 10µl of Ligase to each well
#	7.	Transfer full volume to temp_deck
#	8.	Incubate in PCR at 20°C for 30 min and at 65°C for 10 min
#
#	9.	Add 10µl Fill-in to each well in temp_deck
#	10.	Incubate in PCR at 65°C for 15 min and 80°C for 15 min
#
#		Purify
#
#	1. Add 1.8X SPRI beads
#	2. Wash twice with 80% EtOH
#	3. Elute in 40µl EB
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
    'date': '2019/02/09',
    'description': 'Automated single tube library preperation after Carøe et al. 2017',
}



#### LABWARE SETUP ####
cold_block = labware.load('opentrons-aluminum-block-2ml-eppendorf', '1')
sample_plate = labware.load('96-PCR-flat', '2')
elution_plate = labware.load('96-flat', '3')
temp_deck = modules.load('tempdeck', '10')
temp_plate = labware.load('96-flat', '10', share=True)
trough = labware.load('trough-12row', '6')
mag_deck = modules.load('magdeck', '7')
mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['8','5']]

tipracks_300 = [labware.load('tiprack-200ul', slot, share=True)
                for slot in ['9', '11', '4']]


#### PIPETTE SETUP ####
s10 = instruments.P10_Single(
    mount='right',
    tip_racks=tipracks_10)

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_300)

# reagent setup
ER_mastermix = cold_block.wells('A1')
BGI_adapter = cold_block.wells('B1')
Lig_mastermix = cold_block.wells('C1')
Fill_mastermix = cold_block.wells('D1')
SPRI_beads = trough.wells('A1')
ethanol = trough.wells('A2')
elution_buffer = trough.wells('A3')
liquid_trash = trough.wells('A12')

sample_vol = 35.0

"""
Blund end repair
"""
robot.comment("Yay! \ Blund-end Repair begins.")

temp_deck.set_temperature(4)
temp_deck.wait_for_temp()

s10.transfer(8, ER_mastermix, [well.bottom() for well in temp_plate.wells()])
m300.transfer(32, sample_plate.cols(), temp_plate.cols(),mix_after=(3,30) , new_tip='always',  blow_out =True) 
robot.pause("Yay! \ Please incubate in PCR machine \ at 20°C for 30 minutes, followed by 30 minutes at 65°C. \ Press resume when finished.")


"""
Adapter Addition
"""
robot.comment("End of Blund-end Repair. Adapter Addition begins.")
temp_deck.set_temperature(4)
temp_deck.wait_for_temp()
s10.transfer(2, BGI_adapter, [well.bottom() for well in temp_plate.wells()],mix_after=(3, 10) , new_tip='always',  blow_out =True)

s10.transfer(8, Lig_mastermix, [well.top() for well in temp_plate.wells()], new_tip='once',  blow_out =True)


robot.pause("End of Adapter Addition. Ligase begins. \ Incubate at 20°C for 30 min, followed by 15 min at 65°C. Press resume when finished.")

"""
Fill-in
"""
robot.comment("Fill-in begins.")
temp_deck.set_temperature(4)
temp_deck.wait_for_temp()
s10.transfer(10, Fill_mastermix, [well.top() for well in temp_plate.wells()])
