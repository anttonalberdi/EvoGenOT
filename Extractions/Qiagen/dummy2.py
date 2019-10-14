####### IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

# metadata
metadata = {
    'protocolName': 'DNA Purification',
    'author': 'Name <lassenyholm@gmail.com>',
    'description': 'DNA purification of PowerSoil/Fecal extracts (C1 and bead beating)',
}

### CUSTOM LABWARE ###

plate_name = 'One-Column-reservoir'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(1, 1),                    # specify amount of (columns, rows)
        spacing=(0, 0),               # distances (mm) between each (column, row)
        diameter=81,                     # diameter (mm) of each well on the plate
        depth=35,                       # depth (mm) of each well on the plate
        volume=350000)

plate_name = '1ml_PCR' #Used on the magdeck together with adaptor
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

### LABWARE SETUP ###
mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('1ml_PCR', '7', share=True)
trough = labware.load('trough-12row', '9')
Trash = labware.load('One-Column-reservoir','8')

tipracks_200_1 = labware.load('tiprack-200ul', '4', share=True)

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=300,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=(tipracks_200_1)

###  PURIFICATION REAGENTS SETUP ###
SPRI_beads = trough.wells('A1')
EtOH1 = trough.wells('A4')
EtOH2 = trough.wells('A5')
EtOH3 = trough.wells('A6')
EtOH4 = trough.wells('A7')
Elution_buffer = trough.wells('A12')
Liquid_trash = Trash.wells('A1')

sample_vol = 200
bead_vol = sample_vol
EtOH_vol = 200
elution_vol = 30

#### Sample SETUP

SA1 = sample_plate.wells('A1')
SA2 = sample_plate.wells('A3')
SA3 = sample_plate.wells('A5')
SA4 = sample_plate.wells('A7')
SA5 = sample_plate.wells('A9')
SA6 = sample_plate.wells('A11')

EA1 = elution_plate.wells('A1')
EA2 = elution_plate.wells('A3')
EA3 = elution_plate.wells('A5')
EA4 = elution_plate.wells('A7')
EA5 = elution_plate.wells('A9')
EA6 = elution_plate.wells('A11')

### REMOVING SUPERNATANT ###

#1. Fix blow out (see ### remove supernatant from SA1### WHEN YOU GET BACK)


### remove supernatant from SA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A7'))
m300.aspirate(bead_vol, SA1.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.set_flow_rate(aspirate=130, dispense=130)
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.air_gap(20)
m300.aspirate(bead_vol, SA1.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.air_gap(20)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(Trash.wells('A1').top(-5))
m300.drop_tip()

### remove supernatant from SA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A8'))
m300.aspirate(bead_vol, SA2.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.set_flow_rate(aspirate=130, dispense=130)
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.air_gap(20)
m300.aspirate(bead_vol, SA2.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.air_gap(20)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(Trash.wells('A1').top(-5))
m300.drop_tip()


### remove supernatant from SA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A9'))
m300.aspirate(bead_vol, SA3.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.set_flow_rate(aspirate=130, dispense=130)
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.air_gap(20)
m300.aspirate(bead_vol, SA3.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.air_gap(20)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(Trash.wells('A1').top(-5))
m300.drop_tip()


### remove supernatant from SA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A10'))
m300.aspirate(bead_vol, SA4.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.set_flow_rate(aspirate=130, dispense=130)
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.air_gap(20)
m300.aspirate(bead_vol, SA4.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.air_gap(20)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(Trash.wells('A1').top(-5))
m300.drop_tip()


### remove supernatant from SA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A11'))
m300.aspirate(bead_vol, SA5.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.set_flow_rate(aspirate=130, dispense=130)
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.air_gap(20)
m300.aspirate(bead_vol, SA5.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.air_gap(20)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(Trash.wells('A1').top(-5))
m300.drop_tip()


### remove supernatant from SA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_1.wells('A12'))
m300.aspirate(bead_vol, SA6.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.set_flow_rate(aspirate=130, dispense=130)
m300.delay(seconds=5)
m300.blow_out(Trash.wells('A1').top(-5))
m300.air_gap(20)
m300.aspirate(bead_vol, SA6.bottom(1))
m300.dispense(bead_vol, Trash.wells('A1').top(-5))
m300.delay(seconds=5)
m300.air_gap(20)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(Trash.wells('A1').top(-5))
m300.drop_tip()
