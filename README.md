# ISA Chatbot
## Centro de informacion para institucion educativa

[![Python Logo](https://pngpress.com/wp-content/uploads/2020/03/Python-Logo-PNG-Image-120x120.png)]()
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Rasa_nlu_horizontal_purple.svg/2560px-Rasa_nlu_horizontal_purple.svg.png" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="300" height="120" />




[![Python Versions](https://img.shields.io/badge/Python-3.8-green)]()
[![Rasa Versions](https://img.shields.io/badge/Rasa-2.8.1-purple)]()
[![Django Versions](https://img.shields.io/badge/Django-2.8-green)]()

## Introduccion
ISA es un prototipo chatbot diseñado con el fin de servir como centro de información principal de un institución educativa, brindando información como ubicaciones, normativas, horarios de docentes, horarios de laboratorios y datos de interés general. ISA usa a rasa para su proceso de lenguaje natural y posee una página web para la alimentación de información la cual fue diseñada con la ayuda de Django, los usuarios podrán interactuar con él a través de telegram una red social bastante popular que brinda la facilidad de estos tipos de chatbot de manera gratuita.

## Características

- NLU natual language understanding
- Una pagina web para la actualizacion y creacion de informacion del bot
- Sin necesidad de interactuar con codigo 



## Instalacíon

Con ctrl + Alt + t puede abrir un terminal, en el acceda a la carpeta "ISA_fin" e introduzca los siguentes comandos:


```sh
source bin/activate
sudo apt install python3-pip
pip3 install -U --user pip && pip3 install rasa
python3 -m pip install Django
pip install pandas
python3 -m pip install --user -U pyTelegramBotAPI
pip install datetime
pip install django-import_export
```
para la instalación hay dos opciones, la primera tiene un límite de 2 horas de uso cada vez que se actualiza el link de conexión:
```sh
sudo apt install curl
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```
La segunda opcion no tiene limite de tiempo por link de conexion. Para poder usar esta opcion debe de crear una cuenta de ngrok e instalar el programa con su cuenta https://ngrok.com/download

## Funcionamiento

Para poner en funcionamiento a ISA es necesario seguir los siguentes pasos:
1. En un terminal dentro del entorno virtual y dentro de ISA_fin escribir el comando:
    ```sh
    ngrok http 5005
    ```
      Luego de esto copiar el fowarding desde "https" hasta "ngrok.io" y en el archivo credentials de rasa pegar lo que copió en frente de "webhook_url:" seguido de "/webhooks/telegram/webhook" todo dentro de comillas y guarde el archivo con "CTRL + s".
2. En otro terminal dentro del entorno virtual y dentro de ISA_fin escribir los siguentes comandos:
    ```sh
    cd src
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
    ```
3. Aceder a la pagina con el link dado en el teminal seguido de home ej: http://127.0.0.1:8000/home.
    Ya dentro de la pagina hacer click al boton "Actualizar ISA" en la esquina superior derecha de la pagina.

##### ¡LISTO! ya puedes escribirle a ISA atravez de telegram con el usuario @Isabella_Unibot

    


