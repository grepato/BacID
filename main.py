#BAKTERITE ID-TARKVARA

    # Programmi jooksutamiseks oma arvutis tuleb installida
    # bacdive package: Tools -> Manage packages.. -> otsi "bacdive"
    # -> install -> taaskäivita Thonny
    
    #Katsetamiseks olen kasutanud liiginimesid Acetivibrio cellulolyticus, Bacteroides caccae 

import bacdive

# Bacdive API päringute töötlemine
class Bakter:
    def __init__(self, bacdive_liik):
        self.lühikirjeldus = bacdive_liik['General']['description'] \
                             if 'description' in bacdive_liik['General'] \
                             else ""
        self.taksonoomia = self.taksonoomia(bacdive_liik) \
                           if 'Name and taxonomic classification' in bacdive_liik \
                           else ""
        self.teaduslik_nimetus = bacdive_liik['Name and taxonomic classification']['full scientific name'] \
                                 if 'full scientific name' in bacdive_liik['Name and taxonomic classification'] \
                                 else bacdive_liik['Name and taxonomic classification']['LPSN']['full scientific name'].replace(
                                     '<I>', '').replace('</I>', '')
        self.sünonüümid = self.sünonüümid(bacdive_liik) \
                          if 'synonyms' in bacdive_liik['Name and taxonomic classification']['LPSN'] \
                          else ""
        # siit edasi ei ole konstruktorid korralikult tehtud veel
        #self.morfoloogia = bacdive_liik['Morphology'] if bool(self.sünonüümid(bacdive_liik)) is not None else ""
        #self.kasvutingimused = bacdive_liik['Culture and growth conditions'] if bool(self.sünonüümid(bacdive_liik)) is not None else ""
        #self.füsioloogia = bacdive_liik['Physiology and metabolism'] if bool(self.sünonüümid(bacdive_liik)) is not None else ""
        #self.muu_info = bacdive_liik['Isolation, sampling and environmental information'] if bool(self.sünonüümid(bacdive_liik)) is not None else ""
        
    def taksonoomia(self, bacdive_liik):
        bacdive_nimi = bacdive_liik['Name and taxonomic classification']
        return bacdive_nimi['domain'] + ' - ' + bacdive_nimi['phylum'] + ' - ' + \
               bacdive_nimi['class'] + ' - ' + bacdive_nimi['order'] + ' - ' + \
               bacdive_nimi['family'] + ' - ' + bacdive_nimi['genus'] + ' - ' + \
               bacdive_nimi['species']
                
    def sünonüümid(self, bacdive_liik):
        sünonüümid = ""
        bacdive_sünonüümid = bacdive_liik['Name and taxonomic classification']['LPSN']['synonyms']
        for sünonüüm in bacdive_sünonüümid:
            sünonüümid += sünonüüm['synonym'] + ', '
        return sünonüümid[:-2]
    
    def __str__(self):
        return f"{self.teaduslik_nimetus}. lühikirjeldus: {self.lühikirjeldus}"

# Andmebaasiga autentimine
client = bacdive.BacdiveClient('grete.paat@gmail.com', 'LBWLWeEjzD6y9!f')

# UI
print("Tere tulemast!")
print("Kasutad tarkvara, mis võimaldab bakterite identifitseerimist") # otsingusõnad tuleb sisestada inglise keeles
print("Täida küsimuste väljad (kui tead) ja me anname sulle vasted")  # vb peaks terve programmi tegema ingliskeelseks
liiginimi = input("Sisesta liiginimi: ")
märksõnad = input("Sisesta muid uuritava organismiga seotud märksõnu (eralda komaga): ").split(", ") # seda infot programm hetkel ei kasuta   

vastete_nr = client.search(taxonomy = liiginimi)
otsinguvasted = []

for vaste in client.retrieve():
    print(vaste)
    otsinguvasted.append(Bakter(vaste))
    
print()
print("Leitud " + str(vastete_nr) + " vastet:")
print()
for i in range(vastete_nr):
    print(str(i+1) + ".", otsinguvasted[i])
    print()

