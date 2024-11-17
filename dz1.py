class Igrac:
    def __init__(self, ime, lista, broj):
        self.ime = ime
        self.figurice = lista
        self.brojFigurica = 4
        self.brojFiguricaNaPolju = 0
        self.broj = broj
        self.start = None
        self.cilj = None
        self.UKucici = 0
        self.prefix = ''
        self.oznakaFigurica(lista)
        
    def oznakaFigurica(self, figurice):
        trenutni = figurice.prvi
        if self.ime == 'Crveni':
            self.prefix = 'c'
        if self.ime == 'Plavi':
            self.prefix = 'p'
        if self.ime == 'Zeleni':
            self.prefix = 'z'
        if self.ime == 'Zuti':
            self.prefix = 'ž'
        while trenutni:
            trenutni.podatak = self.prefix + str(trenutni.podatak)
            trenutni = trenutni.sledeci
     
class ElementListe:
    def __init__(self, data):
        self.podatak = data
        self.sledeci = None

class Lista:
    def __init__(self):
        self.prvi = None
        self.poslednji = None
        
def dodajNaKraj(lista, element):
    if lista.poslednji is not None:
        lista.poslednji.sledeci = element
    else:
        lista.prvi = element
    lista.poslednji = element
    
def ukloniPrviElement(lista):
    if lista.prvi:
        lista.prvi = lista.prvi.sledeci

def Namestaljka():
    return 6

seed = 12345

def lkg():
    global seed
    m = 2**32
    a = 429493445
    c = 907633385
    result =  (a * seed + c) % m
    seed = result
    return result / m

def diceRoll():
    x = lkg() * 6
    if x >= 5:
        return 6
    if x >= 4:
        return 5
    if x >= 3:
        return 4
    if x >= 2:
        return 3
    if x >= 1:
        return 2
    else:
        return 1

def triBacanja(trenutniIgrac, igraci, cooSys):
    print('Imate pravo na tri bacanja.')
    kocka = 0
    for i in range(3):
        if kocka == 6:
            return
        while True:
            print(f'Na potezu je igrac: {trenutniIgrac.ime}')
            print("------MENI-----\n"
              "Izaberite opciju:\n"
              "1. Baci kockicu\n"
              "2. Ispis table\n"
              "3. Pregled preostalih figurice van polja (za jednog igraca)\n"
              "4. Pregled preostalih figurica van polja (svih igraca)\n"
              "5. Zavrsi igru\n")
            try:
                opcija = int(input())
                if opcija < 1 or opcija > 5:
                    print("Unesite ispravnu opciju\n")
                else:
                    if opcija == 1:
                        kocka = diceRoll()
                        print(f'Dobili ste: {kocka}')
                        if kocka == 6:
                            for i in cooSys:
                                if i[2][0] != trenutniIgrac.prefix and trenutniIgrac.start == [i[0], i[1]]:
                                    print(f'Izbacili ste novu figuricu {trenutniIgrac.figurice.prvi.podatak} na polje [{trenutniIgrac.start[0]}, {trenutniIgrac.start[1]}], i time pojeli figuricu {i[2]}')
                                    for igrac in igraci:
                                        if igrac.prefix == i[2][0]:
                                            dodajNaKraj(igrac.figurice, ElementListe(i[2]))
                                            cooSys.remove(i)
                                            igrac.brojFigurica += 1
                                            igrac.brojFiguricaNaPolju -= 1
                                            break
                                    break
                            print(f'Postavljena je figurica {trenutniIgrac.figurice.prvi.podatak} na start polje [{trenutniIgrac.start[0]}, {trenutniIgrac.start[1]}]')
                            cooSys.append([trenutniIgrac.start[0], trenutniIgrac.start[1], trenutniIgrac.figurice.prvi.podatak])
                            ukloniPrviElement(trenutniIgrac.figurice)
                            trenutniIgrac.brojFigurica -= 1
                            trenutniIgrac.brojFiguricaNaPolju += 1
                            break
                        else:
                            break
                    if opcija == 2:
                        ispisPolja(cooSys, velicinaPolja)
                        break
                    
                    if opcija == 3:
                        while True:
                            imena = []
                            for i in igraci:
                                imena.append(i.ime)
                            print(f'Unesite ime igraca cije figurice zelite da pogledate: ({imena})')
                            imeIgracaUnos = input()
                            if imeIgracaUnos not in imena:
                                print('Nevalidan unos. Unesite ime igraca koji je trenutno u igri (Rec pocinje velikim slovom npr. Crveni)')
                            else:
                                for i in igraci:
                                    if i.ime == imeIgracaUnos:
                                        ispisPreostalihFigurica(i)
                                        break
                                break
                        break
                    if opcija == 4:
                        for i in range(brojIgraca):
                            ispisPreostalihFigurica(igraci[i])
                        break
                    if opcija == 5:
                        igraci.clear()
                        break
            except ValueError:
                print("Unesite broj kao opciju\n")

def ispisPolja(cooSys, velicinaPolja):
    maxSirina = len(str(velicinaPolja * velicinaPolja - 1))
    for i in range(velicinaPolja):
        red = []
        for j in range(velicinaPolja):
            check = False
            for x in cooSys:
                if x[0] == i and x[1] == j:
                    check = True
                    break
            if check:
                red.append(x[2])
            else:
                red.append(0)
        formatiraniRed = [f"{i:>{maxSirina}}" for i in red]
        print(" ".join(formatiraniRed))

def ispisPreostalihFigurica(trenutniIgrac):
    trenutni = trenutniIgrac.figurice.prvi
    s = ''
    while trenutni:
        s += f'{trenutni.podatak}, '
        trenutni = trenutni.sledeci
    print(f'Figurice koje nisu na polju igraca {trenutniIgrac.ime}: ')
    print(s.strip())

velicinaPolja = 0
print('Unesite dimenzije polja: (Broj mora biti neparan i najmanje 7)')
while True:
    try:
        velicinaPolja = int(input())
        if velicinaPolja % 2 == 0:
            print('Broj mora biti neparan. Probajte ponovo.')
        elif velicinaPolja < 7:
            print('Broj mora biti barem 7.')
        else:
            break
    except ValueError:
        print("Niste uneli ceo broj. Probajte ponovo.")
        

brojIgraca = 0
print('Unesite broj igraca. Minimalan broj igraca je 2 a maksimalni 4.')
while True:
    try:
        brojIgraca = int(input())
        if brojIgraca < 2 or brojIgraca > 4:
            print('Nevalidan unos, obratite paznju da broj igraca mora biti u opsegu [2, 4]')
        else:
            break
    except ValueError:
        print('Niste uneli ceo broj. Probajte ponovo.')

igraci = []
izboriBoja = [1, 2, 3, 4]
listaFigurica = []

for i in range(brojIgraca):
    figurice = Lista()
    for i in range(1, 5):
        figurica = ElementListe(i)
        dodajNaKraj(figurice, figurica)
    listaFigurica.append(figurice)
        
for i in range(brojIgraca):
    print(f'Igracu {i + 1}, Birajte boju: (1 - Crvena, 2 - Plava, 3 - Zelena, 4 - Zuta)')
    
    while True:
        try:
            izborBoje = int(input())
            if izborBoje < 1 or izborBoje > 4:
                print('Nevalidan unos, obratite paznju da izbor mora biti u opsegu [1, 4]')
            elif izborBoje not in izboriBoja:
                print('Ta boja je vec izabrana, izaberite drugu boju.')
            else:
                if izborBoje == 1:
                    imeIgraca = 'Crveni'
                elif izborBoje == 2:
                    imeIgraca = 'Plavi'
                elif izborBoje == 3:
                    imeIgraca = 'Zeleni'
                elif izborBoje == 4:
                    imeIgraca = 'Zuti'
                izboriBoja.remove(izborBoje)
                break
        except ValueError:
            print('Niste uneli ceo broj. Probajte ponovo.')
            
    IDIgraca = i + 1
    
    igrac = Igrac(imeIgraca, listaFigurica[i], IDIgraca)
    
    if IDIgraca == 1:
        igrac.start = [velicinaPolja - 1, 0]
        igrac.cilj = [velicinaPolja - 1, 1]
    if IDIgraca == 2:
        igrac.start = [0, 0]
        igrac.cilj = [1, 0]
    if IDIgraca == 3:
        igrac.start = [0, velicinaPolja - 1]
        igrac.cilj =  [0, velicinaPolja - 2]
    if IDIgraca == 4:
        igrac.start = [velicinaPolja - 1, velicinaPolja - 1]
        igrac.cilj = [velicinaPolja - 2, velicinaPolja - 1]
        
    igraci.append(igrac)
    
listaFigurica.clear()
    
cooSys = []

brojac = 0

while igraci:
    
    brojacK = 0
    for igrac in igraci:
        if igrac.UKucici == 4:
            brojacK += 1
    if brojacK == brojIgraca:
        break
    
    if brojac == brojIgraca:
        brojac = 0
        
    trenutniIgrac = igraci[brojac]
    
    if trenutniIgrac.UKucici == 4:
        brojac += 1
        continue
    
    if trenutniIgrac.brojFigurica == 4:
        triBacanja(trenutniIgrac, igraci, cooSys)
        brojac += 1
        
    else:
        print(f'Na potezu je igrac: {trenutniIgrac.ime}')
        print("------MENI-----\n"
          "Izaberite opciju:\n"
          "1. Baci kockicu\n"
          "2. Ispis table\n"
          "3. Pregled preostalih figurice van polja (za jednog igraca)\n"
          "4. Pregled preostalih figurica van polja (svih igraca)\n"
          "5. Zavrsi igru\n")
        
        while True:
            try:
                izbor = int(input())
                if izbor < 1 or izbor > 5:
                    print('Nevalidan unos, niste uneli broj u opsegu [1, 5]')
                else:
                    if izbor == 1:
                        skip1 = False
                        kocka = diceRoll()
                        print(f'Dobili ste: {kocka}')
                        if kocka == 6 and trenutniIgrac.brojFigurica > 0:
                            print('Zelite li da izvucete novu figuru na polje ili da pomerite neku figuru koja je vec na polju?\n (1 - Izvuci novu, 2 - Odigraj nekom figuricom)')
                            while True:
                                try:
                                    skip1 = False
                                    specIzbor = int(input())
                                    if specIzbor != 1 and specIzbor != 2:
                                        print('Izaberite validnu opciju (1 ili 2)')
                                    elif specIzbor == 1:
                                        for i in cooSys:
                                            if [i[0], i[1]] == trenutniIgrac.start:
                                                if i[2][0] == trenutniIgrac.prefix:
                                                    print('Ne mozete da izvucete novu figuricu kad je jedna tvoja vec na pocetnoj poziciji.')
                                                    skip1 = True
                                                elif i[2][0] != trenutniIgrac.prefix:
                                                    print(f'Izbacili ste novu figuricu, i time pojeli figuricu {i[2]}')
                                                    for igrac in igraci:
                                                        if igrac.prefix == i[2][0]:
                                                            dodajNaKraj(igrac.figurice, ElementListe(i[2]))
                                                            cooSys.remove(i)
                                                            igrac.brojFigurica += 1
                                                            igrac.brojFiguricaNaPolju -= 1
                                                            break
                                        if skip1:
                                            print('Izaberite ponovo (Opcija 1 ocigledno nije trenutno dostupna pa pritisnite 2)')
                                            continue
                                        print(f'Postavljena je figurica {trenutniIgrac.figurice.prvi.podatak} na start polje [{trenutniIgrac.start[0]}, {trenutniIgrac.start[1]}]')
                                        cooSys.append([trenutniIgrac.start[0], trenutniIgrac.start[1], trenutniIgrac.figurice.prvi.podatak])
                                        ukloniPrviElement(trenutniIgrac.figurice)
                                        trenutniIgrac.brojFiguricaNaPolju += 1
                                        trenutniIgrac.brojFigurica -= 1
                                        skip1 = True
                                        brojac += 1
                                        break
                                    elif specIzbor == 2:
                                        break
                                except ValueError:
                                    print('Unesite broj')
                        
                        if skip1:
                            break
                        
                        temp = [0, 0]
                        
                        brojacPokusaja = 0
                            
                        while True:
                            try:
                                if brojacPokusaja == trenutniIgrac.brojFiguricaNaPolju:
                                    if kocka != 6:
                                        print('Nije moguc ni jedan validan potez u ovom krugu.')
                                        break
                                    elif kocka == 6 and trenutniIgrac.brojFigurica == 0:
                                        print('Nije moguc ni jedan validan potez u ovom krugu.')
                                        break
                                    elif kocka == 6 and trenutniIgrac.brojFigurica > 0:
                                        print('Jedini potez vam je da izvucete novu figuricu.')
                                        for i in cooSys:
                                            if [i[0], i[1]] == trenutniIgrac.start:
                                                if i[2][0] == trenutniIgrac.prefix:
                                                    print('Ne mozete da izvucete novu figuricu kad je jedna tvoja vec na pocetnoj poziciji.')
                                                    skip1 = True
                                                elif i[2][0] != trenutniIgrac.prefix:
                                                    print(f'Izbacili ste novu figuricu, i time pojeli figuricu {i[2]}')
                                                    for igrac in igraci:
                                                        if igrac.prefix == i[2][0]:
                                                            dodajNaKraj(igrac.figurice, ElementListe(i[2]))
                                                            cooSys.remove(i)
                                                            igrac.brojFigurica += 1
                                                            igrac.brojFiguricaNaPolju -= 1
                                                            break
                                        if skip1:
                                            print('Nije moguc ni jedan validan potez u ovom krugu.')
                                            break
                                        print(f'Postavljena je figurica {trenutniIgrac.figurice.prvi.podatak} na start polje [{trenutniIgrac.start[0]}, {trenutniIgrac.start[1]}]')
                                        cooSys.append([trenutniIgrac.start[0], trenutniIgrac.start[1], trenutniIgrac.figurice.prvi.podatak])
                                        ukloniPrviElement(trenutniIgrac.figurice)
                                        trenutniIgrac.brojFiguricaNaPolju += 1
                                        trenutniIgrac.brojFigurica -= 1
                                        break
                                        
                                
                                skip2 = False
                                print('Izaberite koju figuricu zelite da pomerite: ')
                                opcijeFigurica = []
                                for j in cooSys:
                                    if trenutniIgrac.prefix == j[2][0]:
                                        print(f'Za figuricu {j[2]} pritisnite: {j[2][1]}')
                                        opcijeFigurica.append(int(j[2][1]))
                                izborFigurice = int(input())
                                if izborFigurice not in opcijeFigurica:
                                    print(f'Izaberite validnu opciju.')
                                    
                                else:
                                    izabranaFigurica = []
                                    for i in cooSys:
                                        if izborFigurice == int(i[2][1]) and trenutniIgrac.prefix == i[2][0]:
                                            izabranaFigurica = i[:]
                                            break
                                            
                                    x = izabranaFigurica[0]
                                    y = izabranaFigurica[1]
                                    temp = [x, y]
                                    
                                    if x == 1 and y != velicinaPolja - 1 and y != 0 and y != velicinaPolja - 2:
                                        for i in range(kocka):
                                            if temp[1] + 1 > 4:
                                                print('Ne mozete odigrati ovaj potez jer prelazite poslednje polje, odigrajte drugom figuricom, ako je moguce.')
                                                brojacPokusaja += 1
                                                skip2 = True
                                                break
                                            else:
                                                temp[1] += 1
                                        if skip2:
                                            continue
                                        
                                    elif y == velicinaPolja - 2 and x != 0 and x != velicinaPolja - 1 and x != velicinaPolja - 2:
                                        for i in range(kocka):
                                            if temp[0] + 1 > 4:
                                                print('Ne mozete odigrati ovaj potez jer prelazite poslednje polje, odigrajte drugom figuricom, ako je moguce.')
                                                brojacPokusaja += 1
                                                skip2 = True
                                                break
                                            else:
                                                temp[0] += 1
                                        if skip2:
                                            continue
                                    elif x == velicinaPolja - 2 and y != 0 and y != 1 and y != velicinaPolja - 1:
                                        for i in range(kocka):
                                            if temp[1] - 1 < velicinaPolja - 5:
                                                print('Ne mozete odigrati ovaj potez jer prelazite poslednje polje, odigrajte drugom figuricom, ako je moguce.')
                                                brojacPokusaja += 1
                                                skip2 = True
                                                break
                                            else:
                                                temp[1] -= 1
                                        if skip2:
                                            continue
                                    elif y == 1 and x != 0 and x != 1 and x != velicinaPolja - 1:
                                            for i in range(kocka):
                                                if temp[0] - 1 < velicinaPolja - 5:
                                                    print('Ne mozete odigrati ovaj potez jer prelazite poslednje polje, odigrajte drugom figuricom, ako je moguce.')
                                                    brojacPokusaja += 1
                                                    skip2 = True
                                                    break
                                                else:
                                                    temp[0] -= 1
                                            if skip2:
                                                continue
                                            
                                    if x == 0:
                                        for i in range(kocka):
                                            if temp[1] + 1 == velicinaPolja:
                                                temp[0] += 1
                                            elif temp == trenutniIgrac.cilj:
                                                if kocka - i > 4:
                                                    print('Ne mozete odigrati ovaj potez jer nema mesta u kucici, odigrajte drugom figuricom, ako je moguce.')
                                                    brojacPokusaja += 1
                                                    skip2 = True
                                                    break
                                                else:
                                                    temp[0] += 1
                                                    trenutniIgrac.UKucici += 1
                                            else:
                                                temp[1] += 1
                                                
                                        if skip2:
                                            continue
                                    
                                    elif y == velicinaPolja - 1:
                                        for i in range(kocka):
                                            if temp[0] + 1 == velicinaPolja:
                                                temp[1] -= 1
                                            elif temp == trenutniIgrac.cilj:
                                                if kocka - i > 4:
                                                    print('Ne mozete odigrati ovaj potez jer nema mesta u kucici, odigrajte drugom figuricom, ako je moguce.')
                                                    skip2 = True
                                                    brojacPokusaja += 1
                                                    break
                                                else:
                                                    temp[1] =- 1
                                                    trenutniIgrac.UKucici += 1
                                            else:
                                                temp[0] += 1
                                                
                                        if skip2:
                                            continue
                                    elif x == velicinaPolja - 1:
                                        for i in range(kocka):
                                            if temp[1] - 1 < 0:
                                                temp[0] -= 1
                                            elif temp == trenutniIgrac.cilj:
                                                if kocka - i > 4:
                                                    print('Ne mozete odigrati ovaj potez jer nema mesta u kucici, odigrajte drugom figuricom, ako je moguce.')
                                                    brojacPokusaja += 1
                                                    skip2 = True
                                                    break
                                                else:
                                                    temp[0] -= 1
                                                    trenutniIgrac.UKucici += 1
                                            else:
                                                temp[1] -= 1
                                        if skip2:
                                            continue
                                    
                                    elif y == 0:
                                        for i in range(kocka):
                                            if temp[0] - 1 < 0:
                                                temp[1] += 1
                                            elif temp == trenutniIgrac.cilj:
                                                if kocka - i > 4:
                                                    print('Ne mozete odigrati ovaj potez jer prelazite poslednje polje, odigrajte drugom figuricom, ako je moguce.')
                                                    brojacPokusaja += 1
                                                    skip2 = True
                                                    break
                                                else:
                                                    temp[1] += 1
                                                    trenutniIgrac.UKucici += 1
                                            else:
                                                temp[0] -= 1
                                        if skip2:
                                            continue
    
                                    
                                    
                                    for i in cooSys:
                                        if temp == [i[0],i[1]] and trenutniIgrac.prefix == i[2][0]:
                                            print('Na ovom polju vec imate figuricu izaberite drugu.')
                                            skip2 = True
                                            brojacPokusaja += 1
                                            break
                                        
                                        elif temp == [i[0],i[1]] and trenutniIgrac.prefix != i[2][0]:
                                            print(f'Pojeli ste figuricu: {i[2]} na polju [{temp[0]}, {temp[1]}]')
                                            for igrac in igraci:
                                                if igrac.prefix == i[2][0]:
                                                    igrac.brojFiguricaNaPolju -= 1
                                                    dodajNaKraj(igrac.figurice, ElementListe(i[2]))
                                                    cooSys.remove(i)
                                                    igrac.brojFigurica += 1
                                                    break
                                    if skip2:
                                        continue
                                        
                                    for i in cooSys:
                                        if izabranaFigurica[2] == i[2]:
                                            i[0] = temp[0]
                                            i[1] = temp[1]
                                            print(f'Pomerili ste figuricu {izabranaFigurica[2]} na polje: [{i[0]}, {i[1]}]')
                                            break
                                    break
                            except ValueError:
                                print('Niste uneli ceo broj. Probajte ponovo.')
                        brojac += 1
                        break
                            
                    if izbor == 2:
                        ispisPolja(cooSys, velicinaPolja)
                        break
                    
                    if izbor == 3:
                        while True:
                            imena = []
                            for i in igraci:
                                imena.append(i.ime)
                            print(f'Unesite ime igraca cije figurice zelite da pogledate: ({imena})')
                            imeIgracaUnos = input()
                            if imeIgracaUnos not in imena:
                                print('Nevalidan unos. Unesite ime igraca koji je trenutno u igri (Rec pocinje velikim slovom npr. Crveni)')
                            else:
                                for i in igraci:
                                    if i.ime == imeIgracaUnos:
                                        ispisPreostalihFigurica(i)
                                        break
                                break
                        break
                    if izbor == 4:
                        for i in range(brojIgraca):
                            ispisPreostalihFigurica(igraci[i])
                        break
                    if izbor == 5:
                        igraci.clear()
                        break
            except ValueError:
                print('Niste uneli ceo broj. Probajte ponovo.')
                
        
            
            
            
                
    
    
    
    
    
    
    
    
    
    
    