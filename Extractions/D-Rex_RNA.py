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
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'D-Rex RNA Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of D-Rex RNA protocol for stool samples in SHIELD',
}


#### LABWARE SETUP ####
elution_plate_RNA = labware.load('96-flat', '1')
trough = labware.load('trough-12row', '2')
RNA_plate = labware.load('1ml_PCR', '7')
mag_deck = modules.load('magdeck', '7')
trash_box = labware.load('trash-box', '8')

tipracks_200 = [labware.load('tiprack-200ul', slot)
               for slot in ['4','5','6','11']]



#### PIPETTE SETUP ####
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks_200)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_200)

#### REAGENT SETUP
Elution_buffer = trough.wells('A4')

EtOH1 = trough.wells('A5')
EtOH2 = trough.wells('A6')
EtOH3 = trough.wells('A7')
EtOH4 = trough.wells('A8')
Wash = trough.wells('A9')
BufferC = trough.wells('A10')
DNase = trough.wells('A11')

Liquid_trash = trash_box.wells('A1')
#### Plate SETUP for Purification

RA1 = RNA_plate.wells('A1')
RA2 = RNA_plate.wells('A2')
RA3 = RNA_plate.wells('A3')
RA4 = RNA_plate.wells('A4')
RA5 = RNA_plate.wells('A5')
RA6 = RNA_plate.wells('A6')
RA7 = RNA_plate.wells('A7')
RA8 = RNA_plate.wells('A8')
RA9 = RNA_plate.wells('A9')
RA10 = RNA_plate.wells('A10')
RA11 = RNA_plate.wells('A11')
RA12 = RNA_plate.wells('A12')
#### VOLUME SETUP


Sample_vol = 200
EtOH_vol = 2.0*Sample_vol
Wash_1_vol = 1.0*Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50


#### PROTOCOL ####
## Ethanol Wash 1
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH1, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)

m300.transfer(Wash_1_vol, RA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)


## Ethanol Wash 2
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH2, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(200, RA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

## Dry beads before DNase treatment
m300.delay(minutes=5)
m300.transfer(30, DNase, [wells.top(-15) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)

m300.delay(minutes=10)

## Buffer C rebind
mag_deck.disengage()
m300.transfer(200, BufferC, [wells.top(-15) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)

m300.delay(minutes=10)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(200, RA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 3
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH3, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)

m300.transfer(200, RA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 4
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH4, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(200, RA1.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA2.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA3.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA4.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA5.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA6.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA7.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA8.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA9.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA10.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA11.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RA12.bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

## Dry beads before elution
m300.delay(minutes=10)

## Elution
mag_deck.disengage()
m300.transfer(Elution_vol, Elution_buffer, [wells.top(-15) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=5)

m300.transfer(200, RA1.bottom(2), elution_plate_RNA.wells('A1'), new_tip='always',  blow_out =True)
m300.transfer(200, RA2.bottom(2), elution_plate_RNA.wells('A2'), new_tip='always',  blow_out =True)
m300.transfer(200, RA3.bottom(2), elution_plate_RNA.wells('A3'), new_tip='always',  blow_out =True)
m300.transfer(200, RA4.bottom(2), elution_plate_RNA.wells('A4'), new_tip='always',  blow_out =True)
m300.transfer(200, RA5.bottom(2), elution_plate_RNA.wells('A5'), new_tip='always',  blow_out =True)
m300.transfer(200, RA6.bottom(2), elution_plate_RNA.wells('A6'), new_tip='always',  blow_out =True)
m300.transfer(200, RA7.bottom(2), elution_plate_RNA.wells('A7'), new_tip='always',  blow_out =True)
m300.transfer(200, RA8.bottom(2), elution_plate_RNA.wells('A8'), new_tip='always',  blow_out =True)
m300.transfer(200, RA9.bottom(2), elution_plate_RNA.wells('A9'), new_tip='always',  blow_out =True)
m300.transfer(200, RA10.bottom(2), elution_plate_RNA.wells('A10'), new_tip='always',  blow_out =True)
m300.transfer(200, RA11.bottom(2), elution_plate_RNA.wells('A11'), new_tip='always',  blow_out =True)
m300.transfer(200, RA12.bottom(2), elution_plate_RNA.wells('A12'), new_tip='always',  blow_out =True)
mag_deck.disengage()
robot.comment("Job's done")
