metadata = {
    'protocolName': 'Standard PCR primer mixing',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/03/05',
    'validation_date': 'XXXXX',
    'description': 'Standard protocol for PCR primer mixing',
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

#Water rack
tube_rack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '9', share=True)
  #A1 = 1.5 ml ddH2O
  #A2 = 1.5 ml ddH2O

#Forward primers rack
tube_rack2 = labware.load('opentrons-tuberack-2ml-eppendorf', '6', share=True)
  #A1-A6: Tag1-6
  #B1-B6: Tag7-12
  #C1-C6: Tag13-18
  #D1-D6: Tag19-24

#Reverse primers rack
tube_rack3 = labware.load('opentrons-tuberack-2ml-eppendorf', '3', share=True)
  #A1-A6: Tag1-6
  #B1-B6: Tag7-12
  #C1-C6: Tag13-18
  #D1-D6: Tag19-24

#Primer mix rack
temp_deck = modules.load('tempdeck', '5') #an 96-well ice rack can be also used
temp_plate = labware.load('PCR-strip-tall', '2', share=True) #note that although no plate will be used, this is necessary

#### TIP RACKS ####
tiprack_200 = labware.load('labsolute-tiprack-200µl', '8')

#### PIPETTES ####
s50 = instruments.P50_Single(mount='left', tip_racks=[tiprack_200])

#### INPUT FILES ####

#Load data file
combinations=[]
forward=[]
forwardvol=[]
reverse=[]
reversevol=[]
water=[]
with open("/root/csv/primer_mixing_v1_map.csv", "r") as csvfile:
    settings = csv.reader(csvfile, delimiter=',')
    for i in settings:
        combinations.append(i[0])
        forward.append(i[1])
        forwardvol.append(i[2])
        reverse.append(i[3])
        reversevol.append(i[4])
        water.append(i[5])

combinations.pop(0)
forward.pop(0)
forwardvol.pop(0)
reverse.pop(0)
reversevol.pop(0)
water.pop(0)

#### PREPARATIONS ####

#Get number of combinations
combnumber = len(combinations)

# call the funciton
#tagmap = {'Tag1':'A1', 'Tag2':'A2', 'Tag3':'A3', 'Tag4':'A4', 'Tag5':'A5', 'Tag6':'A6', 'Tag7':'B1', 'Tag8':'B2', 'Tag9':'B3', 'Tag10':'B4', 'Tag11':'B5', 'Tag12':'B6', 'Tag13':'C1', 'Tag14':'C2', 'Tag15':'C3', 'Tag16':'C4', 'Tag17':'C5', 'Tag18':'C6', 'Tag19':'D1', 'Tag20':'D2', 'Tag21':'D3', 'Tag22':'D4', 'Tag23':'D5', 'Tag24':'D6'}

forwardPos=forward
reversePos=reverse

#Get mix well possition information
totalmixlist = ['A1','B1','C1','D1','E1','F1','G1','H1','A3','B3','C3','D3','E3','F3','G3','H3','A5','B5','C5','D5','E5','F5','G5','H5','A7','B7','C7','D7','E7','F7','G7','H7','A9','B9','C9','D9','E9','F9','G9','H9','A11','B11','C11','D11','E11','F11','G11','H11']
mixlist = totalmixlist[:combnumber]
mixlist_first = totalmixlist[:int(combnumber/2)] #first 50%
mixlist_last = totalmixlist[int(combnumber/2):combnumber] #last 50%

#### LIQUID HANDLING ####

#Transfer Water (without changing the tip)
s50.transfer(water, tube_rack1.wells('A1'), temp_plate.wells(mixlist_first))
s50.transfer(water, tube_rack1.wells('A2'), temp_plate.wells(mixlist_last))

#Transfer Forward primer (always changing the tip)
s50.transfer(forwardvol, tube_rack1.wells(forwardPos), temp_plate.wells(mixlist), new_tip='always')

#Transfer Reverse primer (always changing the tip)
s50.transfer(reversevol, tube_rack1.wells(reversePos), temp_plate.wells(mixlist), new_tip='always')
