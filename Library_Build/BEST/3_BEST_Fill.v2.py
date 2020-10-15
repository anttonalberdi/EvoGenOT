###########################
###  BEST library build ###
###########################

## Description of procedure ##

# BEFORE PROTOCOL BEGINS
    # Fill in step mastex mix reagents and volumes:
    #                       1X     96(+10)X
    # Water                 5.6    593.6
    # Isothermal buffer     2      212
    # dNTP 25 mM            0.8    84.8
    # Bst 2.0 Polymerase    1.6    169.6
    # Mix                   10     1060
    # Sample                50
    # Reaction size         60
    #
# 1) Pre-mix buffers in 1.5 ml tube and distribute to Column 7 (Fill_mastermix)
#       Water                   593.6
#       Isothermal buffers      212
#       dNTP 25 mM              84.8
#       For each well           111.3
#
# 2) Pre-mix enzymes in 1.5 ml tube and distribute to Column 3 (Enzyme_Fill)
#       Bts 2.0 Polymerase      169.6
#       For each well           21.2
#
# ROBOT PROTOCOL BEGINS
#
# 3) Transfer 11.3 ul from Column 7 to Column 3 and mix
#
# 4) Distribute 10 ul to each well in the sample plate and mix thoroughly

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


    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 9)



    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi', mount='left', tip_racks=(tipracks_200_1,))

    m10 = protocol.load_instrument('p10_multi', mount='right', tip_racks=(tipracks_10_1,))

    ## Enzyme SETUP
    # Enzyme_ER = MM_plate.wells('A1')
    # Enzyme_Lig = MM_plate.wells('A2')
    Enzyme_Fill = MM_plate['A3']

    ## Reagent SETUP
    # ER_mastermix = MM_plate.wells('A4')
    # BGI_adapter = MM_plate.wells('A5')
    # Lig_mastermix = MM_plate.wells('A6')
    Fill_mastermix = MM_plate['A7']

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
    #Lig_vol = 8
    Fill_vol = 10
    #MM_dist_ER = ER_vol * col_num
    #MM_dist_Lig = Lig_vol * col_num
    MM_dist_Fill = Fill_vol * col_num

#### PROTOCOL ####
    temp_deck_1.set_temperature(10)
    temp_deck_2.set_temperature(10)

    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']

### Addition of Fill in mastermix to enzymes
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A1']) # Slow down head speed 0.5X for bead handling
    m300.move_to(Fill_mastermix.bottom())
    m300.mix(3, 50, Fill_mastermix.bottom(4))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(MM_dist_Fill, Fill_mastermix.bottom(1))
    m300.move_to(Enzyme_Fill.bottom())
    m300.dispense(MM_dist_Fill, Enzyme_Fill.bottom(2))
    m300.mix(5, 30, Enzyme_Fill.bottom(4))
    protocol.delay(seconds=3)
    m300.flow_rate.aspirate = 180
    m300.flow_rate.dispense = 180
    m300.move_to(Enzyme_Fill.top(-4))
    m300.blow_out()
    m300.return_tip()

    ### Addition of Fill in mastermix to libraries

    for i in list_of_cols:
        m10.flow_rate.aspirate = 100
        m10.flow_rate.dispense = 100
        m10.pick_up_tip(tipracks_10_1[i]) # Slow down head speed 0.5X for bead handling
        m10.mix(3, 10, Enzyme_Fill.bottom(4))
        m10.flow_rate.aspirate = 50
        m10.flow_rate.dispense = 50
        m10.aspirate(Fill_vol, Enzyme_Fill.bottom(1))
        m10.move_to(temp_plate[i].bottom())
        m10.dispense(Fill_vol, temp_plate[i].bottom(3))
        m10.flow_rate.aspirate = 20
        m10.flow_rate.dispense = 20
        m10.mix(2, 10, temp_plate[i].bottom(3))
        protocol.delay(seconds=2)
        m10.move_to(temp_plate[i].top(-4))
        m10.return_tip()

    temp_deck_1.deactivate()
    temp_deck_2.deactivate()
    protocol.comment("Yay! \ Please incubate in PCR machine \ at 65°C for 15 minutes, followed by 15 minutes at 80°C. \ Press resume when finished.")
