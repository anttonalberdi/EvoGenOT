## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Bead beat samples at maximum speed for 5 minutes (If needed do Proteinase K for digestion of tissue)
# 	2. Spin down samples 10.000 rpm for 1 minute
#	3. Transfer 200µl lysed sample to a deep well plate

### Procedure ###


######## IMPORT LIBRARIES ########
from opentrons import protocol_api

#### METADATA ####

metadata = {
    'protocolName': 'D-Rex RNA Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'update': 'Martina Cardinali <martina.cardinali.4@gmail.com>',
    'apiLevel': '2.2',
    'date': '2021/08/23',
    'description': 'Automation of D-Rex RNA protocol for stool samples in SHIELD',
}

def run(protocol):
    #### LABWARE SETUP ####
    elution_plate_RNA = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1)
    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 2)
    mag_deck = protocol.load_module('magdeck', 10)
    RNA_plate = mag_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')
    trash_box = protocol.load_labware('biorad_96_wellplate_1000ul_w_adaptor', 4)
    #EtOH_wash = protocol.load_labware('agilent_1_reservoir_290ml', 6)
    # Load a Temperature Module GEN1 in deck slot 7.
    temp_deck = protocol.load_module('tempdeck', 7)
    incubation_plate = temp_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 8)
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 9)
    tipracks_200_4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)
    tipracks_10_1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 6)


    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                        tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4))
    m20 = protocol.load_instrument('p20_multi_gen2', mount='right', tip_racks=[tipracks_10_1])

    #### REAGENT SETUP 1                           Description             Volume needed for protocol
    #EtOH1 = EtOH_wash['A1']                # 80% ethanol           88 ml in tot, but I would add 44 + 44

    #### REAGENT SETUP                             Description             Volume needed for protocol
    DNase = trough['A6']                    # DNase Buffer                          3.3 ml
    BufferC_1 = trough['A7']                # Buffer C RNA rebind                   11 ml
    # BufferC_2 = trough['A7']                # Buffer C RNA rebind                 11 ml -> to use only if running full plate
    Elution_buffer = trough['A8']           # Buffer D                              5.5 ml
    EtOH1 = trough['A4']                    # Wash 1 and 3 (to refill for the 3)    11 ml
    EtOH2 = trough['A5']                    # Wash 2 and 4 (to refill for the 4)    11 ml
    # necessity to add other 2 EtOH columns if running full plate

    #### Plate SETUP for Purification
    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    list_of_cols = ['A1','A2','A3','A4','A5','A6']

    #### VOLUME SETUP
    Sample_vol = 200
    EtOH_vol = 2.0*Sample_vol
    Wash_1_vol = 1.0*Sample_vol
    Wash_2_vol = 1.0*Sample_vol
    Elution_vol = 50
    BufferC_vol = 1.0*Sample_vol

    ## Place RNA_plate with DNAse just added on the temp_deck
    temp_deck.set_temperature(25)
    protocol.delay(minutes=10)
    #protocol.delay(minutes=1) # used for testing, while commenting the real waiting time

    ### Buffer C rebind, by using tiprack 1
    ### Transfer buffer C and beads to RNA_plate(incubation_plate)
    for i in list_of_cols[:6]:
        m300.pick_up_tip(tipracks_200_1[i])
        # m300.mix(3, BufferC_vol, BufferC_1.bottom(4))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(BufferC_vol, BufferC_1.bottom(3))
        m300.dispense(BufferC_vol, incubation_plate[i].bottom(4))
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.mix(5, BufferC_vol, incubation_plate[i].bottom(2))
        m300.blow_out(incubation_plate[i].bottom(10))
        protocol.delay(seconds=5)
        m300.air_gap(height=2)
        m300.return_tip()

    ### Transfer buffer C and beads to RNA_plate
    for i in list_of_cols[6:]:
        m300.pick_up_tip(tipracks_200_1[i])
        #m300.mix(3, BufferC_vol, BufferC_2.bottom(3))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
        m300.dispense(BufferC_vol, incubation_plate[i].bottom(4))
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.mix(5, BufferC_vol, incubation_plate[i].bottom(2))
        m300.blow_out(incubation_plate[i].bottom(10))
        protocol.delay(seconds=5)
        m300.air_gap(height=2)
        m300.return_tip()

    # Incubate for 10 min at 25°C (temp already set from before)
    protocol.delay(minutes=5)
    #protocol.delay(minutes=1)
    mag_deck.engage(height=34)
    temp_deck.deactivate()

    # Move all solutions to plate above magnetic_deck (RNA_plate)
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i])
        #m300.mix(3, BufferC_vol, incubation_plate[i].bottom(3))
        m300.aspirate(125, incubation_plate[i].bottom(2))
        m300.dispense(125, RNA_plate[i].top(-4))
        protocol.delay(seconds=5)
        #m300.air_gap(height=2)
        m300.aspirate(125, incubation_plate[i].bottom(0.8))
        m300.dispense(125, RNA_plate[i].top(-4))
        m300.blow_out(RNA_plate[i].top(-4))
        protocol.delay(seconds=5)
        m300.air_gap(height=2)
        m300.return_tip()


    ### Remove supernatant from RNA_plate by re-using tiprack 1
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i])
        m300.aspirate(125, RNA_plate[i].bottom(2))
        m300.dispense(125, trash_box[i].top(-4))
        m300.blow_out(trash_box[i].top(-4))
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.aspirate(125, RNA_plate[i].bottom(0.8))
        m300.dispense(125, trash_box[i].top(-4))
        m300.blow_out(trash_box[i].top(-4))
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height=2)
        m300.return_tip()

    ## Ethanol Wash 3, using tiprack 2
    mag_deck.disengage()

    ### Transfer Wash 3 to RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i])
        m300.aspirate(Wash_1_vol, EtOH1.bottom(4))
        m300.dispense(Wash_1_vol, RNA_plate[i].top(-3))
        m300.mix(5, 170, RNA_plate[i].bottom(2))
        m300.move_to(RNA_plate[i].top(-9))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 200
        m300.blow_out()
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-2, radius=0.8)
        m300.air_gap(height=2)
        m300.return_tip()

    mag_deck.engage(height=34)
    protocol.delay(minutes=2)

    ## Remove supernatant, by re-using tiprack 2
    ### remove supernatant from RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i])
        m300.aspirate(Wash_1_vol, RNA_plate[i].bottom(0.8))
        m300.dispense(Wash_1_vol, trash_box[i].top(-4))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 200
        m300.blow_out(trash_box[i].top(-3))
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height = 2)
        m300.return_tip()

    ## Ethanol Wash 4, by using tiprack 3
    mag_deck.disengage()

    ### Transfer Wash 4 to RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(Wash_2_vol, EtOH2.bottom(4))
        m300.dispense(Wash_2_vol, RNA_plate[i].top(-3))
        m300.mix(5, 170, RNA_plate[i].bottom(2))
        m300.move_to(RNA_plate[i].top(-9))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out()
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-2, radius=0.8)
        m300.air_gap(height=2)
        m300.return_tip()

    mag_deck.engage(height=34)
    protocol.delay(minutes=2)

    ## Remove supernatant, by re-using tiprack 3
    ### remove supernatant from RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(Wash_2_vol, RNA_plate[i].bottom(1))
        m300.dispense(Wash_2_vol, trash_box[i].top(-4))
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 200
        m300.blow_out(trash_box[i].top(-3))
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height = 2)
        # repeat to avoid to leave too much supernatant not removable with 10ul pipette
        m300.aspirate(Wash_2_vol, RNA_plate[i].bottom(1))
        m300.dispense(Wash_2_vol, trash_box[i].top(-4))
        m300.flow_rate.dispense = 200
        m300.blow_out(trash_box[i].top(-4))
        protocol.delay(seconds=5)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.air_gap(height = 2)
        m300.return_tip()

    ### Remove the remaining supernatant with 20ul pipette
    for i in list_of_cols:
        m20.flow_rate.aspirate = 50
        m20.flow_rate.dispense = 100
        m20.pick_up_tip(tipracks_10_1[i])
        m20.aspirate(10, RNA_plate[i].bottom(0.8))
        m20.dispense(10, trash_box[i].top(-4))
        m20.blow_out()
        m20.touch_tip(v_offset=-5, radius=0.8)
        m20.return_tip()

    ## Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)
    protocol.delay(minutes=2)
    mag_deck.disengage()

    ## Elution

    #### Transfer elution buffer to RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_4[i])
        m300.aspirate(Elution_vol, Elution_buffer.bottom(3))
        m300.dispense(Elution_vol, RNA_plate[i].top(-4))
        m300.mix(5, 30, RNA_plate[i].bottom(3))
        m300.blow_out(RNA_plate[i].bottom(6))
        protocol.delay(seconds=5)
        m300.return_tip()

    protocol.pause("Place RNA_plate on the temp_deck and add a new rack above mag_deck")
    temp_deck.set_temperature(25)
    protocol.delay(minutes=5)
    #protocol.delay(minutes=1)
    mag_deck.engage(height=34)

    # Transfer elutes from rack above temp_deck to rack above magnetic_deck
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_4[i])
        m300.aspirate(Elution_vol, incubation_plate[i].bottom(0.8))
        m300.dispense(Elution_vol, RNA_plate[i].top(-4))
        m300.blow_out(RNA_plate[i].top(-4))
        m300.touch_tip(v_offset=-4, radius=0.8)
        protocol.delay(seconds=5)
        m300.return_tip()

    temp_deck.deactivate()
    protocol.delay(minutes=3)

    ### Transfer elutes to elution_plate
    for i in list_of_cols:
        m300.pick_up_tip(tipracks_200_4[i])
        m300.flow_rate.aspirate = 5
        m300.flow_rate.dispense = 50
        m300.aspirate(70, RNA_plate[i].bottom(1))
        m300.dispense(70, elution_plate_RNA[i].bottom(3))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(elution_plate_RNA[i].top(-4))
        m300.return_tip()

    mag_deck.disengage()

    protocol.pause("Cover plate with aluminium seal and or store in -80ºC freezer until further process.")
