#BAKTERITE ID-TARKVARA

    # Programmi jooksutamiseks oma arvutis tuleb installida
    # bacdive package: Tools -> Manage packages.. -> otsi "bacdive"
    # bacdive package: Tools -> Manage packages.. -> otsi "customtkinter"
    # -> install -> taaskäivita Thonny
    
    #Katsetamiseks olen kasutanud liiginimesid Acetivibrio cellulolyticus, Bacteroides caccae 

import bacdive
import tkinter as tk
import customtkinter as ct

ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")

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
    
    
    
    
## UI algus 
    
class CheckboxFrame(ct.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []
        
        self.title = ct.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=5)
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")
        
        for i, value in enumerate(self.values):
            checkbox = ct.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
            self.checkboxes.append(checkbox)
        
    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class ResultsFrame(ct.CTkScrollableFrame):
    def __init__(self, master, values=None):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values

class BakterUI(ct.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Bakterite ID-Tarkvara")
        self.geometry("800x600")
        # self.iconbitmap('Images/bacteria.ico') #Võib mingi ilusa pildi panna! 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frame = ct.CTkFrame(self)
        self.frame.grid(padx = 40, pady=20, sticky="nsew")
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        # Praegu disabled, kuna marksõnade otsing ei tööta.
        # self.checkbox_frame = CheckboxFrame(self.frame, "Otsingute valikud:", values=["Märksõnad"])
        # self.checkbox_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew", columnspan=1)
        
        self.liiginimi_label = ct.CTkLabel(self.frame, text="Sisesta liiginimi:",fg_color="gray30", corner_radius=5, font=("Roboto", 16))
        self.liiginimi_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew",columnspan=2)
        
        self.liiginimi_entry = ct.CTkEntry(self.frame, font=("Roboto", 14))
        self.liiginimi_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        
        self.guesser_label = ct.CTkLabel(self.frame, text="Võimalikud liigid",fg_color="gray30", corner_radius=5, font=("Roboto", 16))
        self.guesser_label.grid(row=0, column=2, padx=10, pady=10, sticky="ew", columnspan=1)
        
        self.guesser_list = tk.Listbox(self.frame, width=50, font=("Roboto", 14))
        self.guesser_list.grid(row=1, column=2, padx=10, pady=10, sticky="nsew", columnspan=1, rowspan=2)
        self.update_guesser(liiginimed)
        self.guesser_list.bind("<<ListboxSelect>>", self.fillout)
        self.liiginimi_entry.bind("<KeyRelease>", self.check)
        
       # self.label2 = ct.CTkLabel(self, text="Sisesta märksõnad (eralda komaga):")
       # self.label2.grid(padx=10, pady=10)
       # self.marksonad_entry = ct.CTkEntry(self)
       # self.marksonad_entry.grid(padx=10, pady=10)
       # self.test_button = ct.CTkButton(self, text="test", command=self.button_callback)
       # self.test_button.grid(row=4, column=1, padx=10, pady=12, columnspan=2)

        self.search_button = ct.CTkButton(self.frame, text="Otsi", command=self.perform_search, font=("Roboto", 16))
        self.search_button.grid(row=2, column=0, padx=10, sticky="ew", pady=12)
    
        self.results_frame = ResultsFrame(self.frame)
        
        self.result_text = ct.CTkTextbox(self.frame)
        self.result_text.grid(row=3, column=0, padx=10, pady=12, sticky="nsew", columnspan=3, rowspan=4)

    # def button_callback(self):
    #     print("Checked checkboxes:", self.checkbox_frame.get())

        
    def perform_search(self):
        liiginimi = self.liiginimi_entry.get()
#         marksonad = self.marksonad_entry.get().split(", ")
        otsinguvasted = []
        
        vastete_nr = client.search(taxonomy = liiginimi)
        
        for vaste in client.retrieve():
            otsinguvasted.append(Bakter(vaste))
        
        result_text = f"Leitud {vastete_nr} vastet:\n\n"
        
        for i, vaste in enumerate(otsinguvasted, start=1):
            result_text += f"{i}. {vaste}\n\n"
        
        self.result_text.delete(1.0, "end")
        self.result_text.insert("end", result_text)
        
        self.results_frame.update_values(otsinguvasted)


    # Uuenda guesser listi, mis aitab pakkuda liigi nimesid
    def update_guesser(self, data):
        self.guesser_list.delete(0, tk.END)
        
        for item in data:
            self.guesser_list.insert(tk.END, item)
            
            
    # Kontrollib kas meie liiginimede guesseris on meie entry (ehk search area)
    def check(self, event):
        typed = self.liiginimi_entry.get()
        
        if typed == '':
            data = liiginimed
        else:
            data = []
            for item in liiginimed:
                if typed.lower() in item.lower():
                    data.append(item)
                    
        # Muudame liiginimede guesserit, et võimalikud vastused oleksid need milles on meie sisestatud tähed
        self.update_guesser(data)            
            
    
    # Uuenda search entry boxi guesser listile klikates
    def fillout(self, event):
        self.liiginimi_entry.delete(0, tk.END)
        self.liiginimi_entry.insert(0, self.guesser_list.get(tk.ACTIVE))
            
            
            
            
# Andmebaasiga autentimine
client = bacdive.BacdiveClient('martinhehexd@gmail.com', 'tfx-rkr7BUC9cdw!txb')

# Placeholder võimalikud liigid helper list, praegu pole kindel kuidas arendada seda.
liiginimed = ["Acetivibrio cellulolyticus", "Bacteroides caccae"]

# UI
print("Tere tulemast!")
print("Kasutad tarkvara, mis võimaldab bakterite identifitseerimist") # otsingusõnad tuleb sisestada inglise keeles
print("Täida küsimuste väljad (kui tead) ja me anname sulle vasted")  # vb peaks terve programmi tegema ingliskeelseks

ui = input("Kas soovid proovida BETA GUI'd? (y/n): ")
if ui == "y":
    print("UI peaks nüüd ilmuma! (Võib olla minimized)")
    bakter_ui = BakterUI()
    bakter_ui.mainloop()

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


## Martin: Alguses plaanisin õppida ja kasutada React + Bootstrapi, researchisin seda suht korralikult aga ei suutnud välja mõelda kuidas kasutada BacDive backendi, ja tundus, et asi on minu võimekusest väljas 