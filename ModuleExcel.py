import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.cell.cell import MergedCell
from copy import copy

import xlsxwriter
import xlrd

import os, sys

import shutil
import tempfile

from pathlib import Path
from win32com.client import Dispatch

import ModuleFunctions

# # Class to manage excel data with openpyxl.
# class Copy_excel:
#     def __init__(self,src):
#         self.wb = load_workbook(src)
#         #self.ws = self.wb.get_sheet_by_name("Sheet1") # Deprecated
#         self.ws = self.wb["Sheet1"]
#         self.dest="destination.xlsx"

#     # Write the value in the cell defined by row_dest+column_dest         
#     def write_workbook(self,row_dest,column_dest,value):
#         c = self.ws.cell(row = row_dest, column = column_dest)
#         c.value = value
    
#     # Save excel file
#     def save_excel(self) :  
#         self.wb.save(self.dest)




def copia_layout_colonne(ws, col_start_src, col_end_src, col_start_dst, righe_da_copiare=50):
    num_colonne = col_end_src - col_start_src + 1

    # Crea una copia delle celle unite per evitare modifiche durante l'iterazione
    merged_ranges = list(ws.merged_cells.ranges)

    celle_unite = set()
    for area in merged_ranges:
        for row in range(area.min_row, area.max_row + 1):
            for col in range(area.min_col, area.max_col + 1):
                celle_unite.add((row, col))
            pass
        pass
    pass

    for i in range(num_colonne):
        col_src = col_start_src + i
        col_dst = col_start_dst + i

        lettera_src = get_column_letter(col_src)
        lettera_dst = get_column_letter(col_dst)

        if lettera_src in ws.column_dimensions:
            ws.column_dimensions[lettera_dst].width = ws.column_dimensions[lettera_src].width
        pass

        for riga in range(1, righe_da_copiare + 1):
            if (riga, col_src) in celle_unite and (riga, col_src) != (riga, col_src):#
                continue  # salta le celle non principali delle unioni
            pass

            cella_src = ws.cell(row=riga, column=col_src)
            cella_dst = ws.cell(row=riga, column=col_dst)

            if not isinstance(cella_src, MergedCell):
                try:
                    cella_dst.value = cella_src.value
                except AttributeError:
                    pass

                if cella_src.has_style:
                    cella_dst.font = copy(cella_src.font)
                    cella_dst.border = copy(cella_src.border)
                    cella_dst.fill = copy(cella_src.fill)
                    cella_dst.number_format = copy(cella_src.number_format)
                    cella_dst.protection = copy(cella_src.protection)
                    cella_dst.alignment = copy(cella_src.alignment)
                pass
            pass
        pass
    pass

    # Copia celle unite e applica stile su tutte le celle dell'unione
    for area in merged_ranges:
        if (col_start_src <= area.min_col <= col_end_src) and (col_start_src <= area.max_col <= col_end_src):
            offset_col = col_start_dst - col_start_src
            nuova_min_col = area.min_col + offset_col
            nuova_max_col = area.max_col + offset_col
            nuova_area = ws.cell(row=area.min_row, column=nuova_min_col).coordinate + ":" + \
                         ws.cell(row=area.max_row, column=nuova_max_col).coordinate
            ws.merge_cells(nuova_area)

            # Copia stile da cella principale
            cella_principale_src = ws.cell(row=area.min_row, column=area.min_col)
            for riga in range(area.min_row, area.max_row + 1):
                for col in range(area.min_col, area.max_col + 1):
                    cella_dst = ws.cell(row=riga, column=col + offset_col)
                    if cella_principale_src.has_style:
                        cella_dst.font = copy(cella_principale_src.font)
                        cella_dst.border = copy(cella_principale_src.border)
                        cella_dst.fill = copy(cella_principale_src.fill)
                        cella_dst.number_format = copy(cella_principale_src.number_format)
                        cella_dst.protection = copy(cella_principale_src.protection)
                        cella_dst.alignment = copy(cella_principale_src.alignment)
                    pass
                pass
            pass
        pass
    pass

def duplica_blocco_layout(nome_file, colonna_inizio="A", colonna_fine="G", ripetizioni=2, righe_max=50, output_file="TabMensile_modificato.xlsx"):
    # Load the workbook and worksheet
    wb = openpyxl.load_workbook(nome_file)
    ws = wb.active

    # Parametri
    # colonna_inizio = "A"
    # colonna_fine = "G"
    # ripetizioni = 2
    # righe_max = 50

    col_start = column_index_from_string(colonna_inizio)
    col_end = column_index_from_string(colonna_fine)
    blocco_larghezza = col_end - col_start + 1

    for i in range(ripetizioni):
        col_dest = col_end + 1 + i * blocco_larghezza
        copia_layout_colonne(ws, col_start, col_end, col_dest, righe_da_copiare=righe_max)
    pass

    wb.save(output_file)

def aggiungi_togli_foglio_excel(FileXls):

	# Carica il file Excel esistente
	#workbook = openpyxl.load_workbook('file.xlsx')
	workbook = openpyxl.load_workbook(FileXls)

	# Aggiungi un nuovo foglio
	new_sheet = workbook.create_sheet(title='FoglioTemporaneo')

	# Salva il file con il nuovo foglio
	workbook.save('file_con_foglio_aggiunto.xlsx')

	# Rimuovi il foglio appena aggiunto
	workbook.remove(new_sheet)

	# Salva nuovamente il file senza il foglio aggiunto
	workbook.save('file_finale.xlsx')

	#print("Foglio aggiunto e poi rimosso con successo.")

################################################

def run_excel_macro_CaricaFoglio(FileSrc, NomeMacro):
	i = 0

	#FileNameExt = os.path.basename(FileSrc)

	FileNameExt = Path(FileSrc).name
	FileName = ModuleFunctions.get_filename_without_ext(FileNameExt)

	try:
		excel = Dispatch("Excel.Application")
		excel.Visible = True

		workbook = excel.Workbooks.Open(FileSrc)
		#workbook.Application.Run("CaricaFoglio")
		workbook.Application.Run(NomeMacro)

		## Ottieni il percorso della cartella temporanea
		# cartella_temp = tempfile.gettempdir()		
		# # Costruisci il percorso completo del file
		# percorso_file_tmp = os.path.join(cartella_temp, FileNameExt)
		# aggiungi_toglio_foglio_excel(percorso_file_tmp)

		l=1

	except IOError as e:
		#print("Error")
		print(str(e))
		l =-1

	return l

################################################

def run_excel_macro(FileSrc, NomeMacro, parametri):
    i = 0

    FileNameExt = Path(FileSrc).name
    FileName = ModuleFunctions.get_filename_without_ext(FileNameExt)

    try:
        excel = Dispatch("Excel.Application")
        excel.Visible = True

        workbook = excel.Workbooks.Open(FileSrc)

        #workbook.Application.Run("CaricaFoglio")
        #workbook.Application.Run(NomeMacro)     
        #excel.Application.Run("Modulo1.NomeMacro", parametro)

        workbook.Application.Run("ModuloDuplicaColonne.DuplicaColonne", parametri)
        
        l=1

    #except IOError as e:
    except Exception as e:
        print(str(e))
        l =-1

    return l

# file_xls = "TabMensile.xlsx"
	
# abspath = os.path.dirname(os.path.realpath(sys.argv[0]))
# root_path = "D:\\Dati_EdaC_Tirreno_Power_Napoli_BASE_CAMINO"
# FileSourceXls = root_path + "\\File_XL\\" + file_xls

# # Ottieni il percorso della cartella temporanea
# cartella_temp = tempfile.gettempdir()

# # Costruisci il percorso completo del file
# nome_file_tmp = os.path.join(cartella_temp, file_xls)

# shutil.copy(FileSourceXls, nome_file_tmp)

# # Parametri
# colonna_inizio = "A"
# colonna_fine = "G"
# ripetizioni = 2
# righe_max = 50

# duplica_blocco_layout(FileSourceXls, "A", "G", 2, 50, FileSourceXls)

# # # Load the workbook and worksheet
# # wb = openpyxl.load_workbook(nome_file_tmp)
# # ws = wb.active

# # col_start = column_index_from_string(colonna_inizio)
# # col_end = column_index_from_string(colonna_fine)
# # blocco_larghezza = col_end - col_start + 1

# # for i in range(ripetizioni):
# #     col_dest = col_end + 1 + i * blocco_larghezza
# #     copia_layout_colonne(ws, col_start, col_end, col_dest, righe_da_copiare=righe_max)
# # pass

# # wb.save(nome_file_tmp)





