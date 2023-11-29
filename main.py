#BAKTERITE ID-TARKVARA

    #Programmi jooksutamiseks oma arvutis tuleb installida
    #bacdive package: Tools -> Manage packages.. -> otsi "bacdive"
    # -> install -> taaskäivita Thonny

import bacdive

client = bacdive.BacdiveClient('grete.paat@gmail.com', 'LBWLWeEjzD6y9!f')

print("Tere tulemast!")
print("Kasutad tarkvara, mis võimaldab bakterite identifitseerimist")
print("Täida küsimuste väljad (kui tead) ja me anname sulle vasted")
liiginimi = input("Sisesta liiginimi: ")
märksõnad = input("Sisesta muid uuritava organismiga seotud märksõnu (eralda komaga): ").split(", ")    

vastus = client.search(taxonomy = liiginimi)
print("Leitud " + str(vastus) + " vastet.")

