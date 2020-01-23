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
    trash = protocol.load_labware('agilent_1_reservoir_290ml','8') ## Need to be created
    trough = protocol.load_labware('12_column_reservoir', '10')

### Pipette tips ###

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '4')
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '5')

### Pipettes ###

    m300 = protocol.load_instrument('p300_multi', mount='left', tip_racks=(tipracks_200_1,tipracks_200_2))


###  PURIFICATION REAGENTS SETUP ###

    EtOH1 = trough['A4']
    EtOH2 = trough['A5']



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

### Notes ###


    mag_deck.engage(height=16)

    mag_deck.engage(height=17)

    mag_deck.engage(height=18)

### Wash with EtOH1 ####

    ### Transfer EtOH1 to SA1
    m300.pick_up_tip(tipracks_200_1['A7'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA1.top(-3))
    m300.air_gap(gap)
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA1.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA1.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA1.top(-10))
    m300.air_gap(gap)
    m300.return_tip()


    ### Transfer EtOH1 to SA2
    m300.pick_up_tip(tipracks_200_1['A8'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA2.top(-3))
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA2.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA2.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA2.top(-10))
    m300.touch_tip()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA3
    m300.pick_up_tip(tipracks_200_1['A9'])
    m300.move_to(EtOH1.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA3.top(-3))
    m300.aspirate(EtOH_vol, EtOH1.top(-35))
    m300.move_to(EtOH1.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA3.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA3.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA3.top(-10))
    m300.touch_tip()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA4
    m300.pick_up_tip(tipracks_200_1['A10'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA4.top(-3))
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA4.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA4.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA4.top(-10))
    m300.touch_tip()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA5
    m300.pick_up_tip(tipracks_200_1['A10'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA5.top(-3))
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA5.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA5.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA5.top(-10))
    m300.touch_tip()
    m300.air_gap(gap)
    m300.return_tip()

    ### Transfer EtOH1 to SA6
    m300.pick_up_tip(tipracks_200_1['A10'])
    m300.move_to(EtOH2.top(-16))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA6.top(-3))
    m300.aspirate(EtOH_vol, EtOH2.top(-35))
    m300.move_to(EtOH2.top(-3))
    m300.touch_tip()
    m300.dispense(EtOH_vol, SA6.top(-3))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, SA6.bottom(5))
    protocol.delay(seconds=5)
    m300.move_to(SA6.top(-10))
    m300.touch_tip()
    m300.air_gap(gap)
    m300.return_tip()
