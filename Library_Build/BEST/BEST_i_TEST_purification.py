from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'BEST in PCR TEST',
    'author': 'DJ Agerbo <genomicsisawesome@gmail.com',
    'description': 'Simple protocol to BEST in OT-PCR',
    'apiLevel': '2.2'
}

#######################################
### BEST Library build Purification ###
#######################################

## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Ensure samples are room temperature and place libraries in magnetic module
# 	2. Ensure SPRI beads are room temperature
#   3. Make freshly made 80% Ethanol for purification
#   4. Distribute:
#                   SPRI beads to Column 1,
#                   Ethanol to Column 2 and 3
#                   Elution Buffer to Column 12
#
# Procedure
#
#		Purification
# 	1.	Distribute 1.5x beads to library and mixes
#	2.	Removes supernatant and adds ethanol for washing, washing will be processed twice
#   3.  Beads will air dry for 4 minutes and 35µl elution buffer will be added
#	4.	Elutes will incubate for 15 minutes at room temperature and be eluted to a new plate in slot 1
#
#	Good Luck!
#
######## IMPORT LIBRARIES ########
# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
import math

def run(BEST):

    #### LABWARE SETUP ####
    # Magnetic module
    Mag_deck = BEST.load_module('magdeck', '4')
    Sample_plate = Mag_deck.load_labware('biorad_96_wellplate_200ul_pcr',label='Samples on MagDeck')

    # others
    PCR_plate = BEST.load_labware('nest_96_wellplate_100ul_pcr_full_skirt','5', label='Non purified BEST libraries')
    trough = BEST.load_labware('usascientific_12_reservoir_22ml', '7', label='Purification reagents')
    trash_box = BEST.load_labware('agilent_1_reservoir_290ml', '8', label='liquid trash')
    elution_plate = BEST.load_labware('biorad_96_wellplate_200ul_pcr','3', label='Purified BEST libraries')
    #### Tipracks
    tipracks_300_1 = BEST.load_labware('opentrons_96_tiprack_300ul', '1')
    tipracks_300_2 = BEST.load_labware('opentrons_96_tiprack_300ul', '2')

    #### PIPETTE SETUP ####
    p50 = BEST.load_instrument('p50_single', mount='right', tip_racks=[tipracks_300_2])

    m300 = BEST.load_instrument('p300_multi', mount='left', tip_racks=[tipracks_300_1, tipracks_300_2])

    ## Reagent SETUP
    Beads = trough.wells_by_name()['A1']
    EtOH1 = trough.wells_by_name()['A2']
    EtOH2 = trough.wells_by_name()['A3']
    TE = trough.wells_by_name()['A4']
    ## Sample Setup

    samples1 = [well.bottom(1) for well in Sample_plate.columns()[0]]
    samples2 = [well.bottom(1) for well in Sample_plate.columns()[1]]
    samples3 = [well.bottom(1) for well in Sample_plate.columns()[2]]
    samples4 = [well.bottom(1) for well in Sample_plate.columns()[3]]

    TE1 = [well.bottom(1) for well in elution_plate.columns()[0]]
    TE2 = [well.bottom(1) for well in elution_plate.columns()[1]]
    TE3 = [well.bottom(1) for well in elution_plate.columns()[2]]
    TE4 = [well.bottom(1) for well in elution_plate.columns()[3]]

    ## Volume setup
    Sample_vol = 60
    Bead_Vol = Sample_vol * 1.6
    EtOH_vol1 = Sample_vol * 2.5
    EtOH_vol2 = Sample_vol * 2.2
    TE_vol = 30


    ### Addition of beads to empty mag plate
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 150
    m300.pick_up_tip()
    Mag_deck.disengage()

    m300.mix(10,200,trough.wells_by_name()['A1'].bottom(5))
    m300.aspirate(Bead_Vol, Beads)
    m300.dispense(Bead_Vol,Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A1'].top(-5))

    m300.aspirate(Bead_Vol, Beads)
    m300.dispense(Bead_Vol,Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A2'].top(-5))

    m300.aspirate(Bead_Vol, Beads)
    m300.dispense(Bead_Vol,Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A3'].top(-5))

    m300.aspirate(Bead_Vol, Beads)
    m300.dispense(Bead_Vol,Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A4'].top(-5))
    m300.drop_tip()

    ### Transfering samples to mag plate containing bead and mix samples
    #Column 1
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300
    m300.pick_up_tip()
    m300.aspirate(Sample_vol, PCR_plate.wells_by_name()['A1'].bottom(1))
    m300.dispense(Sample_vol,Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 200
    m300.mix(3,100,Sample_plate.wells_by_name()['A1'].bottom(5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(Sample_plate.wells_by_name()['A1'].top(-5))
    m300.return_tip()

    #Column 2
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300
    m300.pick_up_tip()
    m300.aspirate(Sample_vol, PCR_plate.wells_by_name()['A2'].bottom(1))
    m300.dispense(Sample_vol,Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 200
    m300.mix(3,100,Sample_plate.wells_by_name()['A2'].bottom(5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(Sample_plate.wells_by_name()['A2'].top(-5))
    m300.return_tip()

    #Column 3
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300
    m300.pick_up_tip()
    m300.aspirate(Sample_vol, PCR_plate.wells_by_name()['A3'].bottom(1))
    m300.dispense(Sample_vol,Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 200
    m300.mix(3,100,Sample_plate.wells_by_name()['A3'].bottom(5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(Sample_plate.wells_by_name()['A3'].top(-5))
    m300.return_tip()

    #Column 4
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300
    m300.pick_up_tip()
    m300.aspirate(Sample_vol, PCR_plate.wells_by_name()['A4'].bottom(1))
    m300.dispense(Sample_vol,Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 200
    m300.mix(3,100,Sample_plate.wells_by_name()['A4'].bottom(5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(Sample_plate.wells_by_name()['A4'].top(-5))
    m300.return_tip()

    BEST.delay(minutes=5)
    ### Transfering supernatant from mag plate to liquid trash
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 150
    Mag_deck.engage()
    #Column 1
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A2'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 2
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A3'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 3
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A4'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 4
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A5'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    ### Start first wash with EtOH
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300

    Mag_deck.disengage()
    m300.pick_up_tip()
    m300.aspirate(EtOH_vol1,EtOH1)
    m300.dispense(EtOH_vol1, Sample_plate.wells_by_name()['A1'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(EtOH_vol1,EtOH1)
    m300.dispense(EtOH_vol1, Sample_plate.wells_by_name()['A2'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(EtOH_vol1,EtOH1)
    m300.dispense(EtOH_vol1, Sample_plate.wells_by_name()['A3'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(EtOH_vol1,EtOH1)
    m300.dispense(EtOH_vol1, Sample_plate.wells_by_name()['A4'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.return_tip()

    ### Transfering supernatant from mag plate to liquid trash
    Mag_deck.engage()
    BEST.delay(minutes=1)
    #Column 1
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A6'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 2
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A7'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 3
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A8'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 4
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A9'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()


    ### Start second wash with EtOH
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300

    Mag_deck.disengage()
    m300.pick_up_tip()
    m300.aspirate(EtOH_vol2,EtOH2)
    m300.dispense(EtOH_vol2, Sample_plate.wells_by_name()['A1'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(EtOH_vol2,EtOH2)
    m300.dispense(EtOH_vol2, Sample_plate.wells_by_name()['A2'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(EtOH_vol2,EtOH2)
    m300.dispense(EtOH_vol2, Sample_plate.wells_by_name()['A3'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(EtOH_vol2,EtOH2)
    m300.dispense(EtOH_vol2, Sample_plate.wells_by_name()['A4'].bottom(2))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.mix(3,100,Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.blow_out(Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.return_tip()

    ### Transfering supernatant from mag plate to liquid trash
    Mag_deck.engage()
    BEST.delay(minutes=1)
    #Column 1
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A10'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 2
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A11'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 3
    m300.pick_up_tip(tipracks_300_1.wells_by_name()['A12'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    #Column 4
    m300.pick_up_tip(tipracks_300_2.wells_by_name()['A1'])
    m300.aspirate(200, Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.dispense(200, trash_box['A1'].top(-5))
    # Blow out disposal volume 5 mm below the top of PCR well
    m300.blow_out(trash_box['A1'])
    m300.return_tip()

    ### Start drying of beads before elution
    Mag_deck.disengage()
    BEST.delay(minutes=3)

    ### Adding elution buffer
    m300.pick_up_tip()
    m300.aspirate(TE_vol, TE)
    m300.dispense(TE_vol,Sample_plate.wells_by_name()['A1'].bottom(2))
    m300.mix(3,30,Sample_plate.wells_by_name()['A1'].bottom(3))
    m300.blow_out(Sample_plate.wells_by_name()['A1'].bottom(4))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(TE_vol, TE)
    m300.dispense(TE_vol,Sample_plate.wells_by_name()['A2'].bottom(2))
    m300.mix(3,30,Sample_plate.wells_by_name()['A2'].bottom(3))
    m300.blow_out(Sample_plate.wells_by_name()['A2'].bottom(4))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(TE_vol, TE)
    m300.dispense(TE_vol,Sample_plate.wells_by_name()['A3'].bottom(2))
    m300.mix(3,30,Sample_plate.wells_by_name()['A3'].bottom(3))
    m300.blow_out(Sample_plate.wells_by_name()['A3'].bottom(4))
    m300.return_tip()

    m300.pick_up_tip()
    m300.aspirate(TE_vol, TE)
    m300.dispense(TE_vol,Sample_plate.wells_by_name()['A4'].bottom(2))
    m300.mix(3,30,Sample_plate.wells_by_name()['A4'].bottom(3))
    m300.blow_out(Sample_plate.wells_by_name()['A4'].bottom(4))
    m300.return_tip()

    ### Incubate beads in 15 minutes and mix them every fifth minute
    BEST.delay(minutes=4, seconds=30)
    m300.pick_up_tip(tipracks_300_2.wells_by_name()['A2'])
    m300.mix(5,30,Sample_plate.wells_by_name()['A1'].bottom(3))
    m300.return_tip()

    m300.pick_up_tip(tipracks_300_2.wells_by_name()['A3'])
    m300.mix(5,30,Sample_plate.wells_by_name()['A2'].bottom(3))
    m300.return_tip()

    m300.pick_up_tip(tipracks_300_2.wells_by_name()['A4'])
    m300.mix(4,30,Sample_plate.wells_by_name()['A3'].bottom(3))
    m300.return_tip()

    m300.pick_up_tip(tipracks_300_2.wells_by_name()['A5'])
    m300.mix(4,30,Sample_plate.wells_by_name()['A4'].bottom(3))
    m300.return_tip()
