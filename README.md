#Installation
- python -m spacy download en_core_web_trf
- export NLTK_DATA=/home/stud/abedinz1/localDisk/opinionconv-refactor
- export IPYTHONDIR=/home/stud/abedinz1/localDisk/opinionconv-refactor/.ipython
- python -m nltk.downloader stopwords
- python MAIN.py
- python -W ignore MAIN.py
- pip3 install torch torchvision torchaudio
- When using bender if you want to update the python version
    a) Do module spider python
    b) module load python.xx
    c) if you have a shell file for job running, add module load python.xx in the shell file also
