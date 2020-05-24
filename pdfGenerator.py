import sys, subprocess, os, json, dbCon, datetime, webbrowser

try:
    from reportlab.pdfgen import canvas
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'reportlab'])
finally:
    from reportlab.pdfgen import canvas

try:
    import barcode
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'python-barcode'])
finally:
    import barcode

from barcode.writer import ImageWriter


with open('config.json') as f:
    configFile = json.load(f)

def createPdfTicket(ticketNumber):
    try:
        os.mkdir('tickets')
    except FileExistsError:
        pass
    finally:

        try:
            os.mkdir('.temp')
        except FileExistsError:
            pass
        finally:
            number = str(ticketNumber)
            CODE128 = barcode.get_barcode_class('code128')
            code128 = CODE128(number, writer=ImageWriter())
            code128.save('.temp/tempBarcode',options={"write_text": False})
            
        pdfName = 'bilet_' + str(ticketNumber)
        selectQuerry='WHERE barcode = '+str(ticketNumber)
        ticketData = dbCon.dataSelect('ticket_view',selectQuerry)[0]

        pdf = canvas.Canvas('tickets/'+pdfName+'.pdf')
        pdf.setTitle(pdfName)

        pdf.drawImage('.temp/tempBarcode.png',300,720,anchorAtXY=True,width=310,height=90)
        pdf.setFontSize(11)
        pdf.drawCentredString(300,660, str(ticketNumber))
        pdf.setFontSize(12)

        #comapnyTitle
        pdf.drawCentredString(300,610,configFile['companyName'])
        pdf.line(80,600,520,600)

        #Event name
        pdf.drawString(80, 570,'Nazwa wydarzenia:')
        pdf.drawString(90,550,ticketData[2])

        #Event date
        pdf.drawRightString(500,570,'Data waznosci:')
        pdf.drawRightString(480,550, str(ticketData[4]))

        pdf.line(80,535,520,535)
        #Owner name
        pdf.drawString(80,510,'Imie i nazwisko:')
        pdf.drawString(90,490,str(ticketData[1]))

        #Ticket Price
        pdf.drawString(280,510,"Cena:")
        ticketPrice = round(float(ticketData[3]),2)
        ticketPrice = str(ticketPrice)
        if len(ticketPrice.split('.')[1]) == 2:
            ticketPrice += ' PLN'
        else:
            ticketPrice += "0 PLN"
        pdf.drawString(290,490,ticketPrice)

        #ticket discount
        pdf.drawRightString(500,510,"Znizka:")
        pdf.drawRightString(490,490,str(ticketData[6])+'%')

        #Footer
        currentDay = datetime.date.today()
        now = datetime.datetime.now()
        currnetYear = str(currentDay).split('-')[0]

        pdf.setFontSize(6)
        pdf.drawString(100,455,configFile['companyName'] +' @'+ str(currnetYear))
        pdf.drawCentredString(300,455,'CURD ticketing sytem')
        pdf.drawCentredString(450,455,'Wygenerowano: '+str(now.strftime("%Y-%m-%d %H:%M:%S")))
        pdf.line(0,450,700,450)

        pdf.save()

        os.remove('.temp/tempBarcode.png')
        os.rmdir('.temp')
        webbrowser.open_new(r'file://'+os.path.realpath('tickets/'+pdfName+'.pdf'))

