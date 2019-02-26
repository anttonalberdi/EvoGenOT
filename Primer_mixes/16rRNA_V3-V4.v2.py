metadata = {
    'protocolName': '16rRNA_V3-V4',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '2.0',
    'date': '2019/14/02',
    'description': 'PCR mix for 16S rRNA (v3-v4) metabarcoding of bacteria',
    'primers': 'Forward: 341F (CCTAYGGGRBGCASCAG), Reverse: R806 (GGACTACNNGGGTATCTAAT)',
    'Comb1':'Tag1,Tag1'
    'Comb2':'Tag2,Tag2'
    'Comb3':'Tag3,Tag3'
    'Comb4':'Tag4,Tag4'
    'Comb5':'Tag5,Tag5'
    'Comb6':'Tag6,Tag6'
    'Comb7':'Tag7,Tag7'
    'Comb8':'Tag8,Tag8'
    'Comb9':'Tag9,Tag9'
    'Comb10':'Tag10,Tag10'
    'Comb11':'Tag11,Tag11'
    'Comb12':'Tag12,Tag12'
    'Comb13':'Tag13,Tag13'
    'Comb14':'Tag14,Tag14'
    'Comb15':'Tag15,Tag15'
    'Comb16':'Tag16,Tag16'
    'Comb17':'Tag17,Tag17'
    'Comb18':'Tag18,Tag18'
    'Comb19':'Tag19,Tag19'
    'Comb20':'Tag20,Tag20'
    'Comb21':'Tag21,Tag21'
    'Comb22':'Tag22,Tag22'
    'Comb23':'Tag23,Tag23'
    'Comb24':'Tag24,Tag24'
}

#### MODULES ####
tube_rack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '3') #Forward
  #A1-A6: Tag1-6
  #B1-B6: Tag7-12
  #C1-C6: Tag13-18
  #D1-D6: Tag19-24
tube_rack2 = labware.load('opentrons-tuberack-2ml-eppendorf', '6') #Reverse
  #A1-A6: Tag1-6
  #B1-B6: Tag7-12
  #C1-C6: Tag13-18
  #D1-D6: Tag19-24
tube_rack3 = labware.load('opentrons-tuberack-2ml-eppendorf', '9') #Reverse
  #A1 = 1.5 ml ddH2O
  #A2 = 1.5 ml ddH2O
ice_rack1 = labware.load('PCR-strip-tall', '2')

#### TIP RACKS ####
#300 ul tip racks in slots 5 and 8
tipracks_200 = labware.load('opentrons-tiprack-300ul', '5')

#### PIPETTES ####
s50 = instruments.P50_Single(mount='left', tip_racks=[tipracks_200])

############
# PROTOCOL #
############

Fvol=10
Rvol=10
Wvol=80

#Transfer water
s50.transfer(Wvol/2, tube_rack3.wells('A1'), ice_rack1.rows('1','3','5'), new_tip='never') 
s50.transfer(Wvol/2, tube_rack3.wells('A2'), ice_rack1.rows('1','3','5'), new_tip='never') 

#Transfer F
s50.transfer(Fvol, tube_rack1.wells('A1','A2','A3','A4','A5','A6','B1','B2'), ice_rack1.wells('A1','B1','C1','D1','E1','F1','G1','H1'), new_tip='always') 
s50.transfer(Fvol, tube_rack1.wells('B3','B4','B5','B6','C1','C2','C3','C4'), ice_rack1.wells('A3','B3','C3','D3','E3','F3','G3','H3'), new_tip='always') 
s50.transfer(Fvol, tube_rack1.wells('C5','C6','D1','D2','D3','D4','D5','D6'), ice_rack1.wells('A5','B5','C5','D5','E5','F5','G5','H5'), new_tip='always') 

#Transfer R
s50.transfer(Rvol, tube_rack2.wells('A1','A2','A3','A4','A5','A6','B1','B2'), ice_rack1.wells('A1','B1','C1','D1','E1','F1','G1','H1'), new_tip='always') 
s50.transfer(Rvol, tube_rack2.wells('B3','B4','B5','B6','C1','C2','C3','C4'), ice_rack1.wells('A3','B3','C3','D3','E3','F3','G3','H3'), new_tip='always') 
s50.transfer(Rvol, tube_rack2.wells('C5','C6','D1','D2','D3','D4','D5','D6'), ice_rack1.wells('A5','B5','C5','D5','E5','F5','G5','H5'), new_tip='always') 
