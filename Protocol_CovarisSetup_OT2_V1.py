#################################
### Covaris plate preparation ###
#################################

## Author Jonas Greve Lauritsen
## Automatic preparation of covaris plates based on csv input

##################################

## Tips available
First_Tip50 = "A2"   ## Input first (clean) tip position for 50 µL tips. Examples "A2" or "H12".
First_Tip10 = "B4"   ## Input first (clean) tip position for 10 µL tips. Examples "A2" or "H12".
First_Covaris_Well= "A2" ## Input first well available in the covaris plate. Examples "A1" or "A5".

#### User Inputs ####
## CSV input - Copy & paste from csv file. Data input shall be flanked by ''' before and after input. 
# "," is the delimiter. Use the names "Well", "Sample_Input_Vol", and "H2O_Input_Vol" as headers in the csv input.
csv_raw = '''
Well,Sample,DNA_Conc,End_Vol,End_Weight,Sample_Input_Vol,H2O_Input_Vol,Total_Input_Weight,Input_Adaptor_Conc
H1,L16,0.457,28,200,28.00,0.00,12.796,10
G1,L17,0.758,28,200,28.00,0.00,21.224,10
F1,L18,0.433,28,200,28.00,0.00,12.124,10
E1,L19,0.495,28,200,28.00,0.00,13.86,10
D1,L20,0.519,28,200,28.00,0.00,14.532,10
C1,K - B27,0,28,200,28.00,0.00,0,10
B1,W1,0.093,28,200,28.00,0.00,2.604,10
A1,W2,0.092,28,200,28.00,0.00,2.576,10
H2,J16,3.62,28,200,28.00,0.00,101.36,20
G2,J17,16.3,28,200,12.27,15.73,200,20
F2,J18,10.4,28,200,19.23,8.77,200,20
E2,J19,7.79,28,200,25.67,2.33,200,20
D2,J20,9.66,28,200,20.70,7.30,200,20
C2,K - B32,0,28,200,28.00,0.00,0,10
B2,W3,0.09,28,200,28.00,0.00,2.52,10
A2,W4,0.083,28,200,28,0,2.324,10
'''


##################################

#### Package loading ####
from opentrons import protocol_api

#### Function to convert copied csv data into a 2D list. ####
def csv_list_converter_covaris(csv_raw):
    import csv
    csv_data = csv_raw.splitlines()[1:]
    csv_reader = csv.DictReader(csv_data)
    Excel = [['Well','Sample_Input_Vol','H2O_Input_Vol']]
    for csv_row in csv_reader:
        Info= [csv_row['Well'], float(csv_row['Sample_Input_Vol']), float(csv_row['H2O_Input_Vol'])]
        Excel.append(Info)
    return(Excel)

#### Function to reposition the sample well to the covaris plate. ####
def Covaris_Plate_Well_Repositioner(Sample_Well,Covaris_Well):
    WellName = ['A1','B1','C1','D1','E1','F1','G1','H1',
    'A2','B2','C2','D2','E2','F2','G2','H2',
    'A3','B3','C3','D3','E3','F3','G3','H3',
    'A4','B4','C4','D4','E4','F4','G4','H4',
    'A5','B5','C5','D5','E5','F5','G5','H5',
    'A6','B6','C6','D6','E6','F6','G6','H6',
    'A7','B7','C7','D7','E7','F7','G7','H7',
    'A8','B8','C8','D8','E8','F8','G8','H8',
    'A9','B9','C9','D9','E9','F9','G9','H9',
    'A10','B10','C10','D10','E10','F10','G10','H10',
    'A11','B11','C11','D11','E11','F11','G11','H11',
    'A12','B12','C12','D12','E12','F12','G12','H12']
    Wellindex = WellName.index(Sample_Well) + WellName.index(Covaris_Well)
    return(Wellindex)


#### Meta Data ####
metadata = {
    'protocolName': 'Covaris Setup',
    'apiLevel': '2.12',
    'author': 'Jonas Lauritsen <jonas.lauritsen@sund.ku.dk>',
    'description': 'Covaris plate setup with user CSV input for automatic dilutions'}

#### Protocol Script ####
def run(protocol: protocol_api.ProtocolContext):

    #### Converts csv paste into a 2D list ####
    Excel = csv_list_converter_covaris(csv_raw)
    Excel = Excel[1:] #Removes headers - Header indices are: [0] Well, [1] Sample_Input_Vol, & [2] Sample_Input_Vol.


    #### LABWARE SETUP ####
    ## Placement of smart and dumb labware.

    ## Sample Plate - Placed in thermocycler
    Input_plate = protocol.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul',4) #Update
    Storage_plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',5) #Update
    Covaris_plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',6) #Customlabware maybe?

    ##Waterposition
    H2O = protocol.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap',9).wells_by_name()["A1"] #Update tubetype

    ## Tip racks (2x 10 µL, 2x 200 µl)
    tiprack_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul',10)
    tiprack_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul',11)
    tiprack_10_1 = protocol.load_labware('opentrons_96_filtertiprack_10ul',7)
    tiprack_10_2 = protocol.load_labware('opentrons_96_filtertiprack_10ul',8)


    #### PIPETTE SETUP ####
    ## Loading pipettes
    p20 = protocol.load_instrument('p10_single', mount='left', tip_racks=(tiprack_10_1,tiprack_10_2))
    p50 = protocol.load_instrument('p50_single', mount='right', tip_racks=(tiprack_200_1,tiprack_200_2))

    ## Setting start tips
    p20.starting_tip = tiprack_10_1.well(First_Tip10)
    p50.starting_tip = tiprack_200_1.well(First_Tip50)



    #### Lab Work Protocol ####
    ## The instructions for the robot to execute.

    ## Loop for mixing samples and moving to  cherrypicking samples
    for i in range(len(Excel)):

        ## Variable definitions for the functions - increases readability of the script.
        Well_pos = Excel[i][0] # Variable setup for well (readability)
        Covaris_Well_pos = Covaris_Plate_Well_Repositioner(Sample_Well = Well_pos,Covaris_Well=First_Covaris_Well) # Repositions the well to covaris
        Sample_Input = Excel[i][1] # Variable setup for sample input (readability)
        H2O_Input = Excel[i][2] # Variable setup for H2O input (readability)


        ## If the sample input volume is equal or greater to 5 µL, and the water input is lower than 5 µL:
        if Sample_Input >= 5 and H2O_Input < 5:

            ## Adding water first if input volume is greater than 0. If command is here to prohibit picking up tips and disposing them without a transfer.
            if H2O_Input>0:
                p20.transfer(volume = H2O_Input, source=H2O,dest=Storage_plate.wells_by_name()[Well_pos], new_tip='always') #Transfer pick up new tip

            ## Adding sample to the water.
            p50.pick_up_tip()
            p50.transfer(volume = Sample_Input, source = Input_plate.wells_by_name()[Well_pos], dest = Storage_plate.wells_by_name()[Well_pos],new_tip = 'never', mix_after=(5,15)) #µL

            ## Moving samples mix to covaris plate. The tip is kept between storage plate and covaris plate.
            p50.transfer(volume = 25, source = Storage_plate.wells_by_name()[Well_pos],dest= Covaris_plate.wells()[Covaris_Well_pos],new_tip = 'never') #µL                       #µL
            p50.drop_tip()

        ## If the sample input volume is equal or greater to 5 µL, and the water input is also equal or greater than 5 µL:
        if Sample_Input >= 5 and H2O_Input >= 5:

            ## Aspirating H2O then sample and dispense them together into the storage plate. Both volume are aspirated together to save time.
            p50.pick_up_tip()
            p50.aspirate(volume = H2O_Input, location = H2O) # First pickup
            p50.touch_tip(location = H2O) # Touching the side of the well to remove excess water.
            p50.aspirate(volume = Sample_Input, location = Input_plate.wells_by_name()[Well_pos]) # Second pickup                       #µL
            p50.dispense(volume = 30, location = Storage_plate.wells_by_name()[Well_pos]) #µL , 30 µL dispense to empty completely
            p50.mix(repetitions = 5, volume = 15, location = Storage_plate.wells_by_name()[Well_pos])

            ## Moving samples mix to covaris plate
            p50.transfer(volume = 25, source = Storage_plate.wells_by_name()[Well_pos],dest = Covaris_plate.wells()[Covaris_Well_pos], new_tip='never') #µL
            p50.drop_tip()

        ## If sample input volume is less than 5 µL. (Water input volume is always above 5 µL)
        if Sample_Input < 5:
            ## Adding sample to storage plate.
            p20.transfer(volume = Sample_Input, source = Input_plate.wells_by_name()[Well_pos],dest=Storage_plate.wells_by_name()[Well_pos], new_tip = 'always') #µL

            ## Dispensing H2O  into a storage plate.
            p50.pick_up_tip()
            p50.transfer(volume = H2O_Input, source = H2O,dest = Storage_plate.wells_by_name()[Well_pos],touch_tip=True,new_tip = 'never',mix_after = (5,15)) #µL

            ## Moving samples mix to covaris plate from storage plate. The tip is kept from the initial water transfer for the well.
            p50.transfer(volume = 25, source = Storage_plate.wells_by_name()[Well_pos], dest= Covaris_plate.wells()[Covaris_Well_pos],new_tip ='never') #µL
            p50.drop_tip()


    protocol.comment("STATUS: Protocol Completed.")
