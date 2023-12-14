#!/bin/python3
#-*- coding:utf-8 -*-

# Importation des modules
import os
import gzip
import subprocess as sp
from argparse import ArgumentParser, MetavarTypeHelpFormatter
from pathlib import Path
from typing import List, Tuple

# Description du programme
DESCRIPTION: str = "Compresse des fichiers FASTQ en un dossier contenant plusieurs fichiers, ou décompresse un dossier contenant des FASTQ compressés en '.gz'."

# Formatteur de l'aide
FORMARTTER_CLASS: callable = lambda prog : MetavarTypeHelpFormatter(prog=prog, max_help_position=100, width=500)

def read_fastq(filename: str) -> List[Tuple[str, str, str]]:
    """
    Lit un fichier FASTQ et retourne une liste de tuples contenant l'ID, la séquence, et la qualité de chaque read.

    Parameters:
    - filename (str): Le chemin du fichier FASTQ.

    Returns:
    List[Tuple[str, str, str]]: Liste de tuples représentant chaque read (ID, séquence, qualité).
    """
    # Ouvre le fichier FASTQ en mode lecture
    with open(filename, mode="r") as reader:
        # Lit toutes les lignes du fichier
        lines = reader.readlines()

        # Utilise une liste en compréhension pour créer des tuples (ID, séquence, qualité)
        reads = [(lines[i].strip(), lines[i + 1].strip(), lines[i + 3].strip()) for i in range(0, len(lines), 4)]

    return reads

def splitter(reads: List[Tuple[str, str, str]], reads_by_file: int) -> List[List[Tuple[str, str, str]]]:
    """
    Divise une liste de reads en sous-listes, chacune contenant un nombre spécifié de reads.

    Parameters:
    - reads (List[Tuple[str, str, str]]): Liste de tuples représentant chaque read (ID, séquence, qualité).
    - reads_by_file (int, optional): Nombre de reads par sous-liste.

    Returns:
    List[List[Tuple[str, str, str]]]: Liste de sous-listes, chacune contenant le nombre spécifié de reads.
    """
    # Utilise une liste en compréhension pour créer des sous-listes de reads
    return [reads[i:i + reads_by_file:1] for i in range(0, len(reads), reads_by_file)]

def compress(filename: str, dirname: str, reads_by_file: int, suppress: bool) -> None:
    """
    Lit un fichier FASTQ, divise les reads en partitions, et les comprime dans des fichiers .gz.

    Parameters:
    - filename (str): Chemin du fichier FASTQ à compresser.
    - dirname (str): Nom du dossier dans lequel sauvegarder les fichiers compressés.
    - reads_by_file (int): Nombre de reads par fichier compressé.
    - suppress (bool): Si True, supprime le fichier FASTQ original après la compression.

    Returns:
    None
    """
    # Lecture des reads à partir du fichier FASTQ
    reads = read_fastq(filename=filename)

    # Division des reads en partitions
    partitions = splitter(reads=reads, reads_by_file=reads_by_file)

    # Création du dossier de sauvegarde
    dir_path = Path(dirname)
    if dir_path.exists():
        # Suppression du dossier existant s'il existe
        sp.run(args=[f"rm -r {dirname}"], shell=True)
    dir_path.mkdir(parents=True, exist_ok=True)

    # Création des noms de fichiers pour les partitions compressées
    filenames = [
        os.path.join(
            dirname,
            (f"{dirname}_0{i+1}.gz" if i < 9 else f"{dirname}_{i+1}.gz")
        )
        for i in range(len(partitions))
    ]

    # Compression des données dans les fichiers .gz
    for i, file_name in enumerate(iterable=filenames, start=0):
        with gzip.open(filename=file_name, mode="wt") as writer:
            for id_, sequence, quality in partitions[i]:
                writer.write(f"{id_}\n{sequence}\n+\n{quality}\n")

    # Suppression du fichier FASTQ original si l'option est activée
    if suppress:
        sp.run(args=[f"rm {filename}"], shell=True)

def decompress(dirname: str, suppress: bool) -> None:
    """
    Décompresse les fichiers .gz dans un dossier et reconstitue un fichier FASTQ.

    Parameters:
    - dirname (str): Nom du dossier contenant les fichiers .gz à décompresser.
    - suppress (bool): Si True, supprime le dossier après la décompression.

    Returns:
    None
    """
    # Création du fichier FASTQ de sortie
    with open(file=f"{dirname}.fastq", mode="wt") as writer:
        # Parcours de tous les fichiers .gz dans le dossier
        for filename in os.listdir(path=dirname):
            path_file = os.path.join(dirname, filename)
            
            # Ouverture du fichier .gz en mode lecture binaire
            with gzip.open(filename=path_file, mode="rb") as reader:
                # Lecture de chaque ligne dans le fichier .gz et écriture dans le fichier FASTQ
                for line in reader.readlines():
                    writer.write(line.decode(encoding="utf-8"))

    # Suppression du dossier si l'option est activée
    if suppress:
        sp.run(args=[f"rm -r {dirname}"], shell=True)


if __name__ == "__main__":
    # Récupérer les arguments passés en paramètre
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=FORMARTTER_CLASS)
    parser.add_argument("-i", "--input", type=str, help="Chemin de l'élément à traiter.")
    parser.add_argument("-c", "--compression", action="store_true", help="Active la compression des fichiers. (défaut = True)")
    parser.add_argument("-n", "--rbf", type=int, default=100, help="Nombre de reads par fichier lors de la compression. (défaut = 100)")
    parser.add_argument("-r", "--remove", action="store_true", help="Supprime le fichier d'origine après la compression/décompression. (défaut = True)")
    args = parser.parse_args()

    # Récuprérer le flag pour la compression
    COMPRESSION: bool = args.compression

    # Appliquer en fonction du flag de compression
    if COMPRESSION ==  True:
        FILENAME: str = args.input
        DIRNAME: str = FILENAME.split(sep='.')[0]
        READS_BY_FILE: int = args.rbf
        SUPPRESS: bool = args.remove
        compress(filename=FILENAME, dirname=DIRNAME, reads_by_file=READS_BY_FILE, suppress=SUPPRESS)
    else:
        DIRNAME: str = args.input
        SUPPRESS: bool = args.remove
        decompress(dirname=DIRNAME, suppress=SUPPRESS)