import xml.etree.ElementTree as XMLParse
import xlwt

def spaceOut(string, length):
    return ' '.join(string[i:i+length] for i in range(0,len(string),length))

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')

wb = xlwt.Workbook()
ws = wb.add_sheet('Addresses')
currentRow = 0

inputFile = input("Enter the Name/Path to Cheat Engine File (.CT): ")
outputFile = input("Enter the Name/Path for the output XLS file: ")


document = XMLParse.parse(inputFile.replace(".CT", "") + ".CT")

# Get all headings

headings = document.findall(".//*GroupHeader/..")

for header in headings:

    ws.write(currentRow, 0, header.find("Description").text.strip("\""))
    currentRow += 1
    ws.write(currentRow, 0, "Name")
    ws.write(currentRow, 1, "Type")
    ws.write(currentRow, 2, "Address")
    currentRow += 1

    addresses = header.findall(".//CheatEntry")

    for address in addresses:

        ws.write(currentRow, 0, address.find("Description").text.strip("\""))
        ws.write(currentRow, 1, address.find("VariableType").text.strip("\""))
        ws.write(currentRow, 2, spaceOut(address.find("LastState").attrib["RealAddress"], 4))
        currentRow += 1

    currentRow += 1

# Uncategorized addresses.
uncats = list(set(document.findall("./CheatEntries/CheatEntry") + headings) - set(headings))

ws.write(currentRow, 0, "Uncategorized")
currentRow += 1
ws.write(currentRow, 0, "Name")
ws.write(currentRow, 1, "Type")
ws.write(currentRow, 2, "Address")
currentRow += 1

for uncat in uncats:

    ws.write(currentRow, 0, uncat.find("Description").text.strip("\""))
    ws.write(currentRow, 1, uncat.find("VariableType").text.strip("\""))
    ws.write(currentRow, 2, spaceOut(uncat.find("LastState").attrib["RealAddress"], 4))
    currentRow += 1

wb.save(outputFile.replace(".xls", "") + ".xls")