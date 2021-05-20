import mysql.connector
from datetime import date

class Database:
	def __init__(self):
		self.mydb = mysql.connector.connect(host='localhost', user='root', passwd='root', database='attendance')
		self.mycur = self.mydb.cursor()
		command = "CREATE TABLE IF NOT EXISTS ROLLNO (Scholar INT(10), Name VARCHAR(50))"
		self.mycur.execute(command)
		command = "CREATE TABLE IF NOT EXISTS ATTENDANCE (Scholar INT(10), date DATE, time TIME, Attend VARCHAR(2))"
		self.mycur.execute(command)

		self.mydb.commit()

	def get_data(self):
		command = 'SELECT * FROM ROLLNO'
		self.mycur.execute(command)
		data = self.mycur.fetchall()
		return data

	def get_returnable_data(self):
		data = self.get_data()
		new_data = []
		today_date = date.today().strftime("%Y-%m-%d")
		for x in data:
			new_data.append([x[0], x[1], today_date, '00:00:00', 'A'])
		return new_data

	def upload(self, data):
		new_data = []
		for x in data:
			new_data.append((str(x[0]), str(x[2]), str(x[3]), str(x[4])))
		command = "INSERT INTO attendance (Scholar, date, time, Attend) VALUES (%s, %s, %s, %s)"
		self.mycur.executemany(command, new_data)
		self.mydb.commit()

	def get_record(self, start_date="1900-01-01", end_date="2500-12-31"):
		detail = self.get_data()
		command = "SELECT * FROM attendance WHERE date >= %s && date <= %s"
		self.mycur.execute(command, (start_date, end_date))
		attendance = self.mycur.fetchall()
		record = dict()
		for x in detail:
			record[x[0]] = [x[1], []]
		for x in attendance:
			record[x[0]][1].append([x[3], x[1], x[2]])
		return record

	def insert(self, name):
		data = self.get_data()
		tot = len(data)
		scholar_new = tot+1;
		command = "INSERT INTO ROLLNO (Scholar, Name) VALUES (%s, %s)"
		self.mycur.execute(command, (scholar_new, name))
		self.mydb.commit()