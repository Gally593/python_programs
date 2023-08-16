import os
from fit2gpx import Converter

# Définition du répertoire d'entrée contenant les fichiers .fit
dir_in = r"files paths"

# Définition du répertoire de sortie pour les fichiers .gpx convertis
dir_out = r"files paths"

# Création de l'instance de Converter
converter = Converter(status_msg=True)

# Conversion des fichiers .fit en .gpx dans le répertoire de sortie
converter.fit_to_gpx_bulk(dir_in=dir_in, dir_out=dir_out)

# Affichage d'un message de confirmation
print("La conversion des fichiers .fit en .gpx est terminée.")
