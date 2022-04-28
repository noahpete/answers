import csv
import os
import utility

EXPORT_TEMPLATE = 'export_template.csv'

def automate(in_data, template, date):
    # load output template as 2D list
    out_data = template

    # was a cbc test performed?
    print('Checking CBC tests')
    if not utility.check_cbc(in_data, date):
        out_data[3][utility.OUTPUT_DATA_COL] = '2'
    else:
        out_data[3][utility.OUTPUT_DATA_COL] = '1'
        # platelet count
        utility.fill_out_lab(in_data, out_data, date, 'platelet', 4)
        # absolute neutrophil count
        utility.fill_out_lab(in_data, out_data, date, 'abs_neutrophil', 6)
        # westergren rbc
        utility.fill_check_lab(in_data, out_data, date, 'west_rbc', 9)
        
    # was a chem profile test performed?
    print('Checking Chem tests')
    if not utility.check_chem(in_data, date):
        out_data[11][utility.OUTPUT_DATA_COL] = '2'
    else:
        out_data[11][utility.OUTPUT_DATA_COL] = '1'
        # creatinine
        utility.fill_out_lab(in_data, out_data, date, 'creatinine', 12)
        # crp
        utility.fill_check_lab(in_data, out_data, date, 'crp', 15)
        # 25-hydroxy vit d
        utility.fill_check_lab(in_data, out_data, date, 'vitamin_d', 18)
    
    # coagulation (inr, d-dimer, chromo x)
    print('Checking Coag tests')
    # inr
    utility.fill_check_lab(in_data, out_data, date, 'inr', 21)
    # d-dimer
    utility.fill_check_lab(in_data, out_data, date, 'd_dimer', 25)
    # chromo x (special case accounted for in function)
    utility.fill_check_lab(in_data, out_data, date, 'chromo_x', 28)

    # ana/ena, anti-dsDNA
    print('Checking ANA/ENA tests')
    # ana
    utility.fill_check_binary_lab(in_data, out_data, date, 'ana', 30)
    # ena
    if utility.check_ena_labs(in_data, date):
        out_data[31][utility.OUTPUT_DATA_COL] = '1'
        utility.fill_ena_labs(in_data, out_data, date)
    else:
        out_data[31][utility.OUTPUT_DATA_COL] = '0'
    # anti-dsDNA
    utility.fill_check_lab(in_data, out_data, date, 'anti_dsdna', 43)

    # complements
    # c3
    utility.fill_check_lab(in_data, out_data, date, 'c3', 46)
    # c4
    utility.fill_check_lab(in_data, out_data, date, 'c4', 49)

    # urine protein/creatine ratio val
    utility.fill_check_lab(in_data, out_data, date, 'prot_creat', 52)

    # mark complete
    print('Complete')
    out_data[54][utility.OUTPUT_DATA_COL] = '2'
    # utility.write_csv(out_data, 'redcap_test_data')
    return out_data