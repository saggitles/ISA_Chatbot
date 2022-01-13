from django import forms
from .models import HorariosProfesores, HorariosLaboratorios, Ubicaciones, ArchivoExcel, ArchivoExcelHorariosLaboratorios, Normatividad, MensajeMasivo
from .models import ArchivoExcelUbicaciones, Calendario, Pensum, AsignacionCasilleros, ActividadesExtra, NormatividadArchivo, Reglamento



class HorariosProfesoresForm(forms.ModelForm):
    class Meta:
        model = HorariosProfesores
    #    def __init__(self, *args, **kwargs):
    #        super(UserColorsForm, self).__init__(*args, **kwargs)
    #        for field in self.fields:
    #            field.wiget.attrs['class'] = 'color'

        fields = ('nombre', 'lunes', 'martes','miercoles', 'jueves', 'viernes', 'sabado', 'domingo')

        widgets = {     'nombre': forms.TextInput(attrs={'class' : 'form-control'}),
                        'lunes': forms.TextInput(attrs={'class' : 'form-control'}),
                        'martes': forms.TextInput(attrs={'class' : 'form-control'}),
                        'miercoles': forms.TextInput(attrs={'class' : 'form-control'}),
                        'jueves': forms.TextInput(attrs={'class' : 'form-control'}),
                        'viernes': forms.TextInput(attrs={'class' : 'form-control'}),
                        'sabado': forms.TextInput(attrs={'class' : 'form-control'}),
                        'domingo': forms.TextInput(attrs={'class' : 'form-control'}),
                        }


class HorariosLaboratoriosForm(forms.ModelForm):
    class Meta:
        model = HorariosLaboratorios

        fields = ('nombre', 'lunes', 'martes','miercoles', 'jueves', 'viernes', 'sabado', 'domingo')

        widgets = {     'nombre': forms.TextInput(attrs={'class' : 'form-control'}),
                        'lunes': forms.TextInput(attrs={'class' : 'form-control'}),
                        'martes': forms.TextInput(attrs={'class' : 'form-control'}),
                        'miercoles': forms.TextInput(attrs={'class' : 'form-control'}),
                        'jueves': forms.TextInput(attrs={'class' : 'form-control'}),
                        'viernes': forms.TextInput(attrs={'class' : 'form-control'}),
                        'sabado': forms.TextInput(attrs={'class' : 'form-control'}),
                        'domingo': forms.TextInput(attrs={'class' : 'form-control'}),
                        }


class UbicacionesForm(forms.ModelForm):
    class Meta:
        model = Ubicaciones

        fields = ('nombre', 'latitud', 'longitud')

        widgets = {     'nombre': forms.TextInput(attrs={'class' : 'form-control'}),
                        'latitud': forms.TextInput(attrs={'class' : 'form-control'}),
                        'longitud': forms.TextInput(attrs={'class' : 'form-control'}),
                        }



class DocumentoHorarioProfesoresForm(forms.ModelForm):
    class Meta:
        model = ArchivoExcel

        fields = ('documento', 'nombre')

class DocumentoHorarioLaboratoriosForm(forms.ModelForm):
    class Meta:
        model = ArchivoExcelHorariosLaboratorios

        fields = ('documento', 'nombre')

class DocumentoUbicacionesForm(forms.ModelForm):
    class Meta:
        model = ArchivoExcelUbicaciones

        fields = ('documento', 'nombre')

class CalendarioForm(forms.ModelForm):
    class Meta:
        model = Calendario

        fields = ('documento', 'nombre')

class PensumForm(forms.ModelForm):
    class Meta:
        model = Pensum

        fields = ('documento', 'nombre')

class ReglamentoForm(forms.ModelForm):
    class Meta:
        model = Reglamento

        fields = ('documento', 'nombre')

class AsignacionCasillerosForm(forms.ModelForm):
    class Meta:
        model = AsignacionCasilleros

        fields = ('documento', 'nombre')

class ActividadesExtraForm(forms.ModelForm):
    class Meta:
        model = ActividadesExtra

        fields = ('documento', 'nombre')

class NormatividadForm(forms.ModelForm):
    class Meta:
        model = Normatividad

        fields = ('intent', 'pregunta', 'respuesta','complemento', 'ejemplo1', 'ejemplo2', 'ejemplo3', 'ejemplo4', 'ejemplo5', 'ejemplo6', 'ejemplo7', 'ejemplo8', 'ejemplo9', 'ejemplo10', 'ejemplo11', 'ejemplo12', 'ejemplo13', 'ejemplo14', 'ejemplo15')

        widgets = {     'intent': forms.TextInput(attrs={'class' : 'form-control'}),
                        'pregunta': forms.TextInput(attrs={'class' : 'form-control'}),
                        'respuesta': forms.TextInput(attrs={'class' : 'form-control'}),
                        'complemento': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo1': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo2': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo3': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo4': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo5': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo6': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo7': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo8': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo9': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo10': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo11': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo12': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo13': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo14': forms.TextInput(attrs={'class' : 'form-control'}),
                        'ejemplo15': forms.TextInput(attrs={'class' : 'form-control'}),
                        }

class NormatividadArchivoForm(forms.ModelForm):
    class Meta:
        model = NormatividadArchivo

        fields = ('documento', 'nombre')


class MensajeMasivoForm(forms.ModelForm):
    class Meta:
        model = MensajeMasivo

        fields = ('tema', 'mensaje')

        widgets = {     'tema': forms.TextInput(attrs={'class' : 'form-control'}),
                        'mensaje': forms.Textarea(attrs={'class' : 'form-control'}),
                        }
