metadata = {
    'protocolName': 'PCR mastermix to plate',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/03/05',
    'validation_date': '',
    'description': 'Standard PCR mastermix preparation and distribution to plate',
}

#### LIBRARIES ####

import csv
#Opentrons presets
from opentrons import labware, instruments, modules, robot
#Custom presets
import os,sys
sys.path.append("/root")
import custom_labware

#### MODULES ####

#Reagent rack
reagent_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '9', share=True)
  #A1 = ddH2O
  #A2 = 10x buffer
  #A3 = MgCl2
  #A4 = BSA (should be avoided)
  #A5 = dNTPs
  #A6 = TagGold
  #C1 = Mastermix1
  #C2 = Mastermix2

#PCR plate
pcr_plate = labware.load('PCR-strip-tall', '6', share=True)

#Primers plate
primer_plate = labware.load('PCR-strip-tall', '3', share=True)
    #Col1 Primer stip 1 (e.g. 1-8)
    #Col2 empty - for opening lids
    #Col3 Primer stip 2 (e.g. 9-16)
    #Col4 empty
    #Col5 Primer stip 3 (e.g. 17-24)
    #Col6 empty

#### TIP RACKS ####
tiprack_200 = labware.load('labsolute-tiprack-200µl', '5')
tiprack_10 = labware.load('labsolute-tiprack-10µl', '2')

#### PIPETTES ####
s50 = instruments.P50_Single(mount='left', tip_racks=[tiprack_200])
m10 = instruments.P10_Multi(mount='right', tip_racks=[tiprack_10])

#### INPUT FILES ####

#Load reagents data file
water=[]
buffer=[]
mgcl2=[]
bsa=[]
dntp=[]
taq=[]
primers=[]
samples=[]
with open("/root/csv/pcr_mix_96plate_v1_reagents.csv", "r") as csvfile:
    settings = csv.reader(csvfile, delimiter=',')
    for i in settings:
        water.append(i[0])
        buffer.append(i[1])
        mgcl2.append(i[2])
        bsa.append(i[3])
        dntp.append(i[4])
        taq.append(i[5])
        primers.append(i[6])
        samples.append(i[7])

#Remove headers
water.pop(0)
buffer.pop(0)
mgcl2.pop(0)
bsa.pop(0)
dntp.pop(0)
taq.pop(0)
primers.pop(0)
samples.pop(0)

#Convert to string
water = float(''.join(water))
buffer = float(''.join(buffer))
mgcl2 = float(''.join(mgcl2))
bsa = float(''.join(bsa))
dntp = float(''.join(dntp))
taq = float(''.join(taq))
primers = float(''.join(primers))
samples = float(''.join(samples))

#Load primer data file
platecols=[]
primercols=[]
with open("/root/csv/pcr_mix_96plate_v1_primers.csv", "r") as csvfile:
    settings = csv.reader(csvfile, delimiter=',')
    for i in settings:
        platecols.append(i[0])
        primercols.append(i[1])

platecols.pop(0)
platecolsStr = ','.join(platecols)
platecolsStr = platecolsStr.replace("," , "','")

primercols.pop(0)
primercolsStr = ','.join(primercols)
primercolsStr = primercolsStr.replace("," , "','")

primerVol = primers

#### PREPARATIONS ####

#Get total volumes
waterTot = water * (samples + round(samples * 0.04))
bufferTot = buffer * (samples + round(samples * 0.04))
mgcl2Tot = mgcl2 * (samples + round(samples * 0.04))
bsaTot = bsa * (samples + round(samples * 0.04))
dntpTot = dntp * (samples + round(samples * 0.04))
taqTot = taq * (samples + round(samples * 0.04))

#Get individual mastermix volumes
indVol = water + buffer + mgcl2 + bsa + dntp + taq

#### MASTERMIX PREPARATION ####

#Transfer Water
s50.transfer(waterTot/2, reagent_rack.wells('A1'), reagent_rack.wells('C1'))
s50.transfer(waterTot/2, reagent_rack.wells('A1'), reagent_rack.wells('C2'))

#Transfer Buffer (dispense it from the top to avoid changing tip)
s50.transfer(bufferTot/2, reagent_rack.wells('A2'), reagent_rack.wells('C1').top())
s50.transfer(bufferTot/2, reagent_rack.wells('A2'), reagent_rack.wells('C2').top())

#Transfer MgCl2 (dispense it from the top to avoid changing tip)
s50.transfer(mgcl2Tot/2, reagent_rack.wells('A3'), reagent_rack.wells('C1').top())
s50.transfer(mgcl2Tot/2, reagent_rack.wells('A3'), reagent_rack.wells('C2').top())

#Transfer BSA (slower pipetting)
if bsaTot != 0:
    s50.set_flow_rate(aspirate=10, dispense=10)
    s50.transfer(bsaTot/2, reagent_rack.wells('A4'), reagent_rack.wells('C1'), new_tip='always')
    s50.transfer(bsaTot/2, reagent_rack.wells('A4'), reagent_rack.wells('C2'), new_tip='always')
    s50.set_flow_rate(aspirate=25, dispense=50)

#Transfer dNTP
s50.transfer(dntpTot/2, reagent_rack.wells('A5'), reagent_rack.wells('C1'), new_tip='always')
s50.transfer(dntpTot/2, reagent_rack.wells('A5'), reagent_rack.wells('C2'), new_tip='always')

#Pause to place polymerase in the rack
robot.pause()

#Transfer taqTot (slower pipetting) - mixing is very slow, need to think another strategy (mixing atomic is not working with space)
s50.set_flow_rate(aspirate=10, dispense=10)
s50.transfer(taqTot/2, reagent_rack.wells('A6'), reagent_rack.wells('C1'), new_tip='always', mix_after=(10, 50))
s50.transfer(taqTot/2, reagent_rack.wells('A6'), reagent_rack.wells('C2'), new_tip='always', mix_after=(10, 50))
s50.set_flow_rate(aspirate=25, dispense=50)


#### MASTERMIX DISTRIBUTION ####
s50.transfer(indVol, reagent_rack.wells('C1'), pcr_plate.cols('1','2','3','4','5','6'))
s50.transfer(indVol, reagent_rack.wells('C2'), pcr_plate.cols('7','8','9','10','11','12'))

#Pause to open primer lids
robot.pause()

#### PRIMER DISTRIBUTION ####
for col in list(range(len(primercols))):
    m10.transfer(primerVol, primer_plate.wells(primercols[col]), pcr_plate.wells(platecols[col]), new_tip='always', mix_before=(3, 10))
