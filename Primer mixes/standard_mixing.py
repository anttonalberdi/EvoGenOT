metadata = {
    'protocolName': 'Standard PCR primer mixing',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'creation_date': '2019/02/25',
    'validation_date': 'XXXXX',
    'description': 'Standard protocol for PCR primer mixing',
}

#### LIBRARIES ####
from opentrons import labware, instruments, modules, robot
import pandas as pd

#### MODULES ####

#Water rack
tube_rack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '9', share=True) #Reverse
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
ice_rack1 = labware.load('PCR-strip-tall', '2', share=True)

#### TIP RACKS ####
tiprack_200 = labware.load('labsolute-tiprack-200ul', '8')
tiprack_10 = labware.load('labsolute-tiprack-10ul', '5')

#### PIPETTES ####
s50 = instruments.P50_Single(mount='left', tip_racks=[tiprack_200])
s10 = instruments.P10_Single(mount='right', tip_racks=[tiprack_10])

#### INPUT FILES ####

#Load data files
tagdata = pd.read_csv("/Users/jpl786/github/EvoGenOT/Primer mixes/Primers/ANML.csv")
tagcomb = pd.read_csv("/Users/jpl786/github/EvoGenOT/Primer mixes/Primers/ANML.comb.v1.csv")
settings = pd.read_csv("/Users/jpl786/github/EvoGenOT/Primer mixes/Primers/ANML.settings.v1.csv")

#Get volumes
Fvol = pd.to_numeric(settings.Forward, downcast='integer')
Rvol = pd.to_numeric(settings.Reverse, downcast='integer')
Wvol = pd.to_numeric(settings.Water, downcast='integer')

#### PREPARATIONS ####

#Get number of combinations
combnumber = len(tagcomb)

#Subset selected combinations
taglist = tagdata[tagdata.Combination.isin(list(tagcomb['Combination']))]

#Get primer tube possition information
tagmap = {'Tag1':'A1', 'Tag2':'A2', 'Tag3':'A3', 'Tag4':'A4', 'Tag5':'A5', 'Tag6':'A6', 'Tag7':'B1', 'Tag8':'B2', 'Tag9':'B3', 'Tag10':'B4', 'Tag11':'B5', 'Tag12':'B6', 'Tag13':'C1', 'Tag14':'C2', 'Tag15':'C3', 'Tag16':'C4', 'Tag17':'C5', 'Tag18':'C6', 'Tag19':'D1', 'Tag20':'D2', 'Tag21':'D3', 'Tag22':'D4', 'Tag23':'D5', 'Tag24':'D6'}
forwardlist=list(taglist['Forward'].map(tagmap))
reverselist=list(taglist['Reverse'].map(tagmap))

#Get mix well possition information
totalmixlist = ['A1','B1','C1','D1','E1','F1','G1','H1','A3','B3','C3','D3','E3','F3','G3','H3','A5','B5','C5','D5','E5','F5','G5','H5','A7','B7','C7','D7','E7','F7','G7','H7','A9','B9','C9','D9','E9','F9','G9','H9','A11','B11','C11','D11','E11','F11','G11','H11']
mixlist = totalmixlist[:combnumber]
mixlist_first = totalmixlist[:combnumber/2]
mixlist_last = totalmixlist[(combnumber/2+1):combnumber/2]

#### LIQUID HANDLING ####

#Transfer Water (without changing the tip)
s50.transfer(Wvol, tube_rack3.wells('A1'), ice_rack1.wells(mixlist_first))
s50.transfer(Wvol, tube_rack3.wells('A2'), ice_rack1.wells(mixlist_last))

#Transfer Forward primer (always changing the tip)
s50.transfer(Fvol, tube_rack1.wells(forwardlist), ice_rack1.wells(mixlist), new_tip='always')

#Transfer Reverse primer (always changing the tip)
s50.transfer(Rvol, tube_rack1.wells(reverselist), ice_rack1.wells(mixlist), new_tip='always')
