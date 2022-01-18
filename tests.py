import unittest
import report_cards
import os
  
class ReportCardTests(unittest.TestCase):

	# Test filename loading
	def test_filename_load(self):
		rp = report_cards.ReportCards(['courses.csv','students.csv','tests.csv','marks.csv','output.json'])
		self.assertIn('output.json',rp.filename_list)
		
	#Test data reading
	def test_data_reading(self):
		rp = report_cards.ReportCards(['courses.csv','students.csv','tests.csv','marks.csv','output.json'])
		data = [0,0,0,0]
		data[0],data[1],data[2],data[3] = rp.read_csv_data()
		for i in range(len(data)):
			self.assertNotEqual(0, data[i].shape[0])
			
	#Test report card generation
	def test_report_card_generation(self):
		rp = report_cards.ReportCards(['courses.csv','students.csv','tests.csv','marks.csv','output.json'])
		data = [0,0,0,0]
		data[0],data[1],data[2],data[3] = rp.read_csv_data()
		output_dict = rp.generate_report_cards(data[0],data[1],data[2],data[3])
		self.assertEqual(len(output_dict['students']),3)
		self.assertEqual(output_dict['students'][0]['name'],'A')
	
	#Test file writing
	def test_output(self):
		rp = report_cards.ReportCards(['courses.csv','students.csv','tests.csv','marks.csv','output_test.json'])
		output_dict = {'testing': 'please pass this test'}
		rp.write_json_file(output_dict)
		self.assertNotEqual(os.path.getsize('.\output_test.json'),0)
  
if __name__ == '__main__':
    unittest.main()
	