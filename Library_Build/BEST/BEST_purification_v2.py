##########################
### BEST Library build ###
##########################

## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Mix mastermix of End-repair, Ligase and Fill-in according to BEST-sheet and sample size.
#				NOTE! This procedure is for full plates
# 	2. Thaw samples in fridge and place them in a slot 2 in a chilling rack.
#
# Procedure
#
#		BEST
# 	1.	Distribute 2µl Adapters mix into temp_deck
#	  2.	Adds 110µl of Fill MM to Enzyme strip (8.4µl * 13 columns)
#   3.  Distribute 10µl of Enzyme-Fill_MM to each well
#	  4.	Incubate in PCR at 65°C for 15 min, and at 80°C for 15 min

#
#	Good Luck!
#
#
######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'BEST_Purification',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/07/04',
    'description': 'Purification procedure of Automated single tube library preperation after Carøe et al. 2017',
}
#### LOADING CUSTOM LABWARE ####

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
trough = labware.load('trough-12row', '2')
Trash = labware.load('One-Column-reservoir','9')
mag_deck = modules.load('magdeck', '7')
mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)
elution_plate = labware.load('biorad-hardshell-96-PCR','1')


tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
                for slot in ['3','4','5','6']]


#### PIPETTE SETUP ####

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)


## Purification reagents SETUP
SPRI_beads = trough.wells('A1')
EtOH1 = trough.wells('A2')
EtOH2 = trough.wells('A3')
Elution_buffer = trough.wells('A12')

Liquid_trash = Trash.wells('A1')

## Sample Setup

col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)

SA1 = mag_plate.wells('A1')
SA2 = mag_plate.wells('A2')
SA3 = mag_plate.wells('A3')
SA4 = mag_plate.wells('A4')
SA5 = mag_plate.wells('A5')
SA6 = mag_plate.wells('A6')
SA7 = mag_plate.wells('A7')
SA8 = mag_plate.wells('A8')
SA9 = mag_plate.wells('A9')
SA10 = mag_plate.wells('A10')
SA11 = mag_plate.wells('A11')
SA12 = mag_plate.wells('A12')

declare -a sample_list=("SA1" "SA2" "SA3" "SA4" "SA5" "SA6" "SA7" "SA8" "SA9" "SA10" "SA11" "SA12")

sample_vol = 60
bead_vol = 1.5*sample_vol
EtOH_vol = 180
EtOH_vol2 = 150
elution_vol = 40

robot.comment("Yay! \ Purification begins!")

### Beads addition
mag_deck.disengage()

    for target in "${sample_list[@]}":
        pipette.set_flow_rate(aspirate=180, dispense=180)
        pipette.pick_up_tip()
        # Slow down head speed 0.5X for bead handling
        pipette.mix(3, 200, SPRI_beads)
        max_speed_per_axis = {
            'x': (50), 'y': (50), 'z': (50), 'a': (10), 'b': (10), 'c': (10)}
        robot.head_speed(
            combined_speed=max(max_speed_per_axis.values()),
            **max_speed_per_axis)

        pipette.set_flow_rate(aspirate=10, dispense=10)
        pipette.transfer(
            bead_vol, SPRI_beads, target, air_gap=0, new_tip='never')
        pipette.set_flow_rate(aspirate=50, dispense=50)
        pipette.mix(5, 100, target)
        pipette.blow_out()
        max_speed_per_axis = {
            'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),
            'c': (40)}
        robot.head_speed(
            combined_speed=max(max_speed_per_axis.values()),
            **max_speed_per_axis)

        pipette.drop_tip()

    # Return robot head speed to the defaults for all axes
        max_speed_per_axis = {
            'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),
            'c': (40)}
        robot.head_speed(
            combined_speed=max(max_speed_per_axis.values()),
            **max_speed_per_axis)

robot.comment("Incubating the beads and PCR products at room temperature \
for 5 minutes. Protocol will resume automatically.")
m300.delay(minutes=5)
mag_deck.engage()
m300.delay(minutes=2)


### Remove supernatant
m300.transfer(180, SA1.bottom(), Liquid_trash.top(-5), blow_out=True,new_tip='always')
m300.transfer(180, SA2.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA3.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA4.bottom(), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA5.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA6.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA7.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA8.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA9.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA10.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA11.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')
m300.transfer(180, SA12.bottom(1), Liquid_trash.top(-5), blow_out=True, new_tip='always')

### Wash with EtOH1
mag_deck.disengage()

m300.transfer(EtOH_vol, EtOH1, SA1.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA2.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA3.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA4.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA5.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA6.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA7.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA8.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA9.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA10.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA11.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol, EtOH1, SA12.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
mag_deck.engage()
m300.delay(minutes=2)

m300.transfer(200, SA1.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA2.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA3.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA4.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA5.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA6.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA7.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA8.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA9.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA10.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA11.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA12.bottom(2), Liquid_trash.top(-5), new_tip='always', blow_out=True)

##Reset tipracks for more tips
robot.pause("Please fill up tips before continuing process and empty trash box")
m300.reset()

### Wash with EtOH2
mag_deck.disengage()

m300.transfer(EtOH_vol2, EtOH2, SA1.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA2.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA3.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA4.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA5.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA6.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA7.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA8.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA9.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA10.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA11.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(EtOH_vol2, EtOH2, SA12.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)

mag_deck.engage()
m300.delay(minutes=2)

m300.transfer(200, SA1.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA2.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA3.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA4.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA5.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA6.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA7.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA8.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA9.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA10.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA11.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)
m300.transfer(200, SA12.bottom(1), Liquid_trash.top(-5), new_tip='always', blow_out=True)

## Dry beads before elution
m300.delay(minutes=3)

## Elution of DNA
m300.transfer(elution_vol, Elution_buffer, SA1.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA2.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA3.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA4.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA5.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA6.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA7.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA8.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA9.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA10.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA11.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)
m300.transfer(elution_vol, Elution_buffer, SA12.bottom(2), mix_after=(5,100),new_tip='always', blow_out=True)

m300.delay(minutes=15)
m300.transfer(35, SA1.bottom(2), elution_plate('A1'), new_tip='always', blow_out=True)
m300.transfer(35, SA2.bottom(2), elution_plate('A2'), new_tip='always', blow_out=True)
m300.transfer(35, SA3.bottom(2), elution_plate('A3'), new_tip='always', blow_out=True)
m300.transfer(35, SA4.bottom(2), elution_plate('A4'), new_tip='always', blow_out=True)
m300.transfer(35, SA5.bottom(2), elution_plate('A5'), new_tip='always', blow_out=True)
m300.transfer(35, SA6.bottom(2), elution_plate('A6'), new_tip='always', blow_out=True)
m300.transfer(35, SA7.bottom(2), elution_plate('A7'), new_tip='always', blow_out=True)
m300.transfer(35, SA8.bottom(2), elution_plate('A8'), new_tip='always', blow_out=True)
m300.transfer(35, SA9.bottom(2), elution_plate('A9'), new_tip='always', blow_out=True)
m300.transfer(35, SA10.bottom(2), elution_plate('A10'), new_tip='always', blow_out=True)
m300.transfer(35, SA11.bottom(2), elution_plate('A11'), new_tip='always', blow_out=True)
m300.transfer(35, SA12.bottom(2), elution_plate('A12'), new_tip='always', blow_out=True)


robot.pause("Yay! \ Purification has finished \ Please store purified libraries as -20°C \ Press resume when finished.")
