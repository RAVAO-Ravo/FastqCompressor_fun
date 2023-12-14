# FastqCompressor_fun

``FastqCompressor`` est un outil simple permettant de compresser un fichier ``FASTQ`` en plusieurs fichiers au format ``'.gz'`` (qui seront contenus dans un dossier), ou de décompresser un ensemble de fichiers ``FASTQ`` (contenu dans un dossier au format ``'.gz'``) en un fichier unique.

## Installation

Ce projet nécessite `Python3`, et peut être récupérer via la commande :

```bash
git clone https://github.com/RAVAO-Ravo/FastqCompressor_fun.git
```

## Utilisation

Le script s'utilise de la façon suivante :

```bash
python3 FastqCompressor.py -i <path> -c -n <int> -r
```

- `-i`, `--input` : Chemin vers l'élément à traiter.
- `-c`, `--compression` : Activer la compression des fichiers (par défaut = True).
- `-n`, `--rbf` : Nombre de reads par fichier lors de la compression (par défaut = 100).
- `-r`, `--remove` : Supprimer le fichier/dossier d'origine après la compression/décompression (par défaut = True).

### Exemples d'utilisation

Compression :

```bash
python3 FastqCompressor.py -i <file.fastq> -c -n 100 -r
```

Décompression :

```bash
python3 FastqCompressor.py -i <directory> -r
```

## Licence

Ce projet est sous licence [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

Vous êtes libre de :

- **Partager** : copier et redistribuer le matériel sous n'importe quel format ou médium.
- **Adapter** : remixer, transformer et construire à partir du matériel.

Selon les conditions suivantes :

- **Attribution** : Vous devez donner le crédit approprié, fournir un lien vers la licence et indiquer si des modifications ont été faites. Vous devez le faire d'une manière raisonnable, mais d'une manière qui n'implique pas que l'auteur vous approuve ou approuve votre utilisation du matériel.
- **ShareAlike** : Si vous remixez, transformez ou construisez à partir du matériel, vous devez distribuer vos contributions sous la même licence que l'original.

Veuillez consulter le fichier [LICENSE](LICENSE) pour plus de détails.
