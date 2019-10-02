import os
import pandas as pd

folder_path = "E:/OneDrive - Ngee Ann Polytechnic/Udacity - Data Engineering/6. Final Capstone PW/Resources/Datasets/Yelp/yelp-dataset/"	# Extracted folder
save_path = "./data/"		# Data folder path

def readFiles(save_path):
	for path, dirname, filename in os.walk(save_path):
		return path, filename

path, file_paths = readFiles(folder_path)
for file in file_paths:
	file_name, file_type = file.split('.', -1)
	## EXTRACT 5000 from JSON
	if (file_type == 'json'):
		if (("review" in file_name) or ("user" in file_name)):
			print("EXTRACTING 5000 LINES TO JSON")
			json = open(path + file, 'r', encoding="utf8")
			new = open(save_path + file_name + "_5000.json", 'w+', encoding="utf8")
			for i in range(1,5000):
				new.write(json.readline())
			new.close()
			json.close()

		elif (("business" in file_name) or ("checkin" in file_name) or ("tip" in file_name)):
			print("CONVERTING JSON TO CSV")
			df = pd.read_json(path + file, lines=True)
			df.to_csv(save_path + file_name + ".csv", index=None, header=True)
			
path, file_paths = readFiles(save_path)
for file in file_paths:
	file_name, file_type = file.split('.', -1)
	print("EXTRACTING 5000 LINES TO CSV")
	if (file_type == 'csv'):
		df = pd.read_csv(path + file, nrows=5000)
		df.to_csv(save_path+ file_name + "_5000.csv", index=None, header=True)
		os.remove(path+file)