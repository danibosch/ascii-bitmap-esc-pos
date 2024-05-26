# ascii-bitmap-esc-pos
Impresión de imágenes Ascii y bitmap usando comandos ESC/POS.


## Modelos soportados/testeados

- Epson TM-300A


## Requerimientos

- Python 3.10, 3.12 (no testeado aún en otras versiones)


## Instalación

### Hardware
1. Conectar la tickeadora o impresora según modelo (ver manuales en `docs/`) a la pc y a la fuente de alimentación.


### Software

#### Linux
1. Instalar entorno virtual e instalar los paquetes
1.1. Con virtualenv (dentro del directorio del proyecto)

```bash
$ cd ascii-bitmap-esc-pos
ascii-bitmap-esc-pos$ virtualenv venv
ascii-bitmap-esc-pos$ source venv/bin/activate
(venv) ascii-bitmap-esc-pos$ pip install -r requirements.txt
```

1.2. Con conda (o miniconda)

```bash
$ cd ascii-bitmap-esc-pos
ascii-bitmap-esc-pos$ conda create --name venv
ascii-bitmap-esc-pos$ conda activate venv
(venv) ascii-bitmap-esc-pos$ conda install -c conda-forge --yes --file requirements.txt
```
o
```bash
(venv) ascii-bitmap-esc-pos$ pip install -r requirements.txt
``` 

2. Ejecutar
```bash
(venv) ascii-bitmap-esc-pos$ cd src
(venv) ascii-bitmap-esc-pos/src$ python main.py
```
