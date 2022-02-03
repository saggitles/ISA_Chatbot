from typing import Dict, Text, Any, List, Optional, Callable, Awaitable
from rasa_sdk import Action,Tracker
from rasa_sdk.executor import CollectingDispatcher
import telebot
import pandas as pd
import glob
import os
from sanic.request import Request



from time import sleep

TOKEN = '1493294417:AAFg14tN8se129BddXINFjqa4DbnDdWlqQ8'
bot = telebot.TeleBot(TOKEN)


class ActionId(Action):

    def name(self) -> Text:
        return 'action_id'


    def run(self, dispatcher, tracker, domain):
        archivo =  '../src/media/Usuarios.xlsx'
        usuario = tracker.sender_id
        print('usuario',usuario)

        df = pd.read_excel(archivo, keep_default_na=False)
        codigos = []
        for y in df.codigo:
            codigos.append(y)

        usuarios= []
        for i in df.id:
            usuarios.append(i)

        if int(usuario) not in usuarios:
            usuarios.append(usuario)
        if len(usuarios) > len(codigos):
            codigos.append(' ')
        df = pd.DataFrame({'id':usuarios, 'codigo':codigos})
        df.to_excel('../src/media/Usuarios.xlsx', index = False)

        ### Fin de la creacion del documento excel ####
        mensaje = "Antes de ayudarte me podrías dar tu código estudiantil por favor?"
        dispatcher.utter_message(mensaje)
        return []

class ActionCodigo(Action):

    def name(self) -> Text:
        return 'action_codigo'


    def run(self, dispatcher, tracker, domain):
        archivo =  '../src/media/Usuarios.xlsx'
        usuario = tracker.sender_id
        entidades = tracker.latest_message['entities']
        for entidad in entidades:
                valor = entidad['value']

        df = pd.read_excel(archivo, keep_default_na=False)
        ids= []
        for y in df.id:
            ids.append(y)

        codigos= []
        for i in df.codigo:
            codigos.append(i)

        for x in range(0,len(df.id)):
            if str(df.id[x]) == usuario:
                codigos[x] = valor

        df = pd.DataFrame({'id':ids, 'codigo':codigos})
        df.to_excel('../src/media/Usuarios.xlsx', index = False)

        ### Fin de la creacion del documento excel ####
        mensaje = "Muchas gracias!"
        dispatcher.utter_message(mensaje)
        return []

class ActionEntityExtractorUbi(Action):
    def name(self) -> Text:
        return "action_entity_extractor"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        archivo = '../src/media/Ubicaciones.xlsx'
        archivo_lista = '../src/media/Lista de posibles ubicaciones.xlsx'
        mensaje = ''
        flag=0
        entidades = tracker.latest_message['entities']
        global TOKEN
        global bot

        for entidad in entidades:
            valor = entidad['value']
            df = pd.read_excel(archivo, keep_default_na=False)
            df_lista = pd.read_excel(archivo_lista, keep_default_na=False)
            print('ubicacion a buscar = ',valor)
            for x in range(0,len(df.nombre)):
                if df.nombre[x] == valor:
                    flag = 1

                    UserID = tracker.sender_id
                    print('ubicacion encontrada',df.nombre[x],df.latitud[x],df.longitud[x])
                    mensaje = "Esta es la ubicacion 📍 de " + str(valor)
                    bot.send_location(UserID, df.latitud[x], df.longitud[x])

            if valor == 'LABORATORIO':
                flag = 1
                labs = df_lista.laboratorios
                mensaje = "Estos son los laboratorios 🧪 actuales en la universidad de Ibagué, por favor busque la ubicación de alguna de ellas: \n\n" + '\n'.join([str(elemento) for elemento in labs])

            if valor == 'SALON':
                flag = 1
                salones = df_lista.salones
                mensaje = "Estos son los salones 📍 actuales en la universidad de Ibagué, por favor busque la ubicación de alguna de ellas: \n\n" + '\n'.join([str(elemento) for elemento in salones])

            if valor == 'BAÑO':
                flag = 1
                baños = df_lista.baños
                mensaje = "Estos son los baños 🚽 actuales en la universidad de Ibagué, por favor busque la ubicación de alguna de ellas: \n\n" + '\n'.join([str(elemento) for elemento in baños])

            if valor == 'OFICINA':
                flag = 1
                oficinas = df_lista.oficinas
                mensaje = "Estas son las oficinas ‍💼 actuales que involucran la carrera de ingeniería electrónica, por favor busque la ubicación de alguna de ellas: \n\n" + '\n'.join([str(elemento) for elemento in oficinas])

            if valor == 'CAFETERIA':
                flag = 1
                cafeterias = df_lista.cafeterias
                mensaje = "Estas son las cafeterias ☕ actuales en la Universidad de Ibagué, por favor busque la ubicación de alguna de ellas: \n\n" + '\n'.join([str(elemento) for elemento in cafeterias])

            if flag == 0:
                mensaje = "Por favor se mas especifico en la ubicación deseada o revisa si tiene algún error. :)"


        dispatcher.utter_message(mensaje)

        return []

class ActionEntityExtractorProf(Action):
    def name(self) -> Text:
        return "action_profesor_extractor"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        archivo = '../src/media/Horario Profesores.xlsx'
        mensaje = ''
        flag=0
        entidades = tracker.latest_message['entities']

        for entidad in entidades:
            valor = entidad['value']
            df = pd.read_excel(archivo, keep_default_na=False)

            for x in range(0,len(df.nombre)):
                if df.nombre[x] == valor:
                    flag = 1
                    horario = [str(df.lunes[x]), str(df.martes[x]), str(df.miercoles[x]), str(df.jueves[x]), str(df.viernes[x]), str(df.sabado[x]), str(df.domingo[x])]
                    semana = ['Lunes: ', 'Martes: ', 'Miercoles: ', 'Jueves: ', 'Viernes: ', 'Sabado: ', 'Domingo: ']
                    horario_final = []
                    pos = []
                    for dia in horario:
                        if dia != '':
                            posicion = horario.index(dia)
                            pos.append(semana[posicion])
                            horario_final.append(dia)

                    fin1 = []
                    for i in range(0,len(horario_final)):
                        fin = pos[i] + horario_final[i]+ '\n'
                        fin1.append(fin)
                        mensaje = 'Profesor 👨‍🏫: '+str(df.nombre[x]) +'\n'+ ''.join(fin1)
            if flag == 0:

                mensaje = "Por favor se mas especifico o revisa si tienes algun error."


        dispatcher.utter_message(text = mensaje)

        return []

class ActionEntityExtractorLab(Action):
    def name(self) -> Text:
        return "action_laboratorio_extractor"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        archivo = '../src/media/Horario Laboratorios.xlsx'
        archivo_lista = '../src/media/Lista de posibles ubicaciones.xlsx'
        mensaje = ''
        flag=0
        entidades = tracker.latest_message['entities']

        for entidad in entidades:
            valor = entidad['value']
            df = pd.read_excel(archivo, keep_default_na=False)
            df_lista = pd.read_excel(archivo_lista, keep_default_na=False)
            print('valor entrante',valor)
            for x in range(0,len(df.nombre)):
                if df.nombre[x] == valor:
                    flag = 1
                    horario = [str(df.lunes[x]), str(df.martes[x]), str(df.miercoles[x]), str(df.jueves[x]), str(df.viernes[x]), str(df.sabado[x]), str(df.domingo[x])]
                    semana = ['Lunes: ', 'Martes: ', 'Miercoles: ', 'Jueves: ', 'Viernes: ', 'Sabado: ', 'Domingo: ']
                    horario_final = []
                    pos = []
                    for dia in horario:
                        if dia != '':
                            posicion = horario.index(dia)
                            pos.append(semana[posicion])
                            horario_final.append(dia)

                    fin1 = []
                    for i in range(0,len(horario_final)):
                        fin = pos[i] + horario_final[i]+ '\n'
                        fin1.append(fin)
                        mensaje = 'Laboratorio 🔬: '+str(df.nombre[x]) +'\n'+ ''.join(fin1)

            

            if valor == 'LABORATORIO':
                flag = 1
                labs = df_lista.laboratorios
                mensaje = "Estos son los laboratorios 🔬 actuales en la universidad de Ibagué, por favor busque la ubicación o el horario de alguna de ellas: \n\n" + '\n'.join([str(elemento) for elemento in labs])


            if flag == 0:

                mensaje = "Por favor se mas especifico o revisa si tienes algún error."


        dispatcher.utter_message(text = mensaje)

        return []

class ActionImagenCalendario(Action):
    def name(self) -> Text:
        return "action_imagen_calendario"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        carpeta = '../src/media/Calendario estudiantil/*'
        global TOKEN
        global bot
        UserID = tracker.sender_id

        list_of_files = glob.glob(carpeta) # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        bot.send_photo(UserID, open(latest_file, 'rb'))

        return []

class ActionImagenActividadesExtra(Action):
    def name(self) -> Text:
        return "action_imagen_actividades_extra"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        carpeta = '../src/media/Actividades Extracuriculares/*'
        global TOKEN
        global bot
        UserID = tracker.sender_id

        list_of_files = glob.glob(carpeta) # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        bot.send_photo(UserID, open(latest_file, 'rb'))

        #dispatcher.utter_message(text = latest_file)
        return []

class ActionImagenPensum(Action):
    def name(self) -> Text:
        return "action_imagen_pensum"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        carpeta = '../src/media/Pensum/*'
        global TOKEN
        global bot
        UserID = tracker.sender_id

        list_of_files = glob.glob(carpeta) # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        bot.send_photo(UserID, open(latest_file, 'rb'))

        return []

class ActionImagenCasillero(Action):
    def name(self) -> Text:
        return "action_imagen_casillero"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global TOKEN
        global bot
        UserID = tracker.sender_id

        carpeta = '../src/media/Asignacion Casilleros/*'
        list_of_files = glob.glob(carpeta) # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)

        bot.send_photo(UserID, open(latest_file, 'rb'))

        return

class ActionReglamentoEstudiantil(Action):
    def name(self) -> Text:
        return "action_reglamento_estudiantil"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        carpeta = '../src/media/Reglamento/*'
        global TOKEN
        global bot
        UserID = tracker.sender_id

        list_of_files = glob.glob(carpeta) # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        bot.send_document(UserID, open(latest_file, 'rb'))

        #dispatcher.utter_message(text = latest_file)
        return []

class ActionFuncionesISA(Action):
    def name(self) -> Text:
        return "action_funciones_isa"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global TOKEN
        global bot
        UserID = tracker.sender_id
        mensaje = 'Para más información sobre mis funciones puedes descargar el siguiente PDF:'
        bot.send_message(UserID, mensaje)
        bot.send_document(UserID, open('../src/media/funciones actuales del bot.pdf', 'rb'))

class ActionExcelNormas(Action):
    def name(self) -> Text:
        return "action_excel_normas"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        archivo = '../src/media/Normatividad.xlsx'
        mensaje = ''
        flag=0
        df = pd.read_excel(archivo, keep_default_na=False)
        intent_de_mensaje = tracker.latest_message['intent'].get('name')
        for x in range(0,len(df.intent)):
            if df.intent[x] == intent_de_mensaje:
                flag = 1

                print('intent encontrado',df.intent[x],df.respuesta[x],df.complemento[x])
                mensaje = str(df.respuesta[x]) +'\n'+ str(df.complemento[x])

        if flag == 0:
            mensaje = "No entendí tu pregunta, me la puedes reformular por favor"


        dispatcher.utter_message(mensaje)

        return []
