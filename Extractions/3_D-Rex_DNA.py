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
elution_plate_DNA = labware.load('biorad-hardshell-96-PCR', '1')
trough = labware.load('trough-12row', '2')
trash_box = labware.load('One-Column-reservoir', '8')
mag_deck = modules.load('magdeck', '7')
DNA_plate = labware.load('1ml_PCR', '7', share=True)

tipracks_200 = [labware.load('tiprack-200ul', slot)
               for slot in ['3','4','5','6','9']]



#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)

#### REAGENT SETUP

Liquid_trash = trash_box.wells('A1')


BufferC = trough.wells('A9')
EtOH1 = trough.wells('A10')
EtOH2 = trough.wells('A11')
Elution_buffer = trough.wells('A12')


#### VOLUME SETUP


Sample_vol = 200
Sample_buffer_vol = 2.5*Sample_vol
BufferC_vol = 1.0*Sample_vol
Wash_1_vol = Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50

#### Plate SETUP
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
mag_deck.engage(height=16)
m300.delay(minutes=2)

#### Remove supernatant
m300.transfer(200, DA1.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA2.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA3.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA4.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA5.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA6.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA7.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA8.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA9.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA10.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA11.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA12.bottom(1), Liquid_trash.top(-4), new_tip='always',  blow_out =True)

#### Wash beads with BufferC
mag_deck.disengage()
m300.transfer(BufferC_vol, BufferC, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(200, DA1.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA2.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA3.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA4.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA5.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA6.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA7.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA8.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA9.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA10.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA11.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(200, DA12.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)

#### Wash beads with EtOH1
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH1, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(180, DA1.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA2.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA3.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA4.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA5.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA6.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA7.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA8.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA9.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA10.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA11.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)
m300.transfer(180, DA12.bottom(2), Liquid_trash.top(-4), new_tip='always',  blow_out =True)

##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process")
m300.reset()

#### Wash beads with EtOH2
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH2, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',  blow_out =True)
mag_deck.engage(height=16)
m300.delay(minutes=2)

m300.transfer(250, DA1.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA2.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA3.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA4.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA5.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA6.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA7.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA8.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA9.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA10.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA11.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(250, DA12.bottom(), Liquid_trash.top(-4), new_tip='once',  blow_out =True)

#### Dry beads before elution
m300.delay(minutes=4)
mag_deck.disengage()

m300.transfer(Elution_vol, Elution_buffer, [wells.top(-5) for wells in DNA_plate.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12')] , new_tip='once',mix_after=(5,40),  blow_out =True)
m300.delay(minutes=5)

mag_deck.engage(height=16)
m300.delay(minutes=2)
m300.transfer(Elution_vol, DA1.bottom(2), elution_plate_DNA.wells('A1'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA2.bottom(2), elution_plate_DNA.wells('A2'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA3.bottom(2), elution_plate_DNA.wells('A3'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA4.bottom(2), elution_plate_DNA.wells('A4'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA5.bottom(2), elution_plate_DNA.wells('A5'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA6.bottom(2), elution_plate_DNA.wells('A6'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA7.bottom(2), elution_plate_DNA.wells('A7'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA8.bottom(2), elution_plate_DNA.wells('A8'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA9.bottom(2), elution_plate_DNA.wells('A9'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA10.bottom(2), elution_plate_DNA.wells('A10'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA11.bottom(2), elution_plate_DNA.wells('A11'), new_tip='always',  blow_out =True)
m300.transfer(Elution_vol, DA12.bottom(2), elution_plate_DNA.wells('A12'), new_tip='always',  blow_out =True)

mag_deck.disengage()
robot.comment("Job's done")