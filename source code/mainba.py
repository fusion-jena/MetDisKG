from os import sep
import pandas as pd
import requests
import pyorcid
from nameparser import HumanName
import logging
import time
import json
from _collections_abc import Iterable

#LogFile to control the correct processing of the ORCID API
logging.basicConfig(filename="logfileORCIDAPI.log", level=logging.INFO)

#AUTHORNAMEDISAMBIGUATION

#read inputdatabase
data1 = pd.read_csv('TRYDB1-50.csv', sep=',', engine='python')
data2 = pd.read_csv('TRYDB51-100.csv', sep=',', engine='python')

df1 = pd.DataFrame(data1, columns=['Authors','Title'])
df2 = pd.DataFrame(data2, columns=['Authors','Title'])
list_aut_tit = []

#function to generate dataframe of only authornames and corresponding titles
def get_auttitle(dataframe):
    for i in range(len(dataframe.index)):
        x = dataframe.values[i][0]
        y = x.split("; ")
        for j in y:
            if not j:
                break
            else:
                list_aut_tit.append((j,dataframe.values[i][1]))

get_auttitle(df1)
get_auttitle(df2)

df_auttit = pd.DataFrame(list_aut_tit)
df_auttit.columns = ['Autor','Titel']
df_auttit.to_csv(r'C:\Users\talmu\Desktop\Bachelorarbeit Florjan\Python Code\Bachelorarbeit\auttitle.csv', index=False, header=True)


#check the inputdatabase in ORCID

#read author-title dataframe
fileextaut = pd.read_csv('auttitle.csv', sep=',', engine='python')

df_autoren = pd.DataFrame(fileextaut, columns= ['Autor'])
df_titel = pd.DataFrame(fileextaut, columns= ['Titel'])

daten_autoren_array = df_autoren['Autor'].values

#generate a list of alle names, surnames and middlenames
list_vornamen = []
list_middle = []
list_nachnamen = []

for name in daten_autoren_array:
    namen= HumanName(name)
    if not namen.middle:
        list_vornamen.append(namen.first)
        list_nachnamen.append(namen.last)
    else:
        list_vornamen.append(namen.first+' '+namen.middle)
        list_nachnamen.append(namen.last)

#transform lists into iterlists for further processing
iterlist_nachnamen = iter(list_nachnamen)
iterlist_vornamen = iter(list_vornamen)


#initialise a list for the found ORCID-IDs and a constant for authors with no ORCID-ID
orcid_id_list = []
no_orcid = 'NO ORCID ID AVAILABLE'

#initialise counter for exit condition
counter = len(list_vornamen)

#initialise a list for author with a false ORCID-profile to disambiguate via features
feature_comparison_list = []

#function to search for an ORCID-profile with the names of the authors
def search_orcidid(vornamen, nachnamen):
#loop to search for ORCID-profiles with name and surname via the pyorcid api
    for i in range(counter):
        vorname = next(vornamen)
        nachname = next(nachnamen)
        try:
            author = pyorcid.search(f'family-name:{nachname}+AND+given-names:{vorname}')
            orcid_id = next(author).orcid
            orcid_id_list.append(orcid_id)
        except StopIteration as ex:
            orcid_id_list.append(no_orcid)

search_orcidid(iterlist_vornamen, iterlist_nachnamen)

#spilt list of surnames in 4 parts
hälfte1nachnamen = list_nachnamen[:len(list_nachnamen)//2]
hälfte2nachnamen = list_nachnamen[len(list_nachnamen)//2:]

teil1nachnamen = hälfte1nachnamen[:len(hälfte1nachnamen)//2]
teil2nachnamen = hälfte1nachnamen[len(hälfte1nachnamen)//2:]
teil3nachnamen = hälfte2nachnamen[:len(hälfte2nachnamen)//2]
teil4nachnamen = hälfte2nachnamen[len(hälfte2nachnamen)//2:]

#split list of names in 4 parts
hälfte1vornamen = list_vornamen[:len(list_vornamen)//2]
hälfte2vornamen = list_vornamen[len(list_vornamen)//2:]

teil1vornamen = hälfte1vornamen[:len(hälfte1vornamen)//2]
teil2vornamen = hälfte1vornamen[len(hälfte1vornamen)//2:]
teil3vornamen = hälfte2vornamen[:len(hälfte2vornamen)//2]
teil4vornamen = hälfte2vornamen[len(hälfte2vornamen)//2:]

#split list of ORCID-IDs in 4 parts
orcid_ids_hälfte1 = orcid_id_list[:len(orcid_id_list)//2]
orcid_ids_hälfte2 = orcid_id_list[len(orcid_id_list)//2:]

orcid_ids_1 = orcid_ids_hälfte1[:len(orcid_ids_hälfte1)//2]
orcid_ids_2 = orcid_ids_hälfte1[len(orcid_ids_hälfte1)//2:]
orcid_ids_3 = orcid_ids_hälfte2[:len(orcid_ids_hälfte2)//2]
orcid_ids_4 = orcid_ids_hälfte2[len(orcid_ids_hälfte2)//2:]

#extract list with all titles
titel_array = df_titel['Titel'].values

#split list of titles in 4 parts
titel_array_hälfte1 = titel_array[:len(titel_array)//2]
titel_array_hälfte2 = titel_array[len(titel_array)//2:]

titel_array1 = titel_array_hälfte1[:len(titel_array_hälfte1)//2]
titel_array2 = titel_array_hälfte1[len(titel_array_hälfte1)//2:]
titel_array3 = titel_array_hälfte2[:len(titel_array_hälfte2)//2]
titel_array4 = titel_array_hälfte2[len(titel_array_hälfte2)//2:]

#counter for all lists for later exit condition
counter_title1 = len(orcid_ids_1)
counter_title2 = len(orcid_ids_2)
counter_title3 = len(orcid_ids_3)
counter_title4 = len(orcid_ids_4)

#initialise a list for the results
ergebnis_liste = []

#function to check for each found profile if its correct
def confirm_orcid(counter, orcididliste, titelarray, nachnamenlist, vornamenlist):
    for j in range(counter):
        if not orcididliste[j] == no_orcid:
            orcid_autor_id = orcididliste[j]
            orcid_res = pyorcid.get(orcid_autor_id)
            logging.info(orcid_res)
            orcid_titel = orcid_res.publications
            counter_pub = len(orcid_titel)
            logging.info(counter_pub)
            if counter_pub == 0:
                ergebnis_liste.append((nachnamenlist[j], vornamenlist[j], orcid_autor_id, titelarray[j], 'leeres ORCID Profil'))
            else:
                for i in range(len(orcid_titel)):
                    title = orcid_titel[i].title
                    title_autor = titelarray[j]
                    if title == title_autor:
                        ergebnis_liste.append((nachnamenlist[j],vornamenlist[j],orcid_autor_id,title_autor,'Titel gefunden'))
                        break
                    if counter_pub <= 1:
                        ergebnis_liste.append((nachnamenlist[j],vornamenlist[j],orcid_autor_id,title_autor,'Titel nicht gefunden'))
                    counter_pub -= 1
        else:
            ergebnis_liste.append((nachnamenlist[j],vornamenlist[j],orcid_id_list[j],titelarray[j],'/'))
            feature_comparison_list.append((nachnamenlist[j],vornamenlist[j],titelarray[j]))

#check the first part of the data
confirm_orcid(counter_title1, orcid_ids_1, titel_array1, teil1nachnamen, teil1vornamen)
erg_extaut1 = pd.DataFrame(ergebnis_liste)
erg_extaut1.columns = ['Nachname', 'Vorname', 'ORCID_ID', 'Titel','Ergebnis']
erg_extaut1.to_csv(r'C:\Users\talmu\Desktop\Bachelorarbeit Florjan\Python Code\Bachelorarbeit\ergebnisorcid1.csv', index=False, header=True)
time.sleep(60)

#check the second part of the data
confirm_orcid(counter_title2, orcid_ids_2, titel_array2, teil2nachnamen, teil2vornamen)
erg_extaut2 = pd.DataFrame(ergebnis_liste)
erg_extaut2.columns = ['Nachname', 'Vorname', 'ORCID_ID', 'Titel','Ergebnis']
erg_extaut2.to_csv(r'C:\Users\talmu\Desktop\Bachelorarbeit Florjan\Python Code\Bachelorarbeit\ergebnisorcid2.csv', index=False, header=True)
time.sleep(60)

#check the thrid part of the data
confirm_orcid(counter_title3, orcid_ids_3, titel_array3, teil3nachnamen, teil3vornamen)
erg_extaut3 = pd.DataFrame(ergebnis_liste)
erg_extaut3.columns = ['Nachname', 'Vorname', 'ORCID_ID', 'Titel','Ergebnis']
erg_extaut3.to_csv(r'C:\Users\talmu\Desktop\Bachelorarbeit Florjan\Python Code\Bachelorarbeit\ergebnisorcid3.csv', index=False, header=True)
#time.sleep(60)

#check the fourth part of the data (did not work probably timeouterror)
#confirm_orcid(counter_title4, orcid_ids_4, titel_array4, teil4nachnamen, teil4vornamen)
#erg_extaut4 = pd.DataFrame(ergebnis_liste)
#erg_extaut4.columns = ['Nachname', 'Vorname', 'ORCID_ID', 'Titel','Ergebnis']
#erg_extaut4.to_csv(r'C:\Users\talmu\Desktop\Bachelorarbeit Florjan\Python Code\Bachelorarbeit\ergebnisorcid4.csv', index=False, header=True)

#generate a csv file with the results
erg_extaut = pd.DataFrame(ergebnis_liste)
erg_extaut.columns = ['Nachname', 'Vorname', 'ORCID_ID', 'Titel','Ergebnis']
erg_extaut.to_csv(r'C:\Users\talmu\Desktop\Bachelorarbeit Florjan\Python Code\Bachelorarbeit\ergebnisorcid.csv', index=False, header=True)

#disambiguate authors via their features

#TBD disambiguation not possible because of missing features

#INSTITUTIONSNAMEDISAMBIGUATION
#disambiguate institutions via their features

#TBD disambiguation not possible because of missing features

#disambiguation of institutionnames via external resource

#access the ror datadump 
with open("ror-data-2021-04-06.json") as ror_file:
    data = json.load(ror_file)

#get all found ORCID-IDs
data_inst = pd.read_csv('ergebnisorcid.csv', sep=',', engine='python')
df_inst = pd.DataFrame(data_inst)
gef_ids = df_inst['ORCID_ID'].values

#search for every ORCID-profile if an affiliation is available
institutionen = []
for id in gef_ids:
    orcid_profil = pyorcid.get(id[0])
    inst = orcid_profil.affiliations
    institutionen.append(inst)

#flatten the list of found institutions
gef_institutionen = []
for i in range(len(institutionen)):
    if not institutionen[i]:
        pass
    else:
        gef_institutionen.append(institutionen[i])

def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item

gef_inst = list(flatten(gef_institutionen))

#initialise a list for all found institutionnames
gefunden = []

#search in ror datadump for all found institutionnames if found extract the ROR-ID
for k in range(len(gef_inst)):
    for l in range(len(data)):
        for element in data[l]:
            name = data[l]['name']
            alias = data[l]['aliases']
            acronym = data[l]['acronyms']
            label = data[l]['labels']['label']
            if (gef_inst[k] == name) or (gef_inst[k] in alias) or (gef_inst[k] in acronym) or (gef_inst[k] in label):
                gefunden.append((gef_inst[k], data[l]['id']))
                break
            else:
                pass

#generate a csv file for the results
df_inst_erg = pd.DataFrame(gefunden)   
df_inst_erg.columns = ['Institut','ROR-ID']
df_inst_erg.to_csv(r'C:\Users\talmu\Desktop\Bachelorarbeit Florjan\Python Code\Bachelorarbeit\rorerg.csv', index=False, header=True)