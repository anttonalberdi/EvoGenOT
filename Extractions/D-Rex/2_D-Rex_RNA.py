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

### Custom LABWARE load
plate_name = '1ml_PCR'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

plate_name = 'One-Column-reservoir'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(1, 1),                    # specify amount of (columns, rows)
        spacing=(0, 0),               # distances (mm) between each (column, row)
        diameter=81,                     # diameter (mm) of each well on the plate
        depth=35,                       # depth (mm) of each well on the plate
        volume=350000)

#### LABWARE SETUP ####
elution_plate_RNA = labware.load('biorad-hardshell-96-PCR', '1')
trough = labware.load('trough-12row', '2')
mag_deck = modules.load('magdeck', '7')
RNA_plate = labware.load('1ml_PCR', '7', share=True)
trash_box = labware.load('One-Column-reservoir', '8')

tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
               for slot in ['3','4','5','6']]



#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)

#### REAGENT SETUP

EtOH1 = trough.wells('A5')
EtOH2 = trough.wells('A6')
EtOH3 = trough.wells('A7')
EtOH4 = trough.wells('A8')
DNase = trough.wells('A9')
BufferC = trough.wells('A10')
Elution_buffer = trough.wells('A12')

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

## Remove supernatant
mag_deck.engage(height=16)
m300.delay(minutes=3)
m300.transfer(700, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

## Ethanol Wash 1
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH1, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(Wash_1_vol, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)


## Ethanol Wash 2
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH2, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=16)
m300.delay(minutes=2)
m300.transfer(250, RA1.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA2.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA3.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA4.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA5.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA6.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA7.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA8.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA9.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA10.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA11.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA12.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

## Dry beads before DNase treatment
mag_deck.disengage()
m300.delay(minutes=3)
m300.transfer(30, DNase, [wells.top(-15) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)

m300.delay(minutes=10)

##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process")
m300.reset()
## Buffer C rebind
m300.transfer(200, BufferC, [wells.top(-15) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='always', mix_after=(3,200),  blow_out =True)

m300.delay(minutes=10)
mag_deck.engage(height=16)
m300.delay(minutes=2)
m300.transfer(200, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

## Ethanol Wash 3
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH3, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(200, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(200, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

## Ethanol Wash 4
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH4, [wells.top(-5) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=16)

##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process")
m300.reset()

## Ethanol Wash 4 - continued
m300.delay(minutes=2)
m300.transfer(250, RA1.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA2.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA3.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA4.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA5.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA6.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA7.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA8.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA9.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA10.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA11.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, RA12.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)



## Dry beads before elution
m300.delay(minutes=5)

## Elution
mag_deck.disengage()
m300.transfer(Elution_vol, Elution_buffer, [wells.top(-15) for wells in RNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='always', mix_after=(3,30),  blow_out =True)
m300.delay(minutes=10)
mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(Elution_vol, RA1.bottom(1), elution_plate_RNA.wells('A1'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA2.bottom(1), elution_plate_RNA.wells('A2'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA3.bottom(1), elution_plate_RNA.wells('A3'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA4.bottom(1), elution_plate_RNA.wells('A4'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA5.bottom(1), elution_plate_RNA.wells('A5'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA6.bottom(1), elution_plate_RNA.wells('A6'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA7.bottom(1), elution_plate_RNA.wells('A7'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA8.bottom(1), elution_plate_RNA.wells('A8'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA9.bottom(1), elution_plate_RNA.wells('A9'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA10.bottom(1), elution_plate_RNA.wells('A10'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA11.bottom(1), elution_plate_RNA.wells('A11'), new_tip='once',  blow_out =True)
m300.transfer(Elution_vol, RA12.bottom(1), elution_plate_RNA.wells('A12'), new_tip='once',  blow_out =True)
mag_deck.disengage()
robot.comment("Job's done")
