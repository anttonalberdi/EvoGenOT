## Description of procedure ##

### Procedure ###

######## IMPORT LIBRARIES ########
from opentrons import protocol_api

#### METADATA ####

metadata = {
    'protocolName': 'Extraction_DNA_RNA',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'update': 'Martina Cardinali <martina.cardinali.4@gmail.com>',
    'apiLevel': '2.2',
    'date': '2020/11/09',
    'description': 'Automation of D-Rex DNA protocol',
}

def run(protocol):
    #### LABWARE SETUP ####
    elution_plate_DNA = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1)
    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 2)
    trash_box = protocol.load_labware('biorad_96_wellplate_1000ul_w_adaptor', 8)
    mag_deck = protocol.load_module('magdeck', 10)
    DNA_plate = mag_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')
    # Load a Temperature Module GEN1 in deck slot 10.
    temp_deck = protocol.load_module('tempdeck', 7)
    incubation_plate = temp_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 6)
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)
    tipracks_200_5 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 11)
    tipracks_200_6 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 2)

    tipracks_10_1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 5)

    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                            tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4))
    m20 = protocol.load_instrument('p20_multi_gen2', mount='right', tip_racks=[tipracks_10_1])

    #### REAGENT SETUP                          Description             Volume needed for protocol
    EtOH1 = trough['A9']                   # 80% Ethanol           # Wash 1 11 ml
    EtOH2 = trough['A10']                   # 80% Ethanol           # Wash 2 11 ml

    Elution_buffer = trough['A12']            # EBT                   6 ml
    BufferC_1 = trough['A11']                    # Buffer C:             10.8 ml
    #BufferC_2 = trough['A6']                    # Buffer C:             10.8 ml


    #### VOLUME SETUP
    Sample_vol = 200
    Sample_buffer_vol = 2.5*Sample_vol
    BufferC_vol = 1.0*Sample_vol
    Wash_1_vol = 1.0*Sample_vol
    Wash_2_vol = 1.0*Sample_vol
    Elution_vol = 50

    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    list_of_cols = ['A1','A2','A3','A4','A5','A6']

    #### PROTOCOL ####

    ### Place DNA_plate on magnetic_deck
    mag_deck.engage(height=34)
    protocol.delay(minutes=4)
    #protocol.delay(minutes=1)

    #### Transfer remaining supernatant to trash
    for i in list_of_cols:
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(70, DNA_plate[i].bottom(1))
        m300.dispense(70, trash_box[i].top(-3))
        protocol.delay(seconds=5)
        m300.blow_out()
        m300.touch_tip(v_offset=-5, radius=0.8)
        #m300.air_gap(height=2)
        m300.return_tip()

    mag_deck.disengage()

    ## add Buffer C to beads with DNA (col 1 to 6)
    for i in list_of_cols[:6]:
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        # m300.mix(3, BufferC_vol, BufferC_1.bottom(4))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
        m300.dispense(BufferC_vol, DNA_plate[i].bottom(5))   # *2 ?? check volume
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, 170, DNA_plate[i].bottom(3))
        m300.blow_out(DNA_plate[i].bottom(10))
        protocol.delay(seconds=5)
        m300.air_gap(height=2)
        m300.return_tip()

    ## add Buffer C to beads with DNA (col 7 to 12)
    for i in list_of_cols[6:]:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(3, BufferC_vol, BufferC_2.bottom(5))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(BufferC_vol, BufferC_2.bottom(3))
        m300.dispense(BufferC_vol, DNA_plate[i].bottom(5))   # *2 ?? check volume
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, BufferC_vol, DNA_plate[i].bottom(3))
        m300.move_to(DNA_plate[i].bottom(6))
        protocol.delay(seconds=5)
        m300.blow_out(DNA_plate[i].bottom(6))
        m300.air_gap(height=2)
        m300.return_tip()

    mag_deck.engage(height=34)
    protocol.delay(minutes=4)
    #protocol.delay(minutes=1)

    ### Remove supernatant from DNA_plate to trash
    for i in list_of_cols:
        m300.flow_rate.aspirate = 25
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(125, DNA_plate[i].bottom(3))
        m300.dispense(125, trash_box[i].top(-3))
        m300.blow_out()
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.aspirate(125, DNA_plate[i].bottom(1.5))
        m300.dispense(125, trash_box[i].top(-3))
        protocol.delay(seconds=2)
        m300.flow_rate.dispense = 200
        m300.blow_out()
        m300.flow_rate.aspirate = 100
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height=2)
        m300.return_tip()

    mag_deck.disengage()

    ### Wash 1 with Ethanol, using tiprack 4
    for i in list_of_cols:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_4[i])
        m300.aspirate(Wash_1_vol, EtOH1.bottom(4))
        m300.dispense(Wash_1_vol, DNA_plate[i].top(-3))
        m300.mix(5, 170, DNA_plate[i].bottom(2))
        m300.move_to(DNA_plate[i].top(-9))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 200
        m300.blow_out()
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height=2)
        m300.return_tip()

    mag_deck.engage(height=34)
    protocol.delay(minutes=2)

    ### Remove supernatant, by re-using tiprack 4
    ### remove supernatant from DNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_4[i])
        m300.aspirate(Wash_1_vol, DNA_plate[i].bottom(0.8))
        m300.dispense(Wash_1_vol, trash_box[i].top(-4))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 200
        m300.blow_out(trash_box[i].top(-3))
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height = 2)
        m300.return_tip()

    mag_deck.disengage()

    #protocol.pause("Please substitute tip racks 1 and 2 before continuing.")
    ##Reset tipracks for more tips
    #m300.reset_tipracks()

    ## Ethanol Wash 2, by using tiprack 1
    ### Transfer Wash 2 to DNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_5[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(Wash_2_vol, EtOH2.bottom(4))
        m300.dispense(Wash_2_vol, DNA_plate[i].top(-3))
        m300.mix(5, 170, DNA_plate[i].bottom(2))
        m300.move_to(DNA_plate[i].top(-9))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out()
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height=2)
        m300.return_tip()

    mag_deck.engage(height=34)
    protocol.delay(minutes=2)

    ### Remove supernatant from DNA_plate by re-using tiprack 1
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_5[i])
        m300.aspirate(Wash_2_vol, DNA_plate[i].bottom(1))
        m300.dispense(Wash_2_vol, trash_box[i].top(-4))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 200
        m300.blow_out(trash_box[i].top(-4))
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height = 2)
        m300.return_tip()

    # Reset the tip tracker
    m300.reset_tipracks()
    protocol.pause("Substitute tiprack position 2 with new 200ul; tiprack position 5 with 20ul tips")

    ### Remove the remaining supernatant with 10ul pipette
    for i in list_of_cols:
        m20.flow_rate.aspirate = 50
        m20.flow_rate.dispense = 100
        m20.pick_up_tip(tipracks_10_1[i])
        m20.aspirate(10, DNA_plate[i].bottom(0.8))
        m20.dispense(10, trash_box[i].top(-4))
        m20.blow_out()
        m20.touch_tip(v_offset=-5, radius=0.8)
        # protocol.delay(seconds=5)
        # m20.blow_out()
        # m20.air_gap(height=2)
        m20.return_tip()

    #### Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)
    protocol.delay(minutes=2)
    mag_deck.disengage()

    ## Elution
    #### Transfer elution buffer to DNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_6[i])
        m300.aspirate(Elution_vol, Elution_buffer.bottom(3))
        m300.dispense(Elution_vol, DNA_plate[i].top(-4))
        m300.mix(5, 30, DNA_plate[i].bottom(3))
        m300.blow_out(DNA_plate[i].bottom(6))
        protocol.delay(seconds=5)
        m300.return_tip()

    temp_deck.set_temperature(25)

    #### Transfer elutes to incubation_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_6[i])
        m300.aspirate(Elution_vol, DNA_plate[i].bottom(1))
        m300.dispense(Elution_vol, incubation_plate[i].top(-4))
        protocol.delay(seconds=5)
        m300.blow_out(incubation_plate[i].bottom(6))
        m300.air_gap(height=2)
        m300.return_tip()

    protocol.delay(minutes=5)
    #protocol.delay(minutes=1)
    mag_deck.engage(height=34)

    #### Move elutes back to plate on magnetic_deck
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_6[i])
        m300.aspirate(Elution_vol, incubation_plate[i].bottom(0.8))
        m300.dispense(Elution_vol, DNA_plate[i].top(-4))
        protocol.delay(seconds=5)
        m300.blow_out(DNA_plate[i].bottom(6))
        m300.touch_tip(v_offset=-4, radius=0.8)
        m300.flow_rate.aspirate = 200
        m300.air_gap(height=2)
        m300.return_tip()

    temp_deck.deactivate()
    protocol.delay(minutes=3)

    ### Transfer elutes to elution_plate
    for i in list_of_cols:
        m300.pick_up_tip(tipracks_200_6[i])
        m300.flow_rate.aspirate = 5
        m300.flow_rate.dispense = 50
        m300.aspirate(70, DNA_plate[i].bottom(1))
        m300.dispense(70, elution_plate_DNA[i].bottom(3))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(elution_plate_DNA[i].top(-4))
        m300.return_tip()

    mag_deck.disengage()

    protocol.pause('Cover DNA plate with foil and proceed with library building or store the samples at -20°C')
