# EvoGenOT
UCPH's EvoGenomics section's Opentrons protocol library.

## Protocol development steps

1. Write the python code
2. Validate the code in the Opentrons software
3. Test the protocol without plasticware (only pipettes)
4. Test the protocol with plasticware and dummy reagents
5. Test the protocol with actual reagents

## Common nomenclature

### Pipettes
Code | Description 
------------ | -------------
s10 | 1-10 ul single channel pipette
m300 | 30-300 ul multichannel pipette
