import binascii, dbCon, datetime, pdfGenerator
from threading import Timer
import tkinter as tk
from tkinter import ttk
import sys, subprocess
from tkinter import messagebox

try:
    import tkcalendar
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'tkcalendar'])
finally:
    import tkcalendar

#accual APP
def barcodeToTicket(barcode):
  i = 1
  while i < len(barcode):
    ticket_id = barcode[:i]
    barcodeID = barcode[i:]
    try:
      testQuerryID = 'WHERE ticket_number = ' + ticket_id
      getTikcetData = dbCon.dataSelect('ticket',testQuerryID)[0]
      getBarcode = getTikcetData[8]
      if getBarcode == barcodeID:
        break
    except:
      ticket_id = barcode[:i]
    finally:
      i+=1
  return ticket_id

def ticketNumberInputGetData(entry1data):
  data = entry1data.get()
  ticketDataShow(data)

def daily_raportDelChoosedItem(barcode):
  dbCon.dataDrop('ticket','barcode',barcode)
  dailyRaport()


#pages
def clear(): #clearing app window to create new wigets
  for windowObject in window.winfo_children():
    windowObject.destroy()

#main menu
def startMenu(): #main menu
  clear()

  titleLabel = tk.Label(window, text='System biletowy "CURD"',font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,columnspan=4,sticky="NEWS", padx=5, pady=5)

  button1 = tk.Button(window, text="Sprzedaj bilet",command=ticketCreation)
  button1.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)


  button2 = tk.Button(window, text="Skasuj bilet", command=ticketNumberInput)
  button2.grid(row=1,column=2,sticky="NEWS", padx=5, pady=5)

  button3 = tk.Button(window, text="Raport dniowy", command=dailyRaport)
  button3.grid(row=2,column=1,sticky="NEWS", padx=5, pady=5)

  button4 = tk.Button(window, text="Wszystkie bielty", command = allTickets)
  button4.grid(row=2,column=2,sticky="NEWS", padx=5, pady=5)

  button5 = tk.Button(window, text="Lista wydarzeń",command=eventList)
  button5.grid(row=4,column=1,columnspan=2,sticky="NEWS", padx=5, pady=5)

  window.grid_rowconfigure(0, weight=1)
  window.grid_rowconfigure(3, weight=1)
  window.grid_columnconfigure(0, weight=1)
  window.grid_columnconfigure(3, weight=1)

#daily raport
def dailyRaport(): #table raport READ & DELETE datas
  def click(event):
    input_id = table.selection()
    input_item = table.item(input_id,"value")[0]
    editData(input_item)
  clear()

  try:
    todaySoldsTickets = dbCon.dataSelect('daily_raport','')[0]
  except:
    messagebox.showerror(title='Błąd krytyczny',message='Wystąpił błąd')
    startMenu()
  finally:
    if todaySoldsTickets[1] != None:
        dailySum = todaySoldsTickets[1]
    else:
      dailySum = 0
    dailySummary = todaySoldsTickets[0]

    titleLabel = tk.Label(window, text="Raport",font='Helvetica 18 bold')
    titleLabel.grid(row=0,column=0,columnspan=4,sticky="NEWS", padx=5, pady=5)

    dailySummary = str(dailySummary) + ' szt.'
    dailySummaryCountLabel = tk.Label(window, text='Ilość sprzedanych dzisaj biletów: ')
    dailySummaryCountLabel.grid(row=1, column=1)
    dailySummaryCount = tk.Label(window, text=dailySummary)
    dailySummaryCount.grid(row=1, column=2)

    dailySum = str(dailySum)
    if len(dailySum.split('.')) == 2:
      dailySum += ' zł'
    else:
      dailySum += "0 zł"
    dailySummarySumLabel = tk.Label(window, text='Dzisiaj zarobiono łącznie: ')
    dailySummarySumLabel.grid(row=1, column=3)
    dailySummarySum = tk.Label(window, text=dailySum)
    dailySummarySum.grid(row=1, column=4)

    label1 = tk.Label(window, text="Wszystkie bilety:")
    label1.grid(row=2, column=1, columnspan=5)

    notChecketTickets = dbCon.dataSelect('ticket_view',"WHERE ticket_status = 0")

    cols = ('Numer biletu','Imię i Nazwisko','Spektakl','Cena','Data ważności','Status')

    #table
    tableFrame = tk.Frame(window)
    tableFrame.grid(row=3, column=1, columnspan=6, pady=10)
    table = ttk.Treeview(tableFrame, columns = cols, show='headings',selectmode='browse')
    vsb = ttk.Scrollbar(tableFrame, orient="vertical", command=table.xview)
    vsb.pack(fill='y',side='right')

    table.configure(yscrollcommand=vsb.set)

    for col in cols:
      table.heading(col, text=col)
    table.column(cols[0],minwidth=400)
    table.column(cols[-0],minwidth=50)
    table.pack()

    
    for i in range(len(notChecketTickets)):
      ticketStatus = str(notChecketTickets[i][5])
      if ticketStatus == '0':
        ticketStatus = 'Skasowany'
      else:
        ticketStatus = 'Nie skasowany'
      ticketPrice = str(notChecketTickets[i][3])
      if len(ticketPrice.split('.')[1]) == 2:
        ticketPrice += ' zł'
      else:
        ticketPrice += "0 zł"
      table.insert("", "end", values=(notChecketTickets[i][0], notChecketTickets[i][1],notChecketTickets[i][2],ticketPrice,notChecketTickets[i][4],ticketStatus))
      table.bind('<Double-1>',click)

    backButton = tk.Button(window, text='Wróć', command=startMenu)
    backButton.grid(row=4,column=1,columnspan=2)

#ticket data
def ticketNumberInput(): #input form to read data
  clear()

  titleLabel = tk.Label(window, text='Podaj numer biletu: ', font='Helvetica 18 bold')
  titleLabel.grid(row=1,column=2,sticky="NEWS", padx=5, pady=5)

  ticketNumber = tk.Entry(window)
  ticketNumber.grid(row=2,column=0,sticky="NEWS", padx=5, pady=5,columnspan=3)


  ticketSubmit = tk.Button(window, text="Sprawdź",command=lambda:ticketNumberInputGetData(ticketNumber))
  ticketSubmit.grid(row=2,column=3,sticky="NEWS", padx=5, pady=5)

  backButton = tk.Button(window, text='Wróć', command=startMenu)
  backButton.grid(row=3,column=1,columnspan=2)

def ticketDataShow(barcode): #raport data (READ)
  clear()
  query = 'WHERE barcode = '+barcode
  ticketData = dbCon.dataSelect('ticket_view',query)[0]

  title = 'Bilet: '+ barcode
  titleLabel = tk.Label(window, text=title, font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan = 2)

  ticketNumberLabelFrame = tk.LabelFrame(window, text='Wydarzenie')
  ticketNumberLabelFrame.grid(row=1,column=1,sticky="NEWS")
  ticketNumber = tk.Label(ticketNumberLabelFrame,text=ticketData[2])
  ticketNumber.pack()

  fullname = ticketData[1]

  fullnameLabelFrame = tk.LabelFrame(window, text='Imię i nazwisko:')
  fullnameLabelFrame.grid(row=1,column=0,sticky="NEWS")
  fullnameLabel = tk.Label(fullnameLabelFrame,text=fullname)
  fullnameLabel.pack()

  ticketPrice = str(ticketData[3])
  if len(ticketPrice.split('.')[1]) == 2:
    ticketPrice += ' zł'
  else:
    ticketPrice += "0 zł"

  priceLabelFrame = tk.LabelFrame(window, text='Cena:')
  priceLabelFrame.grid(row=2,column=0,sticky="NEWS")
  priceLabel = tk.Label(priceLabelFrame,text=ticketPrice)
  priceLabel.pack()
  
  discount = str(ticketData[6]) + '%'

  discountLabelFrame = tk.LabelFrame(window, text='Wartość zniżki:')
  discountLabelFrame.grid(row=2,column=1,sticky="NEWS")
  discountLabel = tk.Label(discountLabelFrame,text=discount)
  discountLabel.pack()

  ticketValidDate = str(ticketData[4])
  currentDay = datetime.date.today()
  if str(currentDay) != ticketValidDate:
    ticketValidDateColor = 'red'
  else:
    ticketValidDateColor = 'green'

  ticketValidDateLabelFrame = tk.LabelFrame(window, text="Data ważności:")
  ticketValidDateLabelFrame.grid(row=3,column=0,sticky="NEWS")
  ticketValidDateLabel = tk.Label(ticketValidDateLabelFrame,text=ticketValidDate, foreground=ticketValidDateColor)
  ticketValidDateLabel.pack()

  ticketStatus = str(ticketData[5])
  if ticketStatus == '0':
    ticketStatus = 'Skasowany'
    ticketStatusColor = 'red'
  else:
    ticketStatus = 'Nie Skasowany'
    ticketStatusColor = 'green'

  ticketStatusLabelFrame = tk.LabelFrame(window, text="Status:")
  ticketStatusLabelFrame.grid(row=3,column=1,sticky="NEWS")
  ticketStatusLabel = tk.Label(ticketStatusLabelFrame,text=ticketStatus,foreground=ticketStatusColor)
  ticketStatusLabel.pack()


  buttonHolder = tk.LabelFrame(window)
  buttonHolder.grid(row=4,column=0)
  backButton = tk.Button(buttonHolder, text='Wróć', command=startMenu)
  backButton.grid(row=0,column=0)

  checkAnotherButton = tk.Button(buttonHolder, text="Sprawdź kolejny", command=ticketNumberInput)
  checkAnotherButton.grid(row=0,column=1)

  checkThatOne = tk.Button(window, text='Skasuj', command=lambda:ticketCheck(ticketData))
  checkThatOne.grid(row=4,column=1)

def ticketCheck(ticketData): #return message after function
  clear()
  ticketID = barcodeToTicket(ticketData[0])
  dateOfValid = str(ticketData[4])
  currentDay = datetime.date.today()
  ticketStatus = str(ticketData[5])
  if str(currentDay) != dateOfValid:
    returnMessage = 'Bilet jest nie aktualny. Nie można go skasować.'
    returnColor = 'red'
  else:
    if ticketStatus == '0':
      returnMessage = 'Bilet jest już skasowany. Nie można go skasować ponownie'
      returnColor = 'red'
    else:
      returnMessage = 'Bilet został skasowany poprawnie'
      returnColor = 'green'
      dbCon.dataUpdate('ticket','ticket_number',str(ticketID),'ticket_status','0')

  messageLabel = tk.Label(window,text=returnMessage,foreground=returnColor,font='Helvetica 18 bold')
  messageLabel.grid(row=1,column=1,sticky='NEWS', padx=5, pady=5,columnspan=2)

  backButton = tk.Button(window,text='Menu',command=startMenu)
  backButton.grid(row=2,column=1,sticky='NEWS', padx=5, pady=5)

  nextButton = tk.Button(window,text='Sprawdź następny',command=ticketNumberInput)
  nextButton.grid(row=2,column=2,sticky='NEWS', padx=5, pady=5)

#create ticket
def ticketCreation():
  clear()
  titleLabel = tk.Label(window,text='Utwórz nowy bilet',font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=2)

  #fullname
  nameInputFrame = tk.LabelFrame(window,text='Imię')
  nameInput = tk.Entry(nameInputFrame)
  nameInput.pack()
  nameInputFrame.grid(row=1,column=0,sticky="NEWS", padx=5, pady=5)

  surnameInputFrame = tk.LabelFrame(window,text='Nazwisko')
  surnameInput = tk.Entry(surnameInputFrame)
  surnameInput.pack()
  surnameInputFrame.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)

  #options menus

  eventList = []

  events = dbCon.dataSelect('movie','')

  for event in events:
    eventList.append(event[1])

  eventsVar = tk.StringVar(window)
  eventsVar.set(eventList[0])

  eventsOptionFrame = tk.LabelFrame(window,text='Wydarzenie')
  eventsOption = tk.OptionMenu(eventsOptionFrame,eventsVar,*eventList)
  eventsOption.pack()
  eventsOptionFrame.grid(row=2,column=0,sticky="NEWS", padx=5, pady=5)

  discounts = ['Normalny - 0%','Szkolny - 25%','Studencki - 30%','Seniorski - 50%']

  discountVar = tk.StringVar(window)
  discountVar.set(discounts[0])

  discountOptionFrame = tk.LabelFrame(window,text='Zniżka')
  discountOption = tk.OptionMenu(discountOptionFrame,discountVar,*discounts)
  discountOption.pack()
  discountOptionFrame.grid(row=2,column=1,sticky="NEWS", padx=5, pady=5)

  #date
  dateOfvaildFrame = tk.LabelFrame(window,text='Data')
  dateOfvaild = tkcalendar.Calendar(dateOfvaildFrame,cursor="hand1")
  dateOfvaild.pack()
  dateOfvaildFrame.grid(row=3,column=0,columnspan=2,sticky="NEWS", padx=5, pady=5)

  backButton = tk.Button(window, text='Wróć', command=startMenu)
  backButton.grid(row=4,column=0)

  submitButton = tk.Button(window, text='Zatwierdź', command=lambda: newTikectData(nameInput,surnameInput,eventsVar,discountVar,dateOfvaild))
  submitButton.grid(row=4,column=1)

def newTikectData(name,surname,event_name,discount,event_date):
  name = name.get()
  surname = surname.get()
  event_name = event_name.get()
  discount = discount.get()
  event_date = event_date.selection_get()
  clear()
  eventQuerry = 'WHERE movie_name = "' + str(event_name) + '"'
  eventInfo = dbCon.dataSelect('movie',eventQuerry)[0]

  eventID = eventInfo[0]
  eventPrice = eventInfo[2]

  realDiscount = discount.split(' ')[-1][:-1]
  currentDay = datetime.date.today()

  ticketBarcode = str(eventID)
  ticketBarcodeData = surname + str(currentDay)
  ticketBarcode += str(int.from_bytes(ticketBarcodeData.encode(), 'big'))

  fullname = str(name) + ' ' + str(surname)
  ticketPrice = round(float(eventPrice) * (1 - int(realDiscount) / 100),2)
  ticketPrice = str(ticketPrice)
  if len(str(ticketPrice).split('.')[1]) == 2:
    ticketPrice += ' zł'
  else:
    ticketPrice += "0 zł"
  discountValue = str(realDiscount) + '%'

  titleLabel = tk.Label(window, text='Nowy bilet', font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=2)

  fullnameLabelFrame = tk.LabelFrame(window, text='Imię i nazwisko:')
  fullnameLabelFrame.grid(row=1,column=0,sticky="NEWS",columnspan=2)
  fullnameLabel = tk.Label(fullnameLabelFrame,text=fullname)
  fullnameLabel.pack()

  ticketEventNameLabelFrame = tk.LabelFrame(window, text='Nazwa wydarzenia')
  ticketEventNameLabelFrame.grid(row=2,column=0,sticky='NEWS')
  ticketEventNameLabel = tk.Label(ticketEventNameLabelFrame,text=event_name)
  ticketEventNameLabel.pack()

  ticketValidDateLabelFrame = tk.LabelFrame(window, text="Data ważności:")
  ticketValidDateLabelFrame.grid(row=2,column=1,sticky="NEWS")
  ticketValidDateLabel = tk.Label(ticketValidDateLabelFrame,text=event_date)
  ticketValidDateLabel.pack()

  priceLabelFrame = tk.LabelFrame(window, text='Cena:')
  priceLabelFrame.grid(row=3,column=0,sticky="NEWS")
  priceLabel = tk.Label(priceLabelFrame,text=ticketPrice)
  priceLabel.pack()

  discountLabelFrame = tk.LabelFrame(window, text='Wartość zniżki:')
  discountLabelFrame.grid(row=3,column=1,sticky="NEWS")
  discountLabel = tk.Label(discountLabelFrame,text=discountValue)
  discountLabel.pack()

  submitButton = tk.Button(window,text='Stwórz',command=lambda: insertData(name,surname,eventID,realDiscount,event_date,currentDay,ticketBarcode))
  submitButton.grid(row=4,column=0,sticky='NEWS', padx=5, pady=5,columnspan=2)

  backButton = tk.Button(window,text='Menu',command=startMenu)
  backButton.grid(row=5,column=0,sticky='NEWS', padx=5, pady=5)

  nextButton = tk.Button(window,text='Stwórz inny',command=ticketCreation)
  nextButton.grid(row=5,column=1,sticky='NEWS', padx=5, pady=5)

def insertData(name,surname,movie_id,discount,day_of_valid,date_of_sold,barcode):
  insertQuery = "'"+str(name)+"','"+str(surname)+"',"+str(movie_id)+','+str(discount)+',"'+str(day_of_valid)+'",1,"'+str(date_of_sold)+'",'+str(barcode)

  try:
    dbCon.dataInsert('ticket',insertQuery)
    resultColor = 'green'
    resultMessage = 'Pomyślnie dodano bilet.'
    
  except:
    resultColor = 'red'
    resultMessage = 'Wysąpił błąd :('
  finally:
    clear()
    resultLabel = tk.Label(window,text=resultMessage,font='Helvetica 18 bold',foreground=resultColor)
    resultLabel.grid(row=0,column=0,columnspan=2,sticky='NEWS', padx=5, pady=5)

    backButton = tk.Button(window,text='Menu',command=startMenu)
    backButton.grid(row=1,column=0,sticky='NEWS', padx=5, pady=5)

    nextButton = tk.Button(window,text='Stwórz następny',command=ticketCreation)
    nextButton.grid(row=1,column=1,sticky='NEWS', padx=5, pady=5)

    #pdfCrating
    insetedTikcetData = dbCon.dataSelect('ticket',str('WHERE barcode = '+str(barcode)))[0]
    realBarcode = str(insetedTikcetData[0]) + str(barcode)
    pdfGenerator.createPdfTicket(realBarcode)

#overall raport
def allTickets(): #table raport READ & DELETE datas
  def click(event):
    input_id = table.selection()
    input_item = table.item(input_id,"value")[0]
    editData(input_item)
  clear()

  todaySoldsTickets = dbCon.dataSelect('overall_raport','')[0]

  if todaySoldsTickets[1] != None:
      dailySum = todaySoldsTickets[1]
  else:
    dailySum = 0
  dailySummary = todaySoldsTickets[0]

  titleLabel = tk.Label(window, text="Raport",font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,columnspan=4,sticky="NEWS", padx=5, pady=5)

  dailySummary = str(dailySummary) + ' szt.'
  dailySummaryCountLabel = tk.Label(window, text='Ilość sprzedanych biletów: ')
  dailySummaryCountLabel.grid(row=1, column=1)
  dailySummaryCount = tk.Label(window, text=dailySummary)
  dailySummaryCount.grid(row=1, column=2)

  dailySum = str(dailySum)
  if len(dailySum.split('.')) == 2:
    dailySum += ' zł'
  else:
    dailySum += "0 zł"
  dailySummarySumLabel = tk.Label(window, text='Zarobiono łącznie: ')
  dailySummarySumLabel.grid(row=1, column=3)
  dailySummarySum = tk.Label(window, text=dailySum)
  dailySummarySum.grid(row=1, column=4)

  label1 = tk.Label(window, text="Wszystkie bilety:")
  label1.grid(row=2, column=1, columnspan=5)

  notChecketTickets = dbCon.dataSelect('ticket_view',"")

  cols = ('Numer biletu','Imię i Nazwisko','Spektakl','Cena','Data ważności','Status')

  #table
  tableFrame = tk.Frame(window)
  tableFrame.grid(row=3, column=1, columnspan=6, pady=10)
  table = ttk.Treeview(tableFrame, columns = cols, show='headings',selectmode='browse')
  vsb = ttk.Scrollbar(tableFrame, orient="vertical", command=table.xview)
  vsb.pack(fill='y',side='right')

  table.configure(yscrollcommand=vsb.set)

  for col in cols:
    table.heading(col, text=col)
  table.column(cols[0],minwidth=400)
  table.column(cols[-0],minwidth=50)
  table.pack()

  
  for i in range(len(notChecketTickets)):
    ticketStatus = str(notChecketTickets[i][5])
    if ticketStatus == '0':
      ticketStatus = 'Skasowany'
    else:
      ticketStatus = 'Nie skasowany'
    ticketPrice = str(notChecketTickets[i][3])
    if len(ticketPrice.split('.')[1]) == 2:
      ticketPrice += ' zł'
    else:
      ticketPrice += "0 zł"
    table.insert("", "end", values=(notChecketTickets[i][0], notChecketTickets[i][1],notChecketTickets[i][2],ticketPrice,notChecketTickets[i][4],ticketStatus))
    table.bind('<Double-1>',click)

  backButton = tk.Button(window, text='Wróć', command=startMenu)
  backButton.grid(row=4,column=1,columnspan=2)    

#edit menu
def editData(barcode):
  ticketID = barcodeToTicket(barcode)
  selectQuerry = 'WHERE ticket_number = ' + ticketID
  currentData = dbCon.dataSelect('ticket',selectQuerry)[0]
  name = currentData[1]
  surname = currentData[2]
  eventID = int(currentData[3])
  clear()

  titleText = 'Edytuj bilet: ' + barcode
  titleLabel = tk.Label(window,text=titleText,font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=2)

  nameInputFrame = tk.LabelFrame(window,text='Imię')
  NameText = tk.StringVar()
  nameInput = tk.Entry(nameInputFrame,textvariable=NameText)
  NameText.set(name)
  nameInput.pack()
  nameInputFrame.grid(row=1,column=0,sticky="NEWS", padx=5, pady=5)

  surnameInputFrame = tk.LabelFrame(window,text='Nazwisko')
  SurnameText=tk.StringVar()
  surnameInput = tk.Entry(surnameInputFrame,textvariable=SurnameText)
  SurnameText.set(surname)
  surnameInput.pack()
  surnameInputFrame.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)

  eventList = []

  events = dbCon.dataSelect('movie','')

  for event in events:
    eventList.append(event[1])
  eventsVar = tk.StringVar(window)
  eventsVar.set(eventList[eventID-1])

  eventsOptionFrame = tk.LabelFrame(window,text='Wydarzenie')
  eventsOption = tk.OptionMenu(eventsOptionFrame,eventsVar,*eventList)
  eventsOption.pack()
  eventsOptionFrame.grid(row=2,column=0,sticky="NEWS", padx=5, pady=5)

  discounts = ['Normalny - 0%','Szkolny - 25%','Studencki - 30%','Seniorski - 50%']
  for i in range(len(discounts)):
    listDiscountValue = discounts[i].split(' ')[-1][:-1]
    if int(listDiscountValue) == int(currentData[4]):
      setValue = discounts[i]
      break
    else:
      setValue = str(int(currentData[4])) + '%'


  discountVar = tk.StringVar(window)
  discountVar.set(setValue)

  discountOptionFrame = tk.LabelFrame(window,text='Zniżka')
  discountOption = tk.OptionMenu(discountOptionFrame,discountVar,*discounts)
  discountOption.pack()
  discountOptionFrame.grid(row=2,column=1,sticky="NEWS", padx=5, pady=5)

  #date
  dataValue = str(currentData[5]).split('-')
  dataValueDay = int(dataValue[2])
  dataValueMonth = int(dataValue[1])
  dataValueYear = int(dataValue[0])

  dateOfvaildFrame = tk.LabelFrame(window,text='Data')
  dateOfvaild = tkcalendar.Calendar(dateOfvaildFrame,cursor="hand1",year=dataValueYear,month=dataValueMonth,day=dataValueDay)
  dateOfvaild.pack()
  dateOfvaildFrame.grid(row=3,column=0,sticky="NEWS", padx=5, pady=5)

  ticketStatusFrame = tk.LabelFrame(window)
  ticketStatusFrame.grid(row=3,column=1,sticky="NEWS", padx=5, pady=5)

  ticketStatuses = ['Skasowany','Nie Skasowany']

  ticketStatus = str(currentData[6])
  if ticketStatus == '0':
    ticketStatus = 0
    ticketStatusColor = 'red'
  else:
    ticketStatus = 1
    ticketStatusColor = 'green'
  
  ticketStatusLabelFrame = tk.LabelFrame(ticketStatusFrame,text='Aktualny status biletu')
  ticketStatusLabel = tk.Label(ticketStatusLabelFrame,text=ticketStatuses[ticketStatus],foreground=ticketStatusColor,font='Helvetica 18 bold')
  ticketStatusLabelFrame.pack(fill='x')
  ticketStatusLabel.pack()

  ticketStatusVar = tk.StringVar(window)
  ticketStatusVar.set(ticketStatuses[ticketStatus])
  ticketStatusSetOption = tk.OptionMenu(ticketStatusFrame,ticketStatusVar,*ticketStatuses)
  ticketStatusSetOption.pack(fill='x')

  
  buttonHolder = tk.LabelFrame(window)
  buttonHolder.grid(row=4,column=0,columnspan=2)

  backButton = tk.Button(buttonHolder, text='Wróć', command=allTickets, foreground='gray')
  backButton.pack(side='left',padx=10,pady=5)
  delButton = tk.Button(buttonHolder,text='Usuń',foreground='red',command=lambda: deleteTicket(ticketID))
  delButton.pack(side='left',padx=10,pady=5)
  showPdfTicket = tk.Button(buttonHolder,text='Pokaż bilet pdf',foreground='gray',command=lambda: pdfGenerator.createPdfTicket(barcode))
  showPdfTicket.pack(side='left',padx=10,pady=5)
  submitButton = tk.Button(buttonHolder, text='Zapisz zmiany',foreground='gray', command=lambda: dataDiffrence(ticketID,nameInput,surnameInput,eventsVar,discountVar,dateOfvaild,ticketStatusVar))
  submitButton.pack(side='left',padx=10,pady=5)

def deleteTicket(ticket_id):
  try:
    dbCon.dataDrop('ticket','ticket_number',ticket_id)
    returnText = 'Poprawnie usunięto'
  except:
    returnText = 'Wystąpił błąd ;('
  finally:
    clear()
    saveReplay = tk.Label(window,text=returnText,font='Helvetica 18 bold')
    saveReplay.grid(row=0,column=0,sticky='NEWS')
    adnotation = tk.Label(window,text='Zachwilę nastąpi przeniesienie do listy')
    adnotation.grid(row=1,column=0,sticky='NEWS')
    backButton = tk.Button(window,text='Wróć teraz',command=allTickets)
    backButton.grid(row=2,column=0,sticky='NEWS')
    timer = Timer(2.5,allTickets)
    timer.start()

def dataDiffrence(ticket_id,name,surname,movie_name,discountFull,day_of_vaild,ticket_status_name):
  ticket_id = ticket_id
  name = name.get()
  surname = surname.get()
  movie_name = movie_name.get()
  discountFull = discountFull.get()
  day_of_vaild = day_of_vaild.selection_get()
  ticket_status_name = ticket_status_name.get()


  orginalDataQuerry = 'WHERE ticket_number = ' + str(ticket_id)
  orginalData = dbCon.dataSelect('ticket',orginalDataQuerry)[0]
  orginalMovieName = 'WHERE movie_id = ' + str(orginalData[3])
  barcode = str(ticket_id)+str(orginalData[8])
  if str(orginalData[6]) == '0':
    orginalTicketStatus = 'Skasowany'
  else:
    orginalTicketStatus = 'Nie Skasowany'
  orginalDatas = [orginalData[1],orginalData[2],orginalData[3],dbCon.dataSelect('movie',orginalMovieName)[0][1],int(orginalData[4]),str(orginalData[5]),int(orginalData[6]),orginalTicketStatus,orginalData[8]]
  newMovieName = 'WHERE movie_name = "' + str(movie_name) + '"'
  discount = str(discountFull).split(' ')[-1][:-1]
  if ticket_status_name == 'Skasowany':
    newTicketStatus = '0'
  else:
    newTicketStatus = '1'

  newDatas = [name,surname,dbCon.dataSelect('movie',newMovieName)[0][0],movie_name,int(discount),str(day_of_vaild),int(newTicketStatus),ticket_status_name,orginalData[8]]

  clear()
  if orginalDatas == newDatas:

    saveReplay = tk.Label(window,text='Nie wprowadzono żadnych zmian',font='Helvetica 18 bold')
    saveReplay.grid(row=0,column=0,sticky='NEWS')
    adnotation = tk.Label(window,text='Zachwilę nastąpi przeniesienie do listy')
    adnotation.grid(row=1,column=0,sticky='NEWS')
    backButton = tk.Button(window,text='Wróć teraz',command=allTickets)
    backButton.grid(row=2,column=0,sticky='NEWS')
    timer = Timer(2.5,allTickets)
    timer.start()
  else:
    titleText = 'Wprowadź zmiany w: ' +str(ticket_id)+str(orginalData[8])
    titleLabel = tk.Label(window,text=titleText,font='Helvetica 18 bold')
    titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=4)
    oldFrame = tk.LabelFrame(window,text='Zamień z')
    oldFrame.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)
    newFrame = tk.LabelFrame(window,text='Zamień na')
    newFrame.grid(row=1,column=2,sticky="NEWS", padx=5, pady=5)
    for i in range(len(newDatas)):
      if newDatas[i] != orginalDatas[i]:
        if i == 2:
          continue
        elif i == 6:
          continue
        elif i == 4:
          oldDataText = str(orginalDatas[i]) + '%'
          newDataText = str(newDatas[i]) + '%'
        else:
          oldDataText = orginalDatas[i]
          newDataText = newDatas[i]
        
        oldData = tk.Label(oldFrame,text=oldDataText)
        oldData.pack(fill='x',padx=5,pady=5)

        newData = tk.Label(newFrame,text=newDataText)
        newData.pack(fill='x',padx=5,pady=5)
    backButton = tk.Button(window,text='Anuluj',command=lambda: editData(barcode))
    backButton.grid(row=2,column=1,sticky='NEWS')

    confirmButton = tk.Button(window,text="Zatwierdź",command=lambda: insertDiffrence(ticket_id,orginalDatas,newDatas))
    confirmButton.grid(row=2,column=2,sticky='NEWS')

def insertDiffrence(ticket_id,oldData,newData):
  columnsNames = ['name','surname','movie_id','movie_name','discount','day_of_valid','ticket_status','ticket_status_name','barcode']
  try:
    for i in range(len(columnsNames)):
      if oldData[i] != newData[i]:
          if i == 3:
            continue
          elif i == 7:
            continue
          elif i == 8:
            continue
          else:
            dbCon.dataUpdate('ticket','ticket_number',str(ticket_id),str(columnsNames[i]),str(newData[i]))
            returnText = 'Pomyślnie wprowadzono zmiany'

            pdfGenerator.createPdfTicket(newData[8])
  except:
    returnText = 'Wystąpił błąd ;('
  finally:
    clear()

    saveReplay = tk.Label(window,text=returnText,font='Helvetica 18 bold')
    saveReplay.grid(row=0,column=0,sticky='NEWS')
    adnotation = tk.Label(window,text='Zachwilę nastąpi przeniesienie do listy')
    adnotation.grid(row=1,column=0,sticky='NEWS')
    backButton = tk.Button(window,text='Wróć teraz',command=allTickets)
    backButton.grid(row=2,column=0,sticky='NEWS')
    timer = Timer(2.5,allTickets)
    timer.start()

#events managment
#event list
def eventList():
  def click(event):
    input_id = table.selection()
    input_item = table.item(input_id,"value")[0]
    editEventData(input_item)
  clear()

  label1 = tk.Label(window, text="Wszystkie wydarzenia:",font='Helvetica 18 bold')
  label1.grid(row=0, column=1, columnspan=5)

  notChecketTickets = dbCon.dataSelect('movie',"")

  cols = ('ID','Nazwa wydarzenia','Cena biletu')

  #table
  tableFrame = tk.Frame(window)
  tableFrame.grid(row=1, column=1, columnspan=6, pady=10)
  table = ttk.Treeview(tableFrame, columns = cols, show='headings',selectmode='browse')
  vsb = ttk.Scrollbar(tableFrame, orient="vertical", command=table.xview)
  vsb.pack(fill='y',side='right')

  table.configure(yscrollcommand=vsb.set)
  for col in cols:
    table.heading(col, text=col)
  table.column(cols[0],width=30)
  table.pack()

  
  for i in range(len(notChecketTickets)):
    ticketPrice = str(notChecketTickets[i][2])
    if len(ticketPrice.split('.')[1]) == 2:
      ticketPrice += ' zł'
    else:
      ticketPrice += "0 zł"
    table.insert("", "end", values=(notChecketTickets[i][0],notChecketTickets[i][1], ticketPrice))
    table.bind('<Double-1>',click)
  buttonFrame = tk.LabelFrame(window)
  buttonFrame.grid(row=2,column=2,columnspan=2)

  backButton = tk.Button(buttonFrame, text='Wróć', command=startMenu)
  backButton.grid(row=0,column=0,pady=5,padx=5)

  createNewButton = tk.Button(buttonFrame,text='Dodaj nowe wydarzenie',command=crateNewEvent)
  createNewButton.grid(row=0,column=1,pady=5,padx=5)

def editEventData(event_id):
  selectQuerry = 'WHERE movie_id = ' + event_id
  currentData = dbCon.dataSelect('movie',selectQuerry)[0]
  name = currentData[1]
  price = currentData[2]
  clear()

  titleText = 'Edytuj wydarzenie: ' + name
  titleLabel = tk.Label(window,text=titleText,font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=2)

  nameInputFrame = tk.LabelFrame(window,text='Nazwa')
  NameText = tk.StringVar()
  nameInput = tk.Entry(nameInputFrame,textvariable=NameText)
  NameText.set(name)
  nameInput.pack()
  nameInputFrame.grid(row=1,column=0,sticky="NEWS", padx=5, pady=5)

  priceInputFrame = tk.LabelFrame(window,text='Cena (w PLN)')
  priceText=tk.StringVar()
  priceInput = tk.Entry(priceInputFrame,textvariable=priceText)
  priceText.set(price)
  priceInput.pack()
  priceInputFrame.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)

  buttonHolder = tk.LabelFrame(window)
  buttonHolder.grid(row=4,column=0,columnspan=2)

  backButton = tk.Button(buttonHolder, text='Wróć', command=eventList, foreground='gray')
  backButton.pack(side='left',padx=10,pady=5)
  delButton = tk.Button(buttonHolder,text='Usuń',foreground='red',command=lambda: deleteEvent(event_id))
  delButton.pack(side='left',padx=10,pady=5)
  submitButton = tk.Button(buttonHolder, text='Zapisz zmiany',foreground='gray', command=lambda: eventDataDiffrence(event_id,NameText,priceText))
  submitButton.pack(side='left',padx=10,pady=5)

def eventDataDiffrence(eventID,newName,newPrice):
  orginalDataQuerry = 'WHERE movie_id = '+str(eventID)
  orginalEventData = dbCon.dataSelect('movie',orginalDataQuerry)[0]
  orginalName = orginalEventData[1]
  orginalPrice = str(orginalEventData[2])

  newName = newName.get()
  newPrice = str(newPrice.get())
  
  clear()
  if orginalName == newName and orginalPrice == newPrice:

    saveReplay = tk.Label(window,text='Nie wprowadzono żadnych zmian',font='Helvetica 18 bold')
    saveReplay.grid(row=0,column=0,sticky='NEWS')
    adnotation = tk.Label(window,text='Zachwilę nastąpi przeniesienie do listy')
    adnotation.grid(row=1,column=0,sticky='NEWS')
    backButton = tk.Button(window,text='Wróć teraz',command=eventList)
    backButton.grid(row=2,column=0,sticky='NEWS')
    timer = Timer(2.5,eventList)
    timer.start()
  
  else:
    titleText = 'Wprowadź zmiany w: ' +str(eventID)+' '+str(orginalName)
    titleLabel = tk.Label(window,text=titleText,font='Helvetica 18 bold')
    titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=4)
    oldFrame = tk.LabelFrame(window,text='Zamień z')
    oldFrame.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)
    newFrame = tk.LabelFrame(window,text='Zamień na')
    newFrame.grid(row=1,column=2,sticky="NEWS", padx=5, pady=5)
    insertName = orginalName
    insertPrice = orginalPrice
    for i in range(1):
      if orginalName != newName:
        oldData = tk.Label(oldFrame,text=orginalName)
        oldData.pack(fill='x',padx=5,pady=5)

        newData = tk.Label(newFrame,text=newName)
        newData.pack(fill='x',padx=5,pady=5)
        insertName = newName
      if orginalPrice != newPrice:
        oldData = tk.Label(oldFrame,text=orginalPrice)
        oldData.pack(fill='x',padx=5,pady=5)

        newData = tk.Label(newFrame,text=newPrice)
        newData.pack(fill='x',padx=5,pady=5)
        insertPrice = newPrice
    backButton = tk.Button(window,text='Anuluj',command=lambda: editEventData(eventID))
    backButton.grid(row=2,column=1,sticky='NEWS')

    confirmButton = tk.Button(window,text="Zatwierdź",command=lambda: insertEventDiffrence(eventID,insertName,insertPrice))
    confirmButton.grid(row=2,column=2,sticky='NEWS')

def insertEventDiffrence(ticket_id,insertName,insertPrice):
  try:
    dbCon.dataUpdate('movie','movie_id',ticket_id,'movie_name','"'+str(insertName)+'"')
    dbCon.dataUpdate('movie','movie_id',ticket_id,'ticket_price','"'+str(insertPrice)+'"')
    returnText = 'Pomyślnie wprowadzono zmiany'
  except:
    returnText = 'Wystąpił błąd ;('
  finally:
    clear()

    saveReplay = tk.Label(window,text=returnText,font='Helvetica 18 bold')
    saveReplay.grid(row=0,column=0,sticky='NEWS')
    adnotation = tk.Label(window,text='Zachwilę nastąpi przeniesienie do listy')
    adnotation.grid(row=1,column=0,sticky='NEWS')
    backButton = tk.Button(window,text='Wróć teraz',command=eventList)
    backButton.grid(row=2,column=0,sticky='NEWS')
    timer = Timer(2.5,eventList)
    timer.start()

#event deleting
def deleteEvent(event_id):
  try:
    dbCon.dataDrop('movie','ticket_id',event_id)
    returnText = 'Poprawnie usunięto'
  except:
    returnText = 'Wystąpił błąd ;('
  finally:
    clear()
    saveReplay = tk.Label(window,text=returnText,font='Helvetica 18 bold')
    saveReplay.grid(row=0,column=0,sticky='NEWS')
    adnotation = tk.Label(window,text='Zachwilę nastąpi przeniesienie do listy')
    adnotation.grid(row=1,column=0,sticky='NEWS')
    backButton = tk.Button(window,text='Wróć teraz',command=eventList)
    backButton.grid(row=2,column=0,sticky='NEWS')
    timer = Timer(2.5,eventList)
    timer.start()

#event crating
def crateNewEvent():
  clear()

  titleText = 'Utwórz nowe wydarzenie:'
  titleLabel = tk.Label(window,text=titleText,font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=2)

  nameInputFrame = tk.LabelFrame(window,text='Nazwa')
  nameText = tk.StringVar()
  nameInput = tk.Entry(nameInputFrame,textvariable=nameText)
  nameInput.pack()
  nameInputFrame.grid(row=1,column=0,sticky="NEWS", padx=5, pady=5)

  priceInputFrame = tk.LabelFrame(window,text='Cena (w PLN)')
  priceText=tk.StringVar()
  priceInput = tk.Entry(priceInputFrame,textvariable=priceText)
  priceInput.pack()
  priceInputFrame.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)

  buttonHolder = tk.LabelFrame(window)
  buttonHolder.grid(row=4,column=0,columnspan=2)

  backButton = tk.Button(buttonHolder, text='Wróć', command=eventList, foreground='gray')
  backButton.pack(side='left',padx=10,pady=5)
  submitButton = tk.Button(buttonHolder, text='Zapisz zmiany',foreground='gray', command=lambda: newEventCheck(nameText,priceText))
  submitButton.pack(side='left',padx=10,pady=5)

def newEventCheck(name,price):
  clear()
  priceText = price.get()
  titleLabel = tk.Label(window,text='Dodaj nowe wydarzenie',font='Helvetica 18 bold')
  titleLabel.grid(row=0,column=0,sticky="NEWS", padx=5, pady=5,columnspan=4)
  nameFrame = tk.LabelFrame(window,text='Nazwa wydarzenia')
  nameFrame.grid(row=1,column=1,sticky="NEWS", padx=5, pady=5)
  priceFrame = tk.LabelFrame(window,text='Podstawowa cena z bilet')
  priceFrame.grid(row=1,column=2,sticky="NEWS", padx=5, pady=5)

  nametext = name.get()
  nameLabel = tk.Label(nameFrame,text=nametext)
  nameLabel.pack()

  if len(priceText.split('.')) == 2:
    if priceText[1] != 0:
      priceText += ' zł'
    else:  
      priceText += '0 zł'
  else:
    priceText += ".00 zł" 
  priceLabel = tk.Label(priceFrame,text=priceText)
  priceLabel.pack()

  submitButton = tk.Button(window,text='Stwórz',command=lambda: insertEventData(nametext,price.get()))
  submitButton.grid(row=3,column=1,sticky='NEWS', padx=5, pady=5,columnspan=2)

  backButton = tk.Button(window,text='Menu',command=startMenu)
  backButton.grid(row=4,column=1,sticky='NEWS', padx=5, pady=5)

  nextButton = tk.Button(window,text='Stwórz inny',command=crateNewEvent)
  nextButton.grid(row=4,column=2,sticky='NEWS', padx=5, pady=5)

def insertEventData(name,price):
  insertQuery = "'"+str(name)+"',"+str(price)

  try:
    dbCon.dataInsert('movie',insertQuery)
    resultColor = 'green'
    resultMessage = 'Pomyślnie dodano bilet.'
    
  except:
    resultColor = 'red'
    resultMessage = 'Wysąpił błąd :('
  finally:
    clear()
    resultLabel = tk.Label(window,text=resultMessage,font='Helvetica 18 bold',foreground=resultColor)
    resultLabel.grid(row=0,column=0,columnspan=2,sticky='NEWS', padx=5, pady=5)

    backButton = tk.Button(window,text='Menu',command=startMenu)
    backButton.grid(row=1,column=0,sticky='NEWS', padx=5, pady=5)

    nextButton = tk.Button(window,text='Stwórz następny',command=crateNewEvent)
    nextButton.grid(row=1,column=1,sticky='NEWS', padx=5, pady=5)


#main funcion
window = tk.Tk()
window.minsize(500,400)
window.title('System biletowy "CURD"')

startMenu()

window.mainloop()