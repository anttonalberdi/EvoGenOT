
from opentrons import protocol_api


metadata = {
    'protocolName': 'DNA Purification',
    'author': 'lasse.nyholm@sund.ku.dk',
    'apiLevel': '2.0'
    }

#
def run(protocol):

### Labware ###

    mag_deck = protocol.load_module('magdeck','7')
    sample_plate = mag_deck.load_labware('1ml_pcr')
    elution_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr','1')
    trash = protocol.load_labware('agilent_1_reservoir_290ml','8') ## Need to be created
    trough = protocol.load_labware('12_column_reservoir', '10')


### Pipette tips ###

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '4')
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '5')
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '6')


### Pipettes ###

    m300 = protocol.load_instrument('p300_multi', mount='left', tip_racks=(tipracks_200_1,tipracks_200_2,tipracks_200_3))

###  PURIFICATION REAGENTS SETUP ###

    SPRI_beads = trough['A1']
    EtOH1 = trough['A4']
    EtOH2 = trough['A5']
    EtOH3 = trough['A6']
    EtOH4 = trough['A7']
    Elution_buffer = trough['A12']
    Liquid_trash = trash['A1']

    sample_vol = 200
    bead_vol = sample_vol
    bead_vol_supernatant = 400/3
    bead_mix_vol = 100
    EtOH_vol = 150
    elution_vol = 50
    gap = 50

    #### Sample SETUP

    SA1 = sample_plate['A1']
    SA2 = sample_plate['A3']
    SA3 = sample_plate['A5']
    SA4 = sample_plate['A7']
    SA5 = sample_plate['A9']
    SA6 = sample_plate['A11']

    EA1 = elution_plate['A1']
    EA2 = elution_plate['A3']
    EA3 = elution_plate['A5']
    EA4 = elution_plate['A7']
    EA5 = elution_plate['A9']
    EA6 = elution_plate['A11']

    ### Notes ###
# Adjust ethanol workings
    # Shake tip?
    # Waiting for 5 seconds are not good

    ### Beads addition ###
    mag_deck.disengage()


    ### Transfer beads to SA1
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A1'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, SA1.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, SA1.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA1.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to SA2
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A2'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, SA2.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, SA2.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA2.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to SA3
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A3'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, SA3.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, SA3.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA3.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to SA4
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A4'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, SA4.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, SA4.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA4.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to SA5
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A5'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, SA5.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, SA5.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA5.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to SA6
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A6'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, SA6.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, SA6.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA6.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()


    #m300.delay(minutes=10)
    mag_deck.engage(height=17)
    #m300.delay(minutes=10)



    ### REMOVING SUPERNATANT ###


    ### remove supernatant from SA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A1'])
    m300.aspirate(bead_vol_supernatant, SA1.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA1.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA1.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A2'])
    m300.aspirate(bead_vol_supernatant, SA2.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA2.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA2.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from SA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A3'])
    m300.aspirate(bead_vol_supernatant, SA3.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA3.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA3.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from SA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A4'])
    m300.aspirate(bead_vol_supernatant, SA4.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA4.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA4.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from SA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A5'])
    m300.aspirate(bead_vol_supernatant, SA5.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA5.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA5.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from SA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A6'])
    m300.aspirate(bead_vol_supernatant, SA6.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA6.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, SA6.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()




    ### Wash with EtOH1 ####

    ### Transfer EtOH1 to SA1
    m300.pick_up_tip(tipracks_200_1['A7'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA1.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA1.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA1.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA1.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()


    ### Transfer EtOH1 to SA2
    m300.pick_up_tip(tipracks_200_1['A8'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA2.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA2.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA2.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA2.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA3
    m300.pick_up_tip(tipracks_200_1['A9'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA3.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA3.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA3.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA3.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA4
    m300.pick_up_tip(tipracks_200_1['A10'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA4.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA4.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA4.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA4.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA5
    m300.pick_up_tip(tipracks_200_1['A11'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA5.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA5.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA5.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA5.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA6
    m300.pick_up_tip(tipracks_200_1['A12'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA6.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA6.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA6.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA6.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()



    ### Remove wash 1 supernatant ###

    #m300.delay(minutes=2)

    ### remove supernatant from SA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A7'])
    m300.aspirate(EtOH_vol, SA1.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA1.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A8'])
    m300.aspirate(EtOH_vol, SA2.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA2.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A9'])
    m300.aspirate(EtOH_vol, SA3.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA3.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A10'])
    m300.aspirate(EtOH_vol, SA4.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA4.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A11'])
    m300.aspirate(EtOH_vol, SA5.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA5.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A12'])
    m300.aspirate(EtOH_vol, SA6.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA6.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### Wash with EtOH2 ####



    ### Transfer EtOH2 to SA1
    m300.pick_up_tip(tipracks_200_2['A1'])
    m300.move_to(EtOH3.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA1.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA1.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA1.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA1.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to SA2
    m300.pick_up_tip(tipracks_200_2['A2'])
    m300.move_to(EtOH3.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA2.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA2.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA2.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA2.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to SA3
    m300.pick_up_tip(tipracks_200_2['A3'])
    m300.move_to(EtOH3.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA3.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA3.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA3.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA3.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to SA4
    m300.pick_up_tip(tipracks_200_2['A4'])
    m300.move_to(EtOH4.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA4.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA4.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA4.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA4.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to SA5
    m300.pick_up_tip(tipracks_200_2['A5'])
    m300.move_to(EtOH4.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA5.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA5.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA5.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA5.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to SA6
    m300.pick_up_tip(tipracks_200_2['A6'])
    m300.move_to(EtOH4.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA6.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, SA6.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA6.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA6.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()


    ### Remove wash 2 supernatant ###

    #m300.delay(minutes=2)

    ### remove supernatant from SA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A1'])
    m300.aspirate(EtOH_vol, SA1.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA1.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A2'])
    m300.aspirate(EtOH_vol, SA2.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA2.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A3'])
    m300.aspirate(EtOH_vol, SA3.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA3.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A4'])
    m300.aspirate(EtOH_vol, SA4.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA4.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A5'])
    m300.aspirate(EtOH_vol, SA5.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA5.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from SA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A6'])
    m300.aspirate(EtOH_vol, SA6.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, SA6.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### Removing last bit of ethanol ####


    ### remove supernatant from SA1
    #m10.set_flow_rate(aspirate=100, dispense=100)
    #m10.pick_up_tip(tipracks_10_1.wells('A1'))
    #m10.aspirate(10, SA1.bottom(0.5))
    #m10.return_tip()

    ### remove supernatant from SA2
    #m10.set_flow_rate(aspirate=100, dispense=100)
    #m10.pick_up_tip(tipracks_10_1.wells('A2'))
    #m10.aspirate(10, SA2.bottom(0.5))
    #m10.return_tip()

    ### remove supernatant from SA3
    #m10.set_flow_rate(aspirate=100, dispense=100)
    #m10.pick_up_tip(tipracks_10_1.wells('A3'))
    #m10.aspirate(10, SA3.bottom(0.5))
    #m10.return_tip()

    ### remove supernatant from SA4
    #m10.set_flow_rate(aspirate=100, dispense=100)
    #m10.pick_up_tip(tipracks_10_1.wells('A4'))
    #m10.aspirate(10, SA4.bottom(0.5))
    #m10.return_tip()

    ### remove supernatant from SA5
    #m10.set_flow_rate(aspirate=100, dispense=100)
    #m10.pick_up_tip(tipracks_10_1.wells('A5'))
    #m10.aspirate(10, SA5.bottom(0.5))
    #m10.return_tip()

    ### remove supernatant from SA6
    #m10.set_flow_rate(aspirate=100, dispense=100)
    #m10.pick_up_tip(tipracks_10_1.wells('A6'))
    #m10.aspirate(10, SA6.bottom(0.5))
    #m10.return_tip()


    ### Drying beads before elution ####

    mag_deck.disengage()

### Transfer Elution buffer to SA1
    m300.pick_up_tip(tipracks_200_2['A7'])
    m300.move_to(Elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, Elution_buffer.top(-35))
    m300.dispense(elution_vol, SA1.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, SA1.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA1.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to SA2
    m300.pick_up_tip(tipracks_200_2['A8'])
    m300.move_to(Elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, Elution_buffer.top(-35))
    m300.dispense(elution_vol, SA2.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, SA2.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA2.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to SA3
    m300.pick_up_tip(tipracks_200_2['A9'])
    m300.move_to(Elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, Elution_buffer.top(-35))
    m300.dispense(elution_vol, SA3.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, SA3.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA3.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to SA4
    m300.pick_up_tip(tipracks_200_2['A10'])
    m300.move_to(Elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, Elution_buffer.top(-35))
    m300.dispense(elution_vol, SA4.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, SA4.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA4.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to SA5
    m300.pick_up_tip(tipracks_200_2['A11'])
    m300.move_to(Elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, Elution_buffer.top(-35))
    m300.dispense(elution_vol, SA5.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, SA5.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA5.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to SA6
    m300.pick_up_tip(tipracks_200_2['A12'])
    m300.move_to(Elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, Elution_buffer.top(-35))
    m300.dispense(elution_vol, SA6.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, SA6.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(SA6.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Incubating beads with elution buffer
#m300.delay(minutes=10)
    mag_deck.engage(height=17)

# m300.delay(minutes=10)

### Transfer Elution buffer to EA1
    m300.pick_up_tip(tipracks_200_3['A1'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, SA1.bottom())
    m300.dispense(elution_vol, EA1.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EA1.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to EA2
    m300.pick_up_tip(tipracks_200_3['A2'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, SA2.bottom())
    m300.dispense(elution_vol, EA2.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EA2.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to EA3
    m300.pick_up_tip(tipracks_200_3['A3'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, SA3.bottom())
    m300.dispense(elution_vol, EA3.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EA3.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to EA4
    m300.pick_up_tip(tipracks_200_3['A4'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, SA4.bottom())
    m300.dispense(elution_vol, EA4.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EA4.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to EA5
    m300.pick_up_tip(tipracks_200_3['A5'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, SA5.bottom())
    m300.dispense(elution_vol, EA5.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EA5.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer Elution buffer to EA6
    m300.pick_up_tip(tipracks_200_3['A6'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, SA6.bottom())
    m300.dispense(elution_vol, EA6.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EA6.top(-10))
    m300.blow_out()
    m300.return_tip()

### Get last bit of elution buffer ### This step increases the chance of getting beads in final extract, but increases the volume of extract

### Transfer Elution buffer to EA1
#m10.pick_up_tip(tipracks_10_1.wells('A7'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, SA1.bottom())
#m10.dispense(10, EA1.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer Elution buffer to EA2
#m10.pick_up_tip(tipracks_10_1.wells('A8'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, SA2.bottom())
#m10.dispense(10, EA2.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer Elution buffer to EA3
#m10.pick_up_tip(tipracks_10_1.wells('A9'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, SA3.bottom())
#m10.dispense(10, EA3.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer Elution buffer to EA4
#m10.pick_up_tip(tipracks_10_1.wells('A10'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, SA4.bottom())
#m10.dispense(10, EA4.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer Elution buffer to EA5
#m10.pick_up_tip(tipracks_10_1.wells('A11'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, SA5.bottom())
#m10.dispense(10, EA5.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer Elution buffer to EA6
#m10.pick_up_tip(tipracks_10_1.wells('A12'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, SA6.bottom())
#m10.dispense(10, EA6.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

    mag_deck.disengage()




    protocol.pause("Yay! \ Purification has finished \ Please store purified samples as -20°C \ Press resume when finished.")
