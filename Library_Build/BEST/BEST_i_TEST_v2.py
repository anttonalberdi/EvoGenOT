from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'BEST in PCR TEST',
    'author': 'DJ Agerbo <genomicsisawesome@gmail.com',
    'description': 'Simple protocol to BEST in OT-PCR',
    'apiLevel': '2.2'
}
###### NOTES ###########################
#Use multipipettes when possible

# Samples could be in 100 ul plate already
    - #Thermocycler lid should open after tempdeck is cooled

#Increase speed when mixing ER

# When adding ligase MM, apiration needs to be super slow and the tip should probably touch the sides of the tube

# Mix MMs before distributing to samples
#######################################
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

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
import math

def run(BEST):

    #### LABWARE SETUP ####
    # Temperature module
    temp_deck = BEST.load_module('temperature module', '4')
    Cold_plate = temp_deck.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap', label='MasterMixes')

    # PCR module
    PCR = BEST.load_module('thermocycler')
    PCR_plate = PCR.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', label='PCR Reactions')
    #Sample platee
    Sample_plate = BEST.load_labware('biorad_96_wellplate_200ul_pcr','5',label='Samples')


    #### Tipracks
    tips10 = [
        BEST.load_labware('opentrons_96_filtertiprack_10ul', slot)
        for slot in ['2','3','6']
        ]
    tips50 = [
        BEST.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['1']
        ]
    #### PIPETTE SETUP ####
    p50 = BEST.load_instrument('p50_single', mount='left', tip_racks=tips50)

    p10 = BEST.load_instrument('p10_single', mount='right', tip_racks=tips10)

    ## Enzyme SETUP
    MM_ER = Cold_plate.wells_by_name()['A1']
    MM_Lig = Cold_plate.wells_by_name()['A2']
    MM_Fill = Cold_plate.wells_by_name()['A3']
    Adapters_1 = Cold_plate.wells_by_name()['A4']
    Adapters_2 = Cold_plate.wells_by_name()['B4']
    Adapters_3 = Cold_plate.wells_by_name()['C4']
    ## Sample Setup

    samples1 = [well.bottom(1) for well in Sample_plate.columns()[0]]
    samples2 = [well.bottom(1) for well in Sample_plate.columns()[1]]
    samples3 = [well.bottom(1) for well in Sample_plate.columns()[2]]
    samples4 = [well.bottom(1) for well in Sample_plate.columns()[3]]

    PCR_rxns1 = [well.bottom(1) for well in PCR_plate.columns()[0]]
    PCR_rxns2 = [well.bottom(1) for well in PCR_plate.columns()[1]]
    PCR_rxns3 = [well.bottom(1) for well in PCR_plate.columns()[2]]
    PCR_rxns4 = [well.bottom(1) for well in PCR_plate.columns()[3]]

    PCR_rxns1_top = [well.top(-5) for well in PCR_plate.columns()[0]]
    PCR_rxns2_top = [well.top(-5) for well in PCR_plate.columns()[1]]
    PCR_rxns3_top = [well.top(-5) for well in PCR_plate.columns()[2]]
    PCR_rxns4_top = [well.top(-5) for well in PCR_plate.columns()[3]]

    ## Volume setup
    ER_vol = 8
    Lig_vol = 8
    Fill_vol = 10
    Sample_Vol = 32



    """
    Blund end repair
    """
    BEST.comment("BLUND END REPAIR will begin")
    PCR.open_lid()
    BEST.comment("Yay! Lid is open! The PCR machine will now fuck up your samples!")

    PCR.set_block_temperature(10)
    PCR.set_lid_temperature(105)
    temp_deck.set_temperature(10)

    # Set PCR profile for ER
    profile = [{'temperature': 20, 'hold_time_minutes': 30}, {'temperature': 65, 'hold_time_minutes': 30}]

    ### Addition of End repair mastermix to PCR machine
    p50.flow_rate.aspirate = 20
    p50.flow_rate.dispense = 50
    p50.pick_up_tip()
    for target in PCR_rxns1:
        p50.aspirate(ER_vol, MM_ER)
        p50.dispense(ER_vol,target)
        p50.blow_out(target)
    for target in PCR_rxns2:
        p50.aspirate(ER_vol, MM_ER)
        p50.dispense(ER_vol,target)
        p50.blow_out(target)
    for target in PCR_rxns3:
        p50.aspirate(ER_vol, MM_ER)
        p50.dispense(ER_vol,target)
        p50.blow_out(target)
    for target in PCR_rxns4:
        p50.aspirate(ER_vol, MM_ER)
        p50.dispense(ER_vol,target)
        p50.blow_out(target)
    p50.drop_tip()

    p50.flow_rate.aspirate = 20
    p50.flow_rate.dispense = 40

## Adding Sample_Volµl sample to PCR plate and mixes after

    p50.pick_up_tip()
    #Picking up tip from B1 of Opentrons 96 Tip Rack 300 µL on 1
    # Aspirating Sample_Vol.0 uL from Samples 1-8 on 5 at 1.0 speed
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['A1'].bottom(2))
    # Dispensing Sample_Vol.0 uL Samples to PCR plate in the bottom
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['A1'].bottom(2))
    # Mixing 40.0uL, three times in PCR plate in the bottom
    p50.mix(3,40,PCR_plate.wells_by_name()['A1'].bottom(3))
    # Blow out disposal volume 10 mm ABOVE the bottom of PCR well
    p50.blow_out(PCR_plate.wells_by_name()['A1'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['B1'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['B1'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['B1'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['B1'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['C1'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['C1'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['C1'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['C1'].bottom(10))
    p50.return_tip()


    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['D1'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['D1'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['D1'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['D1'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['E1'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['E1'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['E1'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['E1'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['F1'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['F1'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['F1'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['F1'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['G1'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['G1'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['G1'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['G1'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['H1'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['H1'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['H1'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['H1'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['A2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['A2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['A2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['A2'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['B2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['B2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['B2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['B2'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['C2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['C2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['C2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['C2'].bottom(10))
    p50.return_tip()


    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['D2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['D2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['D2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['D2'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['E2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['E2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['E2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['E2'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['F2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['F2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['F2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['F2'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['G2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['G2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['G2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['G2'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['H2'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['H2'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['H2'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['H2'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['A3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['A3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['A3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['A3'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['B3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['B3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['B3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['B3'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['C3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['C3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['C3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['C3'].bottom(10))
    p50.return_tip()


    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['D3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['D3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['D3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['D3'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['E3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['E3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['E3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['E3'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['F3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['F3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['F3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['F3'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['G3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['G3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['G3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['G3'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['H3'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['H3'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['H3'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['H3'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['A4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['A4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['A4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['A4'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['B4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['B4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['B4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['B4'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['C4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['C4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['C4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['C4'].bottom(10))
    p50.return_tip()


    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['D4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['D4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['D4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['D4'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['E4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['E4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['E4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['E4'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['F4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['F4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['F4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['F4'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['G4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['G4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['G4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['G4'].bottom(10))
    p50.return_tip()

    p50.pick_up_tip()
    p50.aspirate(Sample_Vol, Sample_plate.wells_by_name()['H4'].bottom(2))
    p50.dispense(Sample_Vol,PCR_plate.wells_by_name()['H4'].bottom(2))
    p50.mix(3,40,PCR_plate.wells_by_name()['H4'].bottom(3))
    p50.blow_out(PCR_plate.wells_by_name()['H4'].bottom(10))
    p50.return_tip()
    PCR.close_lid()
    ## Execute PCR profile
    PCR.execute_profile(steps=profile, repetitions=1, block_max_volume=40)
    PCR.open_lid()

    PCR.set_block_temperature(10)

    """
    Ligation of Adapters
    """

    BEST.comment("LIGATION OF ADAPTERS will begin")
# Add Adapters

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['A1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['B1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['C1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C1'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['D1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['E1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['F1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['G1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['H1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['A2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['B2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['C2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C2'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['D2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['E2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['F2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['G2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['H2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['A3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['B3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['C3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C3'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['D3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['E3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['F3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['G3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['H3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['A4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['B4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['C4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C4'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(2, Adapters_1)
    p10.dispense(2,PCR_plate.wells_by_name()['D4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['E4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_2)
    p10.dispense(2,PCR_plate.wells_by_name()['F4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['G4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(2, Adapters_3)
    p10.dispense(2,PCR_plate.wells_by_name()['H4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H4'].bottom(10))
    p10.return_tip()

# Add Ligase MM
#
    p10.flow_rate.aspirate = 5
    p10.flow_rate.dispense = 2

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['A1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['B1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['C1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C1'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['D1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['E1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['F1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['G1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['H1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['A2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['B2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['C2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C2'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['D2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['E2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['F2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['G2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['H2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['A3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['B3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['C3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['D3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['E3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['F3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['G3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['H3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['A4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['B4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['C4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C4'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['D4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['E4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['F4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['G4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Lig_vol, MM_Lig)
    p10.dispense(Lig_vol,PCR_plate.wells_by_name()['H4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H4'].bottom(10))
    p10.return_tip()

    profile = [
    {'temperature': 20, 'hold_time_minutes': 30},
    {'temperature': 65, 'hold_time_minutes': 10}]

    PCR.close_lid()
    ## Execute PCR profile
    BEST.comment("You know.. This might NOT work!")

    PCR.execute_profile(steps=profile, repetitions=1, block_max_volume=50)

    PCR.open_lid()

    PCR.set_block_temperature(10)

    # Add Fill in MM
    """
    Fill in
    """
    BEST.comment("SHIAT! FILL IN will begin")

    p10.flow_rate.aspirate = 5
    p10.flow_rate.dispense = 10
    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['A1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['B1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['C1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['D1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['E1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['F1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['G1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['H1'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H1'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H1'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['A2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['B2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['C2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['D2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['E2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['F2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['G2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['H2'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H2'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H2'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['A3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['B3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['C3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C3'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['D3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['E3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['F3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['G3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['H3'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H3'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H3'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['A4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['A4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['A4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['B4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['B4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['B4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['C4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['C4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['C4'].bottom(10))
    p10.return_tip()


    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['D4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['D4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['D4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['E4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['E4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['E4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['F4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['F4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['F4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['G4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['G4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['G4'].bottom(10))
    p10.return_tip()

    p10.pick_up_tip()
    p10.aspirate(Fill_vol, MM_Fill)
    p10.dispense(Fill_vol,PCR_plate.wells_by_name()['H4'].bottom(2))
    p10.mix(3,10,PCR_plate.wells_by_name()['H4'].bottom(3))
    p10.blow_out(PCR_plate.wells_by_name()['H4'].bottom(10))
    p10.return_tip()

    profile = [
    {'temperature': 65, 'hold_time_minutes': 15},
    {'temperature': 80, 'hold_time_minutes': 15}]

    PCR.close_lid()
        ## Execute PCR profile
    PCR.execute_profile(steps=profile, repetitions=1, block_max_volume=60)

    PCR.open_lid()

    PCR.set_block_temperature(10)

    BEST.comment("Work work work")
    BEST.comment("Job's done!")
