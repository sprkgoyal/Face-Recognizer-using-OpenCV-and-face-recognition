from database import Database

student_database = Database()

print("\n     ***   Administration   ***\n")
print("Choose your action")
print("1. Add new Student")
print("2. Get Attendance Record")

choice = -1;
while choice != 1 and choice != 2:
	choice = int(input("Enter your option: "))
	if choice != 1 and choice != 2:
		print("Invalid option!!")

if choice == 1:
	name = input("Enter the name of Student: ")
	name = name.title()
	student_database.insert(name)

else:
	print("Attendance Record")

	start_date = input("Enter Start Date (YYYY-MM-DD) : ")
	end_date = input("Enter End Date (YYYY-MM-DD) : ")

	choice = input("1. For one student\n2. For all students\nEnter option : ")

	record = student_database.get_record(start_date, end_date)

	if choice == '1':
		scholar = int(input("Enter Scholar ID : "))
		print()
		print("Scholar ID: {}".format(scholar))
		print("Name: {}".format(record[scholar][0]))
		cnt = 0
		tot = len(record[scholar][1])
		for it in record[scholar][1]:
			if 'P' in it:
				cnt += 1
		print("Attendance Percentage: {}%".format(cnt/tot*100))

	else:
		for scholar, data in record.items():
			print()
			print("Scholar ID: {}".format(scholar))
			print("Name: {}".format(data[0]))
			cnt = 0
			tot = len(data[1])
			for it in data[1]:
				if 'P' in it:
					cnt += 1
			per = cnt / tot * 100 if tot != 0 else 0.0
			print("Attendance Percentage: {}%".format(per))