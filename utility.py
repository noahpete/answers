import csv
import os

EXAMPLE_CSV = 'eg_input.csv'
OUTPUT_CSV_NAME = 'redcap_data.csv'
OUTPUT_TEMPLATE = 'export_template.csv'
OUTPUT_DATA_COL = 3
LABS = {'platelet': 'Platelet Count',
        'abs_neutrophil': 'Absolute Neutrophil Count',
        'west_rbc': 'WESTEGREN RBC SEDI RATE',
        'creatinine': 'CREATININE LEVEL',
        'crp': 'C-REACTIVE PROTEIN SCREEN',
        'vitamin_d': '25-Hydroxyvitamin D, Total',
        'inr': 'INR',
        'd_dimer': 'D-Dimer',
        'chromo_x': 'Chromogenic Factor X',
        'ana': 'NUCLEAR ANTIBODY',
        'sm': 'ANTI-SM',
        'rnp': 'ANTI-RNP',
        'smrnp': 'ANTI-SmRNP',
        'ssa': 'ANTI-SSA/ANTI-RO',
        'ssb': 'ANTI-SSB/ANTI-LA',
        'jo1': 'AUTOANTIBODIES TO JO1 ANTIGEN',
        'scl': 'ANTI SCLERODERMA AB TO 70 AG',
        'ribo_prot': 'RIBOSOMAL PROTEIN',
        'chromatin': 'CHROMATIN',
        'centromere': 'CENTROMERE B',
        'anti_dsdna': 'ANTI-dsDNA ANTIBODY',
        'c3': 'C3 COMPLEMENT',
        'c4': 'C4 COMPLEMENT',
        'prot_creat': 'PROTEIN/CREAT'} # 'PROTEIN/CREAT URINE RATIO' or 'PROTEIN/CREAT RATIO URINE'
ENA_LABS = ['sm', 'rnp', 'smrnp', 'ssa', 'ssb', 'jo1', 'scl', 'ribo_prot',
            'chromatin', 'centromere']
RANGES = {'platelet': [150 , 400],
        'abs_neutrophil': (1.5, 7.2),
        'west_rbc': (0, 20),
        'creatinine': (0.50, 1.00),
        'crp': (0.0, 0.6),
        'vitamin_d': [25, 100], # range is sometimes 25-100, other times 30-100
        'inr': None, # relative reference range, most common 2-3
        'd_dimer': (0.00, 0.58),
        'chromo_x': None,
        'ana': 'Negative',
        'sm': 'Negative',
        'rnp': 'Negative',
        'smrnp': 'Negative',
        'ssa': 'Negative',
        'ssb': 'Negative',
        'jo1': 'Negative',
        'scl': 'Negative',
        'ribo_prot': 'Negative',
        'chromatin': 'Negative',
        'centromere': 'Negative',
        'anti_dsdna': (0.00, 26.9),
        'c3': (83, 240),
        'c4': (13, 60),
        'prot_creat': (0.01, 0.18)}
# EXPORT_TEMPLATE_BAD = [['ANSWER Code',,'studyid','value'],
#                         ['Visit', 'followup_visit_#_arm_1', 'redcap_event_name']
#                    ['What was the platelet value?', 'text (number, Min: 0, Max: 1000)', 'cbcplt_enrollfu',],
#                    ['Was the platelet value low, high, or within the "normal" range?', '0=Low;1=High; 2=Within the range', 'cbcplttest_enrollfu',],

'''
# Effects: imports .csv file whose name is
#          input_csv and returns a 2D list
#          of the data
'''
def load_csv(input_csv):
    data = []
    with open(input_csv) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
        return data

'''
# Effects: generates a csv file with out_name
#          using the data from data
'''
def write_csv(data, out_name):
    if os.path.exists(f'{out_name}.csv'):
        i = 0
        while os.path.exists(f'{out_name}%s.csv' % i):
            i += 1
    
        with open(f'{out_name}%s.csv' % i, 'x') as new_file:
            writer = csv.writer(new_file)
            for row in data:
                writer.writerow(row)
    else:
        with open(f'{out_name}.csv', 'x') as new_file:
            writer = csv.writer(new_file)
            for row in data:
                writer.writerow(row)

# TODO:
'''
# Effects: converts any date format into whichever
#          format is used by the input data
'''
def convert_date(date, input_format = 'MM/DD/YYYY'):
    day = 0
    month = 0
    year = 0
    if input_format == 'MM/DD/YYYY':
        pass



'''
# Effects: returns the value of a lab
#          from data that has date and
#          lab in the same row
# Returns: lab value as string
'''
def get_lab_val(data, date, lab):
    for row in data:
        if len(row) > 4:
            if date in row[2] and LABS.get(lab) in row[3]:
                return row[4]

'''
# Effects: checks to see if relevant cbc test values
#          with correct date are present (platelet,
#          abs neutrophil, western rbc) and returns
#          true if any values are present, false if
#          none are available
'''
def check_cbc(data, date):
    platelet = get_lab_val(data, date, 'platelet')
    neutrophil = get_lab_val(data, date, 'abs_neutrophil')
    western = get_lab_val(data, date, 'west_rbc')
    
    # return false if all 3 values aren't there
    if platelet == None and neutrophil == None and western == None:
        return False
    else:
        return True

'''
# Effects: checks to see if relevant chem test values
#          with correct date are present (creatinine,
#          crp, vitamin d) and returns true if any
#          values are present, false if none available
'''
def check_chem(data, date):
    creatinine = get_lab_val(data, date, 'creatinine')
    crp = get_lab_val(data, date, 'crp')
    vitamin_d = get_lab_val(data, date, 'vitamin_d')

    # return false if all 3 values aren't there
    if creatinine == None and crp == None and vitamin_d == None:
        return False
    else:
        return True

'''
# Effects: checks to see if lab (from LABS) value
#          with correct date is present and returns
#          true if value present, else false
'''
def check_lab(data, date, lab):
    lab_value = get_lab_val(data, date, lab)

    # return false if value not present
    if lab_value == None:
        return False
    else:
        return True

'''
# Effects: assuming lab with date is present in
#          data, returns 0 if value is low, 1 is
#          high, 2 is within range, value must be
#          a float or int!
'''
def check_range(lab, value):
    if RANGES[lab] == None:
        return ''
    elif float(value) < RANGES[lab][0]:
        return 0
    elif float(value) > RANGES[lab][1]:
        return 1
    else:
        return 2

'''
# Effects: checks if lab exists, then fills out
#          value cell and range cell for lab;
#          out_row is the index of the row
#          containing the lab in the output file
'''
def fill_out_lab(input_data, output_data, date, lab, out_row):
    # special case for inr, chromo_x
    if ((lab == 'inr' or lab == 'chromo_x')
        and check_lab(input_data, date, lab)):
        lab_value = get_lab_val(input_data, date, lab)
        output_data[out_row][OUTPUT_DATA_COL] = lab_value
    elif check_lab(input_data, date, lab):
        lab_value = get_lab_val(input_data, date, lab)
        output_data[out_row][OUTPUT_DATA_COL] = lab_value
        output_data[out_row + 1][OUTPUT_DATA_COL] = check_range(lab, lab_value)
    else:
        output_data[out_row][OUTPUT_DATA_COL] = '0'
        if 'low, high, or within' in output_data[out_row + 1][0]:
            output_data[out_row + 1][OUTPUT_DATA_COL] = '2'

'''
# Effects: does same thing as fill_out_lab but
#          for labs that require checking first
'''
def fill_check_lab(input_data, output_data, date, lab, out_val_row):
    if check_lab(input_data, date, lab):
        output_data[out_val_row - 1][OUTPUT_DATA_COL] = '1'
        fill_out_lab(input_data, output_data, date, lab, out_val_row)
    else:
        # special cases where no = '0' rather than '2'
        if (lab == 'd_dimer' or lab == 'chromo_x' or lab == 'anti-dsDNA' or
            lab == 'c3' or lab == 'c4' or lab == 'prot_creat'):
            output_data[out_val_row - 1][OUTPUT_DATA_COL] = '0'
        else:
            output_data[out_val_row - 1][OUTPUT_DATA_COL] = '2'

'''
# Effects: fills out labs that have results that
#          are either Positive or Negative and
#          require checking, where Negative is
#          indicated with a '0'
'''
def fill_check_binary_lab(input_data, output_data, date, lab, out_val_row):
    if check_lab(input_data, date, lab):
        output_data[out_val_row - 1][OUTPUT_DATA_COL] = '1'
        if get_lab_val(input_data, date, lab) == 'Negative':
            output_data[out_val_row][OUTPUT_DATA_COL] = '0'
        else:
            output_data[out_val_row][OUTPUT_DATA_COL] = '1'
    else:
        output_data[out_val_row - 1][OUTPUT_DATA_COL] = '0'

'''
# Effects: fills out labs that are either Pos or Neg,
#          but is tailored for ena labs'''
def fill_binary_lab(input_data, output_data, date, lab, out_val_row):
    if get_lab_val(input_data, date, lab) == 'Negative':
        output_data[out_val_row][OUTPUT_DATA_COL] = '0'
    else:
        output_data[out_val_row][OUTPUT_DATA_COL] = '1'

'''
# Effects: checks to see if ALL ena labs are 
#          present and returns true if all are
#          else false
'''
# TODO: ***TEST THIS***
def check_ena_labs(input_data, date):
    values_present = []
    for lab in ENA_LABS:
        if check_lab(input_data, date, lab):
            values_present.append(lab)
    return values_present == ENA_LABS

'''
# Effects: fills out all ena labs
'''
def fill_ena_labs(input_data, output_data, date):
    i = 0
    for lab in ENA_LABS:
        fill_binary_lab(input_data, output_data, date, lab, 32 + i)
        i += 1

