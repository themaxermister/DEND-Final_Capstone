import os
import random
import string
import logging
import datetime
import numpy as np
import pandas as pd
from ast import literal_eval

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

def readFiles(save_path):
	''' Get list of path and filenames from save_folder '''
	for path, dirname, filename in os.walk(save_path):
		return path, filename

def fillEmpty(df):
	''' Fill empty columns with values according to data type'''
	for col in df:
		dt = df[col].dtype
		if (dt == 'object'):
			df[col] = df[col].fillna('')

		elif (dt == 'int64'):
			df[col] = df[col].fillna(0)

		elif (dt == 'float64'):
			df[col] = df[col].fillna(0.00)

	return df

def id_generator(chars=string.ascii_uppercase + string.digits, size=10):
	'''Generate unique id'''
	return ''.join(random.choice(chars) for _ in range(size))

def main(file, df):
	if ("business" in file):
		# Convert 'is_open' to boolean
		df['is_open'] = df['is_open'].astype(bool)

		# Convert 'categories' to list
		for index in df.index.tolist():
			for i in (df.loc[[index],'categories']):
				if ("{" not in str(i)) and ("}" not in str(i)):
					df.loc[[index],'categories'] = "{%s}" % (i)

	elif ("checkin" in file):
		# Convert 'date' to list
		for index in df.index.tolist():
			for i in (df.loc[[index],'date']):
				if ("{" not in str(i)) and ("}" not in str(i)):
					df.loc[[index],'date'] = "{%s}" % (i)
	
	elif ("user" in file):
		# Convert 'friends' to list
		for index in df.index.tolist():
			for i in (df.loc[[index],'friends']):
				if ("{" not in str(i)) and ("}" not in str(i)):
					df.loc[[index],'friends'] = "{%s}" % (i)
	
	elif ("review" in file):
		df['date'] = df['date'].astype(str)

	# 1. CHECK FOR MISSING VALUES AND FILL
	nans = lambda df: df[df.isna().any(axis=1)]
	nandf = len(nans(df))

	if (nandf > 0):
		print("MISSING VALUES DETECTED")
		df = fillEmpty(df)
		print("MISSING VALUES FILLED")
	else:
		print('NO MISSING VALUES')

# 2. CHECK FOR DUPLICATE ROWS AND REMOVE
	dup_no = len(df[df.duplicated()])
	if (dup_no > 0):
		print( f"{file} HAS {dup_no} duplicates.")
		df = df.drop_duplicates()
	else:
		print(f"{file} HAS NO duplicates.")

# 3. CHANGE COLUMN VALUES
	if ("business" in file):
		# Convert 'is_open' to boolean
		df['is_open'] = df['is_open'].astype(bool)

		# Convert 'categories' to list
		for index in df.index.tolist():
			for i in (df.loc[[index],'categories']):
				if (i[0] != "{") and (i[-1] != "}"):
					df.loc[[index],'categories'] = "{%s}" % (i)

	elif ("checkin" in file):
		# Convert 'date' to list
		for index in df.index.tolist():
			for i in (df.loc[[index],'date']):
				if (i[0] != "{") and (i[-1] != "}"):
					df.loc[[index],'date'] = "{%s}" % (i)
	
	elif ("user" in file):
		# Convert 'friends' to list
		for index in df.index.tolist():
			for i in (df.loc[[index],'friends']):
				if (i[0] != "{") and (i[-1] != "}"):
					df.loc[[index],'friends'] = "{%s}" % (i)
		
		# Convert 'elite' to list
		df['elite'] = df['elite'].astype(str)
		for index in df.index.tolist():
			for i in (df.loc[[index],'elite']):
				if (i[:1] != "{") and (i[:-1] != "}"):
					df.loc[[index],'elite'] = "{%s}" % (i)
	
	elif ("reviews" in file):
		# Remove trailing zeros
		df['date'] = df['date'].astype(str)
		for index in df.index.tolist():
			for i in (df.loc[[index],'date']):
				i = str(i)[:10]
					
# 4. CREATE NEW COLUMNS
	if ('business' in file):
		# Hours column
		df['opening_id'] = ""
		df['Monday'] = ""
		df['Tuesday'] = ""
		df['Wednesday'] = ""
		df['Thursday'] = ""
		df['Friday'] = ""
		df['Saturday'] = ""
		df['Sunday'] = ""

		for index in df.index.tolist():
			for i in (df.loc[[index],'hours']):
				if (i != ""):
					id = df.loc[[index], 'business_id'].iloc[0]
					df.loc[[index], 'opening_id'] = "O-" + id_generator(id)
					hours_list = literal_eval(i)
					for key, value in hours_list.items():
						df.loc[[index], key] = value
	
	# Count total number of dates in checkin
	elif ('checkin' in file):
		df['checkin_count'] = 0
		for index in df.index.tolist():
			for i in (df.loc[[index],'date']):
				date_list = i.split(",")
				df.loc[[index],'checkin_count'] = len(date_list)

	# Create compliment_id
	elif ('user' in file):
		if ('compliment_id' not in df.columns):
			df.insert(11, 'compliment_id', value="")
			for index in df.index.tolist():
				id = df.loc[[index], 'user_id'].iloc[0]
				df.loc[[index], 'compliment_id'] = "C-" + id_generator(id)

	# Create tip_id
	elif('tip' in file):
		if ('tip_id' not in df.columns):
			df.insert(0, 'tip_id', value="")
			for index in df.index.tolist():
				user_id = df.loc[[index], 'user_id'].iloc[0]
				business_id = df.loc[[index], 'business_id'].iloc[0]
				df.loc[[index], 'tip_id'] = "C-" + id_generator(user_id + business_id)

	return df
	

class FileDataQualityOperator(BaseOperator):
	ui_color = '#89DA59'

	@apply_defaults
	def __init__(self,
				 save_path,
				 *args, **kwargs):

		super(FileDataQualityOperator, self).__init__(*args, **kwargs)
		self.save_path = save_path

	def execute(self, context):
		'''Perform data quality check on JSON and CSV files only'''
		path, file_paths = readFiles(self.save_path)
		for file in file_paths:
			logging.info(file)
			file_name, file_type = file.split('.', -1)
			if (file_type == 'json'):
				df = pd.read_json(path + file, lines=True)
				df = main(file, df)
				df.to_json(path+file, orient='records', lines=True)
				
			elif (file_type == "csv"):
				df = pd.read_csv(path+file)
				df = main(file, df)
				df.to_csv(path+file, index=None, header=True)
			
			logging.info(f"{file} HAS BEEN UPDATED AND CHECKED")