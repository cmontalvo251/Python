class Datalogger():
	def __init__(self):
		self.number = 0

	def findfile(self,directory,extension='.txt'):
		found = 0
		while not found:
			self.filename = directory + str(self.number) + extension
			print("Attempting to check for file: " + self.filename);
			try:
				fileout = open(self.filename,"r");
				fileout.close()
				print("File exists. Skipping");
				self.number+=1; #//Number is global in header file
			except FileNotFoundError:
				found = 1
				print("File found for writing = " + self.filename)

	def open(self):
		#If you want the date in the filename use this
		#datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
		print("Attempting to open" + self.filename);
		self.outfile = open(self.filename,"w");
		if not self.outfile:
	 		print("File not opened properly = " + self.filename);
		else:
			print("File " + self.filename + " opened successfully")

	def println(self,out):
		ctr = 0
		for o in out:
			s = str(o)
			if ctr != len(out)-1:
				s+=","
			ctr+=1
			self.outfile.write(s)
		self.outfile.write("\n")
		self.outfile.flush()

	#Close function
	def close(self):
  		print("Closing File");
  		try:
  			self.outfile.close()
	  		print("File closed");
	  	except AttributeError:
	  		print('You have no file to close')