
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.conf.urls.static import static
from isa import models

from django.urls import path, include

from isa.views import HomeView, horarioslaboratoriosview, horariosprofesoresview, ubicacionesview, EliminarHorarioProfView, EliminarHorarioLabView, EliminarNormaView
from isa.views import EliminarUbicacionView, importarhorariosprofesoresview, importarhorarioslaboratoriosview, importarubicacionesview, importarcalendarioview
from isa.views import importarpensumview, importarcasilleroview, importaractividadesextraview, importarnormatividadarchivo, normatividadview
from isa.views import mensajemasivoview, actualizarbotview, reglamentoview
urlpatterns = [
    path('home/',HomeView.as_view(), name= 'home'),
    path('horariosprofesores/importar/', importarhorariosprofesoresview, name= 'importhorarioprof'),
    path('horariosprofesores/<int:pk>/remove/',EliminarHorarioProfView.as_view(), name= 'eliminarhorarioprof'),
    path('horarioslaboratorios/<int:pk>/remove/',EliminarHorarioLabView.as_view(), name= 'eliminarhorariolab'),
    path('normatividad/<int:pk>/remove/',EliminarNormaView.as_view(), name= 'eliminarnorma'),
    path('ubicaciones/<int:pk>/remove/',EliminarUbicacionView.as_view(), name= 'eliminarubicacion'),
    path('horariosprofesores/' , horariosprofesoresview, name= 'horariosprofesores'),
    path('ubicaciones/' , ubicacionesview, name= 'ubicaciones'),
    path('ubicaciones/importar/' , importarubicacionesview, name= 'importubi'),
    path('horarioslaboratorios/' , horarioslaboratoriosview, name= 'horarioslaboratorios'),
    path('horarioslaboratorios/importar/' , importarhorarioslaboratoriosview, name= 'importhorariolab'),
    path('calendario/',importarcalendarioview, name= 'calendario'),
    path('pensum/',importarpensumview, name= 'pensum'),
    path('casillero/',importarcasilleroview, name= 'casillero'),
    path('actividadesextra/',importaractividadesextraview, name= 'actividadesextra'),
    path('normatividad/' , normatividadview, name= 'normatividad'),
    path('normatividad/importar/' , importarnormatividadarchivo, name= 'importnormatividad'),
    path('mensajemasivo/' , mensajemasivoview, name= 'mensajemasivo'),
    path('actualizarbot/' , actualizarbotview, name= 'actualizarbot'),
    path('reglamento/' , reglamentoview, name= 'reglamento'),
    path('admin/', admin.site.urls),

    path('administradores/', include('django.contrib.auth.urls')),
    path('administradores/', include('administradores.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
