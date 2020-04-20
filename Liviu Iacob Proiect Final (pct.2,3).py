"""
    Avem aplicatia care tine stocul unui depozit (Cap 5-6). Efectuati urmatoarele imbunatatiri:

	Este necesar rezolvati minim 3 din punctele de mai jos:

1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;	--pygal--

2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o
limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa
transmita automat un email de avertizare;

3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului) ; 	--SMTP--

4. Utilizati Regex pentru a cauta :
    - un produs introdus de utilizator;
    - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--

5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
    Categoria
        - idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY (integer in loc de int in sqlite3)
        - denc VARCHAR(255) (text in loc de varchar in sqlite3)
    Produs
        - idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idc INT NOT NULL
        - denp VARCHAR(255)
        - pret DECIMAL(8,2) DEFAULT 0 (real in loc de decimal)
        # FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT
    Operatiuni
        - ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idp INT NOT NULL
        - cant DECIMAL(10,3) DEFAULT 0
        - data DATE

6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--

8. Completati aplicatia astfel incat sa permita introducerea pretului la fiecare intrare si iesire.
Pretul de iesire va fi pretul mediu ponderat (la fiecare tranzactie de intrare se va face o medie intre
pretul produselor din stoc si al celor intrate ceea ce va deveni noul pret al produselor stocate).
Pretul de iesire va fi pretul din acel moment; --pentru avansati--

9. Creati doua metode noi, testatile si asigurativa ca functioneaza cu succes;


""" #

from datetime import datetime
from prettytable import PrettyTable
import smtplib
import pftp #modul propriu de parola mail


class Stoc:
    """Tine stocul unui depozit"""

    def __init__(self, prod, categ, um='buc.', sold=0, soldminim=0): #la initializarea obiectului setam soldul minim
        self.prod = prod			# parametri cu valori default ii lasam la sfarsitul listei
        self.categ = categ
        self.sold = sold
        self.um = um
        self.i = {}					# fiecare instanta va avea trei dictionare intrari, iesiri, data
        self.e = {}					# pentru mentinerea corelatiilor cheia operatiunii va fi unica
        self.d = {}
        self.soldminim = soldminim # variabila soldminim cu care comparam sold
        self.Atentie = ''  # mesajul pentru atentionare limita stoc

    def intrari(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        self.data = data
        self.cant = cant
        if self.d.keys():               # dictionarul data are toate cheile (fiecare tranzactie are data)
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.i[cheie] = self.cant       # introducem valorile in dictionarele de intrari si data
        self.d[cheie] = self.data
        self.sold += cant  # recalculam soldul dupa fiecare tranzactie

    def iesiri(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        self.data = data
        self.cant = cant
        if self.d.keys():
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.e[cheie] = self.cant       # similar, introducem datele in dictionarele iesiri si data
        self.d[cheie] = self.data
        self.sold -= self.cant


    def fisaprodus(self):

        print('Fisa produsului ' + self.prod + ': ' + self.um)
        listeaza = PrettyTable()
        listeaza.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire']

        for elem in self.d.keys():
            if elem in self.i.keys():
                listeaza.add_row([elem, self.d[elem], self.i[elem], str(0)])

            else:
                listeaza.add_row([elem, self.d[elem], str(0), self.e[elem]])

        listeaza.add_row(['---------', '--------', '------', '----'])
        listeaza.add_row(['Sold final', self.categ, self.prod, self.sold])
        print(listeaza)


#2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o
#limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa
#transmita automat un email de avertizare;

        if self.sold < self.soldminim:
            self.Atentie = 'Trebuie refacut stocul de ' + self.prod  + ' , mai sunt disponibile doar ' + str(self.soldminim) + ' unitati!'
            print (self.Atentie)
            self.sendMail()  #trimite mail numai daca soldul se afla sub limita impusa


    def sendMail(self):

        expeditor = 'do-not-reply@info-stoc.com'
        destinatar = 'liviu.iacob@yahoo.com'
        username = 'liviu.iacob@info-stoc.com'
        parola = pftp.parola
        mesaj = """From: donot-reply <do-not-reply@info-stoc.com>
                    To: Liviu Iacob <liviu.iacob@yahoo.com>
                    Subject: Refacere Stoc

                        Draga Liviu,
                        
                        {}
                        
                        Robot Gestiune Marfa,""".format(self.Atentie)

        try:
            smtp_ob = smtplib.SMTP('mail.infoacademy.eu:25')
            # smtp_ob.starttls()  	# protocol criptare. e posibil sa nu mearga daca e activat
            smtp_ob.login(username, parola)
            smtp_ob.sendmail(expeditor, destinatar, mesaj)
            print('Mesaj expediat cu succes!')
        except:
            print('Mesajul nu a putut fi expediat!')

#3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
#de exemplu fisa produsului) ; 	--SMTP--

    def fisaprodusMail(self):
        print('Fisa Produsului este:')#
        expeditor = 'do-not-reply@info-stoc.com'
        destinatar = 'liviu.iacob@yahoo.com'
        username = 'liviu.iacob@info-stoc.com'
        parola = pftp.parola
        tabel = PrettyTable()
        tabel.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire']

        for elem in self.d.keys():
            if elem in self.i.keys():
                tabel.add_row([elem, self.d[elem], self.i[elem], str(0)])

            else:
                tabel.add_row([elem, self.d[elem], str(0), self.e[elem]])

        tabel.add_row(['---------','--------','------','----'])
        tabel.add_row(['Sold final', self.categ, self.prod, self.sold])
        mesaj = """ From: do-not-reply <do-not-reply@info-stoc.com>
                    To: Liviu Iacob <liviu.iacob@yahoo.com>
                    Subject: Fisa produsului {0} !


                   Salut Liviu, 
                
                  In mail vei gasi fisa produsului {0}, unitatea de masura: {1}
                  
                         {2}
                                              
                  This is an automated message,""".format(self.prod, self.um, tabel)

        try:
            smtp_ob = smtplib.SMTP('mail.infoacademy.eu:25')
            smtp_ob.login(username, parola)
            smtp_ob.sendmail(expeditor, destinatar, mesaj)
            print('Mesaj expediat cu succes!')
        except:
            print('Mesajul nu a putut fi expediat!')



# -------------------------------------------------------------

# Intrari si Iesiri
# Am introdus doua produse mai jos


lapte = Stoc('lapte','lactate','litri', 0 ,15) #limita de stoc este 15
lapte.intrari(80,'20200205')
lapte.iesiri(45 , '20200206')
lapte.intrari(40 , '20200301')
lapte.iesiri(21, '20200302')


cartofi = Stoc('Cartofi', 'Legume','kg',0,10)  #limita stoc este 10
cartofi.intrari(100, '20200205')
cartofi.iesiri(40,'20200206' )
cartofi.intrari(30, '20200301')
cartofi.iesiri(50, '20200302' )

#Testare

#cartofi.fisaprodus()
#cartofi.fisaprodus()
#cartofi.fisaprodusMail()
#cartofi.sendMail()