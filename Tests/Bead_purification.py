
from opentrons import protocol_api

## NOTES add air gap after dispensing sample

metadata = {
    'protocolName': 'DNA Purification',
    'author': 'lasse.nyholm@sund.ku.dk',
    'apiLevel': '2.0'
    }

#
def run(protocol):

### Labware ###

    mag_deck = protocol.load_module('magdeck','7')
    mag_plate = mag_deck.load_labware('1ml_pcr')
    sample_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr','1')
    elution_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr','3')
    trash = protocol.load_labware('agilent_1_reservoir_290ml','10') ## Need to be crELted
    trough = protocol.load_labware('12_column_reservoir', '4')


### Pipette tips ###

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '11')
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '8')
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '5')
    tipracks_10_1 = protocol.load_labware('opentrons_96_filtertiprack_10ul', '2')


### Pipettes ###

    m300 = protocol.load_instrument('p300_multi', mount='left', tip_racks=(tipracks_200_1,tipracks_200_2,tipracks_200_3))

    m10 = protocol.load_instrument('p10_multi', mount='right', tip_racks=(tipracks_10_1,))

###  PURIFICATION RELGENTS SETUP ###

    SPRI_beads = trough['A1']
    EtOH1 = trough['A4']
    EtOH2 = trough['A5']
    EtOH3 = trough['A6']
    EtOH4 = trough['A7']
    elution_buffer = trough['A12']
    Liquid_trash = trash['A1']

### Volumes (can be modified to fit protocol) ###

    sample_vol = 200
    bead_vol = sample_vol
    bead_vol_supernatant = 400/3
    bead_mix_vol = 100
    EtOH_vol = 150
    elution_vol = 50
    gap = 50

    #### Sample SETUP


    SA1 = sample_plate['A1']
    SA2 = sample_plate['A2']
    SA3 = sample_plate['A3']
    SA4 = sample_plate['A4']
    SA5 = sample_plate['A5']
    SA6 = sample_plate['A6']

    MA1 = mag_plate['A1']
    MA2 = mag_plate['A3']
    MA3 = mag_plate['A5']
    MA4 = mag_plate['A7']
    MA5 = mag_plate['A9']
    MA6 = mag_plate['A11']

    EL1 = elution_plate['A1']
    EL2 = elution_plate['A2']
    EL3 = elution_plate['A3']
    EL4 = elution_plate['A4']
    EL5 = elution_plate['A5']
    EL6 = elution_plate['A6']




    ### Notes ###



    ### Transfer samples to mag_plate ###
    mag_deck.disengage()

    ### Transfer sample to MA1
    m300.pick_up_tip(tipracks_200_1['A1'])
    m300.aspirate(sample_vol, SA1.bottom(1))
    m300.dispense(sample_vol, MA1.top(-4))
    m300.return_tip()

    ### Transfer sample to MA2
    m300.pick_up_tip(tipracks_200_1['A2'])
    m300.aspirate(sample_vol, SA2.bottom(1))
    m300.dispense(sample_vol, MA2.top(-4))
    m300.return_tip()

    ### Transfer sample to MA3
    m300.pick_up_tip(tipracks_200_1['A3'])
    m300.aspirate(sample_vol, SA3.bottom(1))
    m300.dispense(sample_vol, MA3.top(-4))
    m300.return_tip()

    ### Transfer sample to MA4
    m300.pick_up_tip(tipracks_200_1['A4'])
    m300.aspirate(sample_vol, SA4.bottom(1))
    m300.dispense(sample_vol, MA4.top(-4))
    m300.return_tip()

    ### Transfer sample to MA5
    m300.pick_up_tip(tipracks_200_1['A5'])
    m300.aspirate(sample_vol, SA5.bottom(1))
    m300.dispense(sample_vol, MA5.top(-4))
    m300.return_tip()

    ### Transfer sample to MA6
    m300.pick_up_tip(tipracks_200_1['A6'])
    m300.aspirate(sample_vol, SA6.bottom(1))
    m300.dispense(sample_vol, MA6.top(-4))
    m300.return_tip()

    protocol.pause("Make sure all sample is transferred, remove sample plate and press resume.")

    ### beads addition ###


    ### Transfer beads to MA1
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A7'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, MA1.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, MA1.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA1.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to MA2
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A8'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, MA2.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, MA2.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA2.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to MA3
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A9'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, MA3.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, MA3.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA3.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to MA4
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A10'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, MA4.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, MA4.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA4.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to MA5
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A11'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, MA5.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, MA5.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA5.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer beads to MA6
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 200
    m300.pick_up_tip(tipracks_200_1['A12'])
    m300.move_to(SPRI_beads.top(-16))
    m300.mix(7, 200, SPRI_beads.top(-30))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 40
    m300.aspirate(bead_vol, SPRI_beads.top(-35))
    m300.move_to(SPRI_beads.top(-5))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(bead_vol, MA6.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_mix_vol, MA6.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA6.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()


    #m300.delay(minutes=10)
    mag_deck.engage(height=17)
    #m300.delay(minutes=10)



    ### REMOVING SUPERNATANT ###


    ### remove supernatant from MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A7'])
    m300.aspirate(bead_vol_supernatant, MA1.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA1.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA1.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A8'])
    m300.aspirate(bead_vol_supernatant, MA2.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA2.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA2.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A9'])
    m300.aspirate(bead_vol_supernatant, MA3.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA3.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA3.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A10'])
    m300.aspirate(bead_vol_supernatant, MA4.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA4.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA4.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A11'])
    m300.aspirate(bead_vol_supernatant, MA5.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA5.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA5.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### remove supernatant from MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A12'])
    m300.aspirate(bead_vol_supernatant, MA6.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA6.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.aspirate(bead_vol_supernatant, MA6.bottom(1))
    m300.dispense(bead_vol_supernatant, Liquid_trash.top(-5))
    m300.blow_out(Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()




    ### Wash with EtOH1 ####

    ### Transfer EtOH1 to MA1
    m300.pick_up_tip(tipracks_200_2['A1'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA1.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA1.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA1.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA1.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()


    ### Transfer EtOH1 to MA2
    m300.pick_up_tip(tipracks_200_2['A2'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA2.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA2.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA2.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA2.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to MA3
    m300.pick_up_tip(tipracks_200_2['A3'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA3.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA3.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA3.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA3.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to MA4
    m300.pick_up_tip(tipracks_200_2['A4'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA4.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA4.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA4.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA4.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to MA5
    m300.pick_up_tip(tipracks_200_2['A5'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA5.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA5.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA5.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA5.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to MA6
    m300.pick_up_tip(tipracks_200_2['A6'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA6.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA6.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA6.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA6.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()



    ### Remove wash 1 supernatant ###

    #m300.delay(minutes=2)

    ### remove supernatant from MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A1'])
    m300.aspirate(EtOH_vol, MA1.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA1.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A2'])
    m300.aspirate(EtOH_vol, MA2.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA2.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A3'])
    m300.aspirate(EtOH_vol, MA3.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA3.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A4'])
    m300.aspirate(EtOH_vol, MA4.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA4.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A5'])
    m300.aspirate(EtOH_vol, MA5.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA5.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A6'])
    m300.aspirate(EtOH_vol, MA6.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA6.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### Wash with EtOH2 ####



    ### Transfer EtOH2 to MA1
    m300.pick_up_tip(tipracks_200_2['A7'])
    m300.move_to(EtOH3.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA1.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA1.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA1.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA1.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to MA2
    m300.pick_up_tip(tipracks_200_2['A8'])
    m300.move_to(EtOH3.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA2.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA2.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA2.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA2.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to MA3
    m300.pick_up_tip(tipracks_200_2['A9'])
    m300.move_to(EtOH3.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA3.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH3.top(-35))
    m300.move_to(EtOH3.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA3.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA3.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA3.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to MA4
    m300.pick_up_tip(tipracks_200_2['A10'])
    m300.move_to(EtOH4.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA4.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA4.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA4.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA4.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to MA5
    m300.pick_up_tip(tipracks_200_2['A11'])
    m300.move_to(EtOH4.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA5.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA5.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA5.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA5.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH2 to MA6
    m300.pick_up_tip(tipracks_200_2['A12'])
    m300.move_to(EtOH4.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA6.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH4.top(-35))
    m300.move_to(EtOH4.top(-3))
    protocol.delay(seconds=5)
    m300.touch_tip(v_offset=-2) # touch tip 2mm below the top of the current location
    m300.dispense(EtOH_vol, MA6.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA6.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(MA6.top(-10))
    m300.blow_out()
    m300.air_gap(gap)
    m300.return_tip()


    ### Remove wash 2 supernatant ###

    #m300.delay(minutes=2)

    ### remove supernatant from MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A7'])
    m300.aspirate(EtOH_vol, MA1.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA1.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A8'])
    m300.aspirate(EtOH_vol, MA2.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA2.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A9'])
    m300.aspirate(EtOH_vol, MA3.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA3.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A10'])
    m300.aspirate(EtOH_vol, MA4.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA4.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A11'])
    m300.aspirate(EtOH_vol, MA5.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA5.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()

    ### remove supernatant from MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A12'])
    m300.aspirate(EtOH_vol, MA6.bottom(1))
    m300.dispense(EtOH_vol, Liquid_trash.top(-5))
    protocol.delay(seconds=5)
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, MA6.bottom(1))
    m300.dispense(200, Liquid_trash.top(-5))
    m300.air_gap(gap)
    m300.return_tip()


    ### Removing last bit of ethanol ####


    ### remove supernatant from MA1
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.pick_up_tip(tipracks_10_1['A1'])
    m10.aspirate(10, MA1.bottom(0.5))
    m10.return_tip()

    ### remove supernatant from MA2
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.pick_up_tip(tipracks_10_1['A2'])
    m10.aspirate(10, MA2.bottom(0.5))
    m10.return_tip()

    ### remove supernatant from MA3
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.pick_up_tip(tipracks_10_1['A3'])
    m10.aspirate(10, MA3.bottom(0.5))
    m10.return_tip()

    ### remove supernatant from MA4
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.pick_up_tip(tipracks_10_1['A4'])
    m10.aspirate(10, MA4.bottom(0.5))
    m10.return_tip()

    ### remove supernatant from MA5
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.pick_up_tip(tipracks_10_1['A5'])
    m10.aspirate(10, MA5.bottom(0.5))
    m10.return_tip()

    ### remove supernatant from MA6
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.pick_up_tip(tipracks_10_1['A6'])
    m10.aspirate(10, MA6.bottom(0.5))
    m10.return_tip()


    ### Drying beads before elution ####
    mag_deck.disengage()
    #mprotocol.delay(minutes=10)

    protocol.pause("Make sure all ethanol is removed, add elution plate and press resume.")


### Transfer elution buffer to MA1
    m300.pick_up_tip(tipracks_200_3['A1'])
    m300.move_to(elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, elution_buffer.top(-35))
    m300.dispense(elution_vol, MA1.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, MA1.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA1.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to MA2
    m300.pick_up_tip(tipracks_200_3['A2'])
    m300.move_to(elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, elution_buffer.top(-35))
    m300.dispense(elution_vol, MA2.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, MA2.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA2.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to MA3
    m300.pick_up_tip(tipracks_200_3['A3'])
    m300.move_to(elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, elution_buffer.top(-35))
    m300.dispense(elution_vol, MA3.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, MA3.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA3.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to MA4
    m300.pick_up_tip(tipracks_200_3['A4'])
    m300.move_to(elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, elution_buffer.top(-35))
    m300.dispense(elution_vol, MA4.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, MA4.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA4.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to MA5
    m300.pick_up_tip(tipracks_200_3['A5'])
    m300.move_to(elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, elution_buffer.top(-35))
    m300.dispense(elution_vol, MA5.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, MA5.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA5.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to MA6
    m300.pick_up_tip(tipracks_200_3['A6'])
    m300.move_to(elution_buffer.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, elution_buffer.top(-35))
    m300.dispense(elution_vol, MA6.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, elution_vol, MA6.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA6.bottom(10))
    m300.blow_out()
    m300.return_tip()

### Incubating beads with elution buffer
#m300.delay(minutes=10)
    mag_deck.engage(height=17)

# m300.delay(minutes=10)

### Transfer elution buffer to EL1
    m300.pick_up_tip(tipracks_200_3['A7'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, MA1.bottom())
    m300.dispense(elution_vol, EL1.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EL1.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to EL2
    m300.pick_up_tip(tipracks_200_3['A8'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, MA2.bottom())
    m300.dispense(elution_vol, EL2.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EL2.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to EL3
    m300.pick_up_tip(tipracks_200_3['A9'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, MA3.bottom())
    m300.dispense(elution_vol, EL3.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EL3.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to EL4
    m300.pick_up_tip(tipracks_200_3['A10'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, MA4.bottom())
    m300.dispense(elution_vol, EL4.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EL4.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to EL5
    m300.pick_up_tip(tipracks_200_3['A11'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, MA5.bottom())
    m300.dispense(elution_vol, EL5.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EL5.top(-10))
    m300.blow_out()
    m300.return_tip()

### Transfer elution buffer to EL6
    m300.pick_up_tip(tipracks_200_3['A12'])
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(elution_vol, MA6.bottom())
    m300.dispense(elution_vol, EL6.bottom(2))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(EL6.top(-10))
    m300.blow_out()
    m300.return_tip()

### Get last bit of elution buffer ### This step incrELses the chance of getting beads in final extract, but incrELses the volume of extract

### Transfer elution buffer to EL1
#m10.pick_up_tip(tipracks_10_1.wells('A7'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, MA1.bottom())
#m10.dispense(10, EL1.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer elution buffer to EL2
#m10.pick_up_tip(tipracks_10_1.wells('A8'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, MA2.bottom())
#m10.dispense(10, EL2.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer elution buffer to EL3
#m10.pick_up_tip(tipracks_10_1.wells('A9'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, MA3.bottom())
#m10.dispense(10, EL3.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer elution buffer to EL4
#m10.pick_up_tip(tipracks_10_1.wells('A10'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, MA4.bottom())
#m10.dispense(10, EL4.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer elution buffer to EL5
#m10.pick_up_tip(tipracks_10_1.wells('A11'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, MA5.bottom())
#m10.dispense(10, EL5.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

### Transfer elution buffer to EL6
#m10.pick_up_tip(tipracks_10_1.wells('A12'))
#m10.set_flow_rate(aspirate=25, dispense=25)
#m10.aspirate(10, MA6.bottom())
#m10.dispense(10, EL6.bottom(2))
#m10.delay(seconds=5)
#m10.set_flow_rate(aspirate=130, dispense=130)
#m10.return_tip()

    mag_deck.disengage()




    protocol.pause("Yay! \ Purification has finished \ PlELse store purified samples as -20°C \ Press resume when finished.")
