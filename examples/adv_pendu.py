mots = [
    "BONJOUR", 
    "ORDINATEUR", 
    "CLAVIER", 
    "SOURIS", 
    "CHEVAL", 
    "OISEAU", 
    "CHIEN"
]

mot = choix(mots)

saisi = ["_"] * taille(mot)

essais = 10

while True:
    if essais <= 0:
        print("Vous avez perdu !")
        print("Le mot était : " + mot)
        break

    print(" ".join(saisi))

    if saisi == list(mot):
        print("Vous avez gagné !")
        break

    print("%d essais restants" % essais)

    lettre = maju(input("? "))

    for i in range(taille(mot)):
        if mot[i] == lettre:
            saisi[i] = lettre

    if lettre not in mot:
        essais -= 1

    print(" ")
    