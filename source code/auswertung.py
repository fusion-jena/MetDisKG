from os import name
import pandas as pd

#read results of disambiguation
data_orcid = pd.read_csv('ergebnisorcid.csv', sep=',', engine='python')
data_ror = pd.read_csv('rorerg.csv', sep=',', engine='python')
data_publisher = pd.read_csv('dbtry.csv', sep=',', engine='python')

df_orcid_ids = pd.DataFrame(data_orcid, columns=['ORCID_ID'])
df_korrekt = pd.DataFrame(data_orcid, columns=['Ergebnis'])
df_ror_ids = pd.DataFrame(data_ror, columns=['ROR-ID'])
df_pub = pd.DataFrame(data_publisher, columns=['Publisher'])

#number of publishers
counter_for_pub = df_pub['Publisher'].value_counts().rename_axis('Publisher').reset_index(name='Anzahl')
anzahl_pub = len(counter_for_pub['Publisher'].values)
print(anzahl_pub)
#number of unique ORCID ids
counter_for_orcid = df_orcid_ids['ORCID_ID'].value_counts().rename_axis('ID').reset_index(name='Anzahl')
counter_for_orcid.to_csv(r'PATHWHEREFILESHALLBESTORED\counterorcidids.csv', sep=',', index=False, header=True)
anzahl_unique_ids = len(counter_for_orcid['ID'].values)

#number of unique ROR ids
anzahl_ror_ids = df_ror_ids['ROR-ID'].values
print(len(anzahl_ror_ids))
counter_for_ror = df_ror_ids['ROR-ID'].value_counts().rename_axis('ROR-ID').reset_index(name='Anzahl')
counter_for_ror.to_csv(r'PATHWHEREFILESHALLBESTORED\counterrorids.csv', sep=',', index=False, header=True)

#number of correct, uncertain ids and number of authors which have not been found
anzahl_autoren = len(data_orcid.index)
counter_ids = 0
counter_korrekt = 0 
counter_titelnichtgefunden = 0
counter_leer = 0
counter_komisch = 0
counter_noorcid = 0
for i in range(len(data_orcid)):
    if df_orcid_ids.values[i] == 'NO ORCID ID AVAILABLE':
        counter_noorcid += 1
        continue
    else:
        counter_ids += 1
    if df_korrekt.values[i] == 'Titel gefunden':
        counter_korrekt += 1
        continue
    else:
        if df_korrekt.values[i] == 'Titel nicht gefunden':
            counter_titelnichtgefunden += 1
            continue
        else:
            if df_korrekt.values[i] == 'leeres ORCID Profil':
                counter_leer += 1
                continue
            else:
                counter_komisch += 1

counter_leer = counter_komisch + counter_leer

data_ergebnisse = [{'Autoren': anzahl_autoren, 'IDs': counter_ids, 'korrekte IDs': counter_korrekt, 'unschlüssige IDs': counter_titelnichtgefunden, 'leere Profile': counter_leer, 'einzigartige IDs': anzahl_unique_ids, 'Keine ID gefunden': counter_noorcid}]
df_ergebnisse = pd.DataFrame(data_ergebnisse, index=['Anzahl'])
df_ergebnisse.to_csv(r'PATHWHEREFILESHALLBESTORED\ergebniszahlen.csv', sep=',', index=False, header=True)
