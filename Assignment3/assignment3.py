import sys 
inputfromterminal = sys.argv[1]
with open(inputfromterminal,'a') as inputfile:
        inputfile.write('\n')
inputfile = open(inputfromterminal, 'r')
inputlist = inputfile.readlines() #to get all the lines in the input file in a list
for i in inputlist:
    inputlist[inputlist.index(i)] = i[:-1] #to get rid of \n in the input line until -1
inputlist = [i.split(' ') for i in inputlist] 

lettervalue = dict(zip(range(0,27), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", )) #assigning alphabet to numbers
createdcategory = dict()
output_file = open('output.txt','a')

def save_output(entry): #saving to output file and printing to terminal
    output_file.write(entry)
    output_file.write('\n')
    print(entry)

def createcategory(inputcategory): 
    if inputcategory[1] not in list(createdcategory.keys()):
        seatnumber = inputcategory[2].split('x')  # making the input like 20x20 usable in code
        seats = dict()
        for i in range(int(seatnumber[0])):
            seats[lettervalue[i]] = [i for i in range(int(seatnumber[1]))] 
        createdcategory[inputcategory[1]] = seats 
        save_output(f"The category '{inputcategory[1]}' having {int(seatnumber[0])*int(seatnumber[1])} seats has been created")
    else:
        save_output(f"Warning: Cannot create the category for the second time. The stadium has already {inputcategory[1]}")

def sellticket(inputticket):
    name= inputticket[1]
    ticket_type = inputticket[2]
    category_name = inputticket[3]
    seats_to_be_reserved = inputticket[4:]
    seat_reserved_copy = seats_to_be_reserved
    seats_to_be_reserved = [[i] for i in seats_to_be_reserved] #creating a nested list for seat and seat ranges
    for i in seats_to_be_reserved:
        if '-' in i[0]: # making seat ranges like H1-12 usable in code
            letter = i[0][0]
            seat_range = i[0][1:].split('-')         
            for number in range(int(seat_range[0]),int(seat_range[1])+1):
                i.append(f'{letter}{number}')
            i.pop(0)
    try:
        for seat_part in seats_to_be_reserved:
            seat_index = seats_to_be_reserved.index(seat_part)
            len_indicator=0
            seat_list = [int(i[1:]) for i in seat_part]
            for i in seat_part:
                if max(seat_list)>len(createdcategory[category_name][i[0]]): #to find if there is enough column 
                    save_output(f"Error: The category '{category_name}' has less column than the specified index {seat_reserved_copy[seat_index]}!")
                    indicator = 1
                    break
                indicator = 0
                if createdcategory[category_name][i[0]][int(i[1:])] == 'S' or createdcategory[category_name][i[0]][int(i[1:])]== 'F' or createdcategory[category_name][i[0]][int(i[1:])]== 'T':
                    save_output(f'Warning:  The seats {seat_reserved_copy[seat_index]} cannot be sold to {name} due some of them have already been sold')
                    indicator = 1
                    break
                if ticket_type == 'student': # writing s f and t for ticket types on instead of seat numbers
                    createdcategory[category_name][i[0]][int(i[1:])] = 'S'
                elif ticket_type == 'full':
                    createdcategory[category_name][i[0]][int(i[1:])]  = 'F'
                elif ticket_type == 'season':
                    createdcategory[category_name][i[0]][int(i[1:])]  = 'T'
            if indicator != 1:
                save_output(f'Success:  {name} has bought {seat_reserved_copy[seat_index]} at {category_name}')
            if len_indicator == 'column':
                    save_output(f"Error:  The category '{category_name}' has less column than the specified index {i}")
    except:
        save_output(f"Error: The category '{category_name} ' has less row than the specified index {seat_reserved_copy[seat_index]}")

def cancelticket(cancel_input):
    category_name = cancel_input[1]
    seats_to_be_cancelled = cancel_input[2:]
    seat_list = [int(seat_part[1:]) for seat_part in seats_to_be_cancelled]  #list for being able to work with seat and seat ranges
    try:
        for i in seats_to_be_cancelled:
            if max(seat_list)>len(createdcategory[category_name][i[0]]):
                save_output(F"Error:  The category {category_name} has less column than the specified index {i}")
                break
            if type(createdcategory[category_name][i[0]][int(i[1:])])==int:
                save_output(f"Error:  The seat {i} at {category_name} has already been free!  Nothing to cancel")
                break
            createdcategory[category_name][i[0]][int(i[1:])] = 'X'
            save_output(f"Success:  The seat {i} at {category_name} has been canceled and now ready to sell again")
    except:
        save_output(f"Error:  The category '{category_name}' has less row than the specified index {i}")

def balance(category_input):
    category_name = category_input[1]
    student = 0
    full = 0 
    season = 0
    for column in createdcategory[category_name].values():
        for i in column:
            if i == 'S':
                student += 1
            elif i == 'F':
                full += 1 
            elif i == 'T':
                season += 1
    price = student*10 + full*20 + season*250
    save_output(f'category report of {category_name}')
    save_output(len(f'Category report of {category_name}')*'-')
    save_output(f'Sum of students = {student}, Sum of full pay = {full}, Sum of season ticket = {season}, and Revenues = {price} Dollars')

def showcategory(show_input):
    category_name = show_input[1]
    save_output(f'Printing category layout of {category_name}\n')
    for index in range(len(createdcategory[category_name])-1,-1,-1):
        print(lettervalue[index],end='  ')
        output_file.write(f'{lettervalue[index]}  ')
        rows = (createdcategory[category_name][lettervalue[index]])
        for i in rows:
            if type(i) == int: #if the item is still an integer and not a string like s f t putting an x for empty seat
                print('X', end='  ')
                output_file.write('X  ')
            else:  
                print(i, end='  ')
                output_file.write(f'{i}  ')
            if rows.index(i) == int(len(rows)-1):
                print('')
                output_file.write('\n')
    print('   ', end='')
    output_file.write('   ')
    for i in range(0,int(len(rows))):
        x = str(i)
        if i==9:
            print(i, end=' ')
            output_file.write(f'{i} ')
        elif (len(x))<2:
            print(i, end='  ')
            output_file.write(f'{i}  ')
        else:
            print(i, end=' ')
            output_file.write(f'{i} ')
    save_output('') 

for item in inputlist: #calling every function in order
    if item[0] == 'CREATECATEGORY':
        createcategory(item)
    elif item[0] == 'SELLTICKET':
        sellticket(item)
    elif item[0] == 'CANCELTICKET':
        cancelticket(item)
    elif item[0] == 'BALANCE':
        balance(item)
    elif item[0] == 'SHOWCATEGORY':
        showcategory(item)

with open('output.txt','w') as outputfile: #clearing the output file after running the program
    outputfile.write('')