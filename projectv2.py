import tkinter as tk
from tkinter import ttk
import cv2                       ##
import os
from tkinter import  filedialog as tkFileDialog
import matplotlib.pyplot as plt  ##
import numpy as np               ##
from PIL import ImageTk
from PIL import Image
from pathlib import Path


scriptDir = os.path.dirname(__file__)
os.chdir(scriptDir)


mainWindow = tk.Tk()




class MainProject():
    def __init__(self, window):
       
        self.listOfDuplicates = []
        self.indexOfList = 0
        self.indexofHist = 1


        self.listOfButtons = []
        self.dictOfEveryImage = {}
   

        self.isActiveValue = None
        self.isActiveKey = None

        self.path = ""
       
       
        self.prepareGui(window)
       
       



    def prepareGui(self, window):
        window.geometry("550x350")
        window.title("APO projekt")


        label = tk.Label(window, text = "Aktywne obrazy: ")
        label.grid(row=1,columnspan=8)

        rootMenu = tk.Menu()

        self.fileMenu(window,rootMenu)
        self.lab1Menu(window,rootMenu)
        self.lab2Menu(window,rootMenu)
        self.lab3Menu(window,rootMenu)
        self.lab4Menu(window,rootMenu)
        self.lab5Menu(window,rootMenu)
        self.lab6Menu(window,rootMenu)
        self.finalMiniProject(window, rootMenu)



        self.addButton(window)
        #label1 = tk.Label(window, text="20 20 20 20", height=5, width=20, anchor="s", bg="silver").pack()
   

    def fileMenu(self, window,rootMenu):
        file = tk.Menu()
        file.add_command(label="Otworz", command=self.loadImage)
        file.add_command(label="Duplikuj ostatni", command=self.duplicateImage)
        file.add_command(label="Zapisz", command=self.saveImg)

        rootMenu.add_cascade(label="File", menu=file)
        window.config(menu=rootMenu)

    def lab1Menu(self, window, rootMenu):
        lab1 = tk.Menu()
        lab1.add_command(label="Histogram", command=self.printHistogram)
        lab1.add_command(label="Wypisz otwarte obrazy",command=self.printImages )
        lab1.add_command(label="Grayscale",command=self.toGrayscale )
        rootMenu.add_cascade(label="Lab1", menu=lab1)
        window.config(menu=rootMenu)


    def lab2Menu(self, window, rootMenu):
        lab2 = tk.Menu()
        lab2.add_command(label="Rozciągniecie histogramu",command=self.strechHistogram)
        lab2.add_command(label="Rozciągniecie histogramu z par. a i b",command=self.strechHistogramWithParameters)
        lab2.add_command(label="Wyrownanie przez equalizację",command=self.imageEqualization)
        lab2.add_separator()
        lab2.add_command(label="Negacja",command=self.imageNegation)
        lab2.add_command(label="Progowanie binarne",command=self.imageThreshold)
        lab2.add_command(label="Progowanie z zach. poz. szar.",command=self.imageThresholdWithGrayscale)
        lab2.add_command(label="Progowanie z dwoma progami",command=self.imageThresholdWithGrayscaleTwoLimits)
        lab2.add_command(label="Korekcja gamma",command=self.gammaCorrection)
       
        rootMenu.add_cascade(label="Lab2", menu=lab2)
        window.config(menu=rootMenu)

    def lab3Menu(self, window, rootMenu):
        lab3 = tk.Menu()
        lab3.add_command(label="Dodawanie obrazów.",command=self.addImages)
        lab3.add_command(label="Dodawanie stałej",command=self.addConstantImage)
        lab3.add_command(label="Mnożenie przez stała",command=self.multiplicationImages)
        lab3.add_command(label="Dzielenie przez stała",command=self.divideImages)
        lab3.add_command(label="Różnica bezwzg. obrazów",command=self.subtractionImages)
        lab3.add_separator()
        lab3.add_command(label="NOT",command=self.imageNotProcessing)
        lab3.add_command(label="AND",command=self.imageAndProcessing)
        lab3.add_command(label="OR",command=self.imageOrProcessing)
        lab3.add_command(label="XOR",command=self.imageXorProcessing)
       
        rootMenu.add_cascade(label="Lab3", menu=lab3)
        window.config(menu=rootMenu)

    def lab4Menu(self, window, rootMenu):
        lab4 = tk.Menu()
        lab4.add_command(label="Wygładzanie liniowe",command=self.imageSmoothLinear)
        lab4.add_command(label="Wyostrzanie liniowe",command=self.imageSharpeningLinear)
        lab4.add_command(label="Kierunkowa detekcja",command=self.imageEdgeDetection)
        lab4.add_separator()
        lab4.add_command(label="Mediana",command=self.imageMedianProcessing)

       
        rootMenu.add_cascade(label="Lab4", menu=lab4)
        window.config(menu=rootMenu)
       
    def lab5Menu(self, window, rootMenu):
        lab5 = tk.Menu()
        lab5.add_command(label="Detekcja krawedzi",command=self.edgeDetection)
        lab5.add_separator()
        lab5.add_command(label="Progowanie Otsu",command=self.otsuThreshold)
        lab5.add_command(label="Progowanie Adaptacyjne",command=self.adaptiveThreshold)
        lab5.add_command(label="Progowanie Interaktywne",command=self.interactiveTreshold)

       
        rootMenu.add_cascade(label="Lab5", menu=lab5)
        window.config(menu=rootMenu)
    
    def lab6Menu(self, window, rootMenu):
        lab6 = tk.Menu()
        lab6.add_command(label="Operacje morfologiczne",command=self.morphOperations)
        lab6.add_separator()
        lab6.add_command(label="Momenty", command=self.imageMoments)
        lab6.add_command(label="Pole i obwod", command=self.fieldAndPerimeter)
        lab6.add_command(label="Współczynnik kszałtu", command=self.aspectRatio)

       
        rootMenu.add_cascade(label="Lab6", menu=lab6)
        window.config(menu=rootMenu)

    def finalMiniProject(self, window, rootMenu):
        finalMiniProjectMenu = tk.Menu()
        finalMiniProjectMenu.add_command(label="Reprezentacja obrazu monochromatycznego w postaci 8 bitów", command=self.finalMiniProjectCalc)

        rootMenu.add_cascade(label="Zadanie projektowe", menu=finalMiniProjectMenu)
        window.config(menu=rootMenu)

    ########### Menu Lab

    def loadImage(self):
        img_path = tkFileDialog.askopenfilename()

        self.path = img_path

        if len(img_path) > 0:
            image = cv2.imread(img_path)

            self.listOfDuplicates.append(image)
            self.indexOfList += 1
           
            cv2.imshow(str("Obraz pierwotny -" + str(self.indexOfList) + " " + os.path.basename(img_path)), image)
           
            val = "Obraz pierwotny -" + "(" + str(self.indexOfList) + ")" + " " + os.path.basename(img_path)
            self.listOfButtons.append(tk.Button(mainWindow, text=val, command= lambda v=val: self.buttonPressed(v)))
            self.dictOfEveryImage["Obraz pierwotny -" + "(" + str(self.indexOfList)+ ")" + " " + os.path.basename(img_path)] = image

            self.printButtons()

           

    def duplicateImage(self):

        imgToDuplicate = self.isActiveValue
        print(self.isActiveKey)
        cv2.imshow(str(self.indexOfList) + " " + self.isActiveKey, imgToDuplicate)
        self.indexOfList += 1

        self.listOfDuplicates.append(imgToDuplicate)
        self.dictOfEveryImage[os.path.basename("Kopia " + str(self.indexOfList-1) + " " + self.isActiveKey)] = imgToDuplicate

        self.listOfButtons.append(tk.Button(mainWindow, text="Kopia " + "(" + str(self.indexOfList-1)+ ")" + " " + self.isActiveKey, command= lambda v="Kopia " + str(self.indexOfList-1) + " " + self.isActiveKey: self.buttonPressed(v)))

        self.printButtons()

    def isGray(self, image):
            if len(image.shape) < 3:
                return True
            if image.shape[2]  == 1:
                return True
            b,g,r = image[:,:,0], image[:,:,1], image[:,:,2]
            if (b==g).all() and (b==r).all():
                return True
            return False

    def toGrayscale(self):
        imgToGrayscale = self.isActiveValue

       
        rows, cols, _ = imgToGrayscale.shape

        if self.isGray(imgToGrayscale):
            print("to już jest")
        else:

            for i in range(rows):
                for j in range(cols):
                    pixel_b, pixel_g, pixel_r = imgToGrayscale[i][j]
                    grayScale = (0.299*pixel_b + 0.587*pixel_g + 0.114*pixel_r)
                    imgToGrayscale[i,j] = (int(grayScale), int(grayScale), int(grayScale))

            cv2.imshow("Grayscale " + str(self.indexOfList) + " " + self.isActiveKey, imgToGrayscale)

            self.isActiveValue = imgToGrayscale



       
    def printHistogram(self):

        if self.isGray(self.isActiveValue):
            plt.figure()
           
            #helper = list(Image.fromarray(self.isActiveValue).getdata())
            #content = [helper[i][0] for i in range(len(helper))]
            #loaded_image_data = content
           
            imgTmp = self.isActiveValue

            imageTmp = imgTmp[:,:,1]          
            x,y = imageTmp.shape                
            imageTmp = imageTmp.reshape(x*y)
           
            valuesCount = [0 for i in range(256)]
           
            for i in imageTmp:
                valuesCount[i] += 1
           
            xAxis = ([i for i in range(256)])
            yAxis = valuesCount

            plt.bar(xAxis, yAxis) ## yAxis - współrzędne z lewej strony(nasze zliczane wartości), xAxis - to co na dole po prostu jest
            plt.title(self.isActiveKey)
            plt.show(block=False)


        else:

            plt.figure()
            for i in range(3):
                imgTmp = self.isActiveValue
                imageTmp = imgTmp[:,:,i]            # pobieramy i-ty kanał z kolorowego obrazka, potrzebne w przypadku tablic wielowimiarowych
                x,y = imageTmp.shape                # przekształcamy tablicę danych z 2 wymiarów do jednego wymiaru
                imageTmp = imageTmp.reshape(x*y)    # rysujemy histogram
               
                if i==0: plt.hist(imageTmp,256, color="blue")
                if i==1: plt.hist(imageTmp,256, color="red")
                if i==2: plt.hist(imageTmp,256, color="green")
           
            plt.title(self.isActiveKey)
            plt.show(block=False) # pokazujemy  histogram
       



    def printImages(self):
        indexTmp = self.indexOfList
        for t in self.dictOfEveryImage.values():
            cv2.imshow(str(indexTmp) + os.path.basename(self.path) + " ", t)
            indexTmp +=1

        #print(path) # E:/##PULPIT/Kurs_Python/Python_APO/Python/Pr/example_images/lena_binary.bmp
   
    def saveImg(self):
        img_type = tk.StringVar()

        file_path = tkFileDialog.asksaveasfilename(filetypes=(('BMP', '.bmp'), ('PNG', '.png'), ('JPEG', '.jpg')), typevariable=img_type)

        cv2.imwrite(file_path, self.isActiveValue)

    ## ------- Obsługa buttonow


    def addButton(self, window):
 
        def resizeWindow(value):
            resizableResult = tk.Toplevel()
            scrollbarY = tk.Scrollbar(resizableResult, orient=tk.VERTICAL)
            scrollbarX = tk.Scrollbar(resizableResult, orient=tk.HORIZONTAL)
           

            img = self.isActiveValue
            p = value
            w = int(img.shape[1] * p)
            h = int(img.shape[0] * p)
           
            new_img = cv2.resize(img, (w, h))

            b,g,r = cv2.split(new_img)
            mg = cv2.merge((r,g,b))
            image2 = Image.fromarray(mg)
            img1 = ImageTk.PhotoImage(image=image2)
           
            if value == 3:
           
                singupcanv = tk.Canvas(resizableResult, height=1000, width=1900)
                singupcanv.create_image(0, 0, anchor='nw', image=img1)

                singupcanv.config(scrollregion=singupcanv.bbox(tk.ALL), yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
                singupcanv.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

                scrollbarX.grid( row=1, column=0, sticky=tk.E+tk.W)    
                scrollbarY.grid( row=0, column=1, sticky=tk.N+tk.S)    

                scrollbarX.config(command=singupcanv.xview)
                scrollbarY.config(command=singupcanv.yview)
            else:
                singupcanv = tk.Canvas(resizableResult, height=800, width=800)
                singupcanv.create_image(0, 0, anchor='nw', image=img1)

                singupcanv.config(scrollregion=singupcanv.bbox(tk.ALL), yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
                singupcanv.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

                scrollbarX.grid( row=1, column=0, sticky=tk.E+tk.W)    
                scrollbarY.grid( row=0, column=1, sticky=tk.N+tk.S)    

                scrollbarX.config(command=singupcanv.xview)
                scrollbarY.config(command=singupcanv.yview)

           
            resizableResult.mainloop()


        resizeButtons = {"DOP": 3,"200%":2.0, "150%":1.5,"100%":1.0 ,"50%":0.5, "25%":0.25, "20%":0.20, "10%":0.10}
        index = 0
        for key,value in resizeButtons.items():
            resizeButton = tk.Button(window, text=key, command = lambda v=value: resizeWindow(v)).grid(row=0, column=index+1, padx=15)
            index +=1

        #button = tk.Button(window, text="Wypisz aktywne obrazy",command=self.printButtons)
        #button.grid(row=1,columnspan= 8)

    def printButtons(self):

        for i in range(len(self.listOfButtons)):
            self.listOfButtons[i].grid(row=i+3, columnspan=8)

    def buttonPressed(self,value):
        for key in self.dictOfEveryImage:

            if key == value:
                self.isActiveValue = self.dictOfEveryImage[key]
                self.isActiveKey = key
                print(self.isActiveKey)

    ## ------- Obsługa buttonow


    def strechHistogram(self):

        minV = 0
        maxV = 255
        imgTmp = self.isActiveValue

        #for i in range(3):
        imageTmp = imgTmp[:,:,1]                # pobieramy i-ty kanał z kolorowego obrazka, potrzebne w przypadku tablic wielowimiarowych

        x,y = imageTmp.shape                    # przekształcamy tablicę danych z 2 wymiarów do jednego wymiaru (737, 550) - tzn. pierwszy wymiar ma 737 elementów a wdrugi 550
        imageTmp = imageTmp.reshape(x*y)  

        valuesCount = [0 for i in range(256)]       ## Licznik wartości na "podstawowy" histogramu, wypełniamy sobie tablice zerami

        for i in imageTmp:
            valuesCount[i] += 1


        rows, cols, _ = imgTmp.shape
        for index, number in enumerate(valuesCount): ## Wyszkiwanie pierwszego niezerowego elementu od początku (lewa strona histogramu)
            if number:
                firstNonzeroIndex = index
                break
        for index, number in enumerate(valuesCount[::-1]):  ## Wyszkiwanie pierwszego niezerowego elementu od końca (prawa strona histogramu)
            if number:
                firstNonzeroIndexReverse = 255 - index
                break
               

        for i in range(rows):
            for j in range(cols):
                pixel_b, pixel_g, pixel_r = imgTmp[i][j]
                if pixel_b < minV and pixel_g < minV and pixel_r < minV:
                    imgTmp[i,j] = minV,minV,minV
                if pixel_b > maxV and pixel_g > maxV and pixel_r > maxV:
                    imgTmp[i,j] = maxV,maxV,maxV
                else:
                    newValue = ((pixel_b - firstNonzeroIndex ) * maxV) / (firstNonzeroIndexReverse-firstNonzeroIndex)  ## Rozciągniecie zgodnie ze wzorem
                    imgTmp[i,j] = newValue,newValue,newValue



        cv2.imshow("Histogram Strech - " + self.isActiveKey, imgTmp)

    def strechHistogramWithParameters(self):
        strechHistogramWithPara = tk.Toplevel()

        label1 = tk.Label(strechHistogramWithPara,text="(A)Zakres histogramu - od: ")
        label1.grid(row=0, column=0)
        label2 = tk.Label(strechHistogramWithPara,text="(B)Zakres histogramu - od: ")
        label2.grid(row=1, column=0)

        separator = ttk.Separator(strechHistogramWithPara, orient="horizontal")
        separator.grid(row=2, columnspan=3, sticky='we')

        label3 = tk.Label(strechHistogramWithPara,text="Od min: ")
        label3.grid(row=3, column=0)
        label4 = tk.Label(strechHistogramWithPara,text="Do max: ")
        label4.grid(row=4, column=0)

        entry = tk.Entry(strechHistogramWithPara)
        entry.grid(row=0, column=1)
        entry.insert(0, "1")
        entry1 = tk.Entry(strechHistogramWithPara)
        entry1.grid(row=1, column=1)
        entry1.insert(0, "1")

        entry2 = tk.Entry(strechHistogramWithPara)
        entry2.grid(row=3, column=1)
        entry2.insert(0, "1")
        entry3 = tk.Entry(strechHistogramWithPara)
        entry3.grid(row=4, column=1)
        entry3.insert(0, "1")

        button = tk.Button(strechHistogramWithPara, text="Wykonaj", command=lambda: self.strechHistogramWithParametersCalc(entry.get(), entry1.get(), entry2.get() , entry3.get()))
        #button = tk.Button(strechHistogramWithPara, text="Wykonaj", command=lambda: self.strechHistogramWithParametersCalc( entry2.get() , entry3.get()))
        button.grid(columnspan=2)
       

    def strechHistogramWithParametersCalc(self, minV, maxV, valA, valB):
    #def strechHistogramWithParametersCalc(self, valA, valB):


        minV = int(minV)  ## wartości z których mają być brane min/max do rozciągnięcia czyli 0-255 cały zakres, a np. 100-255 to prawa strona histogramu. Po prostu zakres z jakiego będziemy korzystać
        maxV = int(maxV)
        valA = int(valA)  ## A i B, z których wartości ma być rozciągnięty histogram - czyli bierzemy "część" histogramu i rozciągamy go względem powyższego zakresu
        valB = int(valB)  ## czyli wpisujemy A i B 20 -  50, to w tych wartościach będzie rozciągnięty histogram dla ustalonego powyżej zakresu

        ## albo min max - 5 -254 (Czyli praktycznie cały zakres szarości na obrazu), w A i B 50 - 120 (będzie do 120, ale od 20), najlepiej widać na małych wartościach

        imgTmp = self.isActiveValue
        rows, cols, _ = imgTmp.shape
       
                 
        for i in range(rows):
            for j in range(cols):
                pixel_b, pixel_g, pixel_r = imgTmp[i][j]

                if pixel_b <= minV and pixel_g <= minV and pixel_r <= minV:
                    imgTmp[i,j] = valA, valA, valA
                elif pixel_b >= maxV and pixel_g >= maxV and pixel_r >= maxV:
                    imgTmp[i,j] = valB, valB, valB
                else:
                    calc = (pixel_b - minV) * valB / (maxV - minV)
                    imgTmp[i,j] = calc, calc, calc



        cv2.imshow("Histogram Strech with parameters- "+ str(self.indexOfList) + self.isActiveKey, imgTmp)


    ###

    # Equalizacja

    ###

    def imageEqualization(self):

        if self.isGray(self.isActiveValue):

            imgTmp = self.isActiveValue

            def calcCdf(imageList):                   # Dystrybuanta                  
                cdf = {}
                imageListSorted = sorted(imageList)  ## Sortujemy liste, rosnąco
 
                for number in imageList:
                    if number in cdf.keys():         ## Jeżeli jest to kontynuuj,żeby nie dublować kluczy
                        continue
                    else:
                        cdf[number] = countSmallerNums(number, imageListSorted) # dany klucz z wartościa "wystąpień" jest liczony poniżej
                return cdf
               
            def countSmallerNums(numberT, listToCount ): # 50 / 32151
                count = 0
                for i in listToCount:
                    if i <= numberT:                 ## Jeżeli dany numer z klucza cdf jest mniejszy, no to dodajemy, w innym przypadku zwracamy 0
                        count +=1                    ## Tworzymy dzięki temu wartość, liczba:ilość_wystąpień - potrzebne do "rozszerzenia"
                    else:
                        return count
                return count

            imageTmpList = imgTmp[:,:,1]              
            x,y = imageTmpList.shape                    
            imageTmpList = imageTmpList.reshape(x*y) ## Zmieniamy na jedna liste

            #listValues = []
            #for val in imageTmpList:           ## Lista wszystkich wartości na obrazie
            #    listValues.append(val)

            cdfCalc = calcCdf(imageTmpList)      ## Na podstawie tej listy, liczymy sobie dystrybuante

            height = imgTmp.shape[0]          ## Wysokość
            width = imgTmp.shape[1]           ## Szczerokość

            ##cdfMinValue = min(list(filter(lambda x: x != 0, cdfCalc.values())))

            cdfMinValue = min(cdfCalc.values())

            def calcOfEqV(value):
                return round(((cdfCalc[value] - cdfMinValue) / ((height * width) - cdfMinValue)) * 255)  ## Wzór na equalizacje

            def makeImageEq(original):
                rows, cols, _ = original.shape
                for i in range(rows):
                    for j in range(cols):
                        pixel_b, pixel_g, pixel_r = original[i][j]

                        original[i,j] = calcOfEqV(pixel_b),calcOfEqV(pixel_g),calcOfEqV(pixel_r) ## Zamieniamy odpowiednie pixele

                return original

            equalizedImg = makeImageEq(imgTmp) ## Wykonujemy wyrównanie, na podstawie aktywnego obrazu

            cv2.imshow("Equalizazcja " + self.isActiveKey, equalizedImg)

        else:

            print("Załaduj obraz czarno-biały!")
   
    ###

    ## Gamma

    ###
    def gammaCorrection(self):
        addGammaCorrectionWindow = tk.Toplevel()

        label1 = tk.Label(addGammaCorrectionWindow,text="Podaj wartość gamma: ")
        label1.grid(row=0, column=0)

        entry = tk.Entry(addGammaCorrectionWindow)
        entry.grid(row=0, column=1)
        entry.insert(0, "1")

        button = tk.Button(addGammaCorrectionWindow, text="Wykonaj", command=lambda: self.setImageGammaCorrection(entry.get()))
        button.grid()



    def setImageGammaCorrection(self, value):
        imgTmp = self.isActiveValue

        invGamma = float(value)

        def calcGamma(val):
            val = (255 * ( val / 255) ** (1 / invGamma))
           
            return val

        def makeImageEq(originalImage):
            rows, cols, _ = originalImage.shape
            for i in range(rows):
                for j in range(cols):
                   
                    pixel_b, pixel_g, pixel_r = originalImage[i][j]

                    originalImage[i,j] = calcGamma(pixel_b), calcGamma(pixel_g), calcGamma(pixel_r)   ## Zamieniamy odpowiednie pixele

            return originalImage

        cv2.imshow("Gamma corr. " + self.isActiveKey, makeImageEq(imgTmp))



    ###

    # Negacja

    ###

    def imageNegation(self):

        negative = abs(255-self.isActiveValue) # wartość bezwzględna z odejmowania
        self.dictOfEveryImage[self.isActiveKey] = negative

        cv2.imshow("N" + str(self.indexOfList) + self.isActiveKey ,negative)

    ####

    # Progowanie binarne z progiem wpisanym jako parametr
   
    ####

    def imageThreshold(self ):
        addThresholdWindow = tk.Toplevel()

        label1 = tk.Label(addThresholdWindow,text="Podaj wartość progowania od 0-255")
        label1.grid(row=0, column=0)

        entry = tk.Entry(addThresholdWindow)
        entry.grid(row=0, column=1)
        entry.insert(0, "1")

        button = tk.Button(addThresholdWindow, text="Wykonaj", command=lambda: imageTresholdCalc(entry.get()))
        button.grid()


        def imageTresholdCalc( value):

            try:
                int(value)
            except ValueError:
                print("Wpisana wartosc musi byc liczba")
                return
            if not (0 < int(value) < 255):
                print("Wartosc poza zakresem 0-255")
                return

            value = int(value)
            img = self.isActiveValue
            rows, cols, _ = img.shape

            for i in range(rows):
                for j in range(cols):

                    pixel_b, pixel_g, pixel_r = img[i][j]
                
                    if pixel_b > value and pixel_g > value and pixel_r > value:
                        img[i,j] = 255,255,255
                    else:
                        img[i,j] = 0,0,0

            cv2.imshow("Grayscale " + str(self.indexOfList) + " " + self.isActiveKey, img)
            #self.isActiveKey = "Grayscale " + str(self.indexOfList) + " " + self.isActiveKey



    ####

    #progowanie z zachowaniem poziomów szarości zprogiem wskazywanym suwakiem,

    ####

    def imageThresholdWithGrayscale(self):
        addSecondThresholdWindow = tk.Toplevel()

        label1 = tk.Label(addSecondThresholdWindow,text="Próg:").grid(row=0, column=0, padx=15)

        value = tk.IntVar()

        scale = tk.Scale(addSecondThresholdWindow, from_=0, to=255, orient=tk.HORIZONTAL, variable=value) ## albo vertical
        scale.grid(row=1, column=0, padx=5)
       


        button = tk.Button(addSecondThresholdWindow, text="Wykonaj", command=lambda: imageTresholdWithGrayscale(scale.get()))
        button.grid(columnspan=4, pady=10)

        def imageTresholdWithGrayscale( value):
            try:
                int(value)
            except ValueError:
                print("Wpisana wartosc musi by numerem.")
                return
            if not (0 < int(value) < 255):
                print("Wartosc poza zakresem 0-255")
                return
            value = int(value)

            imgTmp = self.isActiveValue
            rows, cols, _ = imgTmp.shape

            for i in range(rows):
                for j in range(cols):
                    pixel_b, pixel_g, pixel_r = imgTmp[i][j]
                
                    if pixel_b > value and pixel_g > value and pixel_r > value:
                        imgTmp[i,j] = pixel_b,pixel_g,pixel_r
                    elif pixel_b <= value and pixel_g <= value and pixel_r <= value:
                        imgTmp[i,j] = 0,0,0

                    
            cv2.imshow("Grayscale with limit" + str(self.indexOfList) + " " + self.isActiveKey, imgTmp)

    ####scale

    #progowanie z dwoma progami wskazanymi przez wskazywanym suwakiem i wpisanym jako parametr.

    ####

    def imageThresholdWithGrayscaleTwoLimits(self):
        addSecondThresholdWindowTwoLimits = tk.Toplevel()

        label1 = tk.Label(addSecondThresholdWindowTwoLimits,text="Próg dolny").grid(row=0, column=0, padx=15)
        label2 = tk.Label(addSecondThresholdWindowTwoLimits,text="Próg górny").grid(row=0, column=2, padx=15)
       


        entry1 = tk.Entry(addSecondThresholdWindowTwoLimits)
        entry1.grid(row=0, column=1)
        entry1.insert(0, "1")

        entry2 = tk.Entry(addSecondThresholdWindowTwoLimits)
        entry2.grid(row=0, column=3)
        entry2.insert(0, "1")

        button = tk.Button(addSecondThresholdWindowTwoLimits, text="Wykonaj", command=lambda: imageTresholdCalcLimits(entry1.get(), entry2.get()))
        button.grid(columnspan=4, pady=10)

        def imageTresholdCalcLimits( value_floor, value2_celling):
            try:
                int(value_floor)
                int(value2_celling)
            except ValueError:
                print("Wpisana wartosc musi by numerem.")
                return
            if not (0 < int(value_floor) < 255) or not (0 < int(value2_celling) < 255):
                print("Wartosc poza zakresem 0-255")
                return
            value_floor = int(value_floor)
            value2_celling = int(value2_celling)

            imgTmp = self.isActiveValue
            rows, cols, _ = imgTmp.shape

            for i in range(rows):
                for j in range(cols):

                    pixel_b, pixel_g, pixel_r = imgTmp[i][j]
                
                    if pixel_b > value2_celling and pixel_g > value2_celling and pixel_r > value2_celling:
                        imgTmp[i,j] = 0,0,0
                    
                    elif pixel_b <= value_floor and pixel_g <= value_floor and pixel_r <= value_floor:
                        imgTmp[i,j] = 0,0,0

                    else:
                        imgTmp[i,j] = 255,255,255

                    
            cv2.imshow("Grayscale with limit" + str(self.indexOfList) + " " + self.isActiveKey, imgTmp)

    ####

    #  Dodawanie obrazów z i bez wys

    ####

    def addImages(self):
        mathAddWindow = tk.Toplevel()
        mathAddWindow.title("Operacja ADD - wybierz obrazy")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathAddWindow, text="Obraz 1", padx=10)
        label2 = tk.Label(mathAddWindow, text="Obraz 2", padx=10)

        combobox1 = ttk.Combobox(mathAddWindow, state='readonly', width=45)
        combobox1["values"] = items
        combobox2 = ttk.Combobox(mathAddWindow, state='readonly', width=45)
        combobox2["values"] = items

        button = tk.Button(mathAddWindow, text="Wykonaj", command = lambda: imageAddProcessingCalc(combobox1.get(), combobox2.get()))

        label1.grid(column=0, row = 0  )
        label2.grid(column=1, row = 0 )

        combobox1.grid(column=0, row = 1, padx=10 )
        combobox2.grid(column=1, row = 1, padx=10 )

        button.grid(columnspan=2, row=2, pady=15)

        def imageAddProcessingCalc(img1, img2):
           
            if img1 and img2:

                test = self.dictOfEveryImage[img1]
                test2 = self.dictOfEveryImage[img2]

                color = (0,0,0)
                w = test.shape[1] #sz
                h = test.shape[0] #w

                pixel_array = np.full((h, w, 3), color, dtype=np.uint8)

                rows, cols, _ = test.shape
                for i in range(rows):
                    for j in range(cols):
                        pixel_b, pixel_g, pixel_r = test[i][j]
                        pixel_b1, pixel_g2, pixel_r3 = test2[i][j]
                        testa = int(pixel_b) + int(pixel_b1)

                        if testa >= 255:
                            pixel_array[i][j] = 255,255,255
                        else:                      
                            pixel_array[i][j] = testa,testa,testa

                cv2.imshow("Add operation " + img1 + " " + img1 ,pixel_array)
   
    ####

    #  Dod. Dziel. Mnoż. przez l. całk z i bez wys

    ####
   
   
    def addConstantImage(self):
        mathMultiWindow = tk.Toplevel()
        mathMultiWindow.title("Operacja dodawania ")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathMultiWindow, text="Obraz 1: ", padx=10)
        label2 = tk.Label(mathMultiWindow, text="Wartość: ", padx=10)
       
        label1.grid(column=0, row = 0 )
        label2.grid(column=0, row = 1 )

        combobox1 = ttk.Combobox(mathMultiWindow, state='readonly', width=45)
        combobox1["values"] = items
       
       
        entry = tk.Entry(mathMultiWindow)
        entry.grid(row=1, column=1, padx=5,pady=5)
        entry.insert(0,"0")
       

        button = tk.Button(mathMultiWindow, text="Wykonaj", command = lambda: imageAddProcessingCalc(combobox1.get(), entry.get()))
       
        combobox1.grid(column=1, row = 0, padx=10 )
       

        button.grid(columnspan=2, row=2, pady=15)

        def imageAddProcessingCalc(img1, value):
            if img1 and value:

                test = self.dictOfEveryImage[img1]

                rows, cols, _ = test.shape
               
                for i in range(rows):
                    for j in range(cols):

                        pixel_b, pixel_g, pixel_r = test[i][j]
                        testa = int(pixel_b) + int(value)
                       
                        if testa > 255:
                            test[i][j] = 255,255,255
                        else:
                            test[i][j] = testa, testa, testa


                cv2.imshow("Add operation " + img1, test)
   

    ####

    #  Dod. Dziel. Mnoż. przez l. całk z i bez wys

    ####

    def multiplicationImages(self):
        mathMultiWindow = tk.Toplevel()
        mathMultiWindow.title("Operacja multiplication - wybierz obrazy")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathMultiWindow, text="Obraz 1: ", padx=10)
        label2 = tk.Label(mathMultiWindow, text="Wartość: ", padx=10)
       
        label1.grid(column=0, row = 0 )
        label2.grid(column=0, row = 1 )

        combobox1 = ttk.Combobox(mathMultiWindow, state='readonly', width=45)
        combobox1["values"] = items
       
       
        entry = tk.Entry(mathMultiWindow)
        entry.grid(row=1, column=1, padx=5,pady=5)
        entry.insert(0,"0")
       

        button = tk.Button(mathMultiWindow, text="Wykonaj", command = lambda: imageMultiProcessingCalc(combobox1.get(), entry.get()))
       
        combobox1.grid(column=1, row = 0, padx=10 )
       

        button.grid(columnspan=2, row=2, pady=15)

        def imageMultiProcessingCalc(img1, value):
            if img1 and value:

                test = self.dictOfEveryImage[img1]

                rows, cols, _ = test.shape
               
                for i in range(rows):
                    for j in range(cols):

                        pixel_b, pixel_g, pixel_r = test[i][j]
                        testa = int(pixel_b) * int(value)
                       
                        if testa > 255:
                            test[i][j] = 255,255,255
                        else:
                            test[i][j] = testa, testa, testa


                cv2.imshow("Multiply operation " + img1, test)

    def divideImages(self):
        mathDivideWin = tk.Toplevel()
        mathDivideWin.title("Operacja divide - wybierz obrazy")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathDivideWin, text="Obraz 1: ", padx=10)
        label2 = tk.Label(mathDivideWin, text="Wartość: ", padx=10)
       
        label1.grid(column=0, row = 0 )
        label2.grid(column=0, row = 1 )

        combobox1 = ttk.Combobox(mathDivideWin, state='readonly', width=45)
        combobox1["values"] = items
       
       
        entry = tk.Entry(mathDivideWin)
        entry.grid(row=1, column=1, padx=5,pady=5)
        entry.insert(0,"0")
       

        button = tk.Button(mathDivideWin, text="Wykonaj", command = lambda: imageMultiProcessingCalc(combobox1.get(), entry.get()))



        combobox1.grid(column=1, row = 0, padx=10 )
       

        button.grid(columnspan=2, row=2, pady=15)

        def imageMultiProcessingCalc(img1, value):
            if img1:

                test = self.dictOfEveryImage[img1]

                rows, cols, _ = test.shape
               
                for i in range(rows):
                    for j in range(cols):

                        pixel_b, pixel_g, pixel_r = test[i][j]
                        testa = int(pixel_b) / int(value)
                       
                       
                        if testa > 255:
                            test[i][j] = 255,255,255
                        else:
                            test[i][j] = int(testa), int(testa), int(testa)


                cv2.imshow("Divide operation " + img1 + " " + img1 ,test)
   
    ####

    #  Różnica bezwzg. obrazów

    ####

    def subtractionImages(self):
        mathAddWindow = tk.Toplevel()
        mathAddWindow.title("Operacja substraction - wybierz obrazy")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathAddWindow, text="Obraz 1", padx=10)
        label2 = tk.Label(mathAddWindow, text="Obraz 2", padx=10)

        combobox1 = ttk.Combobox(mathAddWindow, state='readonly', width=45)
        combobox1["values"] = items
        combobox2 = ttk.Combobox(mathAddWindow, state='readonly', width=45)
        combobox2["values"] = items

        button = tk.Button(mathAddWindow, text="Wykonaj", command = lambda: imageSubsProcessingCalc(combobox1.get(), combobox2.get()))

        label1.grid(column=0, row = 0  )
        label2.grid(column=1, row = 0 )

        combobox1.grid(column=0, row = 1, padx=10 )
        combobox2.grid(column=1, row = 1, padx=10 )

        button.grid(columnspan=2, row=2, pady=15)

        def imageSubsProcessingCalc(img1, img2):
            if img1 and img2:

                test = self.dictOfEveryImage[img1]
                test2 = self.dictOfEveryImage[img2]

                color = (0,0,0)
                w = test.shape[1] #sz
                h = test.shape[0] #w

                pixel_array = np.full((h, w, 3), color, dtype=np.uint8)

                rows, cols, _ = test.shape
                for i in range(rows):
                    for j in range(cols):

                        pixel_b, pixel_g, pixel_r = test[i][j]
                        pixel_b1, pixel_g2, pixel_r3 = test2[i][j]
                        testa = int(pixel_b) - int(pixel_b1)

                        if testa < 0:
                            pixel_array[i][j] = 0,0,0
                        else:
                            pixel_array[i][j] = testa,testa,testa
                cv2.imshow("Substraction operation " + img1 + " " + img1 ,pixel_array)

    ####

    #  NOT

    ####

    def imageNotProcessing(self):
        negative = abs(255-self.isActiveValue) # wartość bezwzględna z odejmowania

        self.dictOfEveryImage[self.isActiveKey] = negative
        #self.isActiveKey = "N" + str(self.indexOfList) + self.isActiveKey

        cv2.imshow("Not operation" + str(self.indexOfList) + self.isActiveKey ,negative)



    ####

    #  And

    ####

    def imageAndProcessing(self):
        mathAndWindow = tk.Toplevel()
        mathAndWindow.title("Operacja AND - wybierz obrazy")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathAndWindow, text="Obraz 1", padx=10)
        label2 = tk.Label(mathAndWindow, text="Obraz 2", padx=10)

        combobox1 = ttk.Combobox(mathAndWindow, state='readonly', width=45)
        combobox1["values"] = items
        combobox2 = ttk.Combobox(mathAndWindow, state='readonly', width=45)
        combobox2["values"] = items

        button = tk.Button(mathAndWindow, text="Wykonaj", command = lambda: imageAndProcessingCalc(combobox1.get(), combobox2.get()))

        label1.grid(column=0, row = 0  )
        label2.grid(column=1, row = 0 )

        combobox1.grid(column=0, row = 1, padx=10 )
        combobox2.grid(column=1, row = 1, padx=10 )


        button.grid(columnspan=2, row=2, pady=15)

        def imageAndProcessingCalc(img1, img2):
            if img1 and img2:

                test = self.dictOfEveryImage[img1]
                test2 = self.dictOfEveryImage[img2]


                w = test.shape[1] #sz
                h = test.shape[0] #w
                color = (0,0,0)
                pixel_array = np.full((h, w,3), color, dtype=np.uint8)

                new_img = cv2.resize(test2, (w, h))
                rows, cols, _ = test.shape

                for i in range(rows):
                    for j in range(cols):
       
                        pixel_b, pixel_g, pixel_r = test[i][j]
                        pixel_b1, pixel_g2, pixel_r3 = new_img[i][j]

                        binFor = f'{pixel_b:08b}'
                        binFor1 = f'{pixel_b1:08b}'

                        clearString = ''

                        for a in range(8):
                            if binFor[a] == "1" and binFor1[a] == "1":
                                clearString += str(1)
                            else:
                                clearString += str(0)
                        clearString = int(clearString,2)
                        pixel_array[i][j] =  clearString , clearString, clearString

                cv2.imshow("And Operation " ,pixel_array)
           
               
       
    ####

    #  Or

    ####

    def imageOrProcessing(self):
        mathOrWindow = tk.Toplevel()
        mathOrWindow.title("Operacja OR - wybierz obrazy")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathOrWindow, text="Obraz 1", padx=10)
        label2 = tk.Label(mathOrWindow, text="Obraz 2", padx=10)

        combobox1 = ttk.Combobox(mathOrWindow, state='readonly', width=45)
        combobox1["values"] = items
        combobox2 = ttk.Combobox(mathOrWindow, state='readonly', width=45)
        combobox2["values"] = items

        button = tk.Button(mathOrWindow, text="Wykonaj", command = lambda: imageOrProcessingCalc(combobox1.get(), combobox2.get()))

        label1.grid(column=0, row = 0  )
        label2.grid(column=1, row = 0 )

        combobox1.grid(column=0, row = 1, padx=10 )
        combobox2.grid(column=1, row = 1, padx=10 )

        button.grid(columnspan=2, row=2, pady=15)

        def imageOrProcessingCalc(img1, img2):
            if img1 and img2:

                test = self.dictOfEveryImage[img1]
                test2 = self.dictOfEveryImage[img2]


                w = test.shape[1] #sz
                h = test.shape[0] #w
                color = (0,0,0)
                pixel_array = np.full((h, w,3), color, dtype=np.uint8)

                new_img = cv2.resize(test2, (w, h))
                rows, cols, _ = test.shape

                for i in range(rows):
                    for j in range(cols):
       
                        pixel_b, pixel_g, pixel_r = test[i][j]
                        pixel_b1, pixel_g2, pixel_r3 = new_img[i][j]

                        binFor = f'{pixel_b:08b}'
                        binFor1 = f'{pixel_b1:08b}'

                        clearString = ''

                        for a in range(8):
                            if binFor[a] == "1" or binFor1[a] == "1":
                                clearString += str(1)
                            else:
                                clearString += str(0)
                        clearString = int(clearString,2)
                        pixel_array[i][j] =  clearString , clearString, clearString

                cv2.imshow("Or Operation " ,pixel_array)
   
    ####

    #  Xor

    ####

    def imageXorProcessing(self):
        mathXorWindow = tk.Toplevel()
        mathXorWindow.title("Operacja XOR - wybierz obrazy")
        items = [x for x in self.dictOfEveryImage.keys()]

        label1 = tk.Label(mathXorWindow, text="Obraz 1", padx=10)
        label2 = tk.Label(mathXorWindow, text="Obraz 2", padx=10)

        combobox1 = ttk.Combobox(mathXorWindow, state='readonly', width=45)
        combobox1["values"] = items
        combobox2 = ttk.Combobox(mathXorWindow, state='readonly', width=45)
        combobox2["values"] = items

        button = tk.Button(mathXorWindow, text="Wykonaj", command = lambda: imageXorProcecssingCalc(combobox1.get(), combobox2.get()))

        label1.grid(column=0, row = 0  )
        label2.grid(column=1, row = 0 )

        combobox1.grid(column=0, row = 1, padx=10 )
        combobox2.grid(column=1, row = 1, padx=10 )

        button.grid(columnspan=2, row=2, pady=15)

        def imageXorProcecssingCalc(img1, img2):
            if img1 and img2:

                test = self.dictOfEveryImage[img1]
                test2 = self.dictOfEveryImage[img2]


                w = test.shape[1] #sz
                h = test.shape[0] #w
                color = (0,0,0)
                pixel_array = np.full((h, w,3), color, dtype=np.uint8)

                new_img = cv2.resize(test2, (w, h))
                rows, cols, _ = test.shape

                for i in range(rows):
                    for j in range(cols):
       
                        pixel_b, pixel_g, pixel_r = test[i][j]
                        pixel_b1, pixel_g2, pixel_r3 = new_img[i][j]

                        binFor = f'{pixel_b:08b}'
                        binFor1 = f'{pixel_b1:08b}'

                        clearString = ''

                        for a in range(8):
                            if binFor[a] == "0" and binFor1[a] == "1" or binFor[a] == "1" and binFor1[a] == "0":
                                clearString += str(1)
                            else:
                                clearString += str(0)
                        clearString = int(clearString,2)
                        pixel_array[i][j] =  clearString , clearString, clearString

                cv2.imshow("Xor Operation " ,pixel_array)
    ####

    #  Wygładzanie liniowe

    ####

    def imageSmoothLinear(self):

        smoothLinearWindow = tk.Toplevel()
        smoothLinearWindow.title("Operacja Wygładzania")

        mask = {"Uśrednienie - [1, 1, 1], [1, 1, 1], [1, 1, 1]": 1,
                "Uśrednienie z wagami - [1, 1, 1], [1, k, 1], [1, 1, 1]": 2,
                "Filtr gaussowski - [1, 2, 1], [2, 4, 2], [1, 2, 1]": 3}

        itemsMask = [x for x in mask.keys()]
       

        marg = {
                    "BORDER_CONSTANT": cv2.BORDER_CONSTANT,
                    "BORDER_WRAP": cv2.BORDER_WRAP,
                    "BORDER_REFLECT": cv2.BORDER_REFLECT}
        itemsMarg = [x for x in marg.keys()]
       

        label1 = tk.Label(smoothLinearWindow, text="Wybór maski", padx=15)
        label2 = tk.Label(smoothLinearWindow, text="Stała maski: ", padx=15)

        entry = tk.Entry(smoothLinearWindow)
        entry.insert(0,"0")

        label3 = tk.Label(smoothLinearWindow, text="Ustawienia pikseli brzegowych", padx=15,  pady=10 )
        label4 = tk.Label(smoothLinearWindow, text="Stała pixeli brzegowych: ", padx=15,  pady=10 )


        entry1 = tk.Entry(smoothLinearWindow)
        entry1.insert(0,"0")


        combobox1 = ttk.Combobox(smoothLinearWindow, state='readonly', width=45)
        combobox1["values"] = itemsMask

        combobox2 = ttk.Combobox(smoothLinearWindow, state='readonly', width=45)
        combobox2["values"] = itemsMarg


        button = tk.Button(smoothLinearWindow, text="Wykonaj", command = lambda: imageSmoothProcessingCalc(combobox1.get(), combobox2.get(), entry.get(),entry1.get()))


        label1.grid(column=0, row = 0  )
        combobox1.grid(column=0, row = 1, padx=15 )
        label2.grid(column=0, row = 2)
        entry.grid(row=3, column=0, padx=5)


        label3.grid(column=0, row = 4  )
        combobox2.grid(column=0, row = 5, padx=15)

        label4.grid(column=0, row = 6  )
        entry1.grid( column=0,row=7, padx=5)
        
        button.grid(columnspan=3, row=8, pady=15)

        def imageSmoothProcessingCalc(value1, value2, value3, value4):

        # value1 - maska
        # value2 - ustawienie pixeli brzegowych
        # value3 - stała dla maski z wagami
        # value4 - stała dla pixeli

            maskTmp = mask[value1]

            imgTmp = self.isActiveValue
            
            if maskTmp == 1:
                maskTmp = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
            elif maskTmp == 2:
                maskTmp = np.array([[1, 1, 1], [1, int(value3), 1], [1, 1, 1]])
            elif maskTmp == 3:
                maskTmp = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])


            if value2 == "BORDER_CONSTANT":
    
                    kernel = np.array(maskTmp,np.float32) / np.sum(maskTmp)
                    imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_CONSTANT, value=(int(value4), int(value4), int(value4)))
                    imgSmooth = cv2.filter2D(imgTmpBorder, -1, kernel)

                    cv2.imshow("Wygladzanie " + self.isActiveKey, imgSmooth)

            elif value2 == "BORDER_WRAP":

                kernel = np.array(maskTmp,np.float32) / np.sum(maskTmp)

                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_WRAP)
                imgSmooth = cv2.filter2D(imgTmpBorder,-1, kernel)

                cv2.imshow("Wygladzanie " + self.isActiveKey, imgSmooth)

            elif value2 == "BORDER_REFLECT":

                kernel = np.array(maskTmp,np.float32) / np.sum(maskTmp)
                
                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_REFLECT)
                imgSmooth = cv2.filter2D(imgTmpBorder,-1, kernel)

                cv2.imshow("Wygladzanie " + self.isActiveKey, imgSmooth)

    ####

    #  Wyostrzanie liniowe

    ####

    def imageSharpeningLinear(self):

        sharpLinearWindow = tk.Toplevel()
        sharpLinearWindow.title("Operacja wyostrzania")

        mask = {"Maska 1 - [0, -1, 0], [-1, 5, -1], [0, -1, 0]": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
                "Maska 2 - [-1, -1, -1], [-1, 9, -1], [-1, -1, -1]": np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]),
                "Maska 3 - [1, -2, 1], [-2, 5, -2], [1, -2, 1]": np.array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]])}
        itemsMask = [x for x in mask.keys()]


        marg = {
                    "BORDER_CONSTANT": cv2.BORDER_CONSTANT,
                    "BORDER_WRAP": cv2.BORDER_WRAP,
                    "BORDER_REFLECT": cv2.BORDER_REFLECT}
        itemsMarg = [x for x in marg.keys()]
       

        label1 = tk.Label(sharpLinearWindow, text="Wybór maski", padx=15)

        label2 = tk.Label(sharpLinearWindow, text="Ustawienia pikseli brzegowych", padx=15,  pady=10 )
        label3 = tk.Label(sharpLinearWindow, text="Stała pixeli brzegowych: ", padx=15,  pady=10 )


        entry1 = tk.Entry(sharpLinearWindow)
        entry1.insert(0,"0")


        combobox1 = ttk.Combobox(sharpLinearWindow, state='readonly', width=45)
        combobox1["values"] = itemsMask

        combobox2 = ttk.Combobox(sharpLinearWindow, state='readonly', width=45)
        combobox2["values"] = itemsMarg


        button = tk.Button(sharpLinearWindow, text="Wykonaj", command = lambda: imageSharpeningProcessingCalc(combobox1.get(), combobox2.get(),entry1.get()))


        label1.grid(column=0, row = 0  )
        combobox1.grid(column=0, row = 1, padx=15 )


        label2.grid(column=0, row = 2  )
        combobox2.grid(column=0, row = 3, padx=15)

        label3.grid(column=0, row = 4  )
        entry1.grid( column=0,row=5, padx=5)
        
        button.grid(columnspan=3, row=6, pady=15)
       
        def imageSharpeningProcessingCalc(value1, value2, value3):

            maskTmp = mask[value1]
            imgTmp = self.isActiveValue
           

            if value2 == "BORDER_CONSTANT":
    
                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_CONSTANT, value=(int(value3), int(value3), int(value3)))
                imgSharp = cv2.filter2D(imgTmpBorder, -1, maskTmp)

                cv2.imshow("Wyostrzanie " + self.isActiveKey, imgSharp)

            elif value2 == "BORDER_WRAP":


                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_WRAP)
                imgSharp = cv2.filter2D(imgTmpBorder,-1, maskTmp)

                cv2.imshow("Wyostrzanie " + self.isActiveKey, imgSharp)

            elif value2 == "BORDER_REFLECT":

                
                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_REFLECT)
                imgSharp = cv2.filter2D(imgTmpBorder,-1, maskTmp)

                cv2.imshow("Wyostrzanie " + self.isActiveKey, imgSharp)



    ####

    #  Kierunkowa detekcja

    ####

    def imageEdgeDetection(self):
        edgeDetectionWindow = tk.Toplevel()
        edgeDetectionWindow.title("Operacja detekcji krawędzi")

        mask = {        
                       "Maska E - [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
                       "Maska SE - [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]": np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]),
                       "Maska S - [[-1, -2, -1],[0, 0, 0], [1, 2, 1]]": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
                       "Maska SW - [[0, -1, -2], [1, 0, -1], [2, 1, 0]]": np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]]),
                       "Maska W - [[1, 0, -1], [2, 0, -2], [1, 0, -1]]": np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]),

                       "Maska NW - [[2, 1, 0], [-1, 0, -1, [0, -1, -2]]": np.array([[2, 1, 0], [-1, 0, -1], [0, -1, -2]]),
                       "Maska N - [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]": np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]),
                       "Maska NE - [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]": np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])}


        itemsMask = [x for x in mask.keys()]


        marg = {
                    "BORDER_CONSTANT": cv2.BORDER_CONSTANT,
                    "BORDER_WRAP": cv2.BORDER_WRAP,
                    "BORDER_REFLECT": cv2.BORDER_REFLECT}
        itemsMarg = [x for x in marg.keys()]
       
        label1 = tk.Label(edgeDetectionWindow, text="Wybór maski", padx=15)

        label2 = tk.Label(edgeDetectionWindow, text="Ustawienia pikseli brzegowych", padx=15,  pady=10 )
        label3 = tk.Label(edgeDetectionWindow, text="Stała pixeli brzegowych: ", padx=15,  pady=10 )


        entry1 = tk.Entry(edgeDetectionWindow)
        entry1.insert(0,"0")


        combobox1 = ttk.Combobox(edgeDetectionWindow, state='readonly', width=45)
        combobox1["values"] = itemsMask

        combobox2 = ttk.Combobox(edgeDetectionWindow, state='readonly', width=45)
        combobox2["values"] = itemsMarg


        button = tk.Button(edgeDetectionWindow, text="Wykonaj", command = lambda: imageEdgeDetectionProcessingCalc(combobox1.get(), combobox2.get(),entry1.get()))


        label1.grid(column=0, row = 0  )
        combobox1.grid(column=0, row = 1, padx=15 )


        label2.grid(column=0, row = 2  )
        combobox2.grid(column=0, row = 3, padx=15)

        label3.grid(column=0, row = 4  )
        entry1.grid( column=0,row=5, padx=5)
        
        button.grid(columnspan=3, row=6, pady=15)

        def imageEdgeDetectionProcessingCalc(value1, value2, value3):

            maskTmp = mask[value1]
            imgTmp = self.isActiveValue
           

            if value2 == "BORDER_CONSTANT":
    
                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_CONSTANT, value = (int(value3), int(value3), int(value3)))
                imgSharp = cv2.filter2D(imgTmpBorder, -1, maskTmp)

                cv2.imshow("Detekcja krawedzi " + self.isActiveKey, imgSharp)

            elif value2 == "BORDER_WRAP":


                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_WRAP)
                imgSharp = cv2.filter2D(imgTmpBorder,-1, maskTmp)

                cv2.imshow("Detekcja krawedzi " + self.isActiveKey, imgSharp)

            elif value2 == "BORDER_REFLECT":

                
                imgTmpBorder = cv2.copyMakeBorder(imgTmp, top=1,bottom=1,left=1,right=1, borderType=cv2.BORDER_REFLECT)
                imgSharp = cv2.filter2D(imgTmpBorder,-1, maskTmp)

                cv2.imshow("Detekcja krawedzi " + self.isActiveKey, imgSharp)

    ####

    #  Operacja Mediany

    ####

    def imageMedianProcessing(self):
        medianWindow = tk.Toplevel()
        medianWindow.title("Operacja Mediany - wybierz obszar")

        mask = {"3x3":3, "5x5":5, "7x7":7, "9x9":9}
        itemsMask = [x for x in mask.keys()]
   
        marg = {
                    "BORDER_CONSTANT": cv2.BORDER_CONSTANT,
                    "BORDER_WRAP": cv2.BORDER_WRAP,
                    "BORDER_REFLECT": cv2.BORDER_REFLECT}

        itemsMarg = [x for x in marg.keys()]
       

        label1 = tk.Label(medianWindow, text="Wybór maski", padx=15)

        label2 = tk.Label(medianWindow, text="Ustawienia pikseli brzegowych", padx=15,  pady=10 )
        label3 = tk.Label(medianWindow, text="Stała pixeli brzegowych: ", padx=15,  pady=10 )


        entry1 = tk.Entry(medianWindow)
        entry1.insert(0,"0")


        combobox1 = ttk.Combobox(medianWindow, state='readonly', width=45)
        combobox1["values"] = itemsMask

        combobox2 = ttk.Combobox(medianWindow, state='readonly', width=45)
        combobox2["values"] = itemsMarg


        button = tk.Button(medianWindow, text="Wykonaj", command = lambda: imageMedianProcessingCalc(combobox1.get(), combobox2.get(),entry1.get()))


        label1.grid(column=0, row = 0  )
        combobox1.grid(column=0, row = 1, padx=15 )


        label2.grid(column=0, row = 2  )
        combobox2.grid(column=0, row = 3, padx=15)

        label3.grid(column=0, row = 4  )
        entry1.grid( column=0,row=5, padx=5)
        
        button.grid(columnspan=3, row=6, pady=15)

        def imageMedianProcessingCalc(value1, value2, value3):

            imgTmp = self.isActiveValue
            sizeTmp = mask[value1]

            if value2 == "BORDER_CONSTANT":
    
                imgTmpMed = cv2.copyMakeBorder(imgTmp, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=(int(value3), int(value3), int(value3)))
                imgMedian = cv2.medianBlur(imgTmpMed, sizeTmp)

                cv2.imshow("Median " + self.isActiveKey, imgMedian)

            elif value2 == "BORDER_WRAP":


                imgTmpMed = cv2.copyMakeBorder(imgTmp, 3, 3, 3, 3, cv2.BORDER_WRAP)
                imgMedian = cv2.medianBlur(imgTmpMed, sizeTmp)

                cv2.imshow("Median " + self.isActiveKey, imgMedian)

            elif value2 == "BORDER_REFLECT":

                
                imgTmpMed = cv2.copyMakeBorder(imgTmp, 3, 3, 3, 3, cv2.BORDER_REFLECT)
                imgMedian = cv2.medianBlur(imgTmpMed, sizeTmp)

                cv2.imshow("Median " + self.isActiveKey, imgMedian)
    ####

    #  Detekcja krawędzi 

    ####
   
    def edgeDetection(self):

        edgeDetectionWindow = tk.Toplevel()
        edgeDetectionWindow.title("Detekcja krawedzi")

        radioValue = tk.StringVar()
        radioSobel = tk.Radiobutton(edgeDetectionWindow, value=1, variable=radioValue, text="Detekcja Sobela",tristatevalue=0 )
        radioPrewitt = tk.Radiobutton(edgeDetectionWindow, value=2,variable=radioValue ,text="Detekcja Prewitta", tristatevalue=0) 
        radioCanny = tk.Radiobutton(edgeDetectionWindow, value=3,variable=radioValue ,text="Detekcja Cannyego", tristatevalue=0) 

        button = tk.Button(edgeDetectionWindow, text="Wykonaj" ,command = lambda: edgeDetectionProcessing(radioValue.get()))
        button.grid(row=1, columnspan=3, padx=15,pady=15)


        radioSobel.grid(row=0, column=0, padx=5, pady=15)
        radioPrewitt.grid(row=0, column=1, padx=5, pady=15)
        radioCanny.grid(row=0, column=2, padx=5, pady=15)


        def edgeDetectionProcessing(value1):

            imgTmp = self.isActiveValue

            if value1 == "1":
                #Sobel

                depth = cv2.CV_16S

                gradX = cv2.Sobel(imgTmp, depth, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
                gradY = cv2.Sobel(imgTmp, depth, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

                absGradX = cv2.convertScaleAbs(gradX)
                absGradY = cv2.convertScaleAbs(gradY)
                grad = cv2.addWeighted(absGradX, 0.5, absGradY, 0.5, 0)

                cv2.imshow('Sobel ' + self.isActiveKey, grad)


            elif value1 == "2":
                #Prewitt

                kernelX = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
                kernelY = np.array([[1, 1, 1],[0, 0, 0], [-1, -1, -1]])

                absGradX = cv2.filter2D(imgTmp, -1, kernelX)
                absGradY = cv2.filter2D(imgTmp, -1, kernelY)

                height = imgTmp.shape[0]
                width = imgTmp.shape[1]

                nImg = np.zeros([height, width, 3])


                for i in range(height):
                    for j in range(width):

                        tmpValue = (absGradX[i,j] + absGradY[i,j])
                        nImg[i,j] = tmpValue

                absNImg = cv2.convertScaleAbs(nImg)
                cv2.imshow('Prewitt '+ self.isActiveKey, absNImg)

            elif value1 == "3":
                #Canny
                cannyEdgeWindow = tk.Toplevel()

                label1 = tk.Label(cannyEdgeWindow,text="Próg 1: ").grid(row=0, column=0, padx=15)
                label2 = tk.Label(cannyEdgeWindow,text="Próg 2: ").grid(row=0, column=2, padx=15)
            
                entry1 = tk.Entry(cannyEdgeWindow)
                entry1.grid(row=0, column=1)
                entry1.insert(0, "1")

                entry2 = tk.Entry(cannyEdgeWindow)
                entry2.grid(row=0, column=3)
                entry2.insert(0, "1")

                button = tk.Button(cannyEdgeWindow, text="Wykonaj", command=lambda: cannyCalc(entry1.get(), entry2.get()))
                button.grid(columnspan=4, pady=10)

            
                def cannyCalc(value1, value2):
                
                
                    imgCanny = cv2.Canny(imgTmp, threshold1=int(value1), threshold2=int(value2))
            
                    cv2.imshow("Canny test", imgCanny)

####

    # Progowanie interaktywne
 
####

    def interactiveTreshold(self):
        interactiveTresholdWindow = tk.Toplevel()
        interactiveTresholdWindow.title("Progowanie interaktywne")

        radioValue = tk.StringVar()

        oneThreshold = tk.Radiobutton(interactiveTresholdWindow, value=1, variable=radioValue, text="Z jednym progiem",tristatevalue=0 )
        twoThreshold = tk.Radiobutton(interactiveTresholdWindow, value=2,variable=radioValue ,text="Z dwoma progami", tristatevalue=0) 

        button = tk.Button(interactiveTresholdWindow, text="Wybierz" , command = lambda:  imageTresholdInteractive( radioValue.get()))
        button.grid(row=1, columnspan=3, padx=15,pady=15)


        oneThreshold.grid(row=0, column=0, padx=5, pady=15)
        twoThreshold.grid(row=0, column=1, padx=5, pady=15)

        def imageTresholdInteractive(value):
            imgTmp = self.isActiveValue

            if value == "1":

                interactiveTresholdWindowSettings = tk.Toplevel()
                interactiveTresholdWindowSettings.title("Progowanie interaktywne - ustawienia")
                interactiveTresholdWindowSettings.geometry("100x100")
                label1 = tk.Label(interactiveTresholdWindowSettings,text="Próg:").grid(row=0, column=0, padx=15)

                scale = tk.Scale(interactiveTresholdWindowSettings, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda scaleValue: imageTresholdInteractive(int(scaleValue))) ## albo vertical
                scale.grid(row=1, column=0, padx=5)


                def imageTresholdInteractive(value):

                    _, newImg = cv2.threshold(imgTmp, int(value),255, cv2.THRESH_BINARY)

                    cv2.imshow("Grayscale with limit"+ self.isActiveKey, newImg)
                    
            elif value == "2":
                interactiveTresholdWindowSettings = tk.Toplevel()
                interactiveTresholdWindowSettings.title("Progowanie interaktywne - ustawienia")
                interactiveTresholdWindowSettings.geometry("125x150")


                labelFlo = tk.Label(interactiveTresholdWindowSettings,text="Próg dolny:").grid(row=0, column=0, padx=15)

                labelCell = tk.Label(interactiveTresholdWindowSettings,text="Próg górny:").grid(row=2, column=0, padx=15)

                valueFlo = tk.IntVar() 
                scaleFlo = tk.Scale(interactiveTresholdWindowSettings, from_=0, to=255, orient=tk.HORIZONTAL,variable=valueFlo,command=lambda scaleValue: imageTresholdInteractive(int(scaleValue), int(valueCell.get()))) ## albo vertical
                scaleFlo.grid(row=1, column=0, padx=5)        

                valueCell = tk.IntVar() 
                scaleCell = tk.Scale(interactiveTresholdWindowSettings, from_=0, to=255, orient=tk.HORIZONTAL, variable=valueCell, command=lambda scaleValue1: imageTresholdInteractive(int(valueFlo.get()), int(scaleValue1))) ## albo vertical
                scaleCell.grid(row=3, column=0, padx=5)
                

                def imageTresholdInteractive(value, value2):

                    imgTmp = self.isActiveValue
                    imgTmpToGray = cv2.cvtColor(imgTmp, cv2.COLOR_BGR2GRAY)

                    gray_filtered = cv2.inRange(imgTmpToGray, value, value2)
                    
                    cv2.imshow("Grayscale with two limits "+ self.isActiveKey, gray_filtered)
                



####

    # Progowanie OTSU
 
####

    def otsuThreshold(self):

        
        imgTmp = self.isActiveValue 
        imgTmpToGray = cv2.cvtColor(imgTmp, cv2.COLOR_BGR2GRAY)

        ret ,calculate = cv2.threshold(imgTmpToGray, 0, 255, cv2.THRESH_OTSU)

        interactiveTresholdWindow = tk.Toplevel()
        interactiveTresholdWindow.title("Wartość OTSU")
        interactiveTresholdWindow.geometry("50x50")

        areaLabelText = tk.Label(interactiveTresholdWindow, text="OTSU: ")
        areaLabelText.grid(row=0, column=0)

        areaLabelText = tk.Label(interactiveTresholdWindow, text=ret)
        areaLabelText.grid(row=0, column=1)

        


        cv2.imshow("Progowanie Otsu " + self.isActiveKey, calculate)

####
    # Progowanie adaptacyjne
 
####

    def adaptiveThreshold(self):

        adaptiveThreshold = tk.Toplevel()
        adaptiveThreshold.title("Progowanie adaptacyjne")


        radioValue = tk.StringVar()
        radioMedian = tk.Radiobutton(adaptiveThreshold, value=1, variable=radioValue, text="Srednia z otoczenia", tristatevalue=0 )
        radioGauss = tk.Radiobutton(adaptiveThreshold, value=2, variable=radioValue ,text="Średnia ważona - gauss", tristatevalue=0) 


        button = tk.Button(adaptiveThreshold, text="Wykonaj" ,command = lambda: adaptiveThresholdProcessing(radioValue.get()))


        def adaptiveThresholdProcessing(val1):

            imgTmp = self.isActiveValue
            imgTmpToGray = cv2.cvtColor(imgTmp, cv2.COLOR_BGR2GRAY)

            if val1 == "1":
                imgMean = cv2.adaptiveThreshold(imgTmpToGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY, 5, 0)
                
                cv2.imshow("Srednia z otoczenia - " + self.isActiveKey, imgMean)

            else:
                imgGauss = cv2.adaptiveThreshold(imgTmpToGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 0)
                cv2.imshow("Srednia ważona Gauss - " + self.isActiveKey, imgGauss)




        button.grid(row=1, columnspan=2, padx=15,pady=15)
        radioMedian.grid(row=0, column=0, padx=5, pady=15)
        radioGauss.grid(row=0, column=1, padx=5, pady=15)
####

    # Operacje morfologiczne
 
####
    def morphOperations(self):
        morhOperationsWindow = tk.Toplevel()
        morhOperationsWindow.title("Operacje morfologiczne")


        radioValue = tk.StringVar()
        radioErode = tk.Radiobutton(morhOperationsWindow, value=1, variable=radioValue, text="Erozja", tristatevalue=0 )
        radioDylation = tk.Radiobutton(morhOperationsWindow, value=2, variable=radioValue ,text="Dylacja", tristatevalue=0) 
        radioOpen = tk.Radiobutton(morhOperationsWindow, value=3, variable=radioValue ,text="Otwarcie", tristatevalue=0) 
        radioClose = tk.Radiobutton(morhOperationsWindow, value=4, variable=radioValue ,text="Zamkniecie", tristatevalue=0) 

        radioErode.grid(row=0, column=0, padx=5, pady=15)
        radioDylation.grid(row=0, column=1, padx=5, pady=15)
        radioOpen.grid(row=0, column=2, padx=5, pady=15)
        radioClose.grid(row=0, column=3, padx=5, pady=15)

        button = tk.Button(morhOperationsWindow, text="Wykonaj" ,command = lambda: morhOperationCalc(radioValue.get()))
        button.grid(row=1, columnspan=4, padx=15,pady=15)
        
        
        def morhOperationCalc(value):
            
            imgTmp = self.isActiveValue
            imgTmpToGray = cv2.cvtColor(imgTmp, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((3, 3), np.uint8)
            
            if value == "1":
                imgErode = cv2.erode(imgTmpToGray, kernel=kernel,iterations=2)
                
                cv2.imshow("Erozja - " + self.isActiveKey, imgErode) 
                
                
            if value == "2":
                
                imgDial = cv2.dilate(imgTmpToGray, kernel=kernel,iterations=2)

                cv2.imshow("Dylacja - " + self.isActiveKey, imgDial)
                
            if value == "3":
                
                imgOpen = cv2.morphologyEx(imgTmpToGray,cv2.MORPH_OPEN, kernel=kernel)
                
                cv2.imshow("Otwarcie - " + self.isActiveKey, imgOpen)
            
            if value == "4":
         
                imgClose = cv2.morphologyEx(imgTmp, cv2.MORPH_CLOSE, kernel=kernel)
                cv2.imshow("Zamkniecie - " + self.isActiveKey, imgClose)

####

    # Momenty
 
####
    def imageMoments(self):
        imgTmp = self.isActiveValue
        grayImg = cv2.cvtColor(imgTmp, cv2.COLOR_BGR2GRAY)

        momentsCalc = cv2.moments(grayImg)

        fieldAndPerimeterWindow = tk.Toplevel()
        fieldAndPerimeterWindow.title("Momenty")

        areaLabelText = tk.Label(fieldAndPerimeterWindow, text="Momenty: ")
        areaLabelText.pack(side=tk.TOP)

        scrollbar = tk.Scrollbar(fieldAndPerimeterWindow)

        momentsCalcTmp = str(momentsCalc)
        momentsCalcTmp = momentsCalcTmp.replace(",","\n")

        txt = Path(self.isActiveKey+"moments.txt").write_text(str(momentsCalcTmp))
        
        textBox = tk.Text(
            fieldAndPerimeterWindow, 
            height=5, # ilość linni
            width=30, # ilość znaków
            padx=5,
            pady=5, ## dopełnienie
            font = "Times 18 bold",
            )

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
        textBox.pack(side=tk.TOP,expand=True, fill=tk.BOTH)
        scrollbar.config(command=textBox.yview) 
        textBox.config(yscrollcommand= scrollbar.set)

        textBox.insert(tk.END, momentsCalc)




####

    # Pole powierzchni i obwód 
 
####
    def fieldAndPerimeter(self):
        imgTmp = self.isActiveValue
        grayImg = cv2.cvtColor(imgTmp, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(grayImg,127,255,0)

        contours,hierarchy = cv2.findContours(thresh, 1, 2) ## [[[ 1 -1 -1 -1] [-1  0 -1 -1]]]
        cnt = contours

        areaList = []
        perimeterList = []

        for e,i in enumerate(cnt):
            area = cv2.contourArea(i)
            areaList.append(area)
            perimeter = cv2.arcLength(i,True)
            perimeterList.append(perimeter)


        fieldAndPerimeterWindow = tk.Toplevel()
        fieldAndPerimeterWindow.title("Pole i obwód")
        fieldAndPerimeterWindow.geometry("200x150")
        fieldAndPerimeterWindow.resizable()

        tmpData = {'Pole': str(areaList) + ";",
                   'Obwod': str(perimeterList) }

        tmpData = str(tmpData).replace(";', '","'\n'")

        txt = Path(self.isActiveKey+"area-perimeter.txt").write_text(str(tmpData))

        areaLabel = tk.Label(fieldAndPerimeterWindow, text=area)
        perimeterLabel = tk.Label(fieldAndPerimeterWindow, text=perimeter)
        
        areaLabelText = tk.Label(fieldAndPerimeterWindow, text="Pole: ")
        perimeterLabelText = tk.Label(fieldAndPerimeterWindow, text="Obwód: ")


        areaLabel.grid(row=0,column=1,ipady=15, ipadx=15)
        perimeterLabel.grid(row=1,column=1,ipady=15, ipadx=15)

        areaLabelText.grid(row=0,column=0,pady=15, padx=15)
        perimeterLabelText.grid(row=1,column=0,ipady=15, ipadx=15)




####

    # Współczynniki kształtu: aspectRatio, extent, solidity, equivalentDiameter 
 
####

    def aspectRatio(self):

        aspectRatio = tk.Toplevel()
        aspectRatio.title("aspectRatio")
        aspectRatio.resizable()

        aspectRatioLabel = tk.Label(aspectRatio, text="aspectRatio: ")
        extentLabel = tk.Label(aspectRatio, text="extent: ")
        solidityLabel = tk.Label(aspectRatio, text="solidity: ")
        equivalentDiameterLabel = tk.Label(aspectRatio, text="equivalentDiameter : ")

        aspectRatioLabel.grid(row=0,column=0,pady=15, padx=15)
        extentLabel.grid(row=1,column=0,ipady=15, ipadx=15)
        solidityLabel.grid(row=2,column=0,ipady=15, ipadx=15)
        equivalentDiameterLabel.grid(row=3,column=0,ipady=15, ipadx=15)


        imgTmp = self.isActiveValue
        grayImg = cv2.cvtColor(imgTmp, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(grayImg, 30, 200)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnt = contours

        
        def solidity(cnt):
            lista = []

            for e,i in enumerate(cnt):
                area = cv2.contourArea(i)
                if area == 0:
                    lista.append("0")
                    continue
                hull = cv2.convexHull(i)
                hull_area = cv2.contourArea(hull)
                solidity = float(area)/hull_area
                sol = round(solidity, 2)
                lista.append(sol)
            return lista
        solid = solidity(cnt)



        def eq_dia(cnt):
            lista = []

            for e,i in enumerate(cnt):
                area = cv2.contourArea(i)
                equi_diameter = np.sqrt(4*area/np.pi)
                equ = round(equi_diameter, 2)
                lista.append(equ)
            return lista

        dia = eq_dia(cnt)

        img = cv2.drawContours(imgTmp,contours,-1,(255,255,0),2)

        aspectList = []
        extentList = []

        for e,i in enumerate(cnt):
            area = cv2.contourArea(i)
            x,y,w,h = cv2.boundingRect(i)
            rect_area = w*h
            extent = float(area)/rect_area
            ext = round(extent, 2)
            extentList.append(ext)

            aspect_ratio = float(w)/h
            asp = round(aspect_ratio, 2)
            aspectList.append(asp)



        tmpData = {'aspectRatio': str(aspectList) + ";",
                   'extent': str(extentList) + ";",
                   'solidity':str(solid) + ";",
                   'equivalentDiameter':str(dia) }

        tmpData = str(tmpData).replace(";', '","'\n'")

        txt = Path(self.isActiveKey+"aspectRatio-extent-solidity-equivalentDiameter.txt").write_text(str(tmpData))

        aspectRatioLabelCalc = tk.Label(aspectRatio, text=aspectList)
        extentLabelCalc = tk.Label(aspectRatio, text=extentList)
        solidityLabelCalc = tk.Label(aspectRatio, text=solid )
        equivalentDiameterLabelCalc = tk.Label(aspectRatio, text=dia )

        aspectRatioLabelCalc.grid(row=0,column=1,ipady=15, ipadx=15)
        extentLabelCalc.grid(row=1,column=1,ipady=15, ipadx=15)
        solidityLabelCalc.grid(row=2,column=1,ipady=15, ipadx=15)
        equivalentDiameterLabelCalc.grid(row=3,column=1,ipady=15, ipadx=15)

        cv2.imshow("aspectRatio", img)



    ##################################################
    ###
    ###
    ###  Implementacjafunkcji reprezentacji obrazu monochromatycznego w postaci 
    ###  ośmiubinarnych obrazów dla każdego bitu 
    ###
    ###
    ###
    ###


    def finalMiniProjectCalc(self):

        finalProjectWindow = tk.Toplevel()
        finalProjectWindow.title("Konfiguracja")
        finalProjectWindow.geometry("525x250")


        activeImg = self.isActiveKey
        if self.isActiveKey is None:
            activeImg = "Obecnie nie ma zadnego obrazu"

        activeImage = tk.Label(finalProjectWindow, text="Aktywny obraz: " + activeImg)
        activeImg = self.isActiveKey

        activeImage.grid(row=0, columnspan=5, pady=15)


        informationLabel = tk.Label(finalProjectWindow, text= "Obszar do zaznaczenia jest tworzony od górnego lewego rogu, prawy dolny róg jest zakończeniem")
        informationLabel.grid(row=3, columnspan=5, pady=5)

        h = self.isActiveValue.shape[0] 
        w = self.isActiveValue.shape[1] 


        sizeOfActiveImage = tk.Label(finalProjectWindow, text="Wielkość aktywnego obrazu: " + str(w) +"px x" + str(h) + "px")
        sizeOfActiveImage.grid(row=4, columnspan=5, pady=15)

        
        fromXY = tk.Label(finalProjectWindow, text="Początek (X,Y)")
        endXY = tk.Label(finalProjectWindow, text="Koniec (X,Y)")

        startX = tk.Entry(finalProjectWindow, width=10)
        startY = tk.Entry(finalProjectWindow, width=10)

        startX.insert(0,"0")
        startY.insert(0,"0")

        endX = tk.Entry(finalProjectWindow, width=10)
        endY = tk.Entry(finalProjectWindow, width=10)

        endX.insert(0,w)
        endY.insert(0,h)


        fromXY.grid(row=5, column=0, columnspan=2)
        endXY.grid(row=5, column=2, columnspan=2)

        startX.grid(row=6, column=0 )
        startY.grid(row=6, column=1 )
        endX.grid(row=6, column=2 )
        endY.grid(row=6, column=3 )

        
        button = tk.Button(finalProjectWindow, text= "Wykonaj", command=lambda: finalProjectImageCalculation( startX.get(), startY.get(), endX.get(), endY.get() ))
        button.grid(row=7, columnspan=4, pady=15)


        def finalProjectImageCalculation(startX , startY , endX , endY ):
            print("Wprowadzone dane: ", startX, startY, endX, endY)
            
            startX = int(startX)  
            startY = int(startY)
            endX = int(endX)
            endY = int(endY)

            if (startX > endX) or (startY > endY):
                print("Wartosci punktu poczatkowego zakresu sa zbyt wielkie od punktu koncowego")
                return
            
            imgTmp = self.isActiveValue

            height = endX - startX                                  ## Określenie wielkości okna wynikowego a podstawie wprowadzonych danych 
            width = endY - startY


            bitsDict = {                                            ## Słownik trzymający wszystkie obrazy binarne obrazy
                0 : np.zeros([width, height, 3]),
                1 : np.zeros([width, height, 3]),
                2 : np.zeros([width, height, 3]),
                3 : np.zeros([width, height, 3]),
                4 : np.zeros([width, height, 3]),
                5 : np.zeros([width, height, 3]),
                6 : np.zeros([width, height, 3]),
                7 : np.zeros([width, height, 3]),
            }
            
            for i in range(width):
                for j in range(height):
                    pixel_b, pixel_g, pixel_r = imgTmp[i][j]         ## Pobranie wartości pixela (dla monochromatycznych )


                    finalList = []                                   ## Lista przetrzymująca wartości pojedynczego pixela
                    result = str(f'{pixel_b:08b}')                   ## Pojedyczny piksel przekonwertowany do liczby binarnej

                    for index in range(8):
                        finalList.append(int(result[index]))         ## Wstawianie wartości piksela do tablicy

                    for listValuesIndex in range(len(finalList)):    ## Pętla służąca do binaryzacji obrazu, wszystkie wartości poza zerem stają się białe
                        if finalList[listValuesIndex] != 0:
                            finalList[listValuesIndex] = 255    


                    bitsDict[0][i,j] = finalList[0]                   ## Rozkładanie kolejno jednego piksela na 8 obrazów
                    bitsDict[1][i,j] = finalList[1]
                    bitsDict[2][i,j] = finalList[2]
                    bitsDict[3][i,j] = finalList[3]
                    bitsDict[4][i,j] = finalList[4]
                    bitsDict[5][i,j] = finalList[5]
                    bitsDict[6][i,j] = finalList[6]
                    bitsDict[7][i,j] = finalList[7]                

            for i in range(8):
                cv2.imshow("Bit: "+ str(i), bitsDict[i])               ## Wyświetlenie obrazów utworzonych wcześniej


project = MainProject(mainWindow)
mainWindow.mainloop()