from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from .models import HorariosProfesores
from .models import HorariosLaboratorios
from .models import Ubicaciones
from .models import ArchivoExcel
from .models import ArchivoExcelHorariosLaboratorios
from .models import ArchivoExcelUbicaciones
from .models import Calendario
from .models import Pensum
from .models import AsignacionCasilleros
from .models import ActividadesExtra
from .models import Normatividad
from .models import NormatividadArchivo
from .models import MensajeMasivo
from .models import Reglamento


from .forms import HorariosProfesoresForm, HorariosLaboratoriosForm , UbicacionesForm, DocumentoHorarioProfesoresForm
from .forms import DocumentoHorarioLaboratoriosForm, DocumentoUbicacionesForm, NormatividadForm, MensajeMasivoForm
from .forms import CalendarioForm, PensumForm, AsignacionCasillerosForm, ActividadesExtraForm, NormatividadArchivoForm, ReglamentoForm


import pickle
import pandas as pd
import telebot
from datetime import date
import yaml

##### Variables Globales #####
flag = 0
flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
flag5 = 0

#### Fin  de Variables Globales #####

class EliminarHorarioProfView (DeleteView):
    model = HorariosProfesores
    template_name = 'eliminarhorarioprof.html'
    success_url = reverse_lazy('horariosprofesores')

class EliminarHorarioLabView (DeleteView):
    model = HorariosLaboratorios
    template_name = 'eliminarhorariolab.html'
    success_url = reverse_lazy('horarioslaboratorios')

class EliminarUbicacionView (DeleteView):
    model = Ubicaciones
    template_name = 'eliminarubicacion.html'
    success_url = reverse_lazy('ubicaciones')

class EliminarNormaView (DeleteView):
    model = Normatividad
    template_name = 'eliminarnorma.html'
    success_url = reverse_lazy('normatividad')

class HomeView(ListView):
    model = HorariosProfesores
    template_name = 'home.html'


def importarhorarioslaboratoriosview(request):
    model = ArchivoExcelUbicaciones
    global flag1


    if request.method == 'POST':
        form = DocumentoHorarioLaboratoriosForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save()
            flag1 = 0

            return redirect('horarioslaboratorios')


    else:
        form =  DocumentoHorarioLaboratoriosForm()


    return render(request, 'importarhorariolab.html', {'form':form})


def horarioslaboratoriosview(request):
    global flag1
    ##### Filtro de Ultimo agregado del mismo nombre ######
    horarioslaboratorioslista = HorariosLaboratorios.objects.all()
    horarioslaboratoriosnombres = HorariosLaboratorios.objects.values_list('id', 'nombre')

    labnomdif = []
    for i in horarioslaboratoriosnombres:
        if i[1] not in labnomdif:
            labnomdif.append(i[1])


    labnombresiguales = []
    for nom in labnomdif:
        for igual in horarioslaboratoriosnombres:
            if nom == igual[1]:
                labnombresiguales.append(igual)

    lablistanombresunicos = []
    x = 0
    y = ' '
    for i in range(len(labnombresiguales)):
        for j in range(len(labnombresiguales)):
            if labnombresiguales[j][1] == labnombresiguales[i][1]:

                if labnombresiguales[j][0] >= labnombresiguales[i][0] and labnombresiguales[j] not in lablistanombresunicos:
                    x = labnombresiguales[j][1]
                    y = labnombresiguales[j][0]

                    if len(lablistanombresunicos) == 0:
                        lablistanombresunicos.append((y,x))

                    if x == lablistanombresunicos[-1][1]:
                        lablistanombresunicos.remove(lablistanombresunicos[-1])
                        lablistanombresunicos.append((y,x))

                    elif x != lablistanombresunicos[-1][1]:
                        lablistanombresunicos.append((y,x))
    laboratorioshorariosfinal = []
    for x in lablistanombresunicos:
        laboratorioshorariosfinal.append(HorariosLaboratorios.objects.get(pk=x[0]))
        ##### Fin de Filtro de Ultimo agregado del mismo nombre ######

    ####  Importacion del Excel #####




    if flag1 == 0:    #if new file has been uploaded

        archivoimportado = ArchivoExcelHorariosLaboratorios.objects.latest('id').documento
        df = pd.read_excel(archivoimportado, keep_default_na=False)


        for index, row in df.iterrows():
            obj = HorariosLaboratorios.objects.create(nombre= row.nombre, lunes= row.lunes, martes= row.martes, miercoles= row.miercoles, jueves= row.jueves, viernes= row.viernes, sabado= row.sabado, domingo= row.domingo)
            obj.save()
        flag1 = 1



    ####  FIN de la Importacion del Excel #####




    ### Creacion del documento excel ####

    labnomfin= []
    for nombre in laboratorioshorariosfinal:
        labnomfin.append(nombre.nombre)

    lablunfin= []
    for lunes in laboratorioshorariosfinal:
        lablunfin.append(lunes.lunes)

    labmarfin= []
    for martes in laboratorioshorariosfinal:
        labmarfin.append(martes.martes)

    labmierfin= []
    for miercoles in laboratorioshorariosfinal:
        labmierfin.append(miercoles.miercoles)

    labjuefin= []
    for jueves in laboratorioshorariosfinal:
        labjuefin.append(jueves.jueves)

    labvierfin= []
    for viernes in laboratorioshorariosfinal:
        labvierfin.append(viernes.viernes)

    labsabfin= []
    for sabado in laboratorioshorariosfinal:
        labsabfin.append(sabado.sabado)

    labdomfin= []
    for domingo in laboratorioshorariosfinal:
        labdomfin.append(domingo.domingo)


    df = pd.DataFrame({'nombre':labnomfin,'lunes':lablunfin,'martes':labmarfin,'miercoles':labmierfin,
                       'jueves':labjuefin,'viernes':labvierfin,'sabado':labsabfin,'domingo':labdomfin})

    df.to_excel('./media/Horario Laboratorios.xlsx', index = False)

    ### Fin de la creacion del documento excel ####



    submitted = 0
    if request.method == "POST":
        form = HorariosLaboratoriosForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/horarioslaboratorios?submitted=1')
        else:
            return HttpResponseRedirect('/horarioslaboratorios?submitted=2')
    else:
        form = HorariosLaboratoriosForm
        if 'submitted' in request.GET:
            submitted = 1
    form = HorariosLaboratoriosForm
    return render(request, 'horarioslaboratorios.html', {'form':form, 'submitted':submitted, 'laboratorioshorariosfinal':laboratorioshorariosfinal})


def importarhorariosprofesoresview(request):
    model = ArchivoExcel
    global flag


    if request.method == 'POST':
        form = DocumentoHorarioProfesoresForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save()
            flag = 0

            return redirect('horariosprofesores')


    else:
        form =  DocumentoHorarioProfesoresForm()


    return render(request, 'importarhorarioprof.html', {'form':form})


def horariosprofesoresview(request):


    ##### Filtro de Ultimo agregado del mismo nombre ######
    horariosprofesoreslista = HorariosProfesores.objects.all()

    horariosprofesoresnombres = HorariosProfesores.objects.values_list('id', 'nombre')
    global flag


    profnomdif = []
    for i in horariosprofesoresnombres:
        if i[1] not in profnomdif:
            profnomdif.append(i[1])


    profnombresiguales = []
    for nom in profnomdif:
        for igual in horariosprofesoresnombres:
            if nom == igual[1]:
                profnombresiguales.append(igual)

    proflistanombresunicos = []
    x = 0
    y = ' '
    for i in range(len(profnombresiguales)):
        for j in range(len(profnombresiguales)):
            if profnombresiguales[j][1] == profnombresiguales[i][1]:

                if profnombresiguales[j][0] >= profnombresiguales[i][0] and profnombresiguales[j] not in proflistanombresunicos:
                    x = profnombresiguales[j][1]
                    y = profnombresiguales[j][0]

                    if len(proflistanombresunicos) == 0:
                        proflistanombresunicos.append((y,x))

                    if x == proflistanombresunicos[-1][1]:
                        proflistanombresunicos.remove(proflistanombresunicos[-1])
                        proflistanombresunicos.append((y,x))

                    elif x != proflistanombresunicos[-1][1]:
                        proflistanombresunicos.append((y,x))
    profesoreshorariosfinal = []
    for x in proflistanombresunicos:
        profesoreshorariosfinal.append(HorariosProfesores.objects.get(pk=x[0]))



        ##### Fin del Filtro de Ultimo agregado del mismo nombre ######



        ####  Importacion del Excel #####




    if flag == 0:    #if new file has been uploaded

        archivoimportado = ArchivoExcel.objects.latest('id').documento
        df = pd.read_excel(archivoimportado, keep_default_na=False)


        for index, row in df.iterrows():
            obj = HorariosProfesores.objects.create(nombre= row.nombre, lunes= row.lunes, martes= row.martes, miercoles= row.miercoles, jueves= row.jueves, viernes= row.viernes, sabado= row.sabado, domingo= row.domingo)
            obj.save()
        flag = 1



        ####  FIN de la Importacion del Excel #####




        ### Creacion del documento excel ####

    profnomfin= []
    for nombre in profesoreshorariosfinal:
        profnomfin.append(nombre.nombre)

    proflunfin= []
    for lunes in profesoreshorariosfinal:
        proflunfin.append(lunes.lunes)

    profmarfin= []
    for martes in profesoreshorariosfinal:
        profmarfin.append(martes.martes)

    profmierfin= []
    for miercoles in profesoreshorariosfinal:
        profmierfin.append(miercoles.miercoles)

    profjuefin= []
    for jueves in profesoreshorariosfinal:
        profjuefin.append(jueves.jueves)

    profvierfin= []
    for viernes in profesoreshorariosfinal:
        profvierfin.append(viernes.viernes)

    profsabfin= []
    for sabado in profesoreshorariosfinal:
        profsabfin.append(sabado.sabado)

    profdomfin= []
    for domingo in profesoreshorariosfinal:
        profdomfin.append(domingo.domingo)


    df = pd.DataFrame({'nombre':profnomfin,'lunes':proflunfin,'martes':profmarfin,'miercoles':profmierfin,
                       'jueves':profjuefin,'viernes':profvierfin,'sabado':profsabfin,'domingo':profdomfin})

    df.to_excel('./media/Horario Profesores.xlsx', index = False)

    ### Fin de la creacion del documento excel ####


    submitted = 0
    if request.method == "POST":
        form = HorariosProfesoresForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/horariosprofesores?submitted=1')
        else:
            return HttpResponseRedirect('/horariosprofesores?submitted=2')
    else:
        form = HorariosProfesoresForm
        if 'submitted' in request.GET:
            submitted = 1
    form = HorariosProfesoresForm
    return render(request, 'horariosprofesores.html', {'form':form, 'submitted':submitted,'profesoreshorariosfinal':profesoreshorariosfinal})


def importarubicacionesview(request):
    model = ArchivoExcelUbicaciones
    global flag2


    if request.method == 'POST':
        form = DocumentoUbicacionesForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save()
            flag2 = 0

            return redirect('ubicaciones')


    else:
        form =  DocumentoUbicacionesForm()


    return render(request, 'importarubicaciones.html', {'form':form})


def ubicacionesview(request):
    global flag2
    ##### Filtro de Ultimo agregado del mismo nombre ######
    ubicacioneslista = Ubicaciones.objects.all()

    ubicacionesnombres = Ubicaciones.objects.values_list('id', 'nombre')


    ubinomdif = []
    for i in ubicacionesnombres:
        if i[1] not in ubinomdif:
            ubinomdif.append(i[1])


    ubinombresiguales = []
    for nom in ubinomdif:
        for igual in ubicacionesnombres:
            if nom == igual[1]:
                ubinombresiguales.append(igual)

    ubilistanombresunicos = []
    x = 0
    y = ' '
    for i in range(len(ubinombresiguales)):
        for j in range(len(ubinombresiguales)):
            if ubinombresiguales[j][1] == ubinombresiguales[i][1]:

                if ubinombresiguales[j][0] >= ubinombresiguales[i][0] and ubinombresiguales[j] not in ubilistanombresunicos:
                    x = ubinombresiguales[j][1]
                    y = ubinombresiguales[j][0]

                    if len(ubilistanombresunicos) == 0:
                        ubilistanombresunicos.append((y,x))

                    if x == ubilistanombresunicos[-1][1]:
                        ubilistanombresunicos.remove(ubilistanombresunicos[-1])
                        ubilistanombresunicos.append((y,x))

                    elif x != ubilistanombresunicos[-1][1]:
                        ubilistanombresunicos.append((y,x))
    ubicacionesfinal = []
    for x in ubilistanombresunicos:
        ubicacionesfinal.append(Ubicaciones.objects.get(pk=x[0]))
        ##### Fin de Filtro de Ultimo agregado del mismo nombre ######

        ####  Importacion del Excel #####
    flag2a = 0
    if flag2 == 0:
        archivoimportado = ArchivoExcelUbicaciones.objects.latest('id').documento
        df = pd.read_excel(archivoimportado, keep_default_na=False)
        for index, row in df.iterrows():
            if  isinstance(row.latitud, float) and isinstance(row.longitud, float):
                print('this is a row with float numbers')

            else:
                flag2 = 1



    if flag2 == 0:    #if new file has been uploaded and all numbers are float

        archivoimportado = ArchivoExcelUbicaciones.objects.latest('id').documento
        df = pd.read_excel(archivoimportado, keep_default_na=False)


        for index, row in df.iterrows():
            obj = Ubicaciones.objects.create(nombre= row.nombre, latitud= row.latitud, longitud= row.longitud)
            #print('lat y long',isinstance(obj.latitud,float),isinstance(obj.longitud,float))
            if isinstance(obj.latitud,float)  and isinstance(obj.longitud,float):
                #print('if obj',obj)
                obj.save()

            else:
                print('else obj', obj)
                break
        flag2 = 1



        ####  FIN de la Importacion del Excel #####




        ### Creacion del documento excel ####

    ubinomfin= []
    for nombre in ubicacionesfinal:
        ubinomfin.append(nombre.nombre)

    ubilatfin= []
    for latitud in ubicacionesfinal:
        ubilatfin.append(latitud.latitud)

    ubilonfin= []
    for longitud in ubicacionesfinal:
        ubilonfin.append(longitud.longitud)




    df = pd.DataFrame({'nombre':ubinomfin,'latitud':ubilatfin,'longitud':ubilonfin})

    df.to_excel('./media/Ubicaciones.xlsx', index = False)

    ### Fin de la creacion del documento excel ####




    submitted = 0
    if request.method == "POST":
        form = UbicacionesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ubicaciones?submitted=1')
        else:
            return HttpResponseRedirect('/ubicaciones?submitted=2')
    else:
        form = UbicacionesForm
        if 'submitted' in request.GET:
            submitted = 1
    form = UbicacionesForm
    return render(request, 'ubicaciones.html', {'form':form, 'submitted':submitted, 'ubicacioneslista':ubicacioneslista, 'ubicacionesfinal':ubicacionesfinal})


def importarcalendarioview(request):
    model = Calendario

    if request.method == 'POST':
        form = CalendarioForm(request.POST ,request.FILES)
        print('form',form)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form =  CalendarioForm()


    return render(request, 'calendario.html', {'form':form})

def reglamentoview(request):
    model = Reglamento

    if request.method == 'POST':
        form = ReglamentoForm(request.POST ,request.FILES)
        print('form',form)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form =  ReglamentoForm()


    return render(request, 'reglamento.html', {'form':form})



def importarpensumview(request):
    model = Pensum

    if request.method == 'POST':
        form = PensumForm(request.POST ,request.FILES)
        print('form',form)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form =  PensumForm()


    return render(request, 'pensum.html', {'form':form})


def importarcasilleroview(request):
    model = AsignacionCasilleros

    if request.method == 'POST':
        form = AsignacionCasillerosForm(request.POST ,request.FILES)
        print('form',form)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form =  AsignacionCasillerosForm()


    return render(request, 'casilleros.html', {'form':form})


def importaractividadesextraview(request):
    model = ActividadesExtra

    if request.method == 'POST':
        form = ActividadesExtraForm(request.POST ,request.FILES)
        print('form',form)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form =  ActividadesExtraForm()


    return render(request, 'actividadesextra.html', {'form':form})


def importarnormatividadarchivo(request):
    global flag3
    model = NormatividadArchivo

    if request.method == 'POST':
        form = NormatividadArchivoForm(request.POST ,request.FILES)
        print('form',form)
        if form.is_valid():
            form.save()
            print('el documento subido es valido')
            flag3 = 0
            return redirect('normatividad')
    else:
        form =  NormatividadArchivoForm()
        print('el documento subido es invalido')


    return render(request, 'normatividadarchivo.html', {'form':form})


def normatividadview(request):
    global flag3
    ##### Filtro de Ultimo agregado del mismo nombre ######
    normatividadlista = Normatividad.objects.all()
    normatividadintents = Normatividad.objects.values_list('id', 'intent')

    normintdif = []
    for i in normatividadintents:
        if i[1] not in normintdif:
            normintdif.append(i[1])


    normintiguales = []
    for nom in normintdif:
        for igual in normatividadintents:
            if nom == igual[1]:
                normintiguales.append(igual)

    normlistaintentsunicos = []
    x = 0
    y = ' '
    for i in range(len(normintiguales)):
        for j in range(len(normintiguales)):
            if normintiguales[j][1] == normintiguales[i][1]:

                if normintiguales[j][0] >= normintiguales[i][0] and normintiguales[j] not in normlistaintentsunicos:
                    x = normintiguales[j][1]
                    y = normintiguales[j][0]

                    if len(normlistaintentsunicos) == 0:
                        normlistaintentsunicos.append((y,x))

                    if x == normlistaintentsunicos[-1][1]:
                        normlistaintentsunicos.remove(normlistaintentsunicos[-1])
                        normlistaintentsunicos.append((y,x))

                    elif x != normlistaintentsunicos[-1][1]:
                        normlistaintentsunicos.append((y,x))
    normasintentfinal = []
    for x in normlistaintentsunicos:
        normasintentfinal.append(Normatividad.objects.get(pk=x[0]))
        ##### Fin de Filtro de Ultimo agregado del mismo nombre ######

    ####  Importacion del Excel #####


    print('flag3 se ha subido un archivo? si = 0',flag3)

    if flag3 == 0:    #if new file has been uploaded

        archivoimportado = NormatividadArchivo.objects.latest('id').documento
        df = pd.read_excel(archivoimportado, keep_default_na=False)


        for index, row in df.iterrows():
            obj = Normatividad.objects.create(intent= row.intent, pregunta= row.pregunta, respuesta= row.respuesta, complemento= row.complemento, ejemplo1= row.ejemplo1, ejemplo2= row.ejemplo2, ejemplo3= row.ejemplo3, ejemplo4= row.ejemplo4, ejemplo5= row.ejemplo5, ejemplo6= row.ejemplo6, ejemplo7= row.ejemplo7, ejemplo8= row.ejemplo8, ejemplo9= row.ejemplo9, ejemplo10= row.ejemplo10, ejemplo11= row.ejemplo11, ejemplo12= row.ejemplo12, ejemplo13= row.ejemplo13, ejemplo14= row.ejemplo14, ejemplo15= row.ejemplo15)
            obj.save()
        flag3 = 1
    print('flag3 se ha subido un archivo? si = 0',flag3)


    ####  FIN de la Importacion del Excel #####




    ### Creacion del documento excel ####

    intentfin= []
    for intent in normasintentfinal:
        intentfin.append(intent.intent)

    preguntafin= []
    for pregunta in normasintentfinal:
        preguntafin.append(pregunta.pregunta)

    respuestafin= []
    for respuesta in normasintentfinal:
        respuestafin.append(respuesta.respuesta)

    complementofin= []
    for complemento in normasintentfinal:
        complementofin.append(complemento.complemento)

    ejemplo1fin= []
    for ejemplo in normasintentfinal:
        ejemplo1fin.append(ejemplo.ejemplo1)

    ejemplo2fin= []
    for ejemplo in normasintentfinal:
        ejemplo2fin.append(ejemplo.ejemplo2)

    ejemplo3fin= []
    for ejemplo in normasintentfinal:
        ejemplo3fin.append(ejemplo.ejemplo3)

    ejemplo4fin= []
    for ejemplo in normasintentfinal:
        ejemplo4fin.append(ejemplo.ejemplo4)

    ejemplo5fin= []
    for ejemplo in normasintentfinal:
        ejemplo5fin.append(ejemplo.ejemplo5)

    ejemplo6fin= []
    for ejemplo in normasintentfinal:
        ejemplo6fin.append(ejemplo.ejemplo6)

    ejemplo7fin= []
    for ejemplo in normasintentfinal:
        ejemplo7fin.append(ejemplo.ejemplo7)

    ejemplo8fin= []
    for ejemplo in normasintentfinal:
        ejemplo8fin.append(ejemplo.ejemplo8)

    ejemplo9fin= []
    for ejemplo in normasintentfinal:
        ejemplo9fin.append(ejemplo.ejemplo9)

    ejemplo10fin= []
    for ejemplo in normasintentfinal:
        ejemplo10fin.append(ejemplo.ejemplo10)

    ejemplo11fin= []
    for ejemplo in normasintentfinal:
        ejemplo11fin.append(ejemplo.ejemplo11)

    ejemplo12fin= []
    for ejemplo in normasintentfinal:
        ejemplo12fin.append(ejemplo.ejemplo12)

    ejemplo13fin= []
    for ejemplo in normasintentfinal:
        ejemplo13fin.append(ejemplo.ejemplo13)

    ejemplo14fin= []
    for ejemplo in normasintentfinal:
        ejemplo14fin.append(ejemplo.ejemplo14)

    ejemplo15fin= []
    for ejemplo in normasintentfinal:
        ejemplo15fin.append(ejemplo.ejemplo15)



    df = pd.DataFrame({'intent':intentfin,'pregunta':preguntafin,'respuesta':respuestafin,'complemento':complementofin, 'ejemplo1':ejemplo1fin, 'ejemplo2':ejemplo2fin, 'ejemplo3':ejemplo3fin, 'ejemplo4':ejemplo4fin, 'ejemplo5':ejemplo5fin, 'ejemplo6':ejemplo6fin, 'ejemplo7':ejemplo7fin, 'ejemplo8':ejemplo8fin, 'ejemplo9':ejemplo9fin, 'ejemplo10':ejemplo10fin, 'ejemplo11':ejemplo11fin, 'ejemplo12':ejemplo12fin, 'ejemplo13':ejemplo13fin, 'ejemplo14':ejemplo14fin, 'ejemplo15':ejemplo15fin})

    df.to_excel('./media/Normatividad.xlsx', index = False)

    ### Fin de la creacion del documento excel ####

    submitted = 0
    if request.method == "POST":
        form = NormatividadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/normatividad?submitted=1')
        else:
            return HttpResponseRedirect('/normatividad?submitted=2')
    else:
        form = NormatividadForm
        if 'submitted' in request.GET:
            submitted = 1
    form = NormatividadForm
    return render(request, 'normatividad.html', {'form':form, 'submitted':submitted, 'normasintentfinal':normasintentfinal})


def mensajemasivoview(request):
    TOKEN = '1493294417:AAFg14tN8se129BddXINFjqa4DbnDdWlqQ8'
    bot = telebot.TeleBot(TOKEN)
    archivo =  './media/Usuarios.xlsx'
    df = pd.read_excel(archivo, keep_default_na=False)
    usuarios = df.id
    codigos = df.codigo
    todays_date = date.today()
    año = todays_date.year



    submitted = 0
    if request.method == "POST":
        form = MensajeMasivoForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = MensajeMasivo.objects.latest('id').mensaje
            print('mensaje',mensaje)
            for x in range(0,len(usuarios)):
                numero = codigos[x]
                if numero != ' ' and len(str(numero)) == 10:
                    dos_digitos = int(str(numero)[:2])
                    fecha_ingreso_estudiante = int(str(numero)[2:6])
                    limite = año - fecha_ingreso_estudiante
                    if dos_digitos == 24 and limite <= 7:
                        bot.send_message(usuarios[x], mensaje)
                        print('Enviado el mensaje masivo exitosamente')
            return HttpResponseRedirect('/mensajemasivo?submitted=1')
        else:
            return HttpResponseRedirect('/mensajemasivo?submitted=2')
    else:
        form = MensajeMasivoForm
        if 'submitted' in request.GET:
            submitted = 1
    form = MensajeMasivoForm
    return render(request, 'mensajemasivo.html', {'form':form, 'submitted':submitted})


def actualizarymlnormatividad(request):

    # Actializar los archivos yml Normatividad
    df = pd.read_excel('./media/Normatividad.xlsx', keep_default_na=False)
    intents_excel_normas= []
    for intent in df.intent:
        intents_excel_normas.append(intent) # se convierte la lista de pandas a una lista de python para evitar errores con operadores logicos en python
    ## editor de domain de normatividad##
    #se importa el archivo yml domain.yml
    f = open("../chatbot_isa/domain.yml", "r")
    lista_de_lineas = f.readlines()

    intents_nuevos= intents_excel_normas.copy()

    for x in range(0,len(lista_de_lineas)):
        for y in range(0,len(lista_de_lineas[x].split())):
            if lista_de_lineas[x].split()[y] == '#' and lista_de_lineas[x].split()[y+1] == 'comienzo':
                save1 = x+1

            if lista_de_lineas[x].split()[y] == '#' and lista_de_lineas[x].split()[y+1] == 'fin':
                save2 = x
    primera_parte = []
    segunda_parte = []
    for i in range(0,save1):
        primera_parte.append(lista_de_lineas[i])
    for x in range(save2,len(lista_de_lineas)):
        segunda_parte.append(lista_de_lineas[x])
    intent_lista= []
    impresion_final= []
    for intent in intents_excel_normas:
        if intent != '':
            intent_lista.extend(['- '+ intent +':\n','    use_entities: true\n'])
    impresion_final.extend(primera_parte)
    impresion_final.extend(intent_lista)
    impresion_final.extend(segunda_parte)

    f = open("../chatbot_isa/domain.yml", "w")
    for i in impresion_final:
        f.write(i)

    f.close()


    #### editor de stories de normatividad #####

    #se importa el archivo yml stories.yml
    f = open("../chatbot_isa/data/stories.yml", "r")
    lista_de_lineas = f.readlines()

    intents_nuevos = intents_excel_normas.copy()
    for x in range(0,len(lista_de_lineas)):
        for y in range(0,len(lista_de_lineas[x].split())):
            if lista_de_lineas[x].split()[y] == '#' and lista_de_lineas[x].split()[y+1] == 'comienzo':
                save1 = x+1
            if lista_de_lineas[x].split()[y] == '#' and lista_de_lineas[x].split()[y+1] == 'fin':
                save2 = x
    primera_parte = []
    segunda_parte = []
    for i in range(0,save1):
        primera_parte.append(lista_de_lineas[i])
    for x in range(save2,len(lista_de_lineas)):
        segunda_parte.append(lista_de_lineas[x])

    intent_lista= []
    impresion_final= []
    for intent in intents_excel_normas:
        if intent != '':
            intent_lista.extend('- story: '+ intent +'story\n')
            intent_lista.extend('  steps:\n')
            intent_lista.extend('  - intent: '+ intent +'\n')
            intent_lista.extend('  - action: action_excel_normas\n')

    impresion_final.extend(primera_parte)
    impresion_final.extend(intent_lista)
    impresion_final.extend(segunda_parte)

    f = open("../chatbot_isa/data/stories.yml", "w")
    for i in impresion_final:
        f.write(i)

    f.close()



    ### Editor de nlu de normatividad #####
    f = open("../chatbot_isa/data/nlu.yml", "r")
    lista_de_lineas = f.readlines()
    posisiones_a_remplazar_comienzo = []
    posisiones_a_remplazar_final = []
    for x in range(0,len(lista_de_lineas)):
        for y in range(0,len(lista_de_lineas[x].split())):
            if lista_de_lineas[x].split()[y] == '#' and lista_de_lineas[x].split()[y+1] == 'comienzo' and lista_de_lineas[x].split()[y+2] == 'normas':
                save1 = x+1
            if lista_de_lineas[x].split()[y] == '#' and lista_de_lineas[x].split()[y+1] == 'fin' and lista_de_lineas[x].split()[y+2] == 'normas':
                save2 = x
    primera_parte = []
    segunda_parte = []
    for i in range(0,save1):
        primera_parte.append(lista_de_lineas[i]) # se guarga el resto del documento (todo menos las intenciones a remplazar)
    for a in range(save2,len(lista_de_lineas)):
        segunda_parte.append(lista_de_lineas[a])

    intents_a_agregar = []
    ejemplos = []
    ejemplos_por_fila = []
    round_number = 0
    for index, row in df.iterrows():
        if round_number == index:
            ejemplos = []
        for i in range(4,len(row)):
            if row[i] != '':
                ejemplos.append(row[i])# se agrega cada ejemplo del intent
        round_number = round_number+1
        ejemplos_por_fila.append(ejemplos)# se guarda la lista de ejemplos de cada intent

    for i in range(0,len(intents_excel_normas)):
        if intents_excel_normas[i] != '':
            intents_a_agregar.append('- intent: '+intents_excel_normas[i]+'\n') #se escriben las intenciones nuevas siguento el syntax de Yaml
            intents_a_agregar.append('  examples: |\n')
            for ejemplo in ejemplos_por_fila[i]:
                intents_a_agregar.append('    - '+ejemplo+'\n')

    archivo_completo_en_filas = []
    archivo_completo_en_filas.extend(primera_parte)      # se unen las tres listas:
    archivo_completo_en_filas.extend(intents_a_agregar)  # primera parte del archivo guardado, las intenciones a agregar y finalmente
    archivo_completo_en_filas.extend(segunda_parte)     # la segunda parte guardado del archivo original


    file = open("../chatbot_isa/data/nlu.yml", "w") # se sobre escribe el archivo nlu ya con la intencion agregada
    for i in archivo_completo_en_filas:
        file.write(i)
    file.close()
    return



import os
import sys
import threading
import concurrent.futures


def run_actions():
    os.system("bash ./rasaRunActions.sh")

def stop_run():
   os.system("bash ./rasaStopRun.sh")

def terminate():
    os.system("bash ./rasakill.sh")

def actualizarbotview(request):
    if str(type(request)) == "<class 'str'>":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            stoprun = executor.submit(stop_run)
            runactions = executor.submit(run_actions)

    elif request.method == 'GET':
        actualizarymlnormatividad(request)
        terminate()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            stoprun = executor.submit(stop_run)
            runactions = executor.submit(run_actions)
    return HttpResponseRedirect('/home?submitted=1')

# if __name__ == "isa.views":
#     actualizarbotview("cualquiercosaxdxdxd")
