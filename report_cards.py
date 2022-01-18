#Author: Tyler Desplenter, PhD
#Written On: 11-01-2022

import json
import pandas as pd
from numpyencoder import NumpyEncoder

#Assumptions
#1) fixed number of command line arguments, 6 in this case
#2) files are small enough to be all loaded into memory
#3) data in the files may not be ordered by any of the columns (random ordering)

class ReportCards:
	def __init__(self, filenames):
		#Filenames are always listed in this order when called: courses, students, tests, marks, and output
		self.filename_list = filenames
		
	def read_csv_data(self):
		#Save file reads and writes by loading each file once into DataFrames
		courses_df = pd.read_csv(self.filename_list[0])
		students_df = pd.read_csv(self.filename_list[1])
		tests_df = pd.read_csv(self.filename_list[2])
		marks_df = pd.read_csv(self.filename_list[3])
		return courses_df, students_df, tests_df, marks_df

	def generate_report_cards(self, courses_df, students_df, tests_df, marks_df):
		#Create an output variables
		student_list = []
		output_dict = {"students" : []}

		#For each student, we need to determine their course and overall grades
		number_of_students = students_df.shape[0]
		for s in range(0,number_of_students):
			#create a student object
			student = {"id" : students_df.loc[s,'id'], "name" : students_df.loc[s,'name'], "totalAverage" : 0, "courses" : {}}
			
			#create an empty DataFrame for holding course information
			courses = pd.DataFrame(columns=['id','name','teacher','courseAverage'])
			
			totalAverage = 0 #zero the totalAverage (for later)
			
			#run through the list of marks
			number_of_marks = marks_df.shape[0]
			for m in range(0,number_of_marks):
				if marks_df.loc[m,'student_id'] == student['id']: #we found a match based on student id
					mark = marks_df.loc[m,'mark'] #record the mark
					test_id = marks_df.loc[m,'test_id'] #record the test id
					
					#run through the list of tests 
					number_of_tests = tests_df.shape[0]
					for t in range(0,number_of_tests):
						if test_id == tests_df.loc[t,'id']: #we found a match based on test id
							weight = tests_df.loc[t,'weight'] #record the weight of the test
							course_id = tests_df.loc[t,'course_id'] #record which course the test corresponds to
							
							#if the course does not yet exist in the course DataFrame, first we need to add it
							if course_id not in courses['id'].tolist():
								course_info = courses_df[courses_df['id'] == course_id] #get the course info
								course_info.insert(course_info.shape[1], 'courseAverage',[0]) #add a column to track courseAverage
								course_info.insert(course_info.shape[1], 'weightTotal',[0]) #add a temporary column to track the total of the test weights
								courses = courses.append(course_info, ignore_index=True)
							col = courses.columns.get_loc('courseAverage')
							row = courses.loc[courses['id'] == course_id].index.values[0]
							courses.iat[row,col] += round(mark * weight / 100, 2) #add the mark to the course grade
							col = col = courses.columns.get_loc('weightTotal')
							courses.iat[row,col] += weight #add the weight to the weight total for this course
							
			#Check weightTotals to see if they all equal 100
			weight_totals = courses['weightTotal'].tolist()
			check_total = 0
			#add up the weight totals from all courses for this student
			for w in weight_totals:
				check_total += w
			if check_total/100 != len(weight_totals): #if any of them don't add up to 100
				output_dict = {"error" : "Invalid course weights"} #generate the error message
				break #break the main loop
			else:
				#Calculate the totalAverage and store it
				number_of_marks = courses.shape[0]
				for i in range(0,number_of_marks):
					col = courses.columns.get_loc('courseAverage')
					totalAverage += courses.iat[i,col]
				totalAverage /= number_of_marks
				student['totalAverage'] = round(totalAverage, 2) #make sure to round as specified
				
				#remove weightTotal column from final output
				courses = courses.drop('weightTotal', axis=1)
				
				student['courses'] = courses.to_dict('records') #transform the DataFrame to a list of dictionaries
				student_list.append(student) #add it to the temporary student list
				output_dict['students'] = student_list #assign the current student list to the output dictionary
		return output_dict
				

	def write_json_file(self, output_dict):
		#Convert the dictionary to a JSON object and dump it into a file
		with open(self.filename_list[4],'w') as output_file:
			json.dump(output_dict, output_file, indent=4, cls=NumpyEncoder) #the NumpyEncoder is there to deal with int64 serialization issues

		
			
		