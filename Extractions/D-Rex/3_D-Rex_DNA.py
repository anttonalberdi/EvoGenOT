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
plate_name = '1ml_magPCR'
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
trough = labware.load('trough-12row', '9')
trash_box = labware.load('One-Column-reservoir', '8')
mag_deck = modules.load('magdeck', '7')
DNA_plate = labware.load('1ml_magPCR', '7', share=True)
backup = labware.load('opentrons-tuberack-50ml', '6')

tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
               for slot in ['3','4','5','6']]

tipracks_1000 = labware.load('tiprack-1000ul', '11', share=True)



#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)

p1000 = instruments.P1000_Single(
    mount='left',
    aspirate_flow_rate=500,
    dispense_flow_rate=500,
    tip_racks=tipracks_1000)

#### REAGENT SETUP

Liquid_trash = trash_box.wells('A1')
EtOH1 = trough.wells('A5')
EtOH2 = trough.wells('A6')
Elution_buffer = trough.wells('A12')

#### Backup SETUP
ETOH_backup = backup.wells('A1')


#### VOLUME SETUP
Sample_vol = 200
Sample_buffer_vol = 2.5*Sample_vol
BufferC_vol = 0.9*Sample_vol
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

sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in DNA_plate.cols()[:col_num]]

#### PROTOCOL ####
mag_deck.engage(height=34)
m300.delay(minutes=2)

## Remove Buffer C
m300.transfer(250, DA1.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA2.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA3.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA4.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA5.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA6.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA7.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA8.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA9.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA10.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA11.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)
m300.transfer(250, DA12.bottom(1), Liquid_trash.top(-4), new_tip='once',  blow_out =True, air_gap=30)

### Wash 1 with Ethanol, using tiprack 2
### Transfer Wash 1 to DA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH1.top(-16))
m300.aspirate(EtOH1, EtOH1.top(-12))
m300.dispense(Wash_1_vol, DA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA1.top(-10))
m300.blow_out()

m300.drop_tip()

### Transfer Wash 1 to DA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH1.bottom())
m300.aspirate(Wash_1_vol, EtOH1.top(-16))
m300.dispense(Wash_1_vol, DA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA2.top(-10))
m300.blow_out()

m300.drop_tip()

### Transfer Wash 1 to DA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, DA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA3.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA4.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA5.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH1.bottom())
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA7.top(-10))
m300.blow_out()
m300.drop_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.move_to(ETOH_backup.top(-4))
p1000.aspirate(800, ETOH_backup.top(-12))
p1000.dispense(800, EtOH1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH1.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-16))
p1000.dispense(800, EtOH1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH1.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-20))
p1000.dispense(800, EtOH1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH1.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Wash 1 to DA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA7.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA8.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA9.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA10.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA11.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 1 to DA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom())
m300.dispense(Wash_1_vol, DA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, DA12.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(DA12.top(-10))
m300.blow_out()
m300.drop_tip()

mag_deck.engage(height=34)
m300.delay(minutes=2)

### Remove supernatant, by re-using tiprack 2
### remove supernatant from DA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A1'))
m300.aspirate(Wash_1_vol, DA1.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A2'))
m300.aspirate(Wash_1_vol, DA2.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A3'))
m300.aspirate(Wash_1_vol, DA3.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A4'))
m300.aspirate(Wash_1_vol, DA4.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A5'))
m300.aspirate(Wash_1_vol, DA5.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A6'))
m300.aspirate(Wash_1_vol, DA6.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A7'))
m300.aspirate(Wash_1_vol, DA7.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A8'))
m300.aspirate(Wash_1_vol, DA8.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A9'))
m300.aspirate(Wash_1_vol, DA9.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A10'))
m300.aspirate(Wash_1_vol, DA10.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A11'))
m300.aspirate(Wash_1_vol, DA11.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_2.wells('A12'))
m300.aspirate(Wash_1_vol, DA12.bottom(1))
m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

mag_deck.disengage()

## Ethanol Wash 2, by using tiprack 3
### Transfer Wash 2 to DA1
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH2.top(-16))
m300.aspirate(Wash_2_vol, EtOH2.top(-12))
m300.dispense(Wash_2_vol, DA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA1.top(-10))
m300.blow_out()

m300.drop_tip()

### Transfer Wash 2 to DA2
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH2.bottom())
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, DA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA2.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA3
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, DA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA3.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA4
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA4.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA5
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA5.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA6
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH2.bottom())
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.drop_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, ETOH_backup.top(-12))
p1000.dispense(800, EtOH2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH2.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-16))
p1000.dispense(800, EtOH2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH2.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-20))
p1000.dispense(800, EtOH2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH2.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Wash 2 to DA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA8
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA8.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA9
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA9.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA10
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA10.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA11
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA11.top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Wash 2 to DA12
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom())
m300.dispense(Wash_2_vol, DA12.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, DA12.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA12.top(-10))
m300.blow_out()
m300.drop_tip()

mag_deck.engage(height=34)
m300.delay(minutes=2)

### Remove supernatant, by using re-using tiprack 3
mag_deck.engage(height=34)
m300.delay(minutes=2)

### remove supernatant from DA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A1'))
m300.aspirate(Wash_2_vol, DA1.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A2'))
m300.aspirate(Wash_2_vol, DA2.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A3'))
m300.aspirate(Wash_2_vol, DA3.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A4'))
m300.aspirate(Wash_2_vol, DA4.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A5'))
m300.aspirate(Wash_2_vol, DA5.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A6'))
m300.aspirate(Wash_2_vol, DA6.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A7'))
m300.aspirate(Wash_2_vol, DA7.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A8'))
m300.aspirate(Wash_2_vol, DA8.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A9'))
m300.aspirate(Wash_2_vol, DA9.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A10'))
m300.aspirate(Wash_2_vol, DA10.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A11'))
m300.aspirate(Wash_2_vol, DA11.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from DA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A12'))
m300.aspirate(Wash_2_vol, DA12.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.drop_tip()

#### Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)

## Elution
mag_deck.disengage()
for target in samples: # Slow down head speed 0.5X for bead handling
    m300.pick_up_tip()
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
    m300.dispense(Elution_vol, target.bottom(1))
    m300.mix(5, 30, target.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(target.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

robot.pause("Please cover the plate with film and incubate 5 min 25°C at 1500 rpm")

mag_deck.engage(height=34)
m300.delay(minutes=5)

### Transfer Elution buffer to elution_plate A1
m300.pick_up_tip(tipracks_200_4.wells('A1'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA1.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A1').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A1').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A2
m300.pick_up_tip(tipracks_200_4.wells('A2'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA2.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A2').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A2').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A3
m300.pick_up_tip(tipracks_200_4.wells('A3'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA3.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A3').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A3').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A4
m300.pick_up_tip(tipracks_200_4.wells('A4'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA4.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A4').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A4').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A5
m300.pick_up_tip(tipracks_200_4.wells('A5'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA5.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A5').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A5').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A6
m300.pick_up_tip(tipracks_200_4.wells('A6'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA6.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A6').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A6').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A7
m300.pick_up_tip(tipracks_200_4.wells('A7'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA7.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A7').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A7').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A8
m300.pick_up_tip(tipracks_200_4.wells('A8'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA8.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A8').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A8').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A9
m300.pick_up_tip(tipracks_200_4.wells('A9'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA9.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A9').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A9').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A10
m300.pick_up_tip(tipracks_200_4.wells('A10'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA10.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A10').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A10').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A11
m300.pick_up_tip(tipracks_200_4.wells('A11'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA11.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A11').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A11').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to elution_plate A12
m300.pick_up_tip(tipracks_200_4.wells('A12'))
m300.set_flow_rate(aspirate=25, dispense=25)
m300.aspirate(Elution_buffer_vol, DA12.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A12').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A12').top(-10))
m300.blow_out()
m300.drop_tip()

mag_deck.disengage()
