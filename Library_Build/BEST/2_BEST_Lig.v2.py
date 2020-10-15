##########################
### BEST library build ###
##########################

## Description of procedure ##

# BEFORE PROTOCOL BEGINS
#
    # Ligation step mastex mix reagents and volumes:
    #                           1X      96(+10)X
    # PEG 4000 50%              6       636
    # T4 DNA ligase buffer      1       106
    # T4 DNA ligase             1       106
    # Mix                       8       848
    # Sample                    40 (+ 2ul adaptors)
    #Reaction size              50
    #
# 1) Distribute 26.5 ul (2 ul for each well) of BGI Adaptor to Column 5 (BGI_adaptor) of chill_rack_96
#
# 2) Pre-mix buffers in 1.5 ml tube and distribute to Column 6 (Lig_mastermix) of chill_rack_96
#       PEG 4000 50%            636
#       T4 DNA ligase buffer    106
#       For each well           92.75
#
# 3) Pre-mix enzymes in 1.5 ml tube and distribute to Column 2 (Enzyme_Lig) of chill_rack_96
#       T4 DNA ligase           106
#       For each well           13.25
#
# ROBOT PROTOCOL BEGINS
#
# 4) Transfer 2 ul of BGI adaptors to each well in the sample plate and mix thoroughly
#
# 5) Transfer 92.75 ul from Column 6 to Column 2 and mix
#
# 6) Distribute 8 ul to each well in the sample plate and mix thoroughly
#
# ROBOT PROTOCOL ENDS
#
# 7) Cover the plate with thin aluminium seal
#
# 8) Incubate the plate 30 min 20ºC, 15 min 65ºC
#
#	Good Luck!
#
#
######## IMPORT LIBRARIES ########
from opentrons import protocol_api


#### METADATA ####

metadata = {
    'protocolName': 'BEST_Lib_build_96_sample',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'apiLevel': '2.2',
    'description': 'End Repair of Automated single tube library preperation after Carøe et al. 2017',
    }


def run(protocol):

    #### LABWARE SETUP ####
    temp_deck_1 = protocol.load_module('tempdeck', 4)
    temp_deck_2 = protocol.load_module('tempdeck', 10)

    temp_deck_1._port = '/dev/ttyACM0'
    temp_deck_2._port = '/dev/ttyACM1'


    if not protocol.is_simulating():
    	temp_deck_1.connect()
    	temp_deck_2.connect()




    MM_plate = temp_deck_1.load_labware('biorad_96_wellplate_200ul_pcr')
# trough = labware.load('trough-12row', '2')
# Trash = labware.load('One-Column-reservoir','3')
    temp_plate = temp_deck_2.load_labware('biorad_96_wellplate_200ul_pcr')
#mag_deck = modules.load('magdeck', '7')
#mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

    tipracks_10_1 = protocol.load_labware('opentrons_96_filtertiprack_10ul', 5)
    tipracks_10_2 = protocol.load_labware('opentrons_96_filtertiprack_10ul', 8)

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 9)


#### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi', mount='left', tip_racks=(tipracks_200_1,))

    m10 = protocol.load_instrument('p10_multi', mount='right', tip_racks=(tipracks_10_1, tipracks_10_2))


## Enzyme SETUP
# Enzyme_ER = MM_plate.wells('A1')
    Enzyme_Lig = MM_plate['A1']
# Enzyme_Fill = MM_plate.wells('A3')

## Reagent SETUP
# ER_mastermix = MM_plate.wells('A4')
    BGI_adapter = MM_plate['A5']
    Lig_mastermix = MM_plate['A6']
# Fill_mastermix = MM_plate.wells('A7')

## Purification reagents SETUP
# SPRI_beads = trough.wells('A8')
# ethanol = trough.wells('A9')
# elution_buffer = trough.wells('A10')
# Liquid_trash = Trash.wells('A1')

## Sample Setup
    sample_number = 96
    col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
    samples = [col for col in temp_plate.columns()[:col_num]]

## Volume setup
#ER_vol = 8
    Lig_vol = 8
#Fill_vol = 10
#MM_dist_ER = ER_vol * col_num
    MM_dist_Lig = Lig_vol * col_num
#MM_dist_Fill = Fill_vol * col_num



    temp_deck_1.set_temperature(10) #  API 2 automatically wait for the tempdeck to reach this temperature
    temp_deck_2.set_temperature(10)

    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']

### Addition of Adapters

    for i in list_of_cols:
        m10.flow_rate.aspirate = 180
        m10.flow_rate.dispense = 180
        m10.pick_up_tip(tipracks_10_1[i]) # Slow down head speed 0.5X for bead handling
        m10.move_to(BGI_adapter.bottom())
        m10.mix(3, 5, BGI_adapter.bottom(4))
        m10.flow_rate.aspirate = 50
        m10.flow_rate.dispense = 50
        m10.aspirate(2, BGI_adapter.bottom(1))
        m10.move_to(temp_plate[i].bottom())
        m10.dispense(2, temp_plate[i].bottom(3))
        m10.mix(3, 10, temp_plate[i].bottom(3))
        protocol.delay(seconds=3)
        m10.flow_rate.aspirate = 180
        m10.flow_rate.dispense = 180
        m10.move_to(temp_plate[i].top(-4))
        m10.return_tip()




    ### Addition of Ligase mastermix to enzymes
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A1']) # Slow down head speed 0.5X for bead handling
    m300.move_to(Lig_mastermix.bottom())
    m300.mix(3, 50, Lig_mastermix.bottom(4))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(MM_dist_Lig,Lig_mastermix.bottom(1))
    m300.move_to(Enzyme_Lig.bottom())
    m300.dispense(MM_dist_Lig, Enzyme_Lig.bottom(4))
    m300.mix(5, 30, Enzyme_Lig.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 180
    m300.flow_rate.dispense = 180
    m300.move_to(Enzyme_Lig.top(-4))
    m300.return_tip()

### Addition of Ligase mastermix to libraries
    for i in list_of_cols:
        m10.flow_rate.aspirate = 100
        m10.flow_rate.dispense = 100
        m10.pick_up_tip(tipracks_10_2[i]) # Slow down head speed 0.5X for bead handling
        m10.mix(3, 10, Enzyme_Lig)
        m10.flow_rate.aspirate = 50
        m10.flow_rate.dispense = 50
        m10.transfer(Lig_vol, Enzyme_Lig.bottom(1), temp_plate[i].bottom(2), new_tip='never')
        m10.flow_rate.aspirate = 40
        m10.flow_rate.dispense = 40
        m10.mix(5, 10, temp_plate[i].bottom(6))
        protocol.delay(seconds=5)
        m10.flow_rate.aspirate = 100
        m10.flow_rate.dispense = 100
        m10.move_to(temp_plate[i].top(-4))
        m10.return_tip()

    temp_deck_1.deactivate()
    temp_deck_2.deactivate()
    protocol.comment("Yay! \ Please incubate in PCR machine \ at 20°C for 30 minutes, followed by 15 minutes at 65°C. \ Press resume when finished.")
