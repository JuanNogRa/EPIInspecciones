#import debug_toolbar
from django.urls import path, include
from gestion_fichas import views
from gestion_fichas.views import ReporteFichaPDF
####For favicon #######
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.conf.urls import url

from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)

urlpatterns = [

    path('',views.home, name = "home"),
    path('fichas_admin/',views.fichas_admin, name = "File_Admin"),
    path('hv_empty/',views.hv_por_crear, name = "hv_empty"),
    path('agregar_inspeccion/<int:id_producto>/',views.agregar_inspeccion, name = "agregar_inspeccion"),
    path('agregar_inspeccion_eslinga/<int:id_producto>/',views.agregar_inspeccion_eslinga, name = "agregar_inspeccion_eslinga"),
    path('agregar_inspeccion_lineas/<int:id_producto>/',views.agregar_inspeccion_lineas, name = "agregar_inspeccion_lineas"),
    path('agregar_inspeccion_casco/<int:id_producto>/',views.agregar_inspeccion_casco, name = "agregar_inspeccion_casco"),
    path('agregar_inspeccion_accesorio/<int:id_producto>/',views.agregar_inspeccion_accesorio, name = "agregar_inspeccion_accesorio"),
    path('agregar_inspeccion_silla/<int:id_producto>/',views.agregar_inspeccion_silla, name = "agregar_inspeccion_silla"),
    path('buscar_hv/',views.buscar_hv, name = "buscar_hv"),
    path('crear_hv/',views.crear_hv, name = "crear_hv"),
    path('hv/<int:numero_producto>/<str:equipo_alturas>/',views.hv_sheet, name = "hv_sheet"),
    path('buscar_inspector/',views.buscar_inspector, name = "buscar_inspector"),
    path('inspector/<str:codigo_inspector>/',views.perfil_inspector, name = "perfil_inspector"),
    path('profile/',views.UserView, name = "profile"),
    path('contactanos/',views.contactanos, name = "contactanos"),
    path('privacidad/',views.privacidad, name = "privacidad"),
    path('login/',views.login, name = "ingresar"),
    path('logout', views.logout, name= "logout"),
    path('registrar/',views.registrar, name = "registrar"),
    path('password/',views.change_password, name = "password"),
    path('update_registro/',views.update_registro, name = "update_registro"),
    url(r'^reporte_ficha_pdf/(?P<id_equipo>[0-9]+)/(?P<flag>[[0-1])/(?P<inspeccion_numero>[[0-9]+)/(?P<equipo_alturas>\w+)/(?P<Activate_photo>\w+)$',ReporteFichaPDF.as_view(), name="reporte_ficha_pdf"),
    #path("protected/", include("protected_media.urls")),
    #path('__debug__/', include(debug_toolbar.urls)),
    #path('perfil/',views.UserView, name = "perfil"),
    #url(r'^reporte_ficha_pdf/(?P<id_equipo>[0-9]+)/(?P<flag>[[0-1])/(?P<inspeccion_numero>[[0-9]+)/(?P<equipo_alturas>\w+)/(?P<Activate_photo>\w+)/$',ReporteFichaPDF.as_view(), name="reporte_ficha_pdf"),
    #url(r'^([0-9]+)/([0-1])/([0-9]+)/reporte_ficha_pdf/$',ReporteFichaPDF.as_view(), name="reporte_ficha_pdf"),
    #url(r'^reporte_personas_pdf/$',login_required(ReporteFichaPDF.as_view()), name="reporte_ficha_pdf"),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/gestion_fichas/img/epi_icon.ico')),
    url(r'^media/(?P<path>.*)', views.protected_access, name='protected'),

]
"""if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += url(r'^media/(?P<path>.*)', views.protected_access, name='protected'),"""

