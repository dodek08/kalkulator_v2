
# -*- coding: UTF-8 -*-

import random

def imie():
	names =['Jan','Stanisław','Andrzej','Józef','Tadeusz','Jerzy','Zbigniew','Krzysztof',
	'Henryk','Ryszard','Kazimierz','Marek','Marian','Piotr','Janusz','Władysław','Adam','Wiesław',
	'Zdzisław','Edward','Antoni','Mieczysław','Maria','Krystyna','Anna','Barbara','Teresa','Teresa','Teresa',
	'Elżbieta','Janina','Karolina','Zofia','Jadwiga','Danuta','Halina','Irena','Ewa','Małgorzata','Helena','Grażyna','Bożena',
	'Stanisława','Jolanta','Marianna','Cudka','Egle','Aldona','Helena','Bolko','Niemierza',
	'Pełka','Kunegunda','Kiejstut','Gabija','Marcin','Giedymin']
	index = random.randint(0,len(names)-1)
	return(names[index])


def nazwisko():
	nazwiska = ['Wójcik','Kowalczyk','Małysz','Kubica',
	'Stoch','Hula','Żyła','Woźniak','Mazur','Krawczyk','Kaczmarek','Wąs',
	'Jajko','Wąż','Dzban','Charcik','Z Gołczy','Król','Kuchwas','Grot','Kubala',
	'Piróg','Krupa','Stańczyk','Mrzygłód','Biłko','Bysiak','Sienkiewicz',
	'Prus','Gombrowicz','Łysiak','Stasiak','Paździoch','Boczek','Giertych','Hall',
	'Kluzik','Samsonowicz','Szumilas','Łuczak','Legutko','Wiatr','Emilewicz',
	'Gowin','Boni','Eysmont','Rokita','Miller','Ziegler','Majer','Piłat','Strąk',
	'Walędziak','Wasserman','Bauc','Belka','Chmielak','Kluza','Kołodko','Raczko',
	'Szczurek','Kopacz','Kosiniak','Kamysz','Pawlak','Opala','Religa','Wojtyła',
	'Sidorowicz','Zembala','Jarubas','Adamiak','Adamczuk','Antczak','Anioł','Diabeł',
	'Tracz','Antoniszyn','Antosiak','Babul','Bajda','Baszko','Błaszczyk','Borek',
	'Gnat','Głowa','Oko','Opania','Duda','Żemajtis']
	index = random.randint(0,len(nazwiska)-1)
	return(nazwiska[index])

def klucz():
	return random.randint(1,200000)

def pesel():
	rok = random.randint(0,99)
	miesiac = random.randint(1,12)
	dzien = random.randint(0,31)
	zz = "00"
	l1 = random.randint(0,9)
	k_m = random.randint(0,1)
	l2 = random.randint(0,9)
	return str(rok)+str(miesiac)+str(dzien)+zz+str(l1)+str(k_m)+str(l2)


