import mysql.connector as sql
import csv
import os  # this is used to dlt the file
while True:
    try:
        students_result_folder = 'students result'
        passcode = input('ENTER THE PASSWORD:-')
        workspace = sql.connect(host='localhost', user='root',
                                password=passcode, database='result')
        cursor = workspace.cursor()
        break
    except:
        print('INCORRECT PASSWORD')
information = ['Id', 'name', 'maths', 'physics',
               'chemistry', 'english', 'computer_science']


def create_table():  # this function is used to create table if doesn't exist
    global information
    query = '''create table students(ID varchar(10) primary key,name varchar(20)
     not null,maths integer,physics integer,chemistry integer,
     english integer,computer_science integer, percentage float);'''
    try:
        cursor.execute(query)
        workspace.commit()
        print('TABLE CREATED')
    except:  # if table is already there
        print('\nTable students already exists\n')
    menu()


def menu():  # used get function in update and
    # insert helps in taking correct input from user
    # this is the menu of our selections
    print('\n-----------------MENU-----------------')
    print('PRESS 0 TO CREATE THE TABLE')
    print('PRESS 1 TO INSERT RECORD')
    print('PRESS 2 TO UPDATE RECORD')
    print('PRESS 3 TO SHOW RECORD')
    print('PRESS 4 TO SHOW REPORT CARD')
    print('PRESS 5 TO DELETE')
    print('PRESS 6 TO DISPLAY ALL THE CONTENTS')
    print('PRESS 7 TO EXECUTE SPECIAL QUERY')
    print('TYPE "EXIT" TO STOP\n')
    work = input('PRESS:-')
    if work == '1':
        insert()
    elif work == '2':
        update()
    elif work == '3':
        show()
    elif work == '4':
        report_card()
    elif work == '5':
        delete()
    elif work == '6':
        display_all()
    elif work == '7':
        mysql()
    elif work == '0':
        create_table()
    elif work.replace(' ', '').lower() == 'exit':
        return
    else:
        print('INVALID CHOICE')
        menu()


def mysql():  # special function to write own query
    query = input('MySQL>>')
    while query.lower() != 'terminate':  # to stop the query
        try:
            # this will tell me what work has to be performed
            work = query.split()[0]
            cursor.execute(query)
            if work == 'insert' or work == 'update' or work == 'delete':
                workspace.commit()
                print('RECORD '+work+'d')  # record delete+d
            elif work == 'select' or work == 'show' or work == 'desc':
                for row in cursor.fetchall():
                    print(row)
                print('-------------------------------------------------')
            else:
                workspace.commit()
                print('task done')

        except:
            print('ERROR!!! CHECK SYNTAX')
        print('NOTE:- WRITE "TERMINATE" TO STOP')
        query = input('MySQL>>')
    menu()


def get(columns_heading):  # to take input from the user
    data = []
    for column in columns_heading:  # name of the column is here
        while True:  # while the data type is correct
            if column.upper() == 'ID':
                info = input('ENTER STUDENT ID:-')
                # to check if record exists or not
                if check(info, 'primary_key_check') == 'record not found':
                    data.append(f'"{info}"')
                    break
                else:
                    print('THIS ID already exists in the TABLE')
            elif column.lower() == 'name':
                info = input('ENTER STUDENT NAME:-')
                if len(info) < 26:  # name shall not containg more than 25 charachters in it
                    data.append(f"'{info}'")
                    break
                else:
                    print('NAME SHOULD NOT CONTAIN MORE THAN 25 CHARACHTERS!!')
            else:
                try:
                    marks = int(input(f'MARKS scored in {column}:-'))
                except ValueError:
                    print('MARKS SHOULD BE INTEGER ONLY!!')
                    continue
                if check(marks, 'marks_constraint') == True:
                    data.append(str(marks))
                    break
                else:
                    print('INVALID MARKS!!! [0-100] only')
    return data


def insert():  # function used to insert data
    try:
        number_of_records = int(
            input('NUMBER OF RECORDS YOU WANT TO INSERT:-'))
    except:
        print('INTEGER ONLY')
        insert()
        return
    for number in range(number_of_records):
        print('RECORD ', number+1)
        data = get(information)
        Id = data[0]
        data.append('(physics+maths+chemistry+computer_science+english)/5')
        # this is the percentage of the final result
        data = ','.join(data)  # CONVERTS list into string
        query = f'insert into students values({data})'
        cursor.execute(query)
        workspace.commit()
        # this function will make the result txt file automatically
        report_card(Id[1:len(Id)-1])
        print('RECORD INSERTED')
    menu()


def update():  # to update an exisisting record
    identity = input('ID of the student:-')
    flag = check(identity, 'primary_key_check')
    if flag == 'record found':  # if record is present that needs to be updated
        show(identity)  # show the data of this identity
        press_key = 1  # to run loop instead of print statements
        for column in information[1:]:
            if column == 'name':
                print(f'PRESS {press_key} TO UPDATE {column}')
            else:
                print(f'PRESS {press_key} TO UPDATE {column} MARKS')
            press_key += 1
        changes_key_press = input('PRESS ALL THE KEYS (seperate by ",")')
        changes_key_press = changes_key_press.replace(' ', '').split(",")
        # the above function helps to convert input to list
        changes = []
        for change_press in changes_key_press:
            # if the key pressed is valid or not
            if change_press in ['1', '2', '3', '4', '5', '6']:
                changes.append(information[eval(change_press)])
            else:
                print(f'\nERROR!!!! wrong key({change_press}) PRESSED\n')
                update()
                return
        data = get(changes)
        # take input from the user
        pos = 0
        for column in changes:  # all the columns are updated one by one
            query = f'update students set {column}={data[pos]} where id="{identity}"'
            pos += 1
            cursor.execute(query)
            workspace.commit()
        query = f'''update students set percentage =
        (maths+english+computer_science+physics+chemistry)/5 where id = "{identity}"'''
        cursor.execute(query)
        workspace.commit()
        report_card(identity)
        print('RECORD UPDATED')
    elif flag == 'record not found':
        print(f'RECORD OF ID {identity} DOES NOT EXISTs')
    menu()


def show(work='nothing'):  # to get record from table
    if work == 'nothing':  # I have used show function at one more place so as to diff. from both the use
        # as if user calls this user need to give input of identity
        # but when inbuilt function (update function) calls it, identity is already given in update function
        # so no need to take an input again
        identity = input('SELECT ID of the student:-')
    else:
        identity = work
    if check(identity, 'primary_key_check') == 'record not found':
        # check is record is already present or not
        print(f'RECORD OF ID {identity} DOES NOT EXISTs')
    else:
        query = f'select * from students where id="{identity}" '
        cursor.execute(query)
        data = cursor.fetchall()[0]  # to get list's element which is a tuple
        # this tuple has all the value of record
        total_marks = data[7]
        pos = 0
        for column in information:
            print(f'{column}:-', data[pos], '\n')
            pos += 1
        if total_marks > 33:
            result = 'PASS'
        else:
            result = 'FAIL'
        print('RESULT', result)

    if work == 'nothing':
        menu()


def delete():  # to delete a record
    identity = input('Enter ID:-')
    if check(identity, 'primary_key_check') == 'record not found':
        print('NO SUCH ID')
    else:
        query = f'delete from students where ID="{identity}"'
        show(identity)
        recheck = input('SURE YOU WANT TO DELETE THE RECORD (YES/NO):-')
        if recheck.lower() == 'yes':
            print('RECORD DELETED')
            # if file exists then dlt it
            if os.path.exists(f'{students_result_folder}//{identity} report card.txt'):
                os.remove(
                    f'{students_result_folder}//{identity} report card.txt')
            cursor.execute(query)
            workspace.commit()
        else:
            print('\nRECORD NOT DELTED!!')
    menu()


def marks_grade(perc):  # this converts marks to grade

    if perc > 90:
        grade = 'A+'
    elif perc > 80:
        grade = 'A'
    elif perc > 70:
        grade = 'B+'
    elif perc > 60:
        grade = 'B'
    elif perc > 50:
        grade = 'C+'
    elif perc > 40:
        grade = 'C'
    elif perc > 30:
        grade = 'D'
    else:
        grade = 'E'
    return grade


def number_alignment(number_of_records):  # for converting marks in string of 3
    number_of_records = str(number_of_records)
    # this function is used in report card as it helps me to change 45 to 045
    # or 9 marks to 009 which is important in alignment
    if len(number_of_records) == 3:
        return number_of_records
    elif len(number_of_records) == 2:
        return f'0{number_of_records}'
    elif len(number_of_records) == 1:
        return f'00{number_of_records}'
    else:
        return '000'


def report_card(identity='nothing'):  # to get the final report card
    flag = 0
    if identity == 'nothing':
        flag = 1
        identity = input('ID of the student:-')
    if check(identity, 'primary_key_check') == 'record not found':
        print('NO SUCH ID')
    else:
        query = f'select * from students where id="{identity}"'
        cursor.execute(query)
        data = list((cursor.fetchall())[0])
        percentage = data[7]
        if percentage > 33:
            result = 'PASS'
        else:
            result = 'FAIL'
        data.append(result)
        result = f'''
	==================================================================================================
							CRPF PUBLIC SCHOOL DWARKA SECTOR 16-B
									REPORT CARD

	Name : {data[1]}
	Identity : {data[0]}

	==================================================================================================

		Subjects                  Marks              Grade

		MATHS            :         {number_alignment(data[2])}  :              {marks_grade(data[2])}
		CHEMISTRY        :         {number_alignment(data[3])}  :              {marks_grade(data[3])}
		PHYSICS          :         {number_alignment(data[4])}  :              {marks_grade(data[4])}
		ENGLISH          :         {number_alignment(data[5])}  :              {marks_grade(data[5])}
		COMPUTER_SCIENCE :         {number_alignment(data[6])}  :              {marks_grade(data[6])}

	===================================================================================================

	Total Marks:      {data[7]*5}
	Percentage:       {percentage}%      :    {marks_grade(percentage) }
	RESULT            {data[8]}'''
        if flag == 1:
            print(result)
        file = open(
            f'{students_result_folder}//{data[0]} report card.txt', 'w+')
        file.write(result)
        file.close()
    if flag == 1:
        menu()


def overview():
    for subject in ['physics', 'chemistry', 'maths', 'computer_science']:
        print(f'\n--------------------{subject}--------------------')
        max_marks_query = f'select Id,name,{subject} from students where {subject}=(select max({subject}) from students)'
        cursor.execute(max_marks_query)
        data_max_marks = cursor.fetchall()
        cursor.execute(f'select avg({subject}) from students')
        avg_marks = cursor.fetchone()
        print(f'\nHIGHEST MARKS SCORED IN {subject}:- {data_max_marks[0][2]}')
        for info in data_max_marks:
            print(f'STUDENT=>   Id:- {info[0]}   NAME:-{info[1]}')
        print(f'\nAVERAGE MARKS SCORED:-{avg_marks[0]}\n')
    print('--------------------OVERALL--------------------')
    cursor.execute('select max(percentage) from students')
    max_percentage = cursor.fetchone()
    print(f'\nHIGHEST PERCENTAGE:-{max_percentage[0]}')
    cursor.execute(
        'select id,name from students where percentage=(select max(percentage) from students)')
    data = cursor.fetchall()
    for topper in data:
        print(f'Id:-{topper[0]} NAME:-{topper[1]}')
    cursor.execute('select avg(percentage) from students')
    avg_percentage = cursor.fetchone()
    print(f'\nAVERAGE PERCENTAGE {avg_percentage[0]}\n')


def display_all():
    data = result_dictionary()
    if len(data) == 0:
        print('No record(s) found!')
        return
    structure_line = (
        "+----------+-------------------------+----------+----------+----------+----------+----------+----------+\n")
    structure_top2 = (
        '|Identity  |Name                     |Physics   |Chemistry |Maths     |English   |CS        |Percentage|\n')

    structure_top = structure_line+structure_top2+structure_line

    rows = []
    rows.append(structure_top)
    excel_rows = []
    for identity in data.keys():
        report_card(identity)
        excel_row = [identity]
        row = ("|" + str(identity) + " "*(10-len(str(identity))) + "|")
        student_data = data[identity]
        for column in student_data.keys():
            excel_row.append(student_data[column])
            if column.lower() == 'name':
                space = 25
            else:
                space = 10
            row = row+((str(student_data[column]))+' ' *
                       (space-len(str(student_data[column])))+'|')
        excel_rows.append(excel_row)
        rows.append(row)

        rows.append('\n'+structure_line)
    file = open('result.txt', 'w+')
    for row in rows:
        print(row)
        file.writelines(row)
    file.close()
    # the below code is to display overiew of the result

    file = open('result.csv', 'w')
    pen = csv.writer(file)
    excel_heading = information.copy()
    excel_heading.append('percentage')
    pen.writerow(excel_heading)
    for row in excel_rows:
        pen.writerow(row)
    file.close()
    overview()
    menu()


def check(value, work):
    # this is a constraint function which checks
    # that the value is consistent with the table
    if work == 'marks_constraint':  # constraint on marks
        if value < 101 and value > -1:
            return True
        else:
            return False
    # to check if input ID is already present or not
    elif work == 'primary_key_check':
        cursor.execute('select id from students')
        primary_keys = cursor.fetchall()
        value = (value,)
        if value in primary_keys:
            return 'record found'
        else:
            return 'record not found'


def result_dictionary():  # this convertts data in dictionary format
    final_result_dictionary = {}
    query = 'select * from students order by percentage desc'
    cursor.execute(query)
    result_data = cursor.fetchall()
    for student_result in result_data:
        student_dictionary = {}
        pos = 1
        for column in information[1:]:
            student_dictionary[column] = student_result[pos]
            pos += 1
        student_dictionary['percentage'] = student_result[pos]
        final_result_dictionary[student_result[0]] = student_dictionary
    return final_result_dictionary


menu()
