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
    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 9)
    trash_box = protocol.load_labware('agilent_1_reservoir_290ml', 8)
    mag_deck = protocol.load_module('magdeck', 7)
    DNA_plate = mag_deck.load_labware('biorad_96_wellplate_1000ul')#, share=True)
    EtOH_wash = protocol.load_labware('agilent_1_reservoir_290ml', 6)


    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 2)#, share=True)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)#, share=True)
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)#, share=True)
    tipracks_200_4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)#, share=True)
    tipracks_200_5 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 7)#, share=True)

    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                            tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4))

    #### REAGENT SETUP                          Description             Volume needed for protocol
    EtOH1 = EtOH_wash['A1']                   # 80% Ethanol           82.5 ml
    Elution_buffer = trough['A12']            # EBT                   6 ml
    BufferC = trough['A5']                    # Buffer C:             19.8 ml
    Liquid_trash = trash_box['A1']

    #### VOLUME SETUP
    Sample_vol = 200
    Sample_buffer_vol = 2.5*Sample_vol
    BufferC_vol = 0.9*Sample_vol
    Wash_1_vol = Sample_vol
    Wash_2_vol = 0.9*Sample_vol
    Elution_vol = 50

    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    list_of_cols = ['A1','A2','A3','A4']
    #### PROTOCOL ####

    mag_deck.disengage()

    ## add Buffer C to beads with DNA
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_5[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(3, BufferC_vol, BufferC.top(-28))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(BufferC_vol, BufferC.top(-28))
        m300.dispense(BufferC_vol, sample_plate[i].bottom(4))   # *2 ?? check volume
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(8, BufferC_vol, sample_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.move_to(sample_plate[i].bottom(5))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()       # or drop tip?

    mag_deck.engage(height_from_base=0)
    #protocol.delay(minutes=4)

    # transfer supernatant from DNA_plate to liquid trash
    for i in list_of_cols:
        m300.transfer(250, DNA_plate[i].bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)

    mag_deck.disengage()

    for i in list_of_cols:
        ### Wash 1 with Ethanol, using tiprack 2
        ### Transfer Wash 1 to DNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(Wash_1_vol, EtOH1.top(-12))
        m300.dispense(Wash_1_vol, DNA_plate[i].top(-4))
        m300.mix(5, Wash_1_vol, DNA_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(DNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    mag_deck.engage(height_from_base=0)
    #protocol.delay(minutes=2)

    for i in list_of_cols:
        ### Remove supernatant, by re-using tiprack 2
        ### remove supernatant from DNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i])
        m300.aspirate(Wash_1_vol, DNA_plate[i].bottom(1))
        m300.dispense(Wash_1_vol, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.return_tip()

    mag_deck.disengage()

    for i in list_of_cols[:6]:
        ## Ethanol Wash 2, by using tiprack 3
        ### Transfer Wash 2 to DNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.move_to(EtOH1.top(-16))
        m300.aspirate(Wash_2_vol, EtOH1.top(-12))
        m300.dispense(Wash_2_vol, DNA_plate[i].top(-4))
        m300.mix(5, Wash_2_vol, DNA_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(DNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    #### Ensure enough buffer i reservoir by adding 3ml from backup
    protocol.pause("Ensure enough buffer in reservoir by adding 3ml from backup")
    # p1000.set_flow_rate(aspirate=500, dispense=400)
    # p1000.pick_up_tip(tipracks_1000.wells('F1'))
    # p1000.aspirate(800, ETOH_backup.top(-45))
    # p1000.dispense(800, EtOH1.top(-4))
    # p1000.delay(seconds=2)
    # p1000.move_to(EtOH1.top(-4))
    # p1000.blow_out()
    # p1000.aspirate(800, ETOH_backup.top(-45))
    # p1000.dispense(800, EtOH1.top(-4))
    # p1000.delay(seconds=2)
    # p1000.move_to(EtOH1.top(-4))
    # p1000.blow_out()
    # p1000.aspirate(800, ETOH_backup.top(-45))
    # p1000.dispense(800, EtOH1.top(-4))
    # p1000.delay(seconds=2)
    # p1000.move_to(EtOH1.top(-4))
    # p1000.blow_out()
    # p1000.drop_tip()

    for i in list_of_cols[6:]:
        ## Ethanol Wash 2, by using tiprack 3
        ### Transfer Wash 2 to DA1
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.move_to(EtOH1.top(-16))
        m300.aspirate(Wash_2_vol, EtOH1.top(-12))
        m300.dispense(Wash_2_vol, DNA_plate[i].top(-4))
        m300.mix(5, Wash_2_vol, DNA_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(DNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    mag_deck.engage(height_from_base=0)
    #protocol.delay(minutes=2)

    ### Remove supernatant, by re-using tiprack 3

    for i in list_of_cols:
        ### remove supernatant from DNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(Wash_2_vol, DNA_plate[i].bottom(1))
        m300.dispense(Wash_2_vol, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.return_tip()

    #### Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)
    protocol.pause('If beads are not dry, let them dry for at least 5 min')
    ## Elution
    mag_deck.disengage()

    #### Transfer elution buffer to DNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_4[i])
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
        m300.dispense(Elution_vol, DNA_plate[i].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.move_to(DNA_plate[i].bottom(5))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()

    protocol.pause("Please cover the plate with foil and incubate 5 min 25°C at 1500 rpm")

    mag_deck.engage(height_from_base=0)
    #protocol.delay(minutes=5)

    for i in list_of_cols:
        ### Transfer Elution buffer to elution_plate
        m300.pick_up_tip(tipracks_200_4[i])
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Elution_vol, DNA_plate[i].bottom(1))
        m300.dispense(Elution_vol, elution_plate_DNA[i].bottom(2))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(elution_plate_DNA[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    mag_deck.disengage()

    protocol.pause('Cover DNA plate with foil and proceed with library building or store the samples at -20°C')
