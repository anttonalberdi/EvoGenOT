## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Bead beat samples at maximum speed for 5 minutes
# 	2. Spin down samples 10.000 rpm for 1 minute
#	3. Transfer 200µl lysed sample to a deep well plate

### Procedure ###


######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'Extraction_DNA_RNA',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of D-Rex DNA protocol for stool samples in SHIELD',
}


#### LABWARE SETUP ####
elution_plate_DNA = labware.load('96-flat', '1')
trough = labware.load('trough-12row', '2')
trash_box = labware.load('trash-box', '8')
mag_deck = modules.load('magdeck', '7')
DNA_plate = labware.load('96-flat', '7', share=True)
sample_plate = labware.load('1ml_PCR','3')

tipracks_200 = [labware.load('tiprack-200ul', slot)
               for slot in ['4','5','6','11']]

tipracks_1000 = [labware.load('tiprack-1000ul', slot, share=True)
                for slot in ['9']]


#### PIPETTE SETUP ####
s1000 = instruments.P1000_Single(
    mount='right',
    tip_racks=tipracks_1000)

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_200)

#### REAGENT SETUP

Beads = trough.wells('A1')
Elution_buffer = trough.wells('A2')

Liquid_trash = trash_box.wells('A1')


BufferC = buffer.wells('A10')
Ethanol_1 = buffer.wells('A2')
Ethanol_2 = buffer.wells('A3')
Wash_1 = buffer.wells('B2')
Wash_2 = buffer.wells('B3')


#### VOLUME SETUP


Sample_vol = 200
Sample_buffer_vol = 2.5*Sample_vol
BufferC_vol = 1.0*Sample_vol
Wash_1_vol = Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50

#### Plate SETUP
SA1 = sample_plate.wells('A1')
SA2 = sample_plate.wells('A2')
SA3 = sample_plate.wells('A3')
SA4 = sample_plate.wells('A4')
SA5 = sample_plate.wells('A5')
SA6 = sample_plate.wells('A6')
SA7 = sample_plate.wells('A7')
SA8 = sample_plate.wells('A8')
SA9 = sample_plate.wells('A9')
SA10 = sample_plate.wells('A10')
SA11 = sample_plate.wells('A11')
SA12 = sample_plate.wells('A12')

DA1 = DNA_plate.wells('A1')
DA2 = DNA_plate.wells('A2')
DA3 = DNA_plate.wells('A3')
DA4 = DNA_plate.wells('A4')
DA5 = DNA_plate.wells('A5')
DA6 = DNA_plate.wells('A6')
DA7 = DNA_plate.wells('A7')
DA8 = DNA_plate.wells('A8')
DA9 = DNA_plate.wells('A9')
DA10 = DNA_plate.wells('A10')
DA11 = DNA_plate.wells('A11')
DA12 = DNA_plate.wells('A12')

#### PROTOCOL ####
## transfer respuspended supernatant to DNA plate
magdeck.disengage()
m300.transfer(100, SA1.bottom(2), DA1.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA2.bottom(2), DA2.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA3.bottom(2), DA3.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA4.bottom(2), DA4.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA5.bottom(2), DA5.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA6.bottom(2), DA6.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA7.bottom(2), DA7.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA8.bottom(2), DA8.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA9.bottom(2), DA9.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA10.bottom(2), DA10.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA11.bottom(2), DA11.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
m300.transfer(100, SA12.bottom(2), DA12.bottom(2), mix_before=(5,70), new_tip='once',  blow_out =True)
mag_deck.engage()

m300.delay(minutes=2)

#### Remove supernatant
m300.transfer(200, DA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

#### Wash beads with BufferC
mag_deck.disengage()
m300.transfer(BufferC_vol, BufferC, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=2)

m300.transfer(200, DA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)


#### Wash beads with ethanol
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH1, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=2)

m300.transfer(200, DA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

#### Wash beads with ethanol
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH2, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=2)

m300.transfer(200, DA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, DA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

#### Dry beads before elution
m300.delay(minutes=4)
mag_deck.disengage()

m300.transfer(Elution_vol, Elution_buffer, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
m300.delay(minutes=5)

mag_deck.engage()
m300.delay(minutes=2)
m300.transfer(200, DA1.bottom(2), elution_plate_DNA.wells('A1'), new_tip='always',  blow_out =True)
m300.transfer(200, DA2.bottom(2), elution_plate_DNA.wells('A2'), new_tip='always',  blow_out =True)
m300.transfer(200, DA3.bottom(2), elution_plate_DNA.wells('A3'), new_tip='always',  blow_out =True)
m300.transfer(200, DA4.bottom(2), elution_plate_DNA.wells('A4'), new_tip='always',  blow_out =True)
m300.transfer(200, DA5.bottom(2), elution_plate_DNA.wells('A5'), new_tip='always',  blow_out =True)
m300.tDAnsfer(200, DA6.bottom(2), elution_plate_DNA.wells('A6'), new_tip='always',  blow_out =True)
m300.transfer(200, DA7.bottom(2), elution_plate_DNA.wells('A7'), new_tip='always',  blow_out =True)
m300.transfer(200, DA8.bottom(2), elution_plate_DNA.wells('A8'), new_tip='always',  blow_out =True)
m300.tDAnsfer(200, DA9.bottom(2), elution_plate_DNA.wells('A9'), new_tip='always',  blow_out =True)
m300.transfer(200, DA10.bottom(2), elution_plate_DNA.wells('A10'), new_tip='always',  blow_out =True)
m300.transfer(200, DA11.bottom(2), elution_plate_DNA.wells('A11'), new_tip='always',  blow_out =True)
m300.transfer(200, DA12.bottom(2), elution_plate_DNA.wells('A12'), new_tip='always',  blow_out =True)

mag_deck.disengage()
robot.comment("Job's done")
