from django.contrib import admin

# Register your models here.
from .models import Ubicaciones
from .models import HorariosProfesores
from .models import HorariosLaboratorios
from .models import ArchivoExcel
from .models import ArchivoExcelHorariosLaboratorios
from .models import ArchivoExcelUbicaciones
from .models import Calendario
from .models import Pensum
from .models import AsignacionCasilleros
from .models import NormatividadArchivo
from .models import Normatividad
from .models import MensajeMasivo
from .models import Reglamento

from import_export.admin import ImportExportModelAdmin


admin.site.register(Ubicaciones)
admin.site.register(HorariosProfesores)
admin.site.register(HorariosLaboratorios)
admin.site.register(ArchivoExcel)
admin.site.register(ArchivoExcelHorariosLaboratorios)
admin.site.register(ArchivoExcelUbicaciones)
admin.site.register(Calendario)
admin.site.register(Pensum)
admin.site.register(AsignacionCasilleros)
admin.site.register(NormatividadArchivo)
admin.site.register(Normatividad)
admin.site.register(MensajeMasivo)
admin.site.register(Reglamento)
