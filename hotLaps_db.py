import sqlite3 as sqlite

class hotLapsDataBase:

	location=""
	resultsTable="results"
	tableDescription = "(RId INTEGER primary key autoincrement, track TEXT, driver TEXT, carClass TEXT, carName TEXT, sector1 TEXT, sector2 TEXT, sector3 TEXT, lapTime TEXT, date TEXT, total REAL);"
	buildQuery = "CREATE TABLE if not exists " + resultsTable + tableDescription
	buildViewUniqueFromOrdered = "CREATE VIEW IF NOT EXISTS topTimes AS SELECT r2.* FROM results r1 JOIN (SELECT r.RId, MIN(r.total) AS fastest FROM results r GROUP BY r.track,r.driver,r.carClass,r.carName) res ON res.RId = r1.RId JOIN results r2 ON res.fastest = r2.total ORDER BY r2.total;"
	insertFields = "(track, driver, carClass, carName, sector1, sector2, sector3, lapTime, date, total)"

	def __init__(self, database_name):
		self.location = database_name
		self.openDB()
		self.crsr.execute(self.buildQuery)
		self.crsr.execute(self.buildViewUniqueFromOrdered)
		
	def _del_ (self):
		self.closeDB()
		
	def openDB(self):
		self.db = sqlite.connect( self.location )
		self.crsr = self.db.cursor()
		
	def closeDB(self):
		if self.crsr: self.crsr.close()
		if self.db: self.db.close()
		
	def query(self, q):
		if self.db: return self.crsr.execute(q)

	def addLaps(self, laps):
		for i in laps: self.insertLapData(i)

	def restore(self, filename):
		self.openDB()
		self.query("DROP TABLE IF EXISTS " + self.resultsTable)
		self.closeDB()

	def getLaps(self):
		if self.crsr and self.db: 
			self.crsr.execute('SELECT * from ' + self.resultsTable + ';')
			return self.crsr.fetchall()
		
	def getUniqueLaps(self):
		if self.crsr and self.db:
			self.crsr.execute('SELECT * FROM topTimes;')
			return self.crsr.fetchall()
	
	def insertLapData(self,lap):
		try:
			if self.crsr and self.db:
				self.crsr.execute("INSERT INTO " + self.resultsTable + self.insertFields +  " VALUES (?,?,?,?,?,?,?,?,?,?);", lap)
				self.db.commit()
				self.crsr.execute("SELECT * FROM results;")
				print self.crsr.fetchall()[-1]
				
		except sqlite.Error:
			if self.db:
				self.db.rollback()

	def transactionCount(self):
		if self.db: return self.db.total_changes
		
