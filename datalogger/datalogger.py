class Datalogger():
	def __init__(self):
		self.number = 0

	def findfile(self,directory):
		found = 0
		while not found:
			self.filename = directory + str(self.number) + ".txt"
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
		print("Attempting to open" + self.filename);
		self.outfile = open(self.filename,"w");
		if not self.outfile:
	 		print("File not opened properly = " + self.filename);
		else:
			print("File " + self.filename + " opened successfully")

	def println(self,out):
		for o in out:
			s = str(o) + ","
			self.outfile.write(s)
		self.outfile.write("\n")

	#Close function
	def close(self):
  		print("Closing File");
  		close(self.outfile);
  		print("File closed");