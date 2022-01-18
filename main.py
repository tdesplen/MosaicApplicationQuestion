#Author: Tyler Desplenter, PhD
#Written On: 11-01-2022

import report_cards
import sys

def main():
	#File names are contained in command line arguments, let's get them first
	generator = report_cards.ReportCards(sys.argv[1:6])
	
	#Gather the data from the files and put them in DataFrames
	courses_df, students_df, tests_df, marks_df = generator.read_csv_data()
	
	#Parse through the data and generate the appropriate dictionary structure
	output_dict = generator.generate_report_cards(courses_df, students_df, tests_df, marks_df)
	
	#Output the dictionary as a JSON object to the output file
	generator.write_json_file(output_dict)
	
main()