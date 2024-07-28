 import xlsxwriter

 def create_excel_file(info_list):
     workbook = xlsxwriter.Workbook('extracted_info.xlsx')
     worksheet = workbook.add_worksheet()

     for i, info in enumerate(info_list):
         worksheet.write(i, 0, info)

     workbook.close()
