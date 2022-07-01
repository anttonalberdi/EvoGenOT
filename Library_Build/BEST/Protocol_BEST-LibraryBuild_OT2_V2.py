############################
### BEST - Library build ###
############################

## Author Jonas Greve Lauritsen
## Adaptation of the library build.

##### User Data Input #####
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

#### Package loading ####
from math import *
from opentrons import protocol_api


#### Function to convert copied csv data into a 2D list. ####
def csv_list_converter_BEST(csv_raw):
    import csv
    csv_data = csv_raw.splitlines()[1:]
    csv_reader = csv.DictReader(csv_data)
    Excel = [['Well','Input_Adaptor_Conc']]
    for csv_row in csv_reader:
        Info= [csv_row['Well'], float(csv_row['Input_Adaptor_Conc'])]
        Excel.append(Info)
    return(Excel)


#### METADATA ####
metadata = {
    'protocolName': 'BEST_Protocol',
    'apiLevel': '2.12',
    'author': 'Jonas Greve Lauritsen <jonas.lauritsen@sund.ku.dk>',
    'description': 'Automated library preparation of DNA samples (96 version)'
    }


#### Protocol script ####
def run(protocol: protocol_api.ProtocolContext):

    #### LABWARE SETUP ####
    ## Placement of smart and dumb labware.
    ## Smart labware; thermocycler and temperature modules.
    thermo_module = protocol.load_module('thermocycler')
    cold_module = protocol.load_module('temperature module',1) 

    ## Sample Plate - Placed in thermocycler. 
    Sample_plate = thermo_module.load_labware('biorad_96_wellplate_200ul_pcr')

    ## Tip racks (4x 10 µL)
    tiprack_10_1 = protocol.load_labware('opentrons_96_filtertiprack_10ul',9)
    tiprack_10_2 = protocol.load_labware('opentrons_96_filtertiprack_10ul',6)
    tiprack_10_3 = protocol.load_labware('opentrons_96_filtertiprack_10ul',3)
    tiprack_10_4 = protocol.load_labware('opentrons_96_filtertiprack_10ul',2)

    ## Mastermix Setup
    cold_plate = cold_module.load_labware('opentrons_96_aluminumblock_nest_wellplate_100ul')

    End_Repair_Mix = cold_plate.wells_by_name()["A1"]
    Adaptors_10mM = cold_plate.wells_by_name()["A3"]    
    Adaptors_20mM = cold_plate.wells_by_name()["C3"]    
    Ligation_Mix = cold_plate.wells_by_name()["A5"]
    Nick_Fill_In_Mix = cold_plate.wells_by_name()["A7"]
        

    #### PIPETTE SETUP ####
    m20 = protocol.load_instrument('p20_multi_gen2', mount='right', tip_racks=(tiprack_10_1,tiprack_10_3,tiprack_10_4))
    p10 = protocol.load_instrument('p10_single',mount='left', tip_racks= tiprack_10_2)

    #### Converts csv paste into a 2D list ####
    Excel = csv_list_converter_BEST(csv_raw)
    Excel = Excel[1:] #Removes headers - Header indices are: [0] Well, & [1] Input_Adaptor_Conc
    
    ## Column setup
    Col_number = int(ceil(len(Excel)/8)) # Scales number of columns in used based on csv data.
    col_name = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12"] # Column is named by top well.


    #### Lab Work Protocol ####
    ## The instructions for the robot to execute.
    
    ## Initial activation of thermocycler module. Activate temperature module early in setup to reduce time waste.
    protocol.comment("STATUS: Activating Modules")
    cold_module.set_temperature(4)
    thermo_module.open_lid()
    thermo_module.set_block_temperature(4)
    thermo_module.set_lid_temperature(105)

 
    ### First step - End repair reaction ###
    ## Transfering End Repair Mix
    protocol.comment("STATUS: End Repair step begun")
    for i in range(Col_number):
        m20.pick_up_tip(tiprack_10_1.wells_by_name()[col_name[i]])
        m20.transfer(volume = 5.85, source = End_Repair_Mix, dest = Sample_plate.wells_by_name()[col_name[i]],mix_before =(2,10),mix_after=(5,10),new_tip='never') #µL
        m20.return_tip()    

    ## End Repair Incubation
    protocol.comment("STATUS: End Repair Incubation Begun")
    thermo_module.close_lid()
    profile = [
        {'temperature':20, 'hold_time_minutes':30},
        {'temperature':65, 'hold_time_minutes':30}]
    thermo_module.execute_profile(steps=profile,repetitions=1,block_max_volume=30)
    thermo_module.set_block_temperature(4)
    thermo_module.open_lid()
    

    ### Second step - Adaptors and Ligation ###
    protocol.comment("STATUS: Adaptor step begun")
    ## Transferring Adaptors. The adaptor concentration is chosen based on the csv input.
    for i in range(len(Excel)):
        p10.pick_up_tip(tiprack_10_2.wells_by_index[i])
        if Excel[i][1] == 20:
            p10.transfer(volume = 1.5, source = Adaptors_20mM, dest = Sample_plate.wells_by_name()[Excel[i][0]],mix_before= (2,10),mix_after=(5,10),new_tip='never')
        if Excel[i][1] == 10:
            p10.transfer(volume = 1.5, source = Adaptors_10mM, dest = Sample_plate.wells_by_name()[Excel[i][0]],mix_before= (2,10),mix_after=(5,10),new_tip='never')
        p10.return_tip


    ## Transfering Ligation Mix 
    ## Changing flowrate for aspiration & dispension, as PEG4000 is viscous and requires slowed pipetting.
    protocol.comment("STATUS: Ligation step begun")
    m20.flow_rate.aspirate = 2 #µL/s
    m20.flow_rate.dispense = 2 #µL/s

    ## Ligation Pipetting
    for i in range(Col_number):
        ## Aspiration, mixing, and dispersion. Extra delays to allow viscous liquids to aspirate/dispense.
        m20.pick_up_tip(tiprack_10_3.wells_by_name()[col_name[i]])
        m20.mix(repetitions = 3, volume = 10, location = Ligation_Mix,rate = 1) #Maybe not include, due to boble-PEG4000 creation          
        m20.aspirate(volume = 6, location = Ligation_Mix) 
        protocol.delay(5) 
        m20.move_to(location = Ligation_Mix.top()) #Moving tips up out of liquid and delays
        protocol.delay(10)
        m20.dispense(volume = 6, location = Sample_plate.wells_by_name()[col_name[i]]) #µL
        m20.mix(repetitions = 3, volume = 10, location = Sample_plate.wells_by_name()[col_name[i]],rate = 10)
        protocol.delay(5)
        m20.move_to(location = Sample_plate.wells_by_name()[col_name[i]].top()) #Moving tips up out of liquid and delays
        protocol.delay(5)
        m20.return_tip()
        
    ## Ligation Incubation
    protocol.comment("STATUS: Second incubation step begun")
    thermo_module.close_lid()
    profile = [
        {'temperature':20, 'hold_time_minutes':30},     # Celsius, Mins
        {'temperature':65, 'hold_time_minutes':10}]     # Celsius, Mins
    thermo_module.execute_profile(steps=profile,repetitions=1,block_max_volume=36)
    thermo_module.set_block_temperature(4)
    thermo_module.open_lid()
    


    ### Third step - Fill-In Reaction ###
    protocol.comment("STATUS: Fill-In step begun")

    ## Transfering Fill-In reaction mix
    ## Changing flowrate for aspiration & dispension (7.6 µL/s is default for 20 µL multichannel pipettes).
    m20.flow_rate.aspirate = 7.6 #µL/s
    m20.flow_rate.dispense = 7.6 #µL/s

    ## Fill-in Reaction pipetting
    for i in range(Col_number):
        m20.pick_up_tip(tiprack_10_4.wells_by_name()[col_name[i]])            
        m20.transfer(volume = 7.5, source = Nick_Fill_In_Mix, dest = Sample_plate.wells_by_name()[col_name[i]],mix_before=(2,10),mix_after=(5,10),new_tip='never')#µL
        m20.return_tip() 

    ## Fill-In Incubation
    protocol.comment("STATUS: Third incubation step begun")
    thermo_module.close_lid()
    profile = [
        {'temperature':65, 'hold_time_minutes':15}, # Celsius, Mins
        {'temperature':80, 'hold_time_minutes':15}] # Celsius, Mins
    thermo_module.execute_profile(steps=profile,repetitions=1,block_max_volume=43.5)
    thermo_module.set_block_temperature(4)
    thermo_module.open_lid()


    ### Protocol finished ###
    protocol.pause("STATUS: Protocol Completed.")

    ## Shuts down modules
    thermo_module.deactivate()
    cold_module.deactivate()