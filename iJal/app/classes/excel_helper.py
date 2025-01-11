import pandas as pd
import openpyxl
from bs4 import BeautifulSoup
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

class ExcelHelper:
    @classmethod
    def convert_html_to_excel(cls, html_file_path, output_excel_path):
        # Read and parse HTML
        with open(html_file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
        
        # Create Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Water Budget Report"
        
        # Define styles
        header_fill = PatternFill(start_color="DEE2E6", end_color="DEE2E6", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Start row for each section
        current_row = 1
        
        # Function to write a table section
        def write_section(section_title, table, start_row):
            nonlocal current_row
            
            # Write section header
            ws.merge_cells(f'A{current_row}:C{current_row}')
            header_cell = ws.cell(row=current_row, column=1, value=section_title)
            header_cell.fill = header_fill
            header_cell.font = Font(bold=True)
            header_cell.alignment = Alignment(horizontal='center')
            current_row += 1
            
            # Write table contents
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['th', 'td'])
                    for col_idx, col in enumerate(cols, 1):
                        cell = ws.cell(row=current_row, column=col_idx, value=col.text.strip())
                        cell.border = border
                        if col.name == 'th' or 'fw-semibold' in col.get('class', []):
                            cell.font = Font(bold=True)
                        if 'text-end' in col.get('class', []):
                            cell.alignment = Alignment(horizontal='right')
                    current_row += 1
                current_row += 1  # Add space between sections
        
        # Process Basic Information
        basic_info_table = soup.find('div', text='BASIC INFORMATION').find_next('table')
        write_section('BASIC INFORMATION', basic_info_table, current_row)
        
        # Process Water Transfer
        transfer_table = soup.find('div', text='WATER TRANSFER').find_next('table')
        write_section('WATER TRANSFER', transfer_table, current_row)
        
        # Process Water Budget
        budget_table = soup.find('div', text='WATER BUDGET').find_next('table')
        write_section('WATER BUDGET', budget_table, current_row)
        
        # Start new column for Demand section
        current_row = 1
        col_offset = 5  # Leave a gap between sections
        
        # Function to write a section in a new column
        def write_section_new_column(section_title, table, col_start):
            nonlocal current_row
            start_row = current_row
            
            # Write section header
            ws.merge_cells(f'{get_column_letter(col_start)}{current_row}:{get_column_letter(col_start+2)}{current_row}')
            header_cell = ws.cell(row=current_row, column=col_start, value=section_title)
            header_cell.fill = header_fill
            header_cell.font = Font(bold=True)
            header_cell.alignment = Alignment(horizontal='center')
            current_row += 1
            
            # Write table contents
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['th', 'td'])
                    for col_idx, col in enumerate(cols):
                        cell = ws.cell(row=current_row, column=col_start + col_idx, value=col.text.strip())
                        cell.border = border
                        if col.name == 'th' or 'fw-semibold' in col.get('class', []):
                            cell.font = Font(bold=True)
                        if 'text-end' in col.get('class', []):
                            cell.alignment = Alignment(horizontal='right')
                    current_row += 1
                current_row += 1
        
        # Process Demand sections
        demand_sections = [
            ('a) Human(in HaM)', 'human'),
            ('b) Livestock(in HaM)', 'livestock'),
            ('c) Crops(in HaM)', 'crops'),
            ('d) Industry(in HaM)', 'industry')
        ]
        
        for section_title, table_id in demand_sections:
            table = soup.find('table', {'id': table_id})
            write_section_new_column(section_title, table, col_offset)
        
        # Start new column for Supply section
        current_row = 1
        col_offset = 10  # Leave a gap between Demand and Supply
        
        # Process Supply sections
        supply_sections = [
            ('a) Surface Water(in HaM)', 'surface_water'),
            ('b) Groundwater(in HaM)', 'groundwater'),
            ('c) Runoff(in HaM)', 'runoff'),
            ('d) Rainfall(in mm)', 'rainfall')
        ]
        
        for section_title, table_id in supply_sections:
            table = soup.find('table', {'id': table_id})
            write_section_new_column(section_title, table, col_offset)
        
        # Adjust column widths
                # Adjust column widths
        for column in range(1, ws.max_column + 1):
            max_length = 0
            column_letter = get_column_letter(column)
            
            for row in range(1, ws.max_row + 1):
                cell = ws.cell(row=row, column=column)
                if isinstance(cell, openpyxl.cell.cell.MergedCell):
                    continue
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Save the workbook
        wb.save(output_excel_path)
        print(f"Excel file created successfully at: {output_excel_path}")
        return output_excel_path

# Example usage
# html_file_path = "water_budget.html"  # Replace with your HTML file path
# output_excel_path = "water_budget_formatted.xlsx"  # Replace with desired output path
# convert_html_to_excel(html_file_path, output_excel_path)
