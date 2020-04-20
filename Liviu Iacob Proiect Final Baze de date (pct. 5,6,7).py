'''5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
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
        - data DATE '''

import mysql.connector

# imi creez in workbench baza de date pythonliviuiacob
# Test change - please delete this line

# Credentiale conectare
host = "localhost"
passwd = "ParolaRoot" #parola root
port = 3306  # normal portul e 3306. Daca e diferit trebuie mentionat acela
user = "root"
dbname = "pythonliviuiacob" #creez baza de date mai intai in Workbench

# Creare obiect conectare
db = mysql.connector.connect( host=host, port=port, user=user, passwd=passwd, db=dbname )

# Creare cursor
cursor = db.cursor ( )
cursor.execute ('USE pythonliviuiacob')


# creez tabela Categoria
cursor.execute("DROP TABLE IF EXISTS Categoria")
cursor.execute("""CREATE TABLE Categoria
                    (idc INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                     denc VARCHAR(255))""")
#creez tabela Produs
cursor.execute("DROP TABLE IF EXISTS Produs")
cursor.execute("""CREATE TABLE Produs
                    (idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                     idc INT NOT NULL, 
                     denp VARCHAR(255), 
                     pret DECIMAL(8,2) DEFAULT 0)""")
                     #foreign key fk_Produs_Categoria(idc) references Categoria(idc) ON UPDATE CASCADE ON DELETE RESTRICT))""")
                     #FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT)""")
#Creez tabela Operatiuni
cursor.execute("DROP TABLE IF EXISTS Operatiuni")

cursor.execute("""CREATE TABLE Operatiuni
               (ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
               idp INT NOT NULL,
               cant DECIMAL(10,3) DEFAULT 0,
               data DATE)""")

#6. Implementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

#inserez date in tabela Categoria
cursor.execute("""INSERT INTO Categoria (denc) VALUES
                                       ('Mezeluri'),
                                       ('Lactate'),
                                       ('Fructe'),
                                       ('Legume')""")
#inserez date in tabela Produs
cursor.execute("""INSERT INTO Produs (idc , denp , pret) VALUES 
                                       (1,'Salam Sibiu', 10.32),
                                       (1,'Carnati afumati', 9.99),
                                       (1,'Crenvursti CrisTIM', 7.41),
                                       (2,'Iaurt Grecesc', 5.33),
                                       (2,'Cascaval Dalia', 32.44),
                                       (2,'Lapte 3.5%',5.60),
                                       (3,'Banane',4.99),
                                       (3,'Mere Golden',2.45),
                                       (3,'Pepene Rosu', 1.99),
                                       (4,'Cartofi', 3.01),
                                       (4,'Rosii',9.99),
                                       (4,'Castraveti Cornison',6.75)""")
#inserez date in tabela Operatiuni
cursor.execute("""INSERT INTO Operatiuni (idp , cant , data) VALUES 
                                     (2, 23.500, '2020-01-21'),
                                     (6, 20.000, '2020-02-13'),
                                     (10, 100.435, '2020-03-01'),
                                     (11, 8.400, '2020-03-04')""")

#7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--

# Doresc sa creez un view care sa imi afiseze toate produsele lactate
# (stiu deja ca produsele lactate au idc=2 din tabelul Categoria)

cursor.execute('create view v$Lactate as select * from Produs where idc=2')

# Doresc sa creez un view care imi afiseaza toate produsele mai ieftine cu 5 lei.
cursor.execute('create view v$produse_sub_5lei as select * from Produs where pret<5')

db.commit()

#afisez rezultatele

#cursor.execute('select* from Categoria;')
cursor.execute('select * from Produs;')
#cursor.execute ('select * from Operatiuni;')

rez = cursor.fetchall()
for r in rez:
    print (r)

cursor.close()

