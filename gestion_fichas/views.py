from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls.base import reverse_lazy
from gestion_fichas.forms import InspectionSheetFormAccesorios, InspectionSheetFormCascos, InspectionSheetFormEslingas, InspectionSheetFormLineasAnclajes, InspectionSheetFormSillas, LoginForm, CrearHvForm, SearchEquipmentForm, \
    InspectionSheetForm, RegisterEquipmentForm, UserForm, SearchInspectorForm 
from gestion_fichas.models import (EquiposAccesorioMetalicos, EquiposCascoSegurida, \
    EquiposEslinga, EquiposLineasAnclajes, EquiposSillasPerchas, InspeccionAccesorioMetalicos, InspeccionCascoSeguridad, InspeccionLineasAnclajes, InspeccionSillasPerchas, ReferenciasAccesorioMetalicos, ReferenciasArnes, EquiposArnes,
    InspeccionArnes as InspeccionArnesModel, InspeccionEslinga ,CustomUser, Inspectores, ReferenciasCascoSeguridad, ReferenciasEslingas, ReferenciasLineasAnclajes, ReferenciasSillasPerchas
    )
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect,FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from django.views.generic import View
from django.db import connection
from django.views.generic import FormView
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak,\
     PageTemplate, Spacer, FrameBreak, NextPageTemplate, SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.units import inch, cm
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4, landscape

from .create_pdf import ReportSheet, ReportSheet_eslingas, ReportSheet_lineas_anclajes, ReportSheet_accesorios,\
    ReportSheet_casco, ReportSheet_sillas

import os
import datetime
from itertools import chain
from django.core.paginator import Paginator

# Create your views here.
now = datetime.datetime.now()
only_date = now.date()
date_now = only_date.strftime("%Y-%m-%d")
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase.ttfonts import TTFont
#Importamos settings para poder tener a la mano la ruta de la carpeta media
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from reportlab.graphics import renderPDF
from django.core.files.base import ContentFile
class ReporteFichaPDF(View):

    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        id_equipo = kwargs['id_equipo']
        flag = kwargs['flag']
        inspeccion_numero = kwargs['inspeccion_numero']
        equipo_alturas=kwargs ['equipo_alturas']
        Activate_photo=kwargs['Activate_photo']
        if (flag =='1'):

            if(equipo_alturas=='1'):
                with transaction.atomic():

                    with connection.cursor() as cursor:
                        
                        cursor.execute("SELECT equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_arnes equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        if Activate_photo:
                            cursor.execute("SELECT IA.comentarios_adicionales, IA.codigo_qr_pdf, IA.fecha_inspeccion, users.first_name, users.last_name, IA.proxima_inspeccion, IA.veredicto, IA.reata_foto, IA.metalicas_foto, IA.costuras_foto, inspectores.foto_inspector, IA.reata_tienen_hoyos_agujeros, IA.reata_deshilachadas, IA.reata_cortadas_desgastadas, IA.reata_talladuras, IA.reata_torsion, IA.reata_suciedad, IA.reata_quemadura, IA.reata_salpicadura_rigidez, IA.reata_sustancia_quimica, IA.otros_arnes_cinta, IA.costuras_completas_continuas, IA.costuras_visibles, IA.costuras_indicador_impacto_activado,  IA.otros_arnes_costuras, IA.metalicas_completas, IA.metalicas_corrosion_oxido, IA.metalicas_deformacion, IA.metalicas_fisuras_golpes_hundimiento, IA.otros_metalicas, IA.observacion_reata_hoyo, IA.observacion_reata_deshilachadas, IA.observacion_reata_cortadas_desgastadas, IA.observacion_reata_talladuras, IA.observacion_reata_torsion, IA.observacion_reata_suciedad, IA.observacion_reata_quemadura, IA.observacion_reata_salpicadura_rigidez, IA.observacion_reata_sustancia_quimica, IA.observacion_reata_otros, IA.observacion_costuras_completas_continuas, IA.observacion_costuras_visibles, IA.observacion_costuras_indicador_impacto,  IA.observacion_costuras_otros, IA.observacion_metalicas_completas, IA.observacion_metalicas_corrosion_oxido, IA.observacion_metalicas_deformacion, IA.observacion_metalicas_fisuras_golpes , IA.observacion_metalicas_otros FROM  inspeccion_arnes IA, gestion_fichas_customuser users, inspectores WHERE IA.equipos_arnes_id = %s AND users.id = IA.user_id AND inspectores.user_id = users.id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        else:
                            cursor.execute("SELECT IA.comentarios_adicionales, IA.codigo_qr_pdf, IA.fecha_inspeccion, users.first_name, users.last_name, IA.proxima_inspeccion, IA.veredicto, IA.reata_foto, IA.metalicas_foto, IA.costuras_foto, IA.reata_tienen_hoyos_agujeros, IA.reata_deshilachadas, IA.reata_cortadas_desgastadas, IA.reata_talladuras, IA.reata_torsion, IA.reata_suciedad, IA.reata_quemadura, IA.reata_salpicadura_rigidez, IA.reata_sustancia_quimica, IA.otros_arnes_cinta, IA.costuras_completas_continuas, IA.costuras_visibles, IA.costuras_indicador_impacto_activado,  IA.otros_arnes_costuras, IA.metalicas_completas, IA.metalicas_corrosion_oxido, IA.metalicas_deformacion, IA.metalicas_fisuras_golpes_hundimiento, IA.otros_metalicas, IA.observacion_reata_hoyo, IA.observacion_reata_deshilachadas, IA.observacion_reata_cortadas_desgastadas, IA.observacion_reata_talladuras, IA.observacion_reata_torsion, IA.observacion_reata_suciedad, IA.observacion_reata_quemadura, IA.observacion_reata_salpicadura_rigidez, IA.observacion_reata_sustancia_quimica, IA.observacion_reata_otros, IA.observacion_costuras_completas_continuas, IA.observacion_costuras_visibles, IA.observacion_costuras_indicador_impacto,  IA.observacion_costuras_otros, IA.observacion_metalicas_completas, IA.observacion_metalicas_corrosion_oxido, IA.observacion_metalicas_deformacion, IA.observacion_metalicas_fisuras_golpes , IA.observacion_metalicas_otros FROM  inspeccion_arnes IA, gestion_fichas_customuser users WHERE IA.equipos_arnes_id = %s AND users.id = IA.user_id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)

                object_pdf =ReportSheet()
            elif(equipo_alturas=='2'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_eslingas equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        if Activate_photo:
                            cursor.execute("SELECT IE.comentarios_adicionales, IE.codigo_qr_pdf, IE.fecha_inspeccion, users.first_name, users.last_name, IE.proxima_inspeccion, IE.veredicto, IE.absorbedor_foto, IE.reata_foto, IE.metalicas_foto, IE.costuras_foto, inspectores.foto_inspector, IE.absorbedor_hoyos_desgarres, IE.absorbedor_costuras_sueltas_reventadas, IE.absorbedor_deterioro, IE.absorbedor_suciedad, IE.absorbedor_quemaduras_soldadura_cigarrillo, IE.absorbedor_salpicadura_rigidez, IE.otros_absorbedor, IE.reata_deshilachadas, IE.reata_desgastadas, IE.reata_talladuras, IE.reata_salpicadura_rigidez, IE.reata_torsion, IE.otros_cinta,  IE.metalicas_completas, IE.metalicas_corrosion_oxido, IE.metalicas_compuertas, IE.metalicas_deformacion_fisuras_golpes_hundimiento, IE.otros_metalicas, IE.costuras_completas_continuas, IE.costuras_visibles, IE.otros_costuras, IE.observacion_absorbedor_hoyos_desgarres, IE.observacion_absorbedor_costuras_sueltas_reventadas, IE.observacion_absorbedor_deterioro, IE.observacion_absorbedor_suciedad, IE.observacion_absorbedor_quemaduras_soldadura_cigarrillo, IE.observacion_absorbedor_salpicadura_rigidez, IE.observacion_otros_absorbedor, IE.observacion_reata_deshilachadas, IE.observacion_reata_desgastadas, IE.observacion_reata_talladuras, IE.observacion_reata_salpicadura_rigidez, IE.observacion_reata_torsion, IE.observacion_reata_otros, IE.observacion_metalicas_completas, IE.observacion_metalicas_corrosion_oxido, IE.observacion_metalicas_compuertas, IE.observacion_metalicas_deformacion_fisuras_golpes, IE.observacion_metalicas_otros, IE.observacion_costuras_completas_continuas , IE.observacion_costuras_visibles, IE.observacion_costuras_otros FROM  inspeccion_eslingas IE, gestion_fichas_customuser users, inspectores WHERE IE.equipos_eslingas_id = %s AND users.id = IE.user_id AND inspectores.user_id = users.id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        else:
                            cursor.execute("SELECT IE.comentarios_adicionales, IE.codigo_qr_pdf, IE.fecha_inspeccion, users.first_name, users.last_name, IE.proxima_inspeccion, IE.veredicto, IE.absorbedor_foto, IE.reata_foto, IE.metalicas_foto, IE.costuras_foto, IE.absorbedor_hoyos_desgarres, IE.absorbedor_costuras_sueltas_reventadas, IE.absorbedor_deterioro, IE.absorbedor_suciedad, IE.absorbedor_quemaduras_soldadura_cigarrillo, IE.absorbedor_salpicadura_rigidez, IE.otros_absorbedor, IE.reata_deshilachadas, IE.reata_desgastadas, IE.reata_talladuras, IE.reata_salpicadura_rigidez, IE.reata_torsion, IE.otros_cinta,  IE.metalicas_completas, IE.metalicas_corrosion_oxido, IE.metalicas_compuertas, IE.metalicas_deformacion_fisuras_golpes_hundimiento, IE.otros_metalicas, IE.costuras_completas_continuas, IE.costuras_visibles, IE.otros_costuras, IE.observacion_absorbedor_hoyos_desgarres, IE.observacion_absorbedor_costuras_sueltas_reventadas, IE.observacion_absorbedor_deterioro, IE.observacion_absorbedor_suciedad, IE.observacion_absorbedor_quemaduras_soldadura_cigarrillo, IE.observacion_absorbedor_salpicadura_rigidez, IE.observacion_otros_absorbedor, IE.observacion_reata_deshilachadas, IE.observacion_reata_desgastadas, IE.observacion_reata_talladuras, IE.observacion_reata_salpicadura_rigidez, IE.observacion_reata_torsion, IE.observacion_reata_otros, IE.observacion_metalicas_completas, IE.observacion_metalicas_corrosion_oxido, IE.observacion_metalicas_compuertas, IE.observacion_metalicas_deformacion_fisuras_golpes, IE.observacion_metalicas_otros, IE.observacion_costuras_completas_continuas , IE.observacion_costuras_visibles, IE.observacion_costuras_otros FROM  inspeccion_eslingas IE, gestion_fichas_customuser users WHERE IE.equipos_eslingas_id = %s AND users.id = IE.user_id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)

                object_pdf =ReportSheet_eslingas()
            elif(equipo_alturas=='3'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_lineas_anclajes equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        if Activate_photo:
                            cursor.execute("SELECT IL.comentarios_adicionales, IL.codigo_qr_pdf, IL.fecha_inspeccion, users.first_name, users.last_name, IL.proxima_inspeccion, IL.veredicto, IL.metalicas_foto, IL.reata_foto, IL.costuras_foto, inspectores.foto_inspector, IL.metalicas_completas, IL.metalicas_fisuras, IL.metalicas_corrosion_oxido, IL.metalicas_golpes_hundimiento, IL.metalicas_compuertas_ganchos, IL.otros_metalicas, IL.reata_deshilachadas, IL.reata_quemadura, IL.reata_torsion_talladuras, IL.reata_salpicadura_rigidez, IL.reata_ruptura, IL.otros_lineas_cinta, IL.costuras_completas_continuas, IL.costuras_visibles, IL.otros_lineas_costuras, IL.observacion_metalicas_completas, IL.observacion_metalicas_fisuras, IL.observacion_metalicas_corrosion_oxido, IL.observacion_metalicas_golpes_hundimientos, IL.observacion_metalicas_compuertas_ganchos, IL.observacion_metalicas_otros, IL.observacion_reata_deshilachadas, IL.observacion_reata_quemadura, IL.observacion_reata_torsion_talladuras, IL.observacion_reata_salpicadura_rigidez, IL.observacion_reata_ruptura, IL.observacion_otros_lineas_cinta, IL.observacion_costuras_completas_continuas, IL.observacion_costuras_visibles, IL.observacion_costuras_otros FROM  inspeccion_lineas_anclajes IL, gestion_fichas_customuser users, inspectores WHERE IL.equipos_lineas_anclajes_id = %s AND users.id = IL.user_id AND inspectores.user_id = users.id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        else:
                            cursor.execute("SELECT IL.comentarios_adicionales, IL.codigo_qr_pdf, IL.fecha_inspeccion, users.first_name, users.last_name, IL.proxima_inspeccion, IL.veredicto, IL.metalicas_foto, IL.reata_foto, IL.costuras_foto, IL.metalicas_completas, IL.metalicas_fisuras, IL.metalicas_corrosion_oxido, IL.metalicas_golpes_hundimiento, IL.metalicas_compuertas_ganchos, IL.otros_metalicas, IL.reata_deshilachadas, IL.reata_quemadura, IL.reata_torsion_talladuras, IL.reata_salpicadura_rigidez, IL.reata_ruptura, IL.otros_lineas_cinta, IL.costuras_completas_continuas, IL.costuras_visibles, IL.otros_lineas_costuras, IL.observacion_metalicas_completas, IL.observacion_metalicas_fisuras, IL.observacion_metalicas_corrosion_oxido, IL.observacion_metalicas_golpes_hundimientos, IL.observacion_metalicas_compuertas_ganchos, IL.observacion_metalicas_otros, IL.observacion_reata_deshilachadas, IL.observacion_reata_quemadura, IL.observacion_reata_torsion_talladuras, IL.observacion_reata_salpicadura_rigidez, IL.observacion_reata_ruptura, IL.observacion_otros_lineas_cinta, IL.observacion_costuras_completas_continuas, IL.observacion_costuras_visibles, IL.observacion_costuras_otros FROM  inspeccion_lineas_anclajes IL, gestion_fichas_customuser users WHERE IL.equipos_lineas_anclajes_id = %s AND users.id = IL.user_id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)

                object_pdf =ReportSheet_lineas_anclajes()
            elif (equipo_alturas=='4'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_cascos equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        if Activate_photo:
                            cursor.execute("SELECT IC.comentarios_adicionales, IC.codigo_qr_pdf, IC.fecha_inspeccion, users.first_name, users.last_name, IC.proxima_inspeccion, IC.veredicto, IC.casquete_foto, IC.suspencion_foto, IC.barbuquejo_foto, inspectores.foto_inspector, IC.casquete_fisuras_golpes_hundimiento, IC.casquete_quemaduras_deterioro_quimicos, IC.casquete_rayadura_decoloracion, IC.otros_casquete, IC.suspencion_completo, IC.suspencion_fisuras_golpes_hundimientos, IC.suspencion_torsion_estiramiento, IC.otros_suspencion, IC.barbuquejo_completo, IC.barbuquejo_cinta_deshilachada_rotas, IC.barbuquejo_salpicadura_pintura_rigidez_cinta, IC.otros_barbuquejo, IC.observacion_casquete_fisuras_golpes_hundimiento, IC.observacion_casquete_quemaduras_deterioro_quimicos, IC.observacion_casquete_rayadura_decoloracion, IC.observacion_casquete_otros, IC.observacion_suspencion_completo, IC.observacion_suspencion_fisuras_golpes_hundimientos, IC.observacion_suspencion_torsion_estiramiento, IC.observacion_suspencion_otros, IC.observacion_barbuquejo_completo, IC.observacion_barbuquejo_cinta_deshilachada_rotas, IC.observacion_barbuquejo_salpicadura_pintura_rigidez_cinta, IC.observacion_barbuquejo_otros FROM  inspeccion_casco IC, gestion_fichas_customuser users, inspectores WHERE IC.equipos_cascos_id = %s AND users.id = IC.user_id AND inspectores.user_id = users.id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        else:
                            cursor.execute("SELECT IC.comentarios_adicionales, IC.codigo_qr_pdf, IC.fecha_inspeccion, users.first_name, users.last_name, IC.proxima_inspeccion, IC.veredicto, IC.casquete_foto, IC.suspencion_foto, IC.barbuquejo_foto, IC.casquete_fisuras_golpes_hundimiento, IC.casquete_quemaduras_deterioro_quimicos, IC.casquete_rayadura_decoloracion, IC.otros_casquete, IC.suspencion_completo, IC.suspencion_fisuras_golpes_hundimientos, IC.suspencion_torsion_estiramiento, IC.otros_suspencion, IC.barbuquejo_completo, IC.barbuquejo_cinta_deshilachada_rotas, IC.barbuquejo_salpicadura_pintura_rigidez_cinta, IC.otros_barbuquejo, IC.observacion_casquete_fisuras_golpes_hundimiento, IC.observacion_casquete_quemaduras_deterioro_quimicos, IC.observacion_casquete_rayadura_decoloracion, IC.observacion_casquete_otros, IC.observacion_suspencion_completo, IC.observacion_suspencion_fisuras_golpes_hundimientos, IC.observacion_suspencion_torsion_estiramiento, IC.observacion_suspencion_otros, IC.observacion_barbuquejo_completo, IC.observacion_barbuquejo_cinta_deshilachada_rotas, IC.observacion_barbuquejo_salpicadura_pintura_rigidez_cinta, IC.observacion_barbuquejo_otros FROM  inspeccion_casco IC, gestion_fichas_customuser users WHERE IC.equipos_cascos_id = %s AND users.id = IC.user_id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)


                object_pdf =ReportSheet_casco()
            elif (equipo_alturas=='5'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_accesorios_metalicos equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        

                        if Activate_photo:
                            cursor.execute("SELECT IAM.comentarios_adicionales, IAM.codigo_qr_pdf, IAM.fecha_inspeccion, users.first_name, users.last_name, IAM.proxima_inspeccion, IAM.veredicto, IAM.mosquetones_foto, IAM.arrestador_poleas_foto, IAM.descendedores_anclajes_foto , inspectores.foto_inspector, IAM.mosquetones_fisuras_golpes_hundimiento, IAM.mosquetones_quemaduras_deterioro_quimicos, IAM.mosquetones_oxidacion_corrocion_mosquetones, IAM.mosquetones_bordes_filosos_rugosos, IAM.mosquetones_compuerta_libre, IAM.mosquetones_deformaciones, IAM.otros_mosquetones, IAM.arrestador_poleas_fisuras_golpes_hundimientos, IAM.arrestador_poleas_frenado_lisa, IAM.arrestador_poleas_oxidacion_corrocion, IAM.arrestador_poleas_bordes_filosos_rugosos, IAM.arrestador_poleas_compuerta_libre, \
                            IAM.arrestador_poleas_deformaciones, IAM.otros_arrestador_poleas, IAM.descendedores_anclajes_fisuras_golpes_hundimientos, IAM.descendedores_anclajes_contacto_lisa, IAM.descendedores_anclajes_oxidacion_corrocion, IAM.descendedores_anclajes_bordes_filosos_rugosos, IAM.descendedores_anclajes_desgaste_disminucion_metal, IAM.descendedores_anclajes_deformaciones, IAM.otros_descendedores_anclajes, IAM.observacion_mosquetones_fisuras_golpes_hundimiento, IAM.observacion_mosquetones_quemaduras_deterioro_quimicos, IAM.observacion_mosquetones_oxidacion_corrocion_mosquetones, IAM.observacion_mosquetones_bordes_filosos_rugosos, IAM.observacion_mosquetones_compuerta_libre, IAM.observacion_mosquetones_deformaciones, IAM.observacion_mosquetones_otros, \
                            IAM.observacion_arrestador_poleas_fisuras_golpes_hundimientos, IAM.observacion_arrestador_poleas_frenado_lisa, IAM.observacion_arrestador_poleas_oxidacion_corrocion, IAM.observacion_arrestador_poleas_bordes_filosos_rugosos, IAM.observacion_arrestador_poleas_compuerta_libre, IAM.observacion_arrestador_poleas_deformaciones, IAM.observacion_arrestador_poleas_otros, IAM.observacion_descendedores_anclajes_fisuras_golpes_hundimientos, IAM.observacion_descendedores_anclajes_frenado_lisa, IAM.observacion_descendedores_anclajes_oxidacion_corrocion, IAM.observacion_descendedores_anclajes_bordes_filosos_rugosos, IAM.observacion_descendedores_anclajes_desgaste_disminucion_metal, IAM.observacion_descendedores_anclajes_deformaciones, \
                            IAM.observacion_descendedores_anclajes_otros FROM  inspeccion_accesorio_metalicos IAM, gestion_fichas_customuser users, inspectores WHERE IAM.equipos_accesorios_metalicos_id = %s AND users.id = IAM.user_id AND inspectores.user_id = users.id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        else:
                            cursor.execute("SELECT IAM.comentarios_adicionales, IAM.codigo_qr_pdf, IAM.fecha_inspeccion, users.first_name, users.last_name, IAM.proxima_inspeccion, IAM.veredicto, IAM.mosquetones_foto, IAM.arrestador_poleas_foto, IAM.descendedores_anclajes_foto ,IAM.mosquetones_fisuras_golpes_hundimiento, IAM.mosquetones_quemaduras_deterioro_quimicos, IAM.mosquetones_oxidacion_corrocion_mosquetones, IAM.mosquetones_bordes_filosos_rugosos, IAM.mosquetones_compuerta_libre, IAM.mosquetones_deformaciones, IAM.otros_mosquetones, IAM.arrestador_poleas_fisuras_golpes_hundimientos, IAM.arrestador_poleas_frenado_lisa, IAM.arrestador_poleas_oxidacion_corrocion, IAM.arrestador_poleas_bordes_filosos_rugosos, IAM.arrestador_poleas_compuerta_libre, \
                            IAM.arrestador_poleas_deformaciones, IAM.otros_arrestador_poleas, IAM.descendedores_anclajes_fisuras_golpes_hundimientos, IAM.descendedores_anclajes_contacto_lisa, IAM.descendedores_anclajes_oxidacion_corrocion, IAM.descendedores_anclajes_bordes_filosos_rugosos, IAM.descendedores_anclajes_desgaste_disminucion_metal, IAM.descendedores_anclajes_deformaciones, IAM.otros_descendedores_anclajes, IAM.observacion_mosquetones_fisuras_golpes_hundimiento, IAM.observacion_mosquetones_quemaduras_deterioro_quimicos, IAM.observacion_mosquetones_oxidacion_corrocion_mosquetones, IAM.observacion_mosquetones_bordes_filosos_rugosos, IAM.observacion_mosquetones_compuerta_libre, IAM.observacion_mosquetones_deformaciones, IAM.observacion_mosquetones_otros, \
                            IAM.observacion_arrestador_poleas_fisuras_golpes_hundimientos, IAM.observacion_arrestador_poleas_frenado_lisa, IAM.observacion_arrestador_poleas_oxidacion_corrocion, IAM.observacion_arrestador_poleas_bordes_filosos_rugosos, IAM.observacion_arrestador_poleas_compuerta_libre, IAM.observacion_arrestador_poleas_deformaciones, IAM.observacion_arrestador_poleas_otros, IAM.observacion_descendedores_anclajes_fisuras_golpes_hundimientos, IAM.observacion_descendedores_anclajes_frenado_lisa, IAM.observacion_descendedores_anclajes_oxidacion_corrocion, IAM.observacion_descendedores_anclajes_bordes_filosos_rugosos, IAM.observacion_descendedores_anclajes_desgaste_disminucion_metal, IAM.observacion_descendedores_anclajes_deformaciones, \
                            IAM.observacion_descendedores_anclajes_otros FROM  inspeccion_accesorio_metalicos IAM, gestion_fichas_customuser users WHERE IAM.equipos_accesorios_metalicos_id = %s AND users.id = IAM.user_id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero])
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)

                object_pdf =ReportSheet_accesorios()

            elif (equipo_alturas=='6'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_sillas_perchas equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        if Activate_photo:
                            cursor.execute("SELECT ISP.comentarios_adicionales, ISP.codigo_qr_pdf, ISP.fecha_inspeccion, users.first_name, users.last_name, ISP.proxima_inspeccion, ISP.veredicto, ISP.cinta_reata_foto, ISP.costuras_foto, ISP.metalicas_foto, ISP.madera_foto, inspectores.foto_inspector, ISP.reata_tienen_hoyos_agujeros, ISP.reata_deshilachadas, ISP.reata_desgastadas, ISP.reata_talladuras, ISP.reata_torsion, ISP.reata_suciedad, ISP.reata_quemadura, ISP.reata_salpicadura_rigidez, ISP.reata_sustancia_quimica, ISP.otros_cinta_reata, ISP.costuras_completas_continuas, ISP.costuras_visibles, ISP.otros_silla_costuras, ISP.metalicas_completas, ISP.metalicas_corrosion, ISP.metalicas_deformacion, ISP.metalicas_fisuras_golpes, ISP.otros_metalicas, ISP.madera_golpes_rupturas, ISP.madera_polillas, ISP.madera_exceso_humeda, ISP.otros_madera, ISP.observacion_reata_tienen_hoyos_agujeros, ISP.observacion_reata_deshilachadas, ISP.observacion_reata_cortadas_desgastadas, ISP.observacion_reata_talladuras, ISP.observacion_reata_torsion, ISP.observacion_reata_suciedad, ISP.observacion_reata_quemadura, ISP.observacion_reata_salpicadura_rigidez, ISP.observacion_reata_sustancia_quimica, ISP.observacion_reata_otros, ISP.observacion_costuras_completas_continuas, ISP.observacion_costuras_visibles,  ISP.observacion_otros_silla_costuras, ISP.observacion_metalicas_completas, ISP.observacion_metalicas_corrosion_oxido, ISP.observacion_metalicas_deformacion, ISP.observacion_metalicas_fisuras_golpes , ISP.observacion_metalicas_otros, ISP.observacion_madera_golpes_rupturas, ISP.observacion_madera_polillas, ISP.observacion_madera_exceso_humeda, ISP.observacion_otros_madera FROM  inspeccion_sillas_perchas ISP, gestion_fichas_customuser users, inspectores WHERE ISP.equipos_sillas_perchas_id = %s AND users.id = ISP.user_id AND inspectores.user_id = users.id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        else:
                            cursor.execute("SELECT ISP.comentarios_adicionales, ISP.codigo_qr_pdf, ISP.fecha_inspeccion, users.first_name, users.last_name, ISP.proxima_inspeccion, ISP.veredicto, ISP.cinta_reata_foto, ISP.costuras_foto, ISP.metalicas_foto, ISP.madera_foto, ISP.reata_tienen_hoyos_agujeros, ISP.reata_deshilachadas, ISP.reata_desgastadas, ISP.reata_talladuras, ISP.reata_torsion, ISP.reata_suciedad, ISP.reata_quemadura, ISP.reata_salpicadura_rigidez, ISP.reata_sustancia_quimica, ISP.otros_cinta_reata, ISP.costuras_completas_continuas, ISP.costuras_visibles, ISP.otros_silla_costuras, ISP.metalicas_completas, ISP.metalicas_corrosion, ISP.metalicas_deformacion, ISP.metalicas_fisuras_golpes, ISP.otros_metalicas, ISP.madera_golpes_rupturas, ISP.madera_polillas, ISP.madera_exceso_humeda, ISP.otros_madera, ISP.observacion_reata_tienen_hoyos_agujeros, ISP.observacion_reata_deshilachadas, ISP.observacion_reata_cortadas_desgastadas, ISP.observacion_reata_talladuras, ISP.observacion_reata_torsion, ISP.observacion_reata_suciedad, ISP.observacion_reata_quemadura, ISP.observacion_reata_salpicadura_rigidez, ISP.observacion_reata_sustancia_quimica, ISP.observacion_reata_otros, ISP.observacion_costuras_completas_continuas, ISP.observacion_costuras_visibles,  ISP.observacion_otros_silla_costuras, ISP.observacion_metalicas_completas, ISP.observacion_metalicas_corrosion_oxido, ISP.observacion_metalicas_deformacion, ISP.observacion_metalicas_fisuras_golpes , ISP.observacion_metalicas_otros, ISP.observacion_madera_golpes_rupturas, ISP.observacion_madera_polillas, ISP.observacion_madera_exceso_humeda, ISP.observacion_otros_madera FROM  inspeccion_sillas_perchas ISP, gestion_fichas_customuser users WHERE ISP.equipos_sillas_perchas_id = %s AND users.id = ISP.user_id AND numero_inspeccion = %s", [id_equipo, inspeccion_numero]) 
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)

                object_pdf =ReportSheet_sillas()
                        
            buffer = BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas("Reporte"+ date_now+ ".pdf", pagesize=A4,bottomup=1,pageCompression=1)
            pdf.setTitle("Reporte de resultados equipo")
            pdf.setAuthor("EPI SAS")
            
            

            object_pdf.get_doc(
                pdf,
                buffer,
                inspection_info,
                equip_info,
                flag,
                Activate_photo
                )
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)

            #response.write(pdf)
        elif flag=='0':

            #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal

           # equipo = get_object_or_404(EquiposArnes, id = id_equipo)
            if(equipo_alturas=='1'):
                with transaction.atomic():

                    with connection.cursor() as cursor:


                        cursor.execute("SELECT equipos.codigo_qr, equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_arnes equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        cursor.execute("SELECT IA.fecha_inspeccion, users.first_name, users.last_name, IA.proxima_inspeccion, IA.veredicto, IA.reata_tienen_hoyos_agujeros, IA.reata_deshilachadas, IA.reata_cortadas_desgastadas, IA.reata_talladuras, IA.reata_torsion, IA.reata_suciedad, IA.reata_quemadura, IA.reata_salpicadura_rigidez, IA.reata_sustancia_quimica, IA.otros_arnes_cinta, IA.costuras_completas_continuas, IA.costuras_visibles, IA.costuras_indicador_impacto_activado,  IA.otros_arnes_costuras, IA.metalicas_completas, IA.metalicas_corrosion_oxido, IA.metalicas_deformacion, IA.metalicas_fisuras_golpes_hundimiento, IA.otros_metalicas FROM  inspeccion_arnes IA, gestion_fichas_customuser users WHERE IA.equipos_arnes_id= %s AND users.id = IA.user_id", [id_equipo])
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)
                object_pdf =ReportSheet()
            elif(equipo_alturas=='2'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.codigo_qr, equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_eslingas equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        cursor.execute("SELECT IE.fecha_inspeccion, users.first_name, users.last_name, IE.proxima_inspeccion, IE.veredicto, IE.absorbedor_hoyos_desgarres, IE.absorbedor_costuras_sueltas_reventadas, IE.absorbedor_deterioro, IE.absorbedor_suciedad, IE.absorbedor_quemaduras_soldadura_cigarrillo, IE.absorbedor_salpicadura_rigidez, IE.otros_absorbedor, IE.reata_deshilachadas, IE.reata_desgastadas, IE.reata_talladuras, IE.reata_salpicadura_rigidez, IE.reata_torsion, IE.otros_cinta,  IE.metalicas_completas, IE.metalicas_corrosion_oxido, IE.metalicas_compuertas, IE.metalicas_deformacion_fisuras_golpes_hundimiento, IE.otros_metalicas, IE.costuras_completas_continuas, IE.costuras_visibles, IE.otros_costuras FROM  inspeccion_eslingas IE, gestion_fichas_customuser users WHERE IE.equipos_eslingas_id = %s AND users.id = IE.user_id", [id_equipo]) 
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)
                object_pdf =ReportSheet_eslingas()
            elif(equipo_alturas=='3'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.codigo_qr, equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_lineas_anclajes equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        cursor.execute("SELECT IL.fecha_inspeccion, users.first_name, users.last_name, IL.proxima_inspeccion, IL.veredicto, IL.metalicas_completas, IL.metalicas_fisuras, IL.metalicas_corrosion_oxido, IL.metalicas_golpes_hundimiento, IL.metalicas_compuertas_ganchos, IL.otros_metalicas, IL.reata_deshilachadas, IL.reata_quemadura, IL.reata_torsion_talladuras, IL.reata_salpicadura_rigidez, IL.reata_ruptura, IL.otros_lineas_cinta, IL.costuras_completas_continuas, IL.costuras_visibles, IL.otros_lineas_costuras FROM  inspeccion_lineas_anclajes IL, gestion_fichas_customuser users WHERE IL.equipos_lineas_anclajes_id = %s AND users.id = IL.user_id", [id_equipo]) 
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)
                object_pdf =ReportSheet_lineas_anclajes()
            elif (equipo_alturas=='4'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.codigo_qr, equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_cascos equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        cursor.execute("SELECT IC.fecha_inspeccion, users.first_name, users.last_name, IC.proxima_inspeccion, IC.veredicto, IC.casquete_fisuras_golpes_hundimiento, IC.casquete_quemaduras_deterioro_quimicos, IC.casquete_rayadura_decoloracion, IC.otros_casquete, IC.suspencion_completo, IC.suspencion_fisuras_golpes_hundimientos, IC.suspencion_torsion_estiramiento, IC.otros_suspencion, IC.barbuquejo_completo, IC.barbuquejo_cinta_deshilachada_rotas, IC.barbuquejo_salpicadura_pintura_rigidez_cinta, IC.otros_barbuquejo FROM  inspeccion_casco IC, gestion_fichas_customuser users WHERE IC.equipos_cascos_id = %s AND users.id = IC.user_id", [id_equipo])
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)
                object_pdf =ReportSheet_casco()
            elif (equipo_alturas=='5'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.codigo_qr, equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_accesorios_metalicos equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        cursor.execute("SELECT IAM.fecha_inspeccion, users.first_name, users.last_name, IAM.proxima_inspeccion, IAM.veredicto, IAM.mosquetones_fisuras_golpes_hundimiento, IAM.mosquetones_quemaduras_deterioro_quimicos, IAM.mosquetones_oxidacion_corrocion_mosquetones, IAM.mosquetones_bordes_filosos_rugosos, IAM.mosquetones_compuerta_libre, IAM.mosquetones_deformaciones, IAM.otros_mosquetones, IAM.arrestador_poleas_fisuras_golpes_hundimientos, IAM.arrestador_poleas_frenado_lisa, IAM.arrestador_poleas_oxidacion_corrocion, IAM.arrestador_poleas_bordes_filosos_rugosos, IAM.arrestador_poleas_compuerta_libre, \
                            IAM.arrestador_poleas_deformaciones, IAM.otros_arrestador_poleas, IAM.descendedores_anclajes_fisuras_golpes_hundimientos, IAM.descendedores_anclajes_contacto_lisa, IAM.descendedores_anclajes_oxidacion_corrocion, IAM.descendedores_anclajes_bordes_filosos_rugosos, IAM.descendedores_anclajes_desgaste_disminucion_metal, IAM.descendedores_anclajes_deformaciones, IAM.otros_descendedores_anclajes\
                            FROM  inspeccion_accesorio_metalicos IAM, gestion_fichas_customuser users WHERE IAM.equipos_accesorios_metalicos_id = %s AND users.id = IAM.user_id", [id_equipo])
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)
                object_pdf =ReportSheet_accesorios()
            elif (equipo_alturas=='6'):
                with transaction.atomic():

                    with connection.cursor() as cursor:

                        cursor.execute("SELECT equipos.codigo_qr, equipos.numero_producto, equipos.fecha_fabricacion, equipos.codigo_interno FROM equipos_sillas_perchas equipos where equipos.id = %s", [id_equipo])
                        equip_info = ReporteFichaPDF.dictfetchall(cursor)

                        cursor.execute("SELECT ISP.fecha_inspeccion, users.first_name, users.last_name, ISP.proxima_inspeccion, ISP.veredicto, ISP.reata_tienen_hoyos_agujeros, ISP.reata_deshilachadas, ISP.reata_desgastadas, ISP.reata_talladuras, ISP.reata_torsion, ISP.reata_suciedad, ISP.reata_quemadura, ISP.reata_salpicadura_rigidez, ISP.reata_sustancia_quimica, ISP.otros_cinta_reata, ISP.costuras_completas_continuas, ISP.costuras_visibles, ISP.otros_silla_costuras, ISP.metalicas_completas, ISP.metalicas_corrosion, ISP.metalicas_deformacion, ISP.metalicas_fisuras_golpes, ISP.otros_metalicas, ISP.madera_golpes_rupturas, ISP.madera_polillas, ISP.madera_exceso_humeda, ISP.otros_madera FROM  inspeccion_sillas_perchas ISP, gestion_fichas_customuser users WHERE ISP.equipos_sillas_perchas_id = %s AND users.id = ISP.user_id", [id_equipo])
                        inspection_info = ReporteFichaPDF.dictfetchall(cursor)
                object_pdf =ReportSheet_sillas()
            buffer = BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer, pagesize=A4,bottomup=1)
            pdf.setTitle("Reporte de resultados equipo")
            pdf.setAuthor("EPI SAS")


            object_pdf.get_doc(
                pdf,
                buffer,
                inspection_info,
                equip_info,
                flag,
                Activate_photo
                )

            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)

        return response

def home(request):

    #tipo_usuario = request.user.has_perm('gestion_fichas.can_view_hv')
    return render(request,'gestion_fichas/home.html')

def logout (request):


    # Finalizamos la sesión

    if request.user.is_authenticated:

        do_logout(request)

    return render(request,'gestion_fichas/fichas_admin.html')
    #
    #  Redireccionamos a la portada
@csrf_exempt
@login_required(login_url="/login/")
@permission_required('gestion_fichas.can_view_hv', login_url='/login/')
def fichas_admin(request):

    return render(request,'gestion_fichas/fichas_admin.html')


def contactanos(request):

    return render(request,'gestion_fichas/contactanos.html')


def privacidad(request):

    return render(request,'gestion_fichas/politica_privacidad.html')


@csrf_exempt
#@login_required(login_url="/login/")
def buscar_hv(request):

    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = SearchEquipmentForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            numero_producto  = form.cleaned_data['numero_producto']
            equipo_alturas = form.cleaned_data['equipo_alturas']
            form = SearchEquipmentForm()
            if equipo_alturas == '1':
                ficha_inspeccion  = EquiposArnes.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    return HttpResponseRedirect(reverse('hv_sheet', args=(numero_producto,equipo_alturas)))

                else:

                    messages.error(request,'El arnes con este numero de lote no existe')

                    return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

            elif equipo_alturas == '2':
                ficha_inspeccion  = EquiposEslinga.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    return HttpResponseRedirect(reverse('hv_sheet', args=(numero_producto,equipo_alturas)))

                else:

                    messages.error(request,'La eslinga con este numero de lote no existe')

                    return render(request, "gestion_fichas/buscar_hv.html", {'form': form})
            
            elif equipo_alturas == '3':
                ficha_inspeccion  = EquiposLineasAnclajes.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    return HttpResponseRedirect(reverse('hv_sheet', args=(numero_producto,equipo_alturas)))

                else:

                    messages.error(request,'La linea ó el anclaje con este numero de lote no existe')

                    return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

            elif equipo_alturas == '4':
                ficha_inspeccion  = EquiposCascoSegurida.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    return HttpResponseRedirect(reverse('hv_sheet', args=(numero_producto,equipo_alturas)))

                else:

                    messages.error(request,'El casco de seguridad con este numero de lote no existe')

                    return render(request, "gestion_fichas/buscar_hv.html", {'form': form})
            
            elif equipo_alturas == '5':
                ficha_inspeccion  = EquiposAccesorioMetalicos.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    return HttpResponseRedirect(reverse('hv_sheet', args=(numero_producto,equipo_alturas)))

                else:
            
                    messages.error(request,'El accesorio metalico con este numero de lote no existe')

                    return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

            elif equipo_alturas == '6':
                ficha_inspeccion  = EquiposSillasPerchas.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    return HttpResponseRedirect(reverse('hv_sheet', args=(numero_producto,equipo_alturas)))

                else:

                    messages.error(request,'La silla ó la percha con este numero de lote no existe')

                    return render(request, "gestion_fichas/buscar_hv.html", {'form': form})
    else:

        form = SearchEquipmentForm()
        
        return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

def warning_inspeccion_f(date_now, date_warn):
    if  date_now >= date_warn:
        warning_inspeccion=True
    else:
        warning_inspeccion=False
    return warning_inspeccion
    
@csrf_exempt
def hv_sheet(request, numero_producto, equipo_alturas):
    global only_date
    equipo = None
    fk = None
    inspecciones = None
    numero_inspecciones = 0
    warning_inspeccion = False

    #if request.method == "POST":

        # Añadimos los datos recibidos al formulario
    """  form = SearchEquipmentForm(data=request.POST)
        # Si el formulario es válido...

        if form.is_valid():

            numero_producto  = form.cleaned_data['numero_producto']

            form = SearchEquipmentForm() """
    # select related, https://stackoverflow.com/questions/40926898/django-select-related-filter, se utiliza para hacer request a los datos
    # de otros modelos que esten relacionados a otros modelos con una fk Many-to-One, por ejemplo equipo obtiene los datos en el modelo EquiposArnes
    # que tengan en el campo el numero_producto escrito en el formulario, fk=equipo.referencias_arnes si se quita el select_related se genera una nueva
    # consulta en la base de datos, aumentando el acceso en disco, y aumentando el tiempo de respuesta del servidor.
    if equipo_alturas == '1':
        equipo = EquiposArnes.objects.select_related().get(numero_producto = numero_producto)

        if equipo.numero_producto != 0:
            fk = equipo.referencias_arnes
            internal_code = equipo.codigo_interno
            
            inspecciones = InspeccionArnesModel.objects.select_related().filter(
                    equipos_arnes = equipo
                    )

            ultima_inspeccion = inspecciones.last()
    
            if  ultima_inspeccion:

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                print("ELLL NUMERO ES",numero_inspecciones)

                warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)

            else:
                warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

            if not internal_code:
                return render(request,'gestion_fichas/hv_por_crear.html')

        else:

            messages.error(request,'El equipo con este numero de lote no existe')
    
    elif equipo_alturas == '2':
        equipo = EquiposEslinga.objects.select_related().get(numero_producto = numero_producto)
        
        if equipo.numero_producto != 0:
            fk = equipo.referencias_eslingas
            internal_code = equipo.codigo_interno

            inspecciones = InspeccionEslinga.objects.select_related().filter(
                    equipos_eslingas = equipo
                    )

            ultima_inspeccion = inspecciones.last()


            if  ultima_inspeccion:

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                print("ELLL NUMERO ES",numero_inspecciones)

                warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)
            else:
                warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

            if not internal_code:
                return render(request,'gestion_fichas/hv_por_crear.html')

        else:

            messages.error(request,'El equipo con este numero de lote no existe')

    elif equipo_alturas == '3':
        equipo = EquiposLineasAnclajes.objects.select_related().get(numero_producto = numero_producto)
        
        if equipo.numero_producto != 0:
            fk = equipo.referencias_anclajes
            internal_code = equipo.codigo_interno

            inspecciones = InspeccionLineasAnclajes.objects.select_related().filter(
                    equipos_lineas_anclajes = equipo
                    )

            ultima_inspeccion = inspecciones.last()


            if  ultima_inspeccion:

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                print("ELLL NUMERO ES",numero_inspecciones)

                warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)
                InspeccionSinObservacion=ultima_inspeccion.pdf_sinObservacion
            else:
                warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

            if not internal_code:

                return render(request,'gestion_fichas/hv_por_crear.html')
           
        else:

            messages.error(request,'El equipo con este numero de lote no existe')

    elif equipo_alturas == '4':
        equipo = EquiposCascoSegurida.objects.select_related().get(numero_producto = numero_producto)

        if equipo.numero_producto != 0:
            fk = equipo.referencias_casco
            internal_code = equipo.codigo_interno

            inspecciones = InspeccionCascoSeguridad.objects.select_related().filter(
                    equipos_cascos = equipo
                    )

            ultima_inspeccion = inspecciones.last()


            if  ultima_inspeccion:

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                print("ELLL NUMERO ES",numero_inspecciones)

                warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)
            else:
                warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

            if not internal_code:

                return render(request,'gestion_fichas/hv_por_crear.html')
            
        else:

            messages.error(request,'El equipo con este numero de lote no existe')
    
    elif equipo_alturas == '5':
        equipo = EquiposAccesorioMetalicos.objects.select_related().get(numero_producto = numero_producto)

        if equipo.numero_producto != 0:
            fk = equipo.referencias_accesorio_metalicos
            internal_code = equipo.codigo_interno

            inspecciones = InspeccionAccesorioMetalicos.objects.select_related().filter(
                    equipos_accesorios_metalicos = equipo
                    )

            ultima_inspeccion = inspecciones.last()



            if  ultima_inspeccion:

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                print("ELLL NUMERO ES",numero_inspecciones)

                
                warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)
            else:
                warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

            if not internal_code:

                return render(request,'gestion_fichas/hv_por_crear.html')
            
        else:

            messages.error(request,'El equipo con este numero de lote no existe')
    
    elif equipo_alturas == '6':
        equipo = EquiposSillasPerchas.objects.select_related().get(numero_producto = numero_producto)

        if equipo.numero_producto != 0:
            fk = equipo.referencias_sillas
            internal_code = equipo.codigo_interno

            inspecciones = InspeccionSillasPerchas.objects.select_related().filter(
                    equipos_sillas_perchas = equipo
                    )

            ultima_inspeccion = inspecciones.last()


            if  ultima_inspeccion:

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                print("ELLL NUMERO ES",numero_inspecciones)

                warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)
            else:
                warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)
                
            if not internal_code:

                return render(request,'gestion_fichas/hv_por_crear.html')
            
        else:

            messages.error(request,'El equipo con este numero de lote no existe')

    """ else:
        if equipo_alturas == '1':
            ficha_inspeccion  = EquiposArnes.objects.filter(numero_producto = numero_producto).exists()


            if ficha_inspeccion:

                equipo = EquiposArnes.objects.get(numero_producto = numero_producto)
                fk = equipo.referencias_arnes
                internal_code = equipo.codigo_interno

                if not internal_code:

                    return render(request,'gestion_fichas/hv_por_crear.html')

                ultima_inspeccion = InspeccionArnesModel.objects.filter(
                        equipos_arnes = equipo
                        ).last()

                if  ultima_inspeccion:

                    numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)

                    inspecciones = InspeccionArnesModel.objects.filter(
                            equipos_arnes = equipo
                            )

                    warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)

                else:
                    warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)
            else:

                messages.error(request,'El equipo con este numero de lote no existe')
        
        elif equipo_alturas == '2':
                ficha_inspeccion  = EquiposEslinga.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    equipo = EquiposEslinga.objects.get(numero_producto = numero_producto)
                    fk = equipo.referencias_eslingas
                    internal_code = equipo.codigo_interno

                    ultima_inspeccion = InspeccionEslinga.objects.filter(
                        equipos_eslingas = equipo
                        ).last()


                    if  ultima_inspeccion:

                        numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                        print("ELLL NUMERO ES",numero_inspecciones)

                        inspecciones = InspeccionEslinga.objects.filter(
                            equipos_eslingas = equipo
                            )

                        warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion.proxima_inspeccion)

                    else:
                        warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)
                else:

                    messages.error(request,'El equipo con este numero de lote no existe')
        
        elif equipo_alturas == '3':
                ficha_inspeccion  = EquiposLineasAnclajes.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    equipo = EquiposLineasAnclajes.objects.get(numero_producto = numero_producto)
                    fk = equipo.referencias_anclajes
                    internal_code = equipo.codigo_interno

                    ultima_inspeccion = InspeccionLineasAnclajes.objects.filter(
                        equipos_lineas_anclajes = equipo
                        ).last()


                    if  ultima_inspeccion:

                        numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                        print("ELLL NUMERO ES",numero_inspecciones)

                        inspecciones = InspeccionLineasAnclajes.objects.filter(
                            equipos_lineas_anclajes = equipo
                            )
                        
                        warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion,equipo)

                    else:
                        warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

                else:

                    messages.error(request,'El equipo con este numero de lote no existe')

        elif equipo_alturas == '4':
                ficha_inspeccion  = EquiposCascoSegurida.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    equipo = EquiposCascoSegurida.objects.get(numero_producto = numero_producto)
                    fk = equipo.referencias_casco
                    internal_code = equipo.codigo_interno

                    ultima_inspeccion = InspeccionCascoSeguridad.objects.filter(
                        equipos_cascos = equipo
                        ).last()


                    if  ultima_inspeccion:

                        numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                        print("ELLL NUMERO ES",numero_inspecciones)

                        inspecciones = InspeccionCascoSeguridad.objects.filter(
                            equipos_cascos = equipo
                            )

                        warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion,equipo)
                    else:
                        warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

                else:

                    messages.error(request,'El equipo con este numero de lote no existe')

        elif equipo_alturas == '5':
                ficha_inspeccion  = EquiposAccesorioMetalicos.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    equipo = EquiposAccesorioMetalicos.objects.get(numero_producto = numero_producto)
                    fk = equipo.referencias_accesorio_metalicos
                    internal_code = equipo.codigo_interno

                    ultima_inspeccion = InspeccionAccesorioMetalicos.objects.filter(
                        equipos_accesorios_metalicos = equipo
                        ).last()


                    if  ultima_inspeccion:

                        numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                        print("ELLL NUMERO ES",numero_inspecciones)

                        inspecciones = InspeccionAccesorioMetalicos.objects.filter(
                            equipos_accesorios_metalicos = equipo
                            )

                        warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion,equipo)
                    else:
                        warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

                else:

                    messages.error(request,'El equipo con este numero de lote no existe')

        elif equipo_alturas == '6':
                ficha_inspeccion  = EquiposSillasPerchas.objects.filter(numero_producto = numero_producto).exists()

                if ficha_inspeccion:

                    equipo = EquiposSillasPerchas.objects.get(numero_producto = numero_producto)
                    fk = equipo.referencias_sillas
                    internal_code = equipo.codigo_interno

                    ultima_inspeccion = InspeccionSillasPerchas.objects.filter(
                        equipos_sillas_perchas = equipo
                        ).last()


                    if  ultima_inspeccion:

                        numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)
                        print("ELLL NUMERO ES",numero_inspecciones)

                        inspecciones = InspeccionSillasPerchas.objects.filter(
                            equipos_sillas_perchas = equipo
                            )

                        warning_inspeccion=warning_inspeccion_f(only_date,ultima_inspeccion,equipo)
                    else:
                        warning_inspeccion=warning_inspeccion_f(only_date,equipo.fecha_puesta_en_uso)

                else:

                    messages.error(request,'El equipo con este numero de lote no existe')
        form = SearchEquipmentForm() """

    # if request.method == "POST" and 'inspection' in request.POST:
    #     return HttpResponseRedirect('agregar_inspeccion', args=(numero_producto,))
    return render(request,'gestion_fichas/hoja_de_vida_equipo.html', {
        "equipo": equipo, "referencia_arnes": fk,
        "numero_inspecciones": numero_inspecciones, "inspecciones":inspecciones,
        "warning_inspeccion":warning_inspeccion,
        "equipo_alturas":equipo_alturas,
        
        } #Variable de control para llevar a los formularios de agregar inspeccion para los demás equipos (eslingas,lineas de vida, casco,etc)
        )

@csrf_exempt
#@login_required(login_url="/login/")
def buscar_inspector(request):

    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = SearchInspectorForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            codigo_inspector  = form.cleaned_data['codigo_inspector']
            form = SearchInspectorForm()

            inspector  = Inspectores.objects.filter(codigo_inspector = codigo_inspector).exists()

            if inspector:
                return HttpResponseRedirect(reverse('perfil_inspector', args=(codigo_inspector,)))
            else:
                messages.error(request,'El inspector con este código no existe')
                return render(request, 'gestion_fichas/buscar_inspector.html', {'form': form})

    else:

        form = SearchInspectorForm()

        return render(request, 'gestion_fichas/buscar_inspector.html', {'form': form})


@csrf_exempt
def perfil_inspector(request, codigo_inspector):
    inspector  =  Inspectores.objects.select_related().get(codigo_inspector = codigo_inspector)
    full_name = str(inspector.user.first_name)+' '+str(inspector.user.last_name)
    email = inspector.user.email

    if (inspector.user.is_active): is_activate='Si' 
    else: is_activate='No'

    return render(request,'gestion_fichas/perfil_inspector.html', {"inspector":inspector, "full_name":full_name, "is_activate":is_activate, "email":email})

@csrf_exempt
@login_required(login_url="/login/")
def crear_hv(request):

    if request.method == "POST":

        # Añadimos los datos recibidos al formulario
        form = CrearHvForm(data=request.POST)
        # Si el formulario es válido...

        if form.is_valid():

            #show empty form

            # Recuperamos las credenciales validadas
            numero_producto  = form.cleaned_data['numero_producto']
            personal_a_cargo = form.cleaned_data['personal_a_cargo']
            fecha_puesta_en_uso  = form.cleaned_data['fecha_puesta_en_uso']
            codigo_interno = form.cleaned_data['codigo_interno']
            equipo_alturas = form.cleaned_data.get('equipo_alturas')
            
            form = CrearHvForm()

            # articulos = EquiposArnes.objects.filter(nombre__icontains =producto)
            # Verificamos las credenciales del usuario
            if equipo_alturas == '1':
                ficha_inspeccion = EquiposArnes.objects.filter(numero_producto = numero_producto).exists()
                # Si existe un usuario con ese nombre y contraseña

                if ficha_inspeccion:

                    equipo = EquiposArnes.objects.get(numero_producto = numero_producto)
                    internal_code = equipo.codigo_interno
                    numero_serie = equipo.numero_producto

                    if internal_code:

                        messages.info(request, 'La hoja de vida del arnes con número de serie '+str(numero_serie)+' ya existe')

                    else:

                        EquiposArnes.objects.filter(numero_producto=numero_producto ).update(personal_a_cargo = personal_a_cargo, fecha_puesta_en_uso = fecha_puesta_en_uso, codigo_interno = codigo_interno, user = request.user )
                        messages.success(request, 'Hoja de vida del arnes con número de serie '+str(numero_serie)+' creada con exito')
                    # object = EquiposArnes.objects.get(numero_producto = numero_producto)

                else:

                    messages.error(request,'El arnes con este numero de lote no existe')

            elif equipo_alturas == '2':
                ficha_inspeccion = EquiposEslinga.objects.filter(numero_producto = numero_producto).exists()
                # Si existe un usuario con ese nombre y contraseña

                if ficha_inspeccion:

                    equipo = EquiposEslinga.objects.get(numero_producto = numero_producto)
                    internal_code = equipo.codigo_interno
                    numero_serie = equipo.numero_producto

                    if internal_code:

                        messages.info(request, 'La hoja de vida de la eslinga con número de serie '+str(numero_serie)+' ya existe')

                    else:

                        EquiposEslinga.objects.filter(numero_producto=numero_producto ).update(personal_a_cargo = personal_a_cargo, fecha_puesta_en_uso = fecha_puesta_en_uso, codigo_interno = codigo_interno, user = request.user )
                        messages.success(request, 'Hoja de vida de la eslinga con número de serie '+str(numero_serie)+' creada con exito')
                    # object = EquiposArnes.objects.get(numero_producto = numero_producto)

                else:

                    messages.error(request,'La eslinga con este numero de lote no existe')
            
            elif equipo_alturas == '3':
                ficha_inspeccion = EquiposLineasAnclajes.objects.filter(numero_producto = numero_producto).exists()
                # Si existe un usuario con ese nombre y contraseña

                if ficha_inspeccion:

                    equipo = EquiposLineasAnclajes.objects.get(numero_producto = numero_producto)
                    internal_code = equipo.codigo_interno
                    numero_serie = equipo.numero_producto

                    if internal_code:

                        messages.info(request, 'La hoja de vida de la linea ó el anclaje con número de serie '+str(numero_serie)+' ya existe')

                    else:

                        EquiposLineasAnclajes.objects.filter(numero_producto=numero_producto ).update(personal_a_cargo = personal_a_cargo, fecha_puesta_en_uso = fecha_puesta_en_uso, codigo_interno = codigo_interno, user = request.user )
                        messages.success(request, 'Hoja de vida de la linea ó el anclaje con número de serie '+str(numero_serie)+' creada con exito')
                    # object = EquiposArnes.objects.get(numero_producto = numero_producto)

                else:

                    messages.error(request,'La linea ó el anclaje arnes con este numero de lote no existe')
            
            elif equipo_alturas == '4':
                ficha_inspeccion = EquiposCascoSegurida.objects.filter(numero_producto = numero_producto).exists()
                # Si existe un usuario con ese nombre y contraseña

                if ficha_inspeccion:

                    equipo = EquiposCascoSegurida.objects.get(numero_producto = numero_producto)
                    internal_code = equipo.codigo_interno
                    numero_serie = equipo.numero_producto

                    if internal_code:

                        messages.info(request, 'La hoja de vida del casco con número de serie '+str(numero_serie)+' ya existe')

                    else:

                        EquiposCascoSegurida.objects.filter(numero_producto=numero_producto ).update(personal_a_cargo = personal_a_cargo, fecha_puesta_en_uso = fecha_puesta_en_uso, codigo_interno = codigo_interno, user = request.user )
                        messages.success(request, 'Hoja de vida del casco con número de serie '+str(numero_serie)+' creada con exito')
                    # object = EquiposArnes.objects.get(numero_producto = numero_producto)

                else:

                    messages.error(request,'El casco con este numero de lote no existe')
            
            elif equipo_alturas == '5':
                ficha_inspeccion = EquiposAccesorioMetalicos.objects.filter(numero_producto = numero_producto).exists()
                # Si existe un usuario con ese nombre y contraseña

                if ficha_inspeccion:

                    equipo = EquiposAccesorioMetalicos.objects.get(numero_producto = numero_producto)
                    internal_code = equipo.codigo_interno
                    numero_serie = equipo.numero_producto

                    if internal_code:

                        messages.info(request, 'La hoja de vida del accesorio metálico con número de serie '+str(numero_serie)+' ya existe')

                    else:

                        EquiposAccesorioMetalicos.objects.filter(numero_producto=numero_producto ).update(personal_a_cargo = personal_a_cargo, fecha_puesta_en_uso = fecha_puesta_en_uso, codigo_interno = codigo_interno, user = request.user )
                        messages.success(request, 'Hoja de vida del accesorio metálico con número de serie '+str(numero_serie)+' creada con exito')
                    # object = EquiposArnes.objects.get(numero_producto = numero_producto)

                else:

                    messages.error(request,'El accesorio metálico con este numero de lote no existe')

            elif equipo_alturas == '6':
                ficha_inspeccion = EquiposSillasPerchas.objects.filter(numero_producto = numero_producto).exists()
                # Si existe un usuario con ese nombre y contraseña

                if ficha_inspeccion:

                    equipo = EquiposSillasPerchas.objects.get(numero_producto = numero_producto)
                    internal_code = equipo.codigo_interno
                    numero_serie = equipo.numero_producto

                    if internal_code:

                        messages.info(request, 'La hoja de vida del de la silla ó percha con número de serie '+str(numero_serie)+' ya existe')

                    else:

                        EquiposSillasPerchas.objects.filter(numero_producto=numero_producto ).update(personal_a_cargo = personal_a_cargo, fecha_puesta_en_uso = fecha_puesta_en_uso, codigo_interno = codigo_interno, user = request.user )
                        messages.success(request, 'Hoja de vida de la silla ó percha con número de serie '+str(numero_serie)+' creada con exito')
                    # object = EquiposArnes.objects.get(numero_producto = numero_producto)

                else:

                    messages.error(request,'La silla ó percha con este numero de lote no existe')
                
    else:

        form = CrearHvForm()

    return render(request, "gestion_fichas/crear_hv.html", {'form': form})


def hv_por_crear(request):

    # filename = employee + ".pdf"
    # filename  = 'Referencias/PDF/MV-FT-008-_50-12-2.pdf'
    # filepath = os.path.join(settings.MEDIA_ROOT, filename)
    # print(filepath)
    # return FileResponse(open(filepath, 'rb'),content_type='application/pdf')
    #content_type='application/pdf'
    return render(request,'gestion_fichas/hv_por_crear.html')

def create_variables_names():

    form_fields_checkbox = [
        'tienen_hoyos_agujeros',
        'deshilachadas',
        'cortadas_desgastadas',
        'talladuras',
        'torsion',
        'suciedad',
        'quemadura',
        'salpicadura_rigidez',
        'sustancia_quimica',
        'otros_arnes_cinta',
        'costuras_completas_continuas',
        'visibles',
        'indicador_impacto_activado',
        'otros_arnes_costuras',
        'metalicas_completas',
        'corrosion_oxido',
        'deformacion',
        'fisuras_golpes',
        'otros_metalicas',
        ]
    form_fields_hints = [
        'tienen_hoyos_agujeros_observacion',
        'deshilachadas_observacion',
        'cortadas_desgastadas_observacion',
        'talladuras_observacion',
        'torsion_observacion',
        'suciedad_observacion',
        'quemadura_observacion',
        'salpicadura_observacion',
        'sustancia_observacion',
        'otros_arnes_cinta_observacion',
        'costuras_completas_continuas_observacion',
        'visibles_observacion',
        'indicador_impacto_activado_observacion',
        'otros_arnes_costuras_observacion',
        'metalicas_completas_observacion',
        'corrosion_oxido_observacion',
        'deformacion_observacion',
        'fisuras_golpes_observacion',
        'otros_metalicas_observacion',
        ]
    return form_fields_checkbox, form_fields_hints

def create_variables_eslinga_names():

    form_fields_checkbox = [
        'presenta_hoyos_desgarres', 
        'costuras_sueltas_reventadas', 
        'deterioro', 
        'presenta_suciedad', 
        'quemaduras_soldadura_cigarrillo',
        'salpicadura_rigidez_cintas',
        'otros_eslingas_absorbedor',
        'deshilachadas', 
        'desgastadas', 
        'talladuras', 
        'salpicadura_rigidez', 
        'torsion',
        'otros_eslingas_cinta',
        'metalicas_completas', 
        'corrosion_oxido', 
        'compuertas_ganchos',
        'deformacion_fisuras_golpes_hundimientos', 
        'otros_metalicas',
        'costuras_completas_continuas', 
        'visibles', 
        'otros_costura',
        ]
    form_fields_hints = [
        'presenta_hoyos_desgarres_observacion', 
        'costuras_sueltas_reventadas_observacion', 
        'deterioro_observacion', 
        'presenta_suciedad_observacion', 
        'quemaduras_soldadura_cigarrillo_observacion',
        'salpicadura_rigidez_cintas_observacion',
        'otros_eslingas_absorbedor_observacion',
        'deshilachadas_observacion', 
        'desgastadas_observacion', 
        'talladuras_observacion', 
        'salpicadura_rigidez_observacion', 
        'torsion_observacion', 
        'otros_eslingas_cinta_observacion',
        'metalicas_completas_observacion', 
        'corrosion_oxido_observacion', 
        'compuertas_ganchos_observacion',
        'deformacion_fisuras_golpes_hundimientos_observacion', 
        'otros_metalicas_observacion',
        'costuras_completas_continuas_observacion', 
        'visibles_observacion', 
        'otros_eslingas_costuras_observacion',
        ]
    return form_fields_checkbox, form_fields_hints

def create_variables_lineas_names():

    form_fields_checkbox = [
        'metalicas_completas', 
        'fisuras',
        'corrosion_oxido',
        'golpes_hundimientos',
        'compuertas_ganchos',  
        'otros_metalicas',
        'deshilachadas', 
        'quemadura_soldadura_cigarrillo_etc',
        'torsion_talladuras', 
        'salpicadura_rigidez', 
        'ruptura', 
        'otros_lineas_cinta',
        'costuras_completas_continuas', 
        'visibles', 
        'otros_lineas_costuras',
        ]
    form_fields_hints = [
        'metalicas_completas_observacion', 
        'fisuras_observacion',
        'corrosion_oxido_observacion',
        'golpes_hundimientos_observacion',
        'compuertas_ganchos_observacion',  
        'otros_metalicas_observacion',
        'deshilachadas_observacion', 
        'quemadura_soldadura_cigarrillo_etc_observacion',
        'torsion_talladuras_observacion', 
        'salpicadura_rigidez_observacion',
        'ruptura_observacion', 
        'otros_lineas_cinta_observacion',
        'costuras_completas_continuas_observacion', 
        'visibles_observacion', 
        'otros_lineas_costuras_observacion',
        ]
    return form_fields_checkbox, form_fields_hints

def create_variables_casco_names():

    form_fields_checkbox = [
        'fisuras_golpes_hundimientos_casquete', 
        'quemaduras_deteriorquimicos',
        'rayadura_decoloracion',
        'otros_casquete',
        'completo_suspencion', 
        'fisuras_golpes_hundimientos_suspencion',
        'torsion_estiramiento',  
        'otros_suspencion',
        'completo_barbuquejo', 
        'cinta_deshilachada_rotas', 
        'salpicadura_pintura_rigidez_cinta',
        'otros_barbuquejo',
        ]
    form_fields_hints = [
        'fisuras_golpes_hundimientos_casquete_observacion', 
        'quemaduras_deteriorquimicos_observacion',
        'rayadura_decoloracion_observacion',
        'otros_casquete_observacion',
        'completo_suspencion_observacion', 
        'fisuras_golpes_hundimientos_suspencion_observacion',
        'torsion_estiramiento_observacion',  
        'otros_suspencion_observacion',
        'completo_barbuquejo_observacion', 
        'cinta_deshilachada_rotas_observacion', 
        'salpicadura_pintura_rigidez_cinta_observacion',
        'otros_barbuquejo_observacion',
        ]
    return form_fields_checkbox, form_fields_hints

def create_variables_accesorio_names():

    form_fields_checkbox = [
        'fisuras_golpes_hundimientos_mosquetones', 
        'quemaduras_deteriorquimicos',
        'oxidacion_corrocion_mosquetones',
        'bordes_filosos_rugosos_mosquetones',
        'compuerta_libre_mosquetones',
        'deformaciones_mosquetones',
        'otros_mosquetones',
        'fisuras_golpes_hundimientos_arrestador',
        'frenado_lisa',
        'oxidacion_corrocion_arrestador',
        'bordes_filosos_rugosos_arrestador',
        'compuerta_libre_arrestador',
        'deformaciones_arrestador',
        'otros_arrestador',
        'fisuras_golpes_hundimientos_descendedor',
        'contacto_lisa',
        'oxidacion_corrocion_descendedor',
        'bordes_filosos_rugosos_descendedor',
        'desgaste_disminucionmetal',
        'deformaciones_descendedor',
        'otros_descendedor',
        ]
    form_fields_hints = [
        'fisuras_golpes_hundimientos_mosquetones_observacion', 
        'quemaduras_deteriorquimicos_observacion',
        'oxidacion_corrocion_mosquetones_observacion',
        'bordes_filosos_rugosos_mosquetones_observacion',
        'compuerta_libre_mosquetones_observacion',
        'deformaciones_mosquetones_observacion',
        'otros_mosquetones_observacion',
        'fisuras_golpes_hundimientos_arrestador_observacion',
        'frenado_lisa_observacion',
        'oxidacion_corrocion_arrestador_observacion',
        'bordes_filosos_rugosos_arrestador_observacion',
        'compuerta_libre_arrestador_observacion',
        'deformaciones_arrestador_observacion',
        'otros_arrestador_observacion',
        'fisuras_golpes_hundimientos_descendedor_observacion',
        'contacto_lisa_observacion',
        'oxidacion_corrocion_descendedor_observacion',
        'bordes_filosos_rugosos_descendedor_observacion',
        'desgaste_disminucionmetal_observacion',
        'deformaciones_descendedor_observacion',
        'otros_descendedor_observacion',
        ]
    return form_fields_checkbox, form_fields_hints

def create_variables_silla_names():

    form_fields_checkbox = [
        'tienen_hoyos_agujeros', 
        'deshilachadas',
        'cortadas_desgastadas',
        'talladuras',
        'torsion',
        'suciedad',
        'quemadura',
        'salpicadura_rigidez',
        'sustancia_quimica',
        'otros_silla_cinta',
        'costuras_completas_continuas',
        'visibles',
        'otros_silla_costuras',
        'metalicas_completas',
        'corrosion_oxido',
        'deformacion',
        'fisuras_golpes',
        'otros_metalicas',
        'golpes_rupturas', 
        'pollillas_gorgojos', 
        'humeda_pintura', 
        'otros_madera',
        ]
    form_fields_hints = [
        'tienen_hoyos_agujeros_observacion', 
        'deshilachadas_observacion', 
        'cortadas_desgastadas_observacion', 
        'talladuras_observacion', 
        'torsion_observacion', 
        'suciedad_observacion', 
        'quemadura_observacion', 
        'salpicadura_observacion', 
        'sustancia_observacion', 
        'otros_silla_cinta_observacion',
        'costuras_completas_continuas_observacion',
        'visibles_observacion',   
        'otros_silla_costuras_observacion',
        'metalicas_completas_observacion', 
        'corrosion_oxido_observacion', 
        'deformacion_observacion', 
        'fisuras_golpes_observacion', 
        'otros_metalicas_observacion',
        'golpes_rupturas_observacion', 
        'pollillas_gorgojos_observacion', 
        'humeda_pintura_observacion', 
        'otros_madera_observacion',
        ]
    return form_fields_checkbox, form_fields_hints

# @transaction.atomic
# def subir_datos():

#     ficha_inspeccion = EquiposArnes.objects.filter(numero_producto = numero_producto).exists()

 #

@csrf_exempt
def login(request):

    # Creamos el formulario de autenticación vacío
    if request.user.is_authenticated:

        return render(request,'gestion_fichas/buscar_hv.html')

    else:

        if request.method == "POST":
            # Añadimos los datos recibidos al formulario
            form = LoginForm(data=request.POST)
            # Si el formulario es válido...
            if form.is_valid():
                # Recuperamos las credenciales validadas
                username = form.cleaned_data['Usuario']
                password = form.cleaned_data['Contraseña']

                # Verificamos las credenciales del usuario
                user = authenticate(username = username, password=password)

                # Si existe un usuario con ese nombre y contraseña
                if user is not None:
                    # Hacemos el login manualmente
                    do_login(request, user)
                    if user.is_superuser:
                        return HttpResponseRedirect('/admin')
                    # Y le redireccionamos a la portada
                    #return redirect('profile/')
                    if 'next' in request.POST:
                        
                        return HttpResponseRedirect(request.POST.get('next'))

                    else:

                        return HttpResponseRedirect('/')

                else:

                    messages.error(request,'Usuario o contraseña incorrectos')

                    return HttpResponseRedirect('/login')

        else:

            form = LoginForm()

        # Si llegamos al final renderizamos el formulario
        return render(request, "gestion_fichas/login.html", {'form': form})

@csrf_exempt
@login_required(login_url="/login/")
def registrar(request):

    if 'term' in request.GET:

        autocomplete_name = ReferenciasArnes.objects.filter(referencia__icontains= request.GET.get('term'))
        titles = list()
        print(autocomplete_name)
        for referencias in autocomplete_name:
            titles.append(referencias.referencia)

        return JsonResponse(titles, safe=False)


    if request.method == "POST":
            # Añadimos los datos recibidos al formulario
            form = RegisterEquipmentForm (data=request.POST)
            # Si el formulario es válido...
            if form.is_valid():

                global date_now

                referencia_equipo = form.cleaned_data['referencia']
                numero_producto = form.cleaned_data['numero_producto']
                lote_fabricacion= form.cleaned_data['lote_fabricacion']
                linea_produccion = form.cleaned_data['linea_produccion']
                cantidad_productos = form.cleaned_data['cantidad_productos_agregar']
                fecha_fabricacion = form.cleaned_data['fecha_fabricacion']
                equipo_alturas = form.cleaned_data.get('equipo_alturas')

                # Verificamos las credenciales del usuario
                form = RegisterEquipmentForm ()
                check_lote = str(lote_fabricacion)+str(linea_produccion)+str(numero_producto).zfill(2)
                if equipo_alturas=='1':
                    if EquiposArnes.objects.filter(numero_producto = check_lote).exists() or not(ReferenciasArnes.objects.filter(referencia = referencia_equipo).exists()):

                        messages.error(request,'Error, verifique la referencia o el lote del equipo')
                        return HttpResponseRedirect('/registrar/')

                    else:

                        referencia_objeto=ReferenciasArnes.objects.get(referencia = referencia_equipo)

                        if cantidad_productos == 1:

                            producto = str(lote_fabricacion)+str(linea_produccion)+str(numero_producto).zfill(2)

                            equipo_add = EquiposArnes(
                                numero_producto = producto,
                                referencias_arnes=referencia_objeto,
                                user=request.user,
                                fecha_fabricacion=fecha_fabricacion,
                                personal_a_cargo = '',
                                veredicto = True,
                                codigo_interno='',
                                )

                            equipo_add.save()

                        else:

                            with transaction.atomic():

                                for lote in range(numero_producto,cantidad_productos+numero_producto):
                                    numero_unico = str(lote)
                                    numero = numero_unico.zfill(2)

                                    producto = str(lote_fabricacion)+str(linea_produccion)+numero

                                    query = EquiposArnes(
                                            numero_producto = producto,
                                            referencias_arnes=referencia_objeto,
                                            user=CustomUser.objects.get(username= request.user),
                                            fecha_fabricacion=fecha_fabricacion,
                                            personal_a_cargo = '',
                                            veredicto = True,
                                            codigo_interno='',
                                        )
                                    query.save()



                            # equipos = []
                            # print("REEEF", referencia_objeto)
                            # for lote in range(numero_producto,cantidad_productos+numero_producto):

                            #     equipos.append(EquiposArnes(
                            #                 numero_producto = lote,
                            #                 referencias_arnes=referencia_objeto,
                            #                 user=CustomUser.objects.get(username= request.user),
                            #                 fecha_fabricacion=fecha_fabricacion,
                            #                 personal_a_cargo = '',
                            #                 veredicto = True,
                            #                 codigo_interno='',
                            #             ))
                            # print("Equiposss",equipos)
                            # EquiposArnes.objects.load_data(equipos)


                            #EquiposArnes.objects.load_data(equipos)
                        # hello = equipos[1]
                        # print("LOS EQUIPOS SON", hello.fecha_fabricacion)
                        # hello.save()
                        # # Insert all the polls at once.

                        messages.success(request,'Equipos Insertados con exito')

                elif equipo_alturas=='2':
                    if EquiposEslinga.objects.filter(numero_producto = check_lote).exists() or not(ReferenciasEslingas.objects.filter(referencia = referencia_equipo).exists()):

                        messages.error(request,'Error, verifique la referencia o el lote del equipo')
                        return HttpResponseRedirect('/registrar/')

                    else:

                        referencia_objeto=ReferenciasEslingas.objects.get(referencia = referencia_equipo)

                        if cantidad_productos == 1:

                            producto = str(lote_fabricacion)+str(linea_produccion)+str(numero_producto).zfill(2)

                            equipo_add = EquiposEslinga(
                                numero_producto = producto,
                                referencias_eslingas=referencia_objeto,
                                user=request.user,
                                fecha_fabricacion=fecha_fabricacion,
                                personal_a_cargo = '',
                                veredicto = True,
                                codigo_interno='',
                                )

                            equipo_add.save()

                        else:

                            with transaction.atomic():

                                for lote in range(numero_producto,cantidad_productos+numero_producto):
                                    numero_unico = str(lote)
                                    numero = numero_unico.zfill(2)

                                    producto = str(lote_fabricacion)+str(linea_produccion)+numero

                                    query = EquiposEslinga(
                                            numero_producto = producto,
                                            referencias_eslingas=referencia_objeto,
                                            user=CustomUser.objects.get(username= request.user),
                                            fecha_fabricacion=fecha_fabricacion,
                                            personal_a_cargo = '',
                                            veredicto = True,
                                            codigo_interno='',
                                        )
                                    query.save()

                        messages.success(request,'Equipos Insertados con exito')
                
                elif equipo_alturas=='3':
                    if EquiposLineasAnclajes.objects.filter(numero_producto = check_lote).exists() or not(ReferenciasLineasAnclajes.objects.filter(referencia = referencia_equipo).exists()):

                        messages.error(request,'Error, verifique la referencia o el lote del equipo')
                        return HttpResponseRedirect('/registrar/')

                    else:

                        referencia_objeto=ReferenciasLineasAnclajes.objects.get(referencia = referencia_equipo)

                        if cantidad_productos == 1:

                            producto = str(lote_fabricacion)+str(linea_produccion)+str(numero_producto).zfill(2)

                            equipo_add = EquiposLineasAnclajes(
                                numero_producto = producto,
                                referencias_anclajes=referencia_objeto,
                                user=request.user,
                                fecha_fabricacion=fecha_fabricacion,
                                personal_a_cargo = '',
                                veredicto = True,
                                codigo_interno='',
                                )

                            equipo_add.save()

                        else:

                            with transaction.atomic():

                                for lote in range(numero_producto,cantidad_productos+numero_producto):
                                    numero_unico = str(lote)
                                    numero = numero_unico.zfill(2)

                                    producto = str(lote_fabricacion)+str(linea_produccion)+numero

                                    query = EquiposLineasAnclajes(
                                            numero_producto = producto,
                                            referencias_anclajes=referencia_objeto,
                                            user=CustomUser.objects.get(username= request.user),
                                            fecha_fabricacion=fecha_fabricacion,
                                            personal_a_cargo = '',
                                            veredicto = True,
                                            codigo_interno='',
                                        )
                                    query.save()

                        messages.success(request,'Equipos Insertados con exito')
                
                elif equipo_alturas=='4':
                    if EquiposCascoSegurida.objects.filter(numero_producto = check_lote).exists() or not(ReferenciasCascoSeguridad.objects.filter(referencia = referencia_equipo).exists()):

                        messages.error(request,'Error, verifique la referencia o el lote del equipo')
                        return HttpResponseRedirect('/registrar/')

                    else:

                        referencia_objeto=ReferenciasCascoSeguridad.objects.get(referencia = referencia_equipo)

                        if cantidad_productos == 1:

                            producto = str(lote_fabricacion)+str(linea_produccion)+str(numero_producto).zfill(2)

                            equipo_add = EquiposCascoSegurida(
                                numero_producto = producto,
                                referencias_casco=referencia_objeto,
                                user=request.user,
                                fecha_fabricacion=fecha_fabricacion,
                                personal_a_cargo = '',
                                veredicto = True,
                                codigo_interno='',
                                )

                            equipo_add.save()

                        else:

                            with transaction.atomic():

                                for lote in range(numero_producto,cantidad_productos+numero_producto):
                                    numero_unico = str(lote)
                                    numero = numero_unico.zfill(2)

                                    producto = str(lote_fabricacion)+str(linea_produccion)+numero

                                    query = EquiposCascoSegurida(
                                            numero_producto = producto,
                                            referencias_casco=referencia_objeto,
                                            user=CustomUser.objects.get(username= request.user),
                                            fecha_fabricacion=fecha_fabricacion,
                                            personal_a_cargo = '',
                                            veredicto = True,
                                            codigo_interno='',
                                        )
                                    query.save()

                        messages.success(request,'Equipos Insertados con exito')
                
                elif equipo_alturas=='5':
                    if EquiposAccesorioMetalicos.objects.filter(numero_producto = check_lote).exists() or not(ReferenciasAccesorioMetalicos.objects.filter(referencia = referencia_equipo).exists()):

                        messages.error(request,'Error, verifique la referencia o el lote del equipo')
                        return HttpResponseRedirect('/registrar/')

                    else:

                        referencia_objeto=ReferenciasAccesorioMetalicos.objects.get(referencia = referencia_equipo)

                        if cantidad_productos == 1:

                            producto = str(lote_fabricacion)+str(linea_produccion)+str(numero_producto).zfill(2)

                            equipo_add = EquiposAccesorioMetalicos(
                                numero_producto = producto,
                                referencias_accesorio_metalicos=referencia_objeto,
                                user=request.user,
                                fecha_fabricacion=fecha_fabricacion,
                                personal_a_cargo = '',
                                veredicto = True,
                                codigo_interno='',
                                )

                            equipo_add.save()

                        else:

                            with transaction.atomic():

                                for lote in range(numero_producto,cantidad_productos+numero_producto):
                                    numero_unico = str(lote)
                                    numero = numero_unico.zfill(2)

                                    producto = str(lote_fabricacion)+str(linea_produccion)+numero

                                    query = EquiposAccesorioMetalicos(
                                            numero_producto = producto,
                                            referencias_accesorio_metalicos=referencia_objeto,
                                            user=CustomUser.objects.get(username= request.user),
                                            fecha_fabricacion=fecha_fabricacion,
                                            personal_a_cargo = '',
                                            veredicto = True,
                                            codigo_interno='',
                                        )
                                    query.save()

                        messages.success(request,'Equipos Insertados con exito')
                    
                elif equipo_alturas=='6':
                    if EquiposSillasPerchas.objects.filter(numero_producto = check_lote).exists() or not(ReferenciasSillasPerchas.objects.filter(referencia = referencia_equipo).exists()):

                        messages.error(request,'Error, verifique la referencia o el lote del equipo')
                        return HttpResponseRedirect('/registrar/')

                    else:

                        referencia_objeto=ReferenciasSillasPerchas.objects.get(referencia = referencia_equipo)

                        if cantidad_productos == 1:

                            producto = str(lote_fabricacion)+str(linea_produccion)+str(numero_producto).zfill(2)

                            equipo_add = EquiposSillasPerchas(
                                numero_producto = producto,
                                referencias_sillas=referencia_objeto,
                                user=request.user,
                                fecha_fabricacion=fecha_fabricacion,
                                personal_a_cargo = '',
                                veredicto = True,
                                codigo_interno='',
                                )

                            equipo_add.save()

                        else:

                            with transaction.atomic():

                                for lote in range(numero_producto,cantidad_productos+numero_producto):
                                    numero_unico = str(lote)
                                    numero = numero_unico.zfill(2)

                                    producto = str(lote_fabricacion)+str(linea_produccion)+numero

                                    query = EquiposSillasPerchas(
                                            numero_producto = producto,
                                            referencias_sillas=referencia_objeto,
                                            user=CustomUser.objects.get(username= request.user),
                                            fecha_fabricacion=fecha_fabricacion,
                                            personal_a_cargo = '',
                                            veredicto = True,
                                            codigo_interno='',
                                        )
                                    query.save()

                        messages.success(request,'Equipos Insertados con exito')
            else:

                messages.error(request,'Datos invalidos')
    else:

        form = RegisterEquipmentForm ()

    return render(request, "gestion_fichas/registrar.html", {'form': form})

from operator import attrgetter
import pandas as pd
@login_required(login_url="/login/")
def UserView(request):
    inspectores = Inspectores.objects.get(user_id=request.user.id)
    
    
    #Filtra todas las inspecciones, las ordena por fecha de inspeccion y solo toma las columnas "veredicto", "fecha_inspeccion", "proxima_inspeccion" ,"numero_inspeccion"
    inspeccionesAccesorios = InspeccionAccesorioMetalicos.objects.select_related ().filter(
                    user=request.user
                    ).order_by('-numero_inspeccion').only("veredicto", "fecha_inspeccion", "proxima_inspeccion" ,"numero_inspeccion")

    inspeccionesArnes = InspeccionArnesModel.objects.select_related ().filter(
                    user=request.user
                    ).order_by('-numero_inspeccion').only("veredicto", "fecha_inspeccion", "proxima_inspeccion" , "numero_inspeccion")

    inspeccionesCasco = InspeccionCascoSeguridad.objects.select_related ().filter(
                    user=request.user
                    ).order_by('-numero_inspeccion').only("veredicto", "fecha_inspeccion", "proxima_inspeccion" ,"numero_inspeccion")

    inspeccionesEslinga = InspeccionEslinga.objects.select_related ().filter(
                    user=request.user
                    ).order_by('-numero_inspeccion').only("veredicto", "fecha_inspeccion", "proxima_inspeccion" ,"numero_inspeccion")
    
    inspeccionesLineas = InspeccionLineasAnclajes.objects.select_related ().filter(
                    user=request.user
                    ).order_by('-numero_inspeccion').only("veredicto", "fecha_inspeccion", "proxima_inspeccion" ,"numero_inspeccion")

    inspeccionesSillas = InspeccionSillasPerchas.objects.select_related ().filter(
                    user=request.user
                    ).order_by('-numero_inspeccion').only("veredicto", "fecha_inspeccion", "proxima_inspeccion" ,"numero_inspeccion")
    
    #Une todas las inspecciones filtradas en un queryset llamado "data" y lo organiza desde la ultima inspección realizada. 
    # https://howchoo.com/django/combine-two-querysets-with-different-models#comments
    
    data = sorted(
        chain(inspeccionesAccesorios, inspeccionesArnes, inspeccionesCasco, inspeccionesEslinga, inspeccionesLineas, inspeccionesSillas),
         key=attrgetter('fecha_inspeccion'), reverse=True)
        
    dataEquipos = []
    for i in range(len(data)):
        if 'InspeccionAccesorioMetalicos' in str(data[i]):
            dataEquipos.append(["Accesorios metalicos", data[i].equipos_accesorios_metalicos.numero_producto, 
            data[i].equipos_accesorios_metalicos.referencias_accesorio_metalicos.referencia, data[i], data[i].equipos_accesorios_metalicos.fecha_puesta_en_uso, '5'])
        elif 'InspeccionArnes' in str(data[i]):
            dataEquipos.append(["Arnés", data[i].equipos_arnes.numero_producto, data[i].equipos_arnes.referencias_arnes.referencia , data[i], data[i].equipos_arnes.fecha_puesta_en_uso, '1'])
        elif 'InspeccionCascoSeguridad' in str(data[i]):
            dataEquipos.append(["Casco de seguridad", data[i].equipos_cascos.numero_producto, data[i].equipos_cascos.referencias_casco.referencia , data[i], data[i].equipos_cascos.fecha_puesta_en_uso,'4'])
        elif 'InspeccionEslinga' in str(data[i]):
            dataEquipos.append(["Eslingas para detención de caída, restricción y posicionamiento",
            data[i].equipos_eslingas.numero_producto, data[i].equipos_eslingas.referencias_eslingas.referencia, data[i], data[i].equipos_eslingas.fecha_puesta_en_uso,'2'])
        elif 'InspeccionLineasAnclajes' in str(data[i]):
            dataEquipos.append(["Lineas de vida y anclajes", data[i].equipos_lineas_anclajes.numero_producto, 
            data[i].equipos_lineas_anclajes.referencias_anclajes.referencia, data[i], data[i].equipos_lineas_anclajes.fecha_puesta_en_uso,'3'])
        elif 'InspeccionSillasPerchas' in str(data[i]):
            dataEquipos.append(["Sillas/Perchas", data[i].equipos_sillas_perchas.numero_producto, 
            data[i].equipos_sillas_perchas.referencias_sillas_perchas.referencia, data[i], data[i].equipos_sillas_perchas.fecha_puesta_en_uso,'6'])
    
    df = pd.DataFrame(dataEquipos)
    result_df = df.drop_duplicates(subset=[0, 1], keep='first')
    dataEquipos=result_df.values.tolist()
    #print(data[0].equipos_eslingas.referencias_eslingas.referencia)
    #Genera varias paginas, https://www.youtube.com/watch?v=N-PB-HMFmdo, el render se realiza en forms.py en el tabholder utilizando el metodo 
    #HTML, junto a la tabla
    
    p = Paginator(dataEquipos, 6)
    page_number = request.GET.get('page')
    pageInspector = p.get_page(page_number)
    nums = "n" * pageInspector.paginator.num_pages
    
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserForm(request.POST, request.FILES)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            form = UserForm()
            if len(request.POST.get('Phone_number')) != 0:
                inspectores.phone=request.POST.get('Phone_number')
                messages.info(request, 'El numero de teléfono fue actualizado a '+str(inspectores.phone)+'.')
            if len(request.POST.get('Enterprise')) != 0:
                inspectores.empresa=request.POST.get('Enterprise')
                messages.info(request, 'El nombre de la empresa en la que esta laborando fue actualizado a '+str(inspectores.empresa)+'.')
            if len(request.FILES) != 0:
                if len(inspectores.foto_inspector) > 0 and inspectores.foto_inspector.path != 'media/default.jpg':
                    os.remove(inspectores.foto_inspector.path) 
                inspectores.foto_inspector = request.FILES['foto_inspector']
                messages.info(request,'La foto del inspector fue actualizada.')
            inspectores.save()
            if len(request.FILES) != 0 or len(request.POST.get('Enterprise')) != 0 or len(request.POST.get('Phone_number')):
                messages.success(request, 'Los datos del inspector fueron actualizados.')
            
            """object_pdf =Certificado()
            pdf = canvas.Canvas(buffer, pagesize=A4,bottomup=1)
            pdf.setTitle("Reporte de resultados equipo")
            pdf.setAuthor("EPI SAS")
            buffer = BytesIO()
            object_pdf.get_doc(
                        pdf, 
                        buffer, 
                        inspectores
                        )
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)"""
    else:
        form = UserForm()
    return render(request,'gestion_fichas/profile.html', {'form': form, "inspectores": inspectores, "pageIns": pageInspector, "nums": nums, "dataEquipos": dataEquipos})

@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'La contraseña a sido cambiada con exito')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige el error.')
            
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'gestion_fichas/ChangePassword.html', {'form': form})


@transaction.atomic
@csrf_exempt
@login_required(login_url="/login/")

def agregar_inspeccion(request, id_producto):

    equipo = get_object_or_404(EquiposArnes, id= id_producto)
    inspectores = Inspectores.objects.get(user_id=request.user.id)

    if request.method == "POST":

        form = InspectionSheetForm(request.POST, request.FILES)

        if form.is_valid():

            global date_now
            comentarios_adicionales = form.cleaned_data.get('comentarios_adicionales')
            imagen_arnes_cinta_reata = form.cleaned_data.get('imagen_arnes_cinta_reata')
            if not imagen_arnes_cinta_reata:
                imagen_arnes_cinta_reata = 'empty.jpg'
            imagen_arnes_costuras = form.cleaned_data.get('imagen_arnes_costuras')

            if not imagen_arnes_costuras:
                imagen_arnes_costuras = 'empty.jpg'
            imagen_arnes_metalicas = form.cleaned_data.get('imagen_arnes_metalicas')
            if not imagen_arnes_metalicas:
                imagen_arnes_metalicas = 'empty.jpg'
            fecha_proxima_inspeccion = form.cleaned_data.get('fecha_proxima_inspeccion')
            pre_veredicto = form.cleaned_data.get('veredicto')
            form_fields_checkbox, form_fields_hints = create_variables_names()
            fecha_inspeccion = date_now
            aspectos_inspeccion = []
            observaciones_inspeccion = []
            if pre_veredicto == '2':
                veredicto = False
            else:
                veredicto = True

            for name_var, text_area in zip(form_fields_checkbox, form_fields_hints):
                aux_var = form.cleaned_data.get(name_var)
                if aux_var == '1':
                    value = True
                else:
                    value = False

                aspectos_inspeccion.append(value)
                observaciones_inspeccion.append(form.cleaned_data.get(text_area))


            inspection_aspects = dict(
                zip(form_fields_checkbox, aspectos_inspeccion)
                )
            inspection_hints = dict(
                zip(form_fields_hints, observaciones_inspeccion)
                )

            form = InspectionSheetForm()

            inspeccion = InspeccionArnesModel.objects.filter(
                equipos_arnes = id_producto
                ).exists()

            if not inspeccion:

                numero_inspecciones = 1

            else:

                ultima_inspeccion = InspeccionArnesModel.objects.filter(
                    equipos_arnes = id_producto
                    ).last()

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)+1

            EquiposArnes.objects.filter(id=id_producto).update(veredicto=veredicto)

            with transaction.atomic():

                # This code executes inside a transaction.
                add_inspection_query = InspeccionArnesModel(
                    fecha_inspeccion=fecha_inspeccion,
                    proxima_inspeccion=fecha_proxima_inspeccion,
                    numero_inspeccion=numero_inspecciones,
                    equipos_arnes = equipo,
                    user = request.user,
                    veredicto=veredicto,
                    comentarios_adicionales=comentarios_adicionales,
                    reata_tienen_hoyos_agujeros=inspection_aspects['tienen_hoyos_agujeros'],
                    reata_deshilachadas=inspection_aspects['deshilachadas'],
                    reata_cortadas_desgastadas=inspection_aspects['cortadas_desgastadas'],
                    reata_talladuras=inspection_aspects['talladuras'],
                    reata_torsion=inspection_aspects['torsion'],
                    reata_suciedad=inspection_aspects['suciedad'],
                    reata_quemadura=inspection_aspects['quemadura'],
                    reata_salpicadura_rigidez=inspection_aspects['salpicadura_rigidez'],
                    reata_sustancia_quimica=inspection_aspects['sustancia_quimica'],
                    otros_arnes_cinta=inspection_aspects['otros_arnes_cinta'],
                    reata_foto=imagen_arnes_cinta_reata,
                    costuras_completas_continuas=inspection_aspects['costuras_completas_continuas'],
                    costuras_visibles=inspection_aspects['visibles'],
                    costuras_indicador_impacto_activado=inspection_aspects['indicador_impacto_activado'],
                    otros_arnes_costuras=inspection_aspects['otros_arnes_costuras'],
                    costuras_foto=imagen_arnes_costuras,
                    metalicas_completas=inspection_aspects['metalicas_completas'],
                    metalicas_corrosion_oxido=inspection_aspects['corrosion_oxido'],
                    metalicas_deformacion=inspection_aspects['deformacion'],
                    metalicas_fisuras_golpes_hundimiento=inspection_aspects['fisuras_golpes'],
                    otros_metalicas=inspection_aspects['otros_metalicas'],
                    metalicas_foto=imagen_arnes_metalicas,
                    observacion_reata_hoyo=inspection_hints['tienen_hoyos_agujeros_observacion'],
                    observacion_reata_deshilachadas=inspection_hints['deshilachadas_observacion'],
                    observacion_reata_cortadas_desgastadas=inspection_hints['cortadas_desgastadas_observacion'],
                    observacion_reata_talladuras=inspection_hints['talladuras_observacion'],
                    observacion_reata_torsion=inspection_hints['torsion_observacion'],
                    observacion_reata_suciedad=inspection_hints['suciedad_observacion'],
                    observacion_reata_quemadura=inspection_hints['quemadura_observacion'],
                    observacion_reata_salpicadura_rigidez=inspection_hints['salpicadura_observacion'],
                    observacion_reata_sustancia_quimica=inspection_hints['sustancia_observacion'],
                    observacion_reata_otros=inspection_hints['otros_arnes_cinta_observacion'],
                    observacion_costuras_completas_continuas=inspection_hints['costuras_completas_continuas_observacion'],
                    observacion_costuras_visibles=inspection_hints['visibles_observacion'],
                    observacion_costuras_indicador_impacto=inspection_hints['indicador_impacto_activado_observacion'],
                    observacion_costuras_otros=inspection_hints['otros_arnes_costuras_observacion'],
                    observacion_metalicas_completas=inspection_hints['metalicas_completas_observacion'],
                    observacion_metalicas_fisuras_golpes=inspection_hints['corrosion_oxido_observacion'],
                    observacion_metalicas_corrosion_oxido=inspection_hints['deformacion_observacion'],
                    observacion_metalicas_deformacion=inspection_hints['fisuras_golpes_observacion'],
                    observacion_metalicas_otros=inspection_hints['otros_metalicas_observacion'],
                    )

                add_inspection_query.save()

            messages.success(request,'Inspección creada con exito')
            return HttpResponseRedirect('/buscar_hv/')
            # return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

        else:

            messages.error(request,'Error campo invalido')

    else:
        form = InspectionSheetForm()

    #return render(request,'gestion_fichas/agregar_inspeccion.html')
    return render(request, 'gestion_fichas/agregar_inspeccion.html',{'form': form, "equipo":equipo, "inspectores":inspectores})

@transaction.atomic
@csrf_exempt
def agregar_inspeccion_eslinga(request, id_producto):

    equipo = get_object_or_404(EquiposEslinga, id= id_producto)
    inspectores = Inspectores.objects.get(user_id=request.user.id)

    if request.method == "POST":

        form = InspectionSheetFormEslingas(request.POST, request.FILES)

        if form.is_valid():

            global date_now
            comentarios_adicionales = form.cleaned_data.get('comentarios_adicionales')
            imagen_eslingas_absorbedor = form.cleaned_data.get('imagen_eslingas_absorbedor')
            if not imagen_eslingas_absorbedor:
                imagen_eslingas_absorbedor = 'empty.jpg'
            
            imagen_eslingas_cinta_reata = form.cleaned_data.get('imagen_eslingas_cinta_reata')
            if not imagen_eslingas_cinta_reata:
                imagen_eslingas_cinta_reata = 'empty.jpg'
            
            imagen_eslingas_metalicas = form.cleaned_data.get('imagen_eslingas_metalicas')
            if not imagen_eslingas_metalicas:
                imagen_eslingas_metalicas = 'empty.jpg'
            
            imagen_eslingas_costuras = form.cleaned_data.get('imagen_eslingas_costuras')
            if not imagen_eslingas_costuras:
                imagen_eslingas_costuras = 'empty.jpg'

            fecha_proxima_inspeccion = form.cleaned_data.get('fecha_proxima_inspeccion')
            pre_veredicto = form.cleaned_data.get('veredicto')
            form_fields_checkbox, form_fields_hints = create_variables_eslinga_names()
            fecha_inspeccion = date_now
            aspectos_inspeccion = []
            observaciones_inspeccion = []
            if pre_veredicto == '2':
                veredicto = False
            else:
                veredicto = True

            for name_var, text_area in zip(form_fields_checkbox, form_fields_hints):
                aux_var = form.cleaned_data.get(name_var)
                if aux_var == '1':
                    value = True
                else:
                    value = False

                aspectos_inspeccion.append(value)
                observaciones_inspeccion.append(form.cleaned_data.get(text_area))


            inspection_aspects = dict(
                zip(form_fields_checkbox, aspectos_inspeccion)
                )
            inspection_hints = dict(
                zip(form_fields_hints, observaciones_inspeccion)
                )

            form = InspectionSheetFormEslingas()

            inspeccion = InspeccionEslinga.objects.filter(
                equipos_eslingas = id_producto
                ).exists()

            if not inspeccion:

                numero_inspecciones = 1

            else:

                ultima_inspeccion = InspeccionEslinga.objects.filter(
                    equipos_eslingas = id_producto
                    ).last()

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)+1

            EquiposEslinga.objects.filter(id=id_producto).update(veredicto=veredicto)

            with transaction.atomic():

                # This code executes inside a transaction.
                add_inspection_query = InspeccionEslinga(
                    fecha_inspeccion=fecha_inspeccion,
                    proxima_inspeccion=fecha_proxima_inspeccion,
                    numero_inspeccion=numero_inspecciones,
                    equipos_eslingas = equipo,
                    user = request.user,
                    veredicto=veredicto,
                    comentarios_adicionales=comentarios_adicionales,
                    absorbedor_hoyos_desgarres = inspection_aspects['presenta_hoyos_desgarres'],
                    absorbedor_costuras_sueltas_reventadas = inspection_aspects['costuras_sueltas_reventadas'],
                    absorbedor_deterioro = inspection_aspects['deterioro'],
                    absorbedor_suciedad = inspection_aspects['presenta_suciedad'],
                    absorbedor_quemaduras_soldadura_cigarrillo = inspection_aspects['quemaduras_soldadura_cigarrillo'],
                    absorbedor_salpicadura_rigidez = inspection_aspects['salpicadura_rigidez_cintas'],
                    otros_absorbedor = inspection_aspects['otros_eslingas_absorbedor'],
                    absorbedor_foto=imagen_eslingas_absorbedor,             
                    reata_deshilachadas=inspection_aspects['deshilachadas'],
                    reata_desgastadas=inspection_aspects['desgastadas'],
                    reata_talladuras=inspection_aspects['talladuras'],
                    reata_salpicadura_rigidez=inspection_aspects['salpicadura_rigidez'],
                    reata_torsion=inspection_aspects['torsion'],
                    otros_cinta=inspection_aspects['otros_eslingas_cinta'],
                    reata_foto=imagen_eslingas_cinta_reata,
                    metalicas_completas=inspection_aspects['metalicas_completas'],
                    metalicas_corrosion_oxido=inspection_aspects['corrosion_oxido'],
                    metalicas_compuertas=inspection_aspects['compuertas_ganchos'],
                    metalicas_deformacion_fisuras_golpes_hundimiento=inspection_aspects['deformacion_fisuras_golpes_hundimientos'],
                    otros_metalicas=inspection_aspects['otros_metalicas'],
                    metalicas_foto=imagen_eslingas_metalicas,
                    costuras_completas_continuas=inspection_aspects['costuras_completas_continuas'],
                    costuras_visibles=inspection_aspects['visibles'],
                    otros_costuras=inspection_aspects['otros_costura'],
                    costuras_foto=imagen_eslingas_costuras,
                    observacion_absorbedor_hoyos_desgarres=inspection_hints['presenta_hoyos_desgarres_observacion'],
                    observacion_absorbedor_costuras_sueltas_reventadas=inspection_hints['costuras_sueltas_reventadas_observacion'],
                    observacion_absorbedor_deterioro=inspection_hints['deterioro_observacion'],
                    observacion_absorbedor_suciedad=inspection_hints['presenta_suciedad_observacion'],
                    observacion_absorbedor_quemaduras_soldadura_cigarrillo=inspection_hints['quemaduras_soldadura_cigarrillo_observacion'],
                    observacion_absorbedor_salpicadura_rigidez=inspection_hints['salpicadura_rigidez_cintas_observacion'],
                    observacion_otros_absorbedor=inspection_hints['otros_eslingas_absorbedor_observacion'],
                    observacion_reata_deshilachadas=inspection_hints['deshilachadas_observacion'],
                    observacion_reata_desgastadas=inspection_hints['desgastadas_observacion'],
                    observacion_reata_talladuras=inspection_hints['talladuras_observacion'],
                    observacion_reata_salpicadura_rigidez=inspection_hints['salpicadura_rigidez_observacion'],
                    observacion_reata_torsion=inspection_hints['torsion_observacion'],
                    observacion_reata_otros=inspection_hints['otros_eslingas_cinta_observacion'],
                    observacion_metalicas_completas=inspection_hints['metalicas_completas_observacion'],
                    observacion_metalicas_corrosion_oxido=inspection_hints['corrosion_oxido_observacion'],
                    observacion_metalicas_compuertas=inspection_hints['compuertas_ganchos_observacion'],
                    observacion_metalicas_deformacion_fisuras_golpes=inspection_hints['deformacion_fisuras_golpes_hundimientos_observacion'],
                    observacion_metalicas_otros=inspection_hints['otros_metalicas_observacion'],
                    observacion_costuras_completas_continuas=inspection_hints['costuras_completas_continuas_observacion'],
                    observacion_costuras_visibles=inspection_hints['visibles_observacion'],
                    observacion_costuras_otros=inspection_hints['otros_eslingas_costuras_observacion'],
                    )

                add_inspection_query.save()

            messages.success(request,'Inspección creada con exito')
            return HttpResponseRedirect('/buscar_hv/')
            # return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

        else:

            messages.error(request,'Error campo invalido')
                
    else:

        form = InspectionSheetFormEslingas()
        
    #return render(request,'gestion_fichas/agregar_inspeccion.html')
    return render(request, 'gestion_fichas/agregar_inspeccion_eslinga.html',{'form': form, "equipo":equipo, "inspectores":inspectores})


def agregar_inspeccion_lineas(request, id_producto):

    equipo = get_object_or_404(EquiposLineasAnclajes, id= id_producto)
    inspectores = Inspectores.objects.get(user_id=request.user.id)

    if request.method == "POST":

        form = InspectionSheetFormLineasAnclajes(request.POST, request.FILES)

        if form.is_valid():

            global date_now
            comentarios_adicionales = form.cleaned_data.get('comentarios_adicionales')

            imagen_lineas_metalicas = form.cleaned_data.get('imagen_lineas_metalicas')
            if not imagen_lineas_metalicas:
                imagen_lineas_metalicas = 'empty.jpg'
            
            imagen_lineas_cinta_reata = form.cleaned_data.get('imagen_lineas_cinta_reata')
            if not imagen_lineas_cinta_reata:
                imagen_lineas_cinta_reata = 'empty.jpg'

            imagen_lineas_costuras = form.cleaned_data.get('imagen_lineas_costuras')
            if not imagen_lineas_costuras:
                imagen_lineas_costuras = 'empty.jpg'

            fecha_proxima_inspeccion = form.cleaned_data.get('fecha_proxima_inspeccion')
            pre_veredicto = form.cleaned_data.get('veredicto')
            form_fields_checkbox, form_fields_hints = create_variables_lineas_names()
            fecha_inspeccion = date_now
            aspectos_inspeccion = []
            observaciones_inspeccion = []
            if pre_veredicto == '2':
                veredicto = False
            else:
                veredicto = True

            for name_var, text_area in zip(form_fields_checkbox, form_fields_hints):
                aux_var = form.cleaned_data.get(name_var)
                if aux_var == '1':
                    value = True
                else:
                    value = False

                aspectos_inspeccion.append(value)
                observaciones_inspeccion.append(form.cleaned_data.get(text_area))

            inspection_aspects = dict(
                zip(form_fields_checkbox, aspectos_inspeccion)
                )
            inspection_hints = dict(
                zip(form_fields_hints, observaciones_inspeccion)
                )

            form = InspectionSheetFormLineasAnclajes()

            inspeccion = InspeccionLineasAnclajes.objects.filter(
                equipos_lineas_anclajes = id_producto
                ).exists()

            if not inspeccion:

                numero_inspecciones = 1

            else:

                ultima_inspeccion = InspeccionLineasAnclajes.objects.filter(
                    equipos_lineas_anclajes = id_producto
                    ).last()

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)+1

            EquiposLineasAnclajes.objects.filter(id=id_producto).update(veredicto=veredicto)

            with transaction.atomic():

                # This code executes inside a transaction.
                add_inspection_query = InspeccionLineasAnclajes(
                    fecha_inspeccion=fecha_inspeccion,
                    proxima_inspeccion=fecha_proxima_inspeccion,
                    numero_inspeccion=numero_inspecciones,
                    equipos_lineas_anclajes = equipo,
                    user = request.user,
                    veredicto=veredicto,
                    comentarios_adicionales=comentarios_adicionales,
                    metalicas_completas = inspection_aspects['metalicas_completas'],
                    metalicas_fisuras = inspection_aspects['fisuras'],
                    metalicas_corrosion_oxido = inspection_aspects['corrosion_oxido'],
                    metalicas_golpes_hundimiento = inspection_aspects['golpes_hundimientos'],
                    metalicas_compuertas_ganchos = inspection_aspects['compuertas_ganchos'],
                    otros_metalicas = inspection_aspects['otros_metalicas'],
                    metalicas_foto=imagen_lineas_metalicas,
                    reata_deshilachadas = inspection_aspects['deshilachadas'],
                    reata_quemadura = inspection_aspects['quemadura_soldadura_cigarrillo_etc'],
                    reata_torsion_talladuras = inspection_aspects['torsion_talladuras'],
                    reata_salpicadura_rigidez = inspection_aspects['salpicadura_rigidez'],
                    reata_ruptura = inspection_aspects['ruptura'],
                    otros_lineas_cinta = inspection_aspects['otros_lineas_cinta'],
                    reata_foto=imagen_lineas_cinta_reata,
                    costuras_completas_continuas = inspection_aspects['costuras_completas_continuas'],
                    costuras_visibles = inspection_aspects['visibles'],
                    otros_lineas_costuras = inspection_aspects['otros_lineas_costuras'],
                    costuras_foto=imagen_lineas_costuras,
                    observacion_metalicas_completas = inspection_hints['metalicas_completas_observacion'],
                    observacion_metalicas_fisuras = inspection_hints['fisuras_observacion'],
                    observacion_metalicas_corrosion_oxido = inspection_hints['corrosion_oxido_observacion'],
                    observacion_metalicas_golpes_hundimientos = inspection_hints['golpes_hundimientos_observacion'],
                    observacion_metalicas_compuertas_ganchos = inspection_hints['compuertas_ganchos_observacion'],
                    observacion_metalicas_otros = inspection_hints['otros_metalicas_observacion'],
                    observacion_reata_deshilachadas = inspection_hints['deshilachadas_observacion'],
                    observacion_reata_quemadura = inspection_hints['quemadura_soldadura_cigarrillo_etc_observacion'],
                    observacion_reata_torsion_talladuras = inspection_hints['torsion_talladuras_observacion'],
                    observacion_reata_salpicadura_rigidez = inspection_hints['salpicadura_rigidez_observacion'],
                    observacion_reata_ruptura = inspection_hints['ruptura_observacion'],
                    observacion_otros_lineas_cinta = inspection_hints['otros_lineas_cinta_observacion'],
                    observacion_costuras_completas_continuas = inspection_hints['costuras_completas_continuas_observacion'],
                    observacion_costuras_visibles = inspection_hints['visibles_observacion'],
                    observacion_costuras_otros = inspection_hints['otros_lineas_costuras_observacion'],
                    )

                add_inspection_query.save()
        
            messages.success(request,'Inspección creada con exito')
            return HttpResponseRedirect('/buscar_hv/')
            # return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

        else:

            messages.error(request,'Error campo invalido')

    else:

        form = InspectionSheetFormLineasAnclajes()

    #return render(request,'gestion_fichas/agregar_inspeccion.html')
    return render(request, 'gestion_fichas/agregar_inspeccion_lineas.html',{'form': form, "equipo":equipo, "inspectores":inspectores})


def agregar_inspeccion_casco(request, id_producto):

    equipo = get_object_or_404(EquiposCascoSegurida, id= id_producto)
    inspectores = Inspectores.objects.get(user_id=request.user.id)

    if request.method == "POST":

        form = InspectionSheetFormCascos(request.POST, request.FILES)

        if form.is_valid():

            global date_now
            comentarios_adicionales = form.cleaned_data.get('comentarios_adicionales')

            imagen_casco_casquete = form.cleaned_data.get('imagen_casco_casquete')
            if not imagen_casco_casquete:
                imagen_casco_casquete = 'empty.jpg'
            
            imagen_casco_suspencion = form.cleaned_data.get('imagen_casco_suspencion')
            if not imagen_casco_suspencion:
                imagen_casco_suspencion = 'empty.jpg'
            
            imagen_casco_barbuquejo = form.cleaned_data.get('imagen_casco_barbuquejo')
            if not imagen_casco_barbuquejo:
                imagen_casco_barbuquejo = 'empty.jpg'

            fecha_proxima_inspeccion = form.cleaned_data.get('fecha_proxima_inspeccion')
            pre_veredicto = form.cleaned_data.get('veredicto')
            form_fields_checkbox, form_fields_hints = create_variables_casco_names()
            fecha_inspeccion = date_now
            aspectos_inspeccion = []
            observaciones_inspeccion = []
            if pre_veredicto == '2':
                veredicto = False
            else:
                veredicto = True

            for name_var, text_area in zip(form_fields_checkbox, form_fields_hints):
                aux_var = form.cleaned_data.get(name_var)
                if aux_var == '1':
                    value = True
                else:
                    value = False

                aspectos_inspeccion.append(value)
                observaciones_inspeccion.append(form.cleaned_data.get(text_area))

            inspection_aspects = dict(
                zip(form_fields_checkbox, aspectos_inspeccion)
                )
            inspection_hints = dict(
                zip(form_fields_hints, observaciones_inspeccion)
                )

            form = InspectionSheetFormCascos()

            inspeccion = InspeccionCascoSeguridad.objects.filter(
                equipos_cascos = id_producto
                ).exists()

            if not inspeccion:

                numero_inspecciones = 1

            else:

                ultima_inspeccion = InspeccionCascoSeguridad.objects.filter(
                    equipos_cascos = id_producto
                    ).last()

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)+1

            EquiposCascoSegurida.objects.filter(id=id_producto).update(veredicto=veredicto)

            with transaction.atomic():

                # This code executes inside a transaction.
                add_inspection_query = InspeccionCascoSeguridad(
                    fecha_inspeccion=fecha_inspeccion,
                    proxima_inspeccion=fecha_proxima_inspeccion,
                    numero_inspeccion=numero_inspecciones,
                    equipos_cascos = equipo,
                    user = request.user,
                    veredicto=veredicto,
                    comentarios_adicionales=comentarios_adicionales,
                    casquete_fisuras_golpes_hundimiento = inspection_aspects['fisuras_golpes_hundimientos_casquete'],
                    casquete_quemaduras_deterioro_quimicos = inspection_aspects['quemaduras_deteriorquimicos'],
                    casquete_rayadura_decoloracion = inspection_aspects['rayadura_decoloracion'],
                    otros_casquete = inspection_aspects['otros_casquete'],
                    casquete_foto=imagen_casco_casquete,
                    suspencion_completo = inspection_aspects['completo_suspencion'],
                    suspencion_fisuras_golpes_hundimientos = inspection_aspects['fisuras_golpes_hundimientos_suspencion'],
                    suspencion_torsion_estiramiento = inspection_aspects['torsion_estiramiento'],
                    otros_suspencion = inspection_aspects['otros_suspencion'],
                    suspencion_foto=imagen_casco_suspencion,
                    barbuquejo_completo = inspection_aspects['completo_barbuquejo'],
                    barbuquejo_cinta_deshilachada_rotas = inspection_aspects['cinta_deshilachada_rotas'],
                    barbuquejo_salpicadura_pintura_rigidez_cinta = inspection_aspects['salpicadura_pintura_rigidez_cinta'],
                    otros_barbuquejo = inspection_aspects['otros_barbuquejo'],
                    barbuquejo_foto=imagen_casco_barbuquejo,
                    observacion_casquete_fisuras_golpes_hundimiento = inspection_hints['fisuras_golpes_hundimientos_casquete_observacion'],
                    observacion_casquete_quemaduras_deterioro_quimicos = inspection_hints['quemaduras_deteriorquimicos_observacion'],
                    observacion_casquete_rayadura_decoloracion = inspection_hints['rayadura_decoloracion_observacion'],
                    observacion_casquete_otros = inspection_hints['otros_casquete_observacion'],
                    observacion_suspencion_completo = inspection_hints['completo_suspencion_observacion'],
                    observacion_suspencion_fisuras_golpes_hundimientos = inspection_hints['fisuras_golpes_hundimientos_suspencion_observacion'],
                    observacion_suspencion_torsion_estiramiento = inspection_hints['torsion_estiramiento_observacion'],
                    observacion_suspencion_otros = inspection_hints['otros_suspencion_observacion'],
                    observacion_barbuquejo_completo = inspection_hints['completo_barbuquejo_observacion'],
                    observacion_barbuquejo_cinta_deshilachada_rotas = inspection_hints['cinta_deshilachada_rotas_observacion'],
                    observacion_barbuquejo_salpicadura_pintura_rigidez_cinta = inspection_hints['salpicadura_pintura_rigidez_cinta_observacion'],
                    observacion_barbuquejo_otros = inspection_hints['otros_barbuquejo_observacion'],
                    )

                add_inspection_query.save()

            messages.success(request,'Inspección creada con exito')
            return HttpResponseRedirect('/buscar_hv/')
            # return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

        else:

            messages.error(request,'Error campo invalido')

    else:

        form = InspectionSheetFormCascos()

    #return render(request,'gestion_fichas/agregar_inspeccion.html')
    return render(request, 'gestion_fichas/agregar_inspeccion_casco.html',{'form': form, "equipo":equipo, "inspectores":inspectores})

def agregar_inspeccion_accesorio(request, id_producto):

    equipo = get_object_or_404(EquiposAccesorioMetalicos, id= id_producto)
    inspectores = Inspectores.objects.get(user_id=request.user.id)

    if request.method == "POST":
        
        form = InspectionSheetFormAccesorios(request.POST, request.FILES)

        if form.is_valid():  
            global date_now
            comentarios_adicionales = form.cleaned_data.get('comentarios_adicionales')

            imagen_accesorio_mosquetones = form.cleaned_data.get('imagen_accesorio_mosquetones')
            if not imagen_accesorio_mosquetones:
                imagen_accesorio_mosquetones = 'empty.jpg'
            
            imagen_accesorio_arrestador_polea = form.cleaned_data.get('imagen_accesorio_arrestador_polea')
            if not imagen_accesorio_arrestador_polea:
                imagen_accesorio_arrestador_polea = 'empty.jpg'

            imagen_accesorio_descendedores_anclajes = form.cleaned_data.get('imagen_accesorio_descendedores_anclajes')
            if not imagen_accesorio_descendedores_anclajes:
                imagen_accesorio_descendedores_anclajes = 'empty.jpg'

            fecha_proxima_inspeccion = form.cleaned_data.get('fecha_proxima_inspeccion')
            pre_veredicto = form.cleaned_data.get('veredicto')
            form_fields_checkbox, form_fields_hints = create_variables_accesorio_names()
            fecha_inspeccion = date_now
            aspectos_inspeccion = []
            observaciones_inspeccion = []
            if pre_veredicto == '2':
                veredicto = False
            else:
                veredicto = True

            for name_var, text_area in zip(form_fields_checkbox, form_fields_hints):
                aux_var = form.cleaned_data.get(name_var)
                if aux_var == '1':
                    value = True
                else:
                    value = False

                aspectos_inspeccion.append(value)
                observaciones_inspeccion.append(form.cleaned_data.get(text_area))

            inspection_aspects = dict(
                zip(form_fields_checkbox, aspectos_inspeccion)
                )
            inspection_hints = dict(
                zip(form_fields_hints, observaciones_inspeccion)
                )

            form = InspectionSheetFormAccesorios()

            inspeccion = InspeccionAccesorioMetalicos.objects.filter(
                equipos_accesorios_metalicos = id_producto
                ).exists()

            if not inspeccion:

                numero_inspecciones = 1

            else:

                ultima_inspeccion = InspeccionAccesorioMetalicos.objects.filter(
                    equipos_accesorios_metalicos = id_producto
                    ).last()

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)+1

            EquiposAccesorioMetalicos.objects.filter(id=id_producto).update(veredicto=veredicto)

            with transaction.atomic():

                # This code executes inside a transaction.
                add_inspection_query = InspeccionAccesorioMetalicos(
                    fecha_inspeccion=fecha_inspeccion,
                    proxima_inspeccion=fecha_proxima_inspeccion,
                    numero_inspeccion=numero_inspecciones,
                    equipos_accesorios_metalicos = equipo,
                    user = request.user,
                    veredicto=veredicto,
                    comentarios_adicionales=comentarios_adicionales,
                    mosquetones_fisuras_golpes_hundimiento = inspection_aspects['fisuras_golpes_hundimientos_mosquetones'],
                    mosquetones_quemaduras_deterioro_quimicos = inspection_aspects['quemaduras_deteriorquimicos'],
                    mosquetones_oxidacion_corrocion_mosquetones = inspection_aspects['oxidacion_corrocion_mosquetones'],
                    mosquetones_bordes_filosos_rugosos = inspection_aspects['bordes_filosos_rugosos_mosquetones'],
                    mosquetones_compuerta_libre = inspection_aspects['compuerta_libre_mosquetones'],
                    mosquetones_deformaciones = inspection_aspects['deformaciones_mosquetones'],
                    otros_mosquetones = inspection_aspects['otros_mosquetones'],
                    mosquetones_foto = imagen_accesorio_mosquetones,
                    arrestador_poleas_fisuras_golpes_hundimientos = inspection_aspects['fisuras_golpes_hundimientos_arrestador'],
                    arrestador_poleas_frenado_lisa = inspection_aspects['frenado_lisa'],
                    arrestador_poleas_oxidacion_corrocion = inspection_aspects['oxidacion_corrocion_arrestador'],
                    arrestador_poleas_bordes_filosos_rugosos = inspection_aspects['bordes_filosos_rugosos_arrestador'],
                    arrestador_poleas_compuerta_libre = inspection_aspects['compuerta_libre_arrestador'],
                    arrestador_poleas_deformaciones = inspection_aspects['deformaciones_arrestador'],
                    otros_arrestador_poleas = inspection_aspects['otros_arrestador'],
                    arrestador_poleas_foto = imagen_accesorio_arrestador_polea,
                    descendedores_anclajes_fisuras_golpes_hundimientos = inspection_aspects['fisuras_golpes_hundimientos_descendedor'],
                    descendedores_anclajes_contacto_lisa = inspection_aspects['contacto_lisa'],
                    descendedores_anclajes_oxidacion_corrocion = inspection_aspects['oxidacion_corrocion_descendedor'],
                    descendedores_anclajes_bordes_filosos_rugosos = inspection_aspects['bordes_filosos_rugosos_descendedor'],
                    descendedores_anclajes_desgaste_disminucion_metal = inspection_aspects['desgaste_disminucionmetal'],
                    descendedores_anclajes_deformaciones = inspection_aspects['deformaciones_descendedor'],
                    otros_descendedores_anclajes = inspection_aspects['otros_descendedor'],
                    descendedores_anclajes_foto = imagen_accesorio_descendedores_anclajes,
                    observacion_mosquetones_fisuras_golpes_hundimiento = inspection_hints['fisuras_golpes_hundimientos_mosquetones_observacion'],
                    observacion_mosquetones_quemaduras_deterioro_quimicos = inspection_hints['quemaduras_deteriorquimicos_observacion'],
                    observacion_mosquetones_oxidacion_corrocion_mosquetones = inspection_hints['oxidacion_corrocion_mosquetones_observacion'],
                    observacion_mosquetones_bordes_filosos_rugosos = inspection_hints['bordes_filosos_rugosos_mosquetones_observacion'],
                    observacion_mosquetones_compuerta_libre = inspection_hints['compuerta_libre_mosquetones_observacion'],
                    observacion_mosquetones_deformaciones = inspection_hints['deformaciones_mosquetones_observacion'],
                    observacion_mosquetones_otros = inspection_hints['otros_mosquetones_observacion'],
                    observacion_arrestador_poleas_fisuras_golpes_hundimientos = inspection_hints['fisuras_golpes_hundimientos_arrestador_observacion'],
                    observacion_arrestador_poleas_frenado_lisa = inspection_hints['frenado_lisa_observacion'],
                    observacion_arrestador_poleas_oxidacion_corrocion = inspection_hints['oxidacion_corrocion_arrestador_observacion'],
                    observacion_arrestador_poleas_bordes_filosos_rugosos = inspection_hints['bordes_filosos_rugosos_arrestador_observacion'],
                    observacion_arrestador_poleas_compuerta_libre = inspection_hints['compuerta_libre_arrestador_observacion'],
                    observacion_arrestador_poleas_deformaciones = inspection_hints['deformaciones_arrestador_observacion'],
                    observacion_arrestador_poleas_otros = inspection_hints['otros_arrestador_observacion'],
                    observacion_descendedores_anclajes_fisuras_golpes_hundimientos = inspection_hints['fisuras_golpes_hundimientos_descendedor_observacion'],
                    observacion_descendedores_anclajes_frenado_lisa = inspection_hints['contacto_lisa_observacion'],
                    observacion_descendedores_anclajes_oxidacion_corrocion = inspection_hints['oxidacion_corrocion_descendedor_observacion'],
                    observacion_descendedores_anclajes_bordes_filosos_rugosos = inspection_hints['bordes_filosos_rugosos_descendedor_observacion'],
                    observacion_descendedores_anclajes_desgaste_disminucion_metal = inspection_hints['desgaste_disminucionmetal_observacion'],
                    observacion_descendedores_anclajes_deformaciones = inspection_hints['deformaciones_descendedor_observacion'],
                    observacion_descendedores_anclajes_otros = inspection_hints['otros_descendedor_observacion'],
                    )

                add_inspection_query.save()
            
            messages.success(request,'Inspección creada con exito')
            return HttpResponseRedirect('/buscar_hv/')
            # return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

        else:
            messages.error(request,'Error campo invalido')

    else:
        form = InspectionSheetFormAccesorios()

    #return render(request,'gestion_fichas/agregar_inspeccion.html')
    return render(request, 'gestion_fichas/agregar_inspeccion_accesorio.html',{'form': form, "equipo":equipo, "inspectores":inspectores})

def agregar_inspeccion_silla(request, id_producto):

    equipo = get_object_or_404(EquiposSillasPerchas, id= id_producto)
    inspectores = Inspectores.objects.get(user_id=request.user.id)

    if request.method == "POST":

        form = InspectionSheetFormSillas(request.POST, request.FILES)

        if form.is_valid():

            global date_now
            comentarios_adicionales = form.cleaned_data.get('comentarios_adicionales')

            imagen_silla_cinta_reata = form.cleaned_data.get('imagen_silla_cinta_reata')
            if not imagen_silla_cinta_reata:
                imagen_silla_cinta_reata = 'empty.jpg'
            
            imagen_silla_costuras = form.cleaned_data.get('imagen_silla_costuras')
            if not imagen_silla_costuras:
                imagen_silla_costuras = 'empty.jpg'

            imagen_silla_metalicas = form.cleaned_data.get('imagen_silla_metalicas')
            if not imagen_silla_metalicas:
                imagen_silla_metalicas = 'empty.jpg'
            
            imagen_silla_madera = form.cleaned_data.get('imagen_silla_madera')
            if not imagen_silla_madera:
                imagen_silla_madera = 'empty.jpg'

            fecha_proxima_inspeccion = form.cleaned_data.get('fecha_proxima_inspeccion')
            pre_veredicto = form.cleaned_data.get('veredicto')
            form_fields_checkbox, form_fields_hints = create_variables_silla_names()
            fecha_inspeccion = date_now
            aspectos_inspeccion = []
            observaciones_inspeccion = []
            if pre_veredicto == '2':
                veredicto = False
            else:
                veredicto = True

            for name_var, text_area in zip(form_fields_checkbox, form_fields_hints):
                aux_var = form.cleaned_data.get(name_var)
                if aux_var == '1':
                    value = True
                else:
                    value = False

                aspectos_inspeccion.append(value)
                observaciones_inspeccion.append(form.cleaned_data.get(text_area))

            inspection_aspects = dict(
                zip(form_fields_checkbox, aspectos_inspeccion)
                )
            inspection_hints = dict(
                zip(form_fields_hints, observaciones_inspeccion)
                )

            form = InspectionSheetFormSillas()

            inspeccion = InspeccionSillasPerchas.objects.filter(
                equipos_sillas_perchas = id_producto
                ).exists()

            if not inspeccion:

                numero_inspecciones = 1

            else:

                ultima_inspeccion = InspeccionSillasPerchas.objects.filter(
                    equipos_sillas_perchas = id_producto
                    ).last()

                numero_inspecciones = int(ultima_inspeccion.numero_inspeccion)+1

            EquiposSillasPerchas.objects.filter(id=id_producto).update(veredicto=veredicto)

            with transaction.atomic():

                # This code executes inside a transaction.
                add_inspection_query = InspeccionSillasPerchas(
                    fecha_inspeccion=fecha_inspeccion,
                    proxima_inspeccion=fecha_proxima_inspeccion,
                    numero_inspeccion=numero_inspecciones,
                    equipos_sillas_perchas = equipo,
                    user = request.user,
                    veredicto=veredicto,
                    comentarios_adicionales=comentarios_adicionales,
                    reata_tienen_hoyos_agujeros = inspection_aspects['tienen_hoyos_agujeros'],
                    reata_deshilachadas = inspection_aspects['deshilachadas'],
                    reata_desgastadas = inspection_aspects['cortadas_desgastadas'],
                    reata_talladuras = inspection_aspects['talladuras'],
                    reata_torsion = inspection_aspects['torsion'],
                    reata_suciedad = inspection_aspects['suciedad'],
                    reata_quemadura = inspection_aspects['quemadura'],
                    reata_salpicadura_rigidez = inspection_aspects['salpicadura_rigidez'],
                    reata_sustancia_quimica = inspection_aspects['sustancia_quimica'],
                    otros_cinta_reata = inspection_aspects['otros_silla_cinta'],
                    cinta_reata_foto = imagen_silla_cinta_reata,
                    costuras_completas_continuas = inspection_aspects['costuras_completas_continuas'],
                    costuras_visibles = inspection_aspects['visibles'],
                    otros_silla_costuras = inspection_aspects['otros_silla_costuras'],
                    costuras_foto = imagen_silla_costuras,
                    metalicas_completas = inspection_aspects['metalicas_completas'],
                    metalicas_corrosion = inspection_aspects['corrosion_oxido'],
                    metalicas_deformacion = inspection_aspects['deformacion'],
                    metalicas_fisuras_golpes = inspection_aspects['fisuras_golpes'],
                    otros_metalicas = inspection_aspects['otros_metalicas'],
                    metalicas_foto = imagen_silla_metalicas,
                    madera_golpes_rupturas = inspection_aspects['golpes_rupturas'],
                    madera_polillas = inspection_aspects['pollillas_gorgojos'],
                    madera_exceso_humeda = inspection_aspects['humeda_pintura'],
                    otros_madera = inspection_aspects['otros_madera'],
                    madera_foto = imagen_silla_madera,
                    observacion_reata_tienen_hoyos_agujeros = inspection_hints['tienen_hoyos_agujeros_observacion'],
                    observacion_reata_deshilachadas = inspection_hints['deshilachadas_observacion'],
                    observacion_reata_cortadas_desgastadas = inspection_hints['cortadas_desgastadas_observacion'],
                    observacion_reata_talladuras = inspection_hints['talladuras_observacion'],
                    observacion_reata_torsion = inspection_hints['torsion_observacion'],
                    observacion_reata_suciedad = inspection_hints['suciedad_observacion'],
                    observacion_reata_quemadura = inspection_hints['quemadura_observacion'],
                    observacion_reata_salpicadura_rigidez = inspection_hints['salpicadura_observacion'],
                    observacion_reata_sustancia_quimica = inspection_hints['sustancia_observacion'],
                    observacion_reata_otros = inspection_hints['otros_silla_cinta_observacion'],
                    observacion_costuras_completas_continuas = inspection_hints['costuras_completas_continuas_observacion'],
                    observacion_costuras_visibles = inspection_hints['visibles_observacion'],
                    observacion_otros_silla_costuras = inspection_hints['otros_silla_costuras_observacion'],
                    observacion_metalicas_completas = inspection_hints['metalicas_completas_observacion'],
                    observacion_metalicas_corrosion_oxido = inspection_hints['corrosion_oxido_observacion'],
                    observacion_metalicas_deformacion = inspection_hints['deformacion_observacion'],
                    observacion_metalicas_fisuras_golpes = inspection_hints['fisuras_golpes_observacion'],
                    observacion_metalicas_otros = inspection_hints['otros_metalicas_observacion'],
                    observacion_madera_golpes_rupturas = inspection_hints['golpes_rupturas_observacion'],
                    observacion_madera_polillas = inspection_hints['pollillas_gorgojos_observacion'],
                    observacion_madera_exceso_humeda = inspection_hints['humeda_pintura_observacion'],
                    observacion_otros_madera = inspection_hints['otros_madera_observacion'],
                    )

                add_inspection_query.save()
            
            messages.success(request,'Inspección creada con exito')
            return HttpResponseRedirect('/buscar_hv/')
            # return render(request, "gestion_fichas/buscar_hv.html", {'form': form})

        else:

            messages.error(request,'Error campo invalido')

    else:

        form = InspectionSheetFormSillas()

    #return render(request,'gestion_fichas/agregar_inspeccion.html')
    return render(request, 'gestion_fichas/agregar_inspeccion_silla.html',{'form': form, "equipo":equipo, "inspectores":inspectores})


def protected_access(request, path):
    """
    When trying to access :
    myproject.com/media/uploads/passport.png

    If access is authorized, the request will be redirected to
    myproject.com/protected/media/uploads/passport.png

    This special URL will be handle by nginx we the help of X-Accel
    """

    access_granted = False
    
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            # If admin, everything is granted
            access_granted = True
        else:
            inspectores = Inspectores.objects.get(user_id=request.user.id)
            # For simple user, only their documents can be accessed
                # add here more allowed documents
            if 'protected' in path:
                if path == inspectores.certificado_inspector.name:
                    access_granted = True
                elif path == inspectores.carnet_inspector.name:
                    access_granted = True
            else:
                access_granted = True

    else:
        if 'protected' in path:
            access_granted = False
        else:
            access_granted = True

    if access_granted:
        response = HttpResponse()
        # Content-type will be detected by nginx
        del response['Content-Type']
        response['X-Accel-Redirect'] = '/protected/' + path
        
        return response
    else:
        return HttpResponseForbidden('Not authorized to access this media.')