import automator
import utility
import ntpath
import PySimpleGUI as sg

def main():
    valid_csv = False
    valid_template = False
    in_data = ''
    template = ''

    control_col = sg.Column([
        [sg.Text('Date of visit (MM/DD/YYYY):')],
        [sg.Input(key = '-DATE-')],
        [sg.Button('Open Template CSV', key = '-TEMP_OPEN-'), sg.Text('Template CSV:', key = '-TEMP_CSV-')],
        [sg.Button('Open CSV', key = '-OPEN-'), sg.Text('Input CSV:', key = '-INPUT_CSV-')],
        [sg.Button('Export', key = '-SAVE-')]])
    
    layout = [[control_col]]

    window = sg.Window('ANSWERS Automator', layout)

    while True:
        event, values = window.read(timeout = 50)
        if event == sg.WIN_CLOSED:
            break
        
        if event == '-TEMP_OPEN-':
            template_path = sg.popup_get_file('Open')
            if template_path != None:
                if template_path.endswith('.csv'):
                    valid_template = True
                    template = utility.load_csv(template_path)
                    template_name = ntpath.basename(template_path)
                    window['-TEMP_CSV-'].update('Template CSV: ' + template_name)
                else:
                    sg.popup('That is not a ".csv" file!')
        
        if event == '-OPEN-':
            open_path = sg.popup_get_file('Open')
            if open_path != None:
                if open_path.endswith('.csv'):
                    valid_csv = True
                    in_data = utility.load_csv(open_path)
                    csv_name = ntpath.basename(open_path)
                    window['-INPUT_CSV-'].update('Input CSV: ' + csv_name)
                else:
                    sg.popup('That is not a ".csv" file!')
        
        if event == '-SAVE-':
            date = values['-DATE-']
            # check if date and .csv file have been given
            if not valid_csv:
                sg.popup('No .csv file selected!')
            if not valid_template:
                sg.popup('No .csv file selected!')
            # if not len(date) == 10:
            #     sg.popup('Invalid date!')     and len(date) == 10
            if valid_csv:
                save_path = sg.popup_get_file('Save',save_as = True, no_window = True)
                out_data = automator.automate(in_data, template, date)
                utility.write_csv(out_data, save_path)
        
    window.close()

if __name__ == '__main__':
    main()