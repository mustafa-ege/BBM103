# Mustafa EGE b2210356088

def read_the_input_file(): # converts the input text file into a list whose elements are the lines of text file
    with open('doctors_aid_inputs.txt','r') as inputfile:
        return inputfile.readlines()

def organized_input(): # organizes the the list as [[func, patient 1 info],[func, patient 2 info],[...]]
    organized_list= []
    for line in read_the_input_file():
        input_patient_list = line.split(', ')
        input_patient_list = input_patient_list[0].split()+ (input_patient_list[1:])
        organized_list.append(input_patient_list)
    return organized_list

def save_output(entry): #creates a text file doctors_aid_outputs.txt and writes onto it
    with open('doctors_aid_outputs.txt','a') as outputfile:
        outputfile.write(entry)

patients_list = []

def create(input_line): #for creating patients and appending them into patients_list
    global patients_list
    patients_list_name = [i[0] for i in patients_list] # gets only the name of the patient
    input_line[2] = format(float(input_line[2])*100, '.2f') # makes the decimal of the percantage 2 digits 
    input_line[6] = int(float(input_line[6])*100) # makes a percentage
    while True:
        if input_line[1] in patients_list_name:
            save_output(f'Patient {input_line[1]} cannot be recorded due to duplication.\n')
            break
        else:
            patient = [i for i in input_line if i!='create'] # appends without the function name 'create'
            patients_list.append(patient)
            save_output(f'Patient {input_line[1]} is recorded.\n')
            break 

def remove(input_line):  #deletes a patient from patients_list
    patients_list_names = [i[0] for i in patients_list]
    while True:
        if input_line[1] in patients_list_names: #checks if the patient exists in the list
            for patient in patients_list:
                if input_line[1] in patient:
                    save_output(f'Patient {patient[0]} is removed.\n')
                    patients_list.remove(patient)
                    break                        
        else:
            save_output(f'Patient {input_line[1]} cannot be removed due to absence\n')
        break

def list():
    global patients_list
    titles = ['Patient Name', 'Diagnosis Accuracy', 'Disease Name', 'Disease Incidence' ,'Treatment Name', 'Treatment Risk']
    titlesfirst = [i.split()[0] for i in titles] # first words patient, diagnosis.. 
    titlessecond = [i.split()[1] for i in titles] # second words name, accuracy...
    patients_list_2 = [i.copy() for i in patients_list] 

    for i in patients_list_2: # we need to add % for the better look in the table so we need a copy of patients list 
        i[1] = i[1] + '%'
        i[5] = str(i[5]) + '%'

    save_output('{:<8}{:<16}{:<24}{:<16}{:<24}{}\n'.format(*titlesfirst)) # {:<} makes the words align with the columns 
    save_output('{:<8}{:<16}{:<24}{:<16}{:<24}{}\n'.format(*titlessecond)) # 8 16 and 24 in brackets make the space between words same with \t tab
    save_output('-'*97) 
    save_output('\n')
    for i in patients_list_2:      
        save_output('{:<8}{:<16}{:<24}{:<16}{:<24}{:<20}\n'.format(*i))

def which_patient(name): # this function gets the patient's index in the list by taking the patient name
    for i in patients_list:
        if i[0] == name:
            return patients_list.index(i)
        else:
            pass

def probability(the_patient,type=None): # calculates the false positive probability 
    if which_patient(the_patient)!= None:
        patient_index = which_patient(the_patient) #gets the index 
        total_number_of_people = patients_list[patient_index][3].split('/')[1] # denominator of disease incidence
        correctly_diagnosed_people = int(patients_list[which_patient(the_patient)][3].split('/')[0]) #numerator of disease incidence
        diagnose_accuracy = patients_list[which_patient(the_patient)][1] #diagnosis accuracy
        wrongly_diagnosed_people = (int(total_number_of_people) * (100-float(diagnose_accuracy)))/100
        total_number_of_diagnosed_people = correctly_diagnosed_people + wrongly_diagnosed_people
        false_positive_possibility = round((correctly_diagnosed_people / total_number_of_diagnosed_people *100),2)
        if false_positive_possibility-int(false_positive_possibility)== 0: #to convert numbers like 80.0 to 80
            false_positive_possibility = int(false_positive_possibility)
        if type == 'return': # to be able to use recommendation function properly 
            return false_positive_possibility
        save_output(f'Patient {the_patient} has a probability of {false_positive_possibility}% of having {patients_list[patient_index][2].lower()}.\n')
        #inside {} brackets it takes the disease name and the probability of having from the list data
    else:
        save_output(f'Probability for {the_patient} cannot be calculated due to absence.\n')

def recommendation(the_patient):
    if which_patient(the_patient)!= None:
        probability_of_having_the_disease = probability(the_patient,'return') # we use return as the second parametere because we need to get the result of return from probability
        treatment_risk_probability =patients_list[which_patient(the_patient)][-1] #treatment risk like %40, %50 
        if probability_of_having_the_disease > treatment_risk_probability:
            save_output(f'System suggests {the_patient} to have the treatment.\n')
        elif probability_of_having_the_disease < treatment_risk_probability:
            save_output(f'System suggests {the_patient} NOT to have the treatment.\n')
    else:
        save_output(f'Recommendation for {the_patient} cannot be calculated due to absence.\n')
            
with open('doctors_aid_outputs.txt','w') as outputfile: #to clear the output file every time we run the code
    outputfile.write('') 

for whole_info in organized_input(): # this block calls every function by the order in input file 
    #whole info is for every line in the input file like [create, Hayriye, 0.999, Breast Cancer, 50/100000, Surgery, 0.40] or [recommendation, Su]
    if whole_info[0] == 'create':
        create(whole_info)
    elif whole_info[0] == 'remove':
        remove(whole_info)
    elif whole_info[0] == 'list':
        list()
    elif whole_info[0] == 'probability':
        person = whole_info[1] # gets the patient's name 
        probability(person)
    elif whole_info[0] == 'recommendation':
        person = whole_info[1] # gets the patient's name 
        recommendation(person)
    else:
        pass

