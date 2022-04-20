from django import forms
from django.db.models.constraints import UniqueConstraint
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, ButtonHolder, Button, Reset
from crispy_forms.bootstrap import TabHolder, Tab


# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
#     def render(self):
        
#         return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
    
class LoginForm (forms.Form):
    Usuario   = forms.CharField()
    Contraseña = forms.CharField(widget=forms.PasswordInput)

class DateInput(forms.DateInput):
    input_type = 'date'

class DateInput(forms.DateInput):
    input_type = 'date'

class TextAreaInput(forms.Textarea):
    input_type = 'textarea'

class NumberInput(forms.NumberInput):
    input_type = 'number'

class CrearHvForm (forms.Form):
    #codigo_interno = forms.CharField(widget= NumberInput())
    numero_producto  = forms.IntegerField(min_value=0)
    cantidad_productos_agregar  = forms.IntegerField(min_value=1, initial=1)
    personal_a_cargo = forms.CharField()
    codigo_interno = forms.IntegerField(min_value=0)
    fecha_puesta_en_uso = forms.DateField(widget= DateInput())
    empresa = forms.CharField()
    correo =forms.CharField()
    telefono=forms.CharField()
    SELECCION_EQUIPOS = [
        ('1', 'Arnes'),
        ('2', 'Eslinga detención de caidas, restrición y posicionamiento'),
        ('3', 'Lineas de vida y Anclaje'),
        ('4', 'Casco de seguridad'),
        ('5', 'Accesorios Metalicos'),
        ('6', 'Sillas y perchas'),
    ]
    equipo_alturas  = forms.ChoiceField(
            choices=SELECCION_EQUIPOS,
            widget=forms.Select,
            )

class SearchEquipmentForm(forms.Form):
    numero_producto  = forms.IntegerField(min_value=0)
    SELECCION_EQUIPOS = [
        ('1', 'Arnes'),
        ('2', 'Eslinga detención de caidas, restrición y posicionamiento'),
        ('3', 'Lineas de vida y Anclaje'),
        ('4', 'Casco de seguridad'),
        ('5', 'Accesorios Metalicos'),
        ('6', 'Sillas y perchas'),
    ]
    equipo_alturas  = forms.ChoiceField(
            choices=SELECCION_EQUIPOS,
            widget=forms.Select,
            )

class RegisterEquipmentForm (forms.Form):
    #codigo_interno = forms.CharField(widget= NumberInput())
    numero_producto = forms.IntegerField(min_value=0,initial=0, max_value=99)
    lote_fabricacion = forms.IntegerField(min_value=0)
    linea_produccion = forms.IntegerField(min_value=1, max_value=9)
    cantidad_productos_agregar  = forms.IntegerField(min_value=1, initial=100,max_value=100)
    fecha_fabricacion = forms.DateField(widget= DateInput())
    referencia  = forms.CharField()
    SELECCION_EQUIPOS = [
        ('1', 'Arnes'),
        ('2', 'Eslinga detención de caidas, restrición y posicionamiento'),
        ('3', 'Lineas de vida y Anclaje'),
        ('4', 'Casco de seguridad'),
        ('5', 'Accesorios Metalicos'),
        ('6', 'Sillas y perchas'),
    ]
    equipo_alturas  = forms.ChoiceField(
            choices=SELECCION_EQUIPOS,
            widget=forms.Select,
            )

class InspectionSheetForm(forms.Form):
    arnes_cinta_reata_fields = [
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
        ]
    arnes_cinta_reata_labels = [
        '¿Tienen hoyos o agujeros?', 
        '¿Están deshilachadas?', 
        '¿Cortadas o desgastadas?', 
        '¿Tienen talladuras?', 
        '¿Hay torsión?', 
        '¿Presentan suciedad?', 
        '¿Quemaduras por soldadura, cigarrilo, etc.?', 
        '¿Salpicadura por pintura y rigidez en la reata?', 
        '¿Sustancias químicas?', 
        '¿Otros?',
        ]
    arnes_costuras_etiquetas_fields = [
        'costuras_completas_continuas', 
        'visibles',
        'indicador_impacto_activado', 
        'otros_arnes_costuras',
        ]
    arnes_costuras_etiquetas_labels = [
        '¿Completas y continuas?', 
        '¿Son visibles?', 
        '¿Indicador de impacto activado?',
        '¿Otros?'
        ]
    arnes_metalicas_fields = [
        'metalicas_completas', 
        'corrosion_oxido', 
        'deformacion', 
        'fisuras_golpes',
        'otros_metalicas',
        ]
    arnes_metalicas_labels = [
        '¿Completas', 
        '¿Presentan Corrosión y óxido?', 
        '¿Deformación?', 
        '¿Fisuras, golpes, hundimientos?',
        '¿Otros?',
        ]
    
    arnes_cinta_reata_observacion_fields = [
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
        ]
    arnes_costuras_etiquetas_observacion_fields = [
        'costuras_completas_continuas_observacion',
        'visibles_observacion',  
        'indicador_impacto_activado_observacion', 
        'otros_arnes_costuras_observacion',
        ]
    arnes_metalicas_observacion_fields = [
        'metalicas_completas_observacion', 
        'corrosion_oxido_observacion', 
        'deformacion_observacion', 
        'fisuras_golpes_observacion', 
        'otros_metalicas_observacion',
        ]
    db_columns = arnes_cinta_reata_fields+arnes_costuras_etiquetas_fields\
        +arnes_metalicas_fields
    
    db_columns_labels = arnes_cinta_reata_labels+arnes_costuras_etiquetas_labels\
        +arnes_metalicas_labels

    db_columns_observacion = arnes_cinta_reata_observacion_fields\
        +arnes_costuras_etiquetas_observacion_fields\
        +arnes_metalicas_observacion_fields
    
    imagen_arnes_cinta_reata = forms.ImageField(
        required=False, 
        label='Subir una foto de la cintas/ reatas del equipo'
        ) 
    imagen_arnes_costuras = forms.ImageField(
        required=False, 
        label='Subir una foto de las costuras y etiquetas'
        )
    imagen_arnes_metalicas = forms.ImageField(
        required=False, 
        label='Subir una foto de las partes metálicas y plasticas del equipo'
        )
    fecha_proxima_inspeccion = forms.DateField(
        widget=DateInput(), 
        label='Fecha próxima inspección'
        )
    comentarios_adicionales = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
        required= False
        )
    
    CHOICES = [('1', 'Apto y puede continuar'),
               ('2', 'No apto y debe ser retirado')
              ]

    SI_NO = [('1', 'SI'),
             ('0', 'NO')
            ]

    veredicto = forms.ChoiceField(
            choices=CHOICES, 
            widget=forms.RadioSelect,
            )
    
    for db_col, label in zip(db_columns,db_columns_labels):
        # if db_columns == 'index' or db_columns == 'id':
        #     continue

        locals()[db_col] = forms.ChoiceField(
            choices=SI_NO, 
            widget=forms.RadioSelect, 
            label=label
            )

        # locals()[db_col] = forms.BooleanField(label=label, required=False)

    for db_col in db_columns_observacion:
        # if db_columns == 'index' or db_columns == 'id':
        #     continue
        locals()[db_col] = forms.CharField(
            widget=forms.Textarea(attrs={'rows':2, 'cols':20}), 
            required=False
            )


class UserForm(forms.Form):
    OldPassword = forms.CharField(widget=forms.PasswordInput, required=False, label='Contraseña actual')
    NewPassword = forms.CharField(widget=forms.PasswordInput, required=False, label='Nueva contraseña')
    NewPasswordConfirm= forms.CharField(widget=forms.PasswordInput, required=False, label='Confirmar nueva contraseña')
    Phone_number = forms.CharField(widget=forms.NumberInput, required=False, label='Numero de teléfono')
    Enterprise = forms.CharField(required=False, label='Empresa')
    foto_inspector= forms.ImageField(required=False, label='Foto de inspector')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Registro de inspecciones',
                    HTML("""
                    <table class="table">
                    <thead>
                        <tr>
                        <th scope="col">Tipo de equipo</th>
                        <th scope="col">Numero de producto</th>
                        <th width="14%" scope="col">Referencia</th>
                        <th scope="col">Veredicto</th>
                        <th scope="col">Puesta en uso</th>
                        <th scope="col">Fecha de inspección</th>
                        <th scope="col">Fecha de próxima inspección</th>
                        <th width="5%" scope="col">Número de inspecciones</th>
                        </tr>
                    </thead>
                    
                    <tbody>
                        {% for i in pageIns %}
                            <tr>
                                <td>{{i.0}}</td>
                                <td><a href={% url 'hv_sheet' i.1 i.5%} >{{i.1}}</a></td>
                                <td>{{i.2}}</td>
                                <td>{% if i.3.veredicto %}
                                    {{'Apto'}}
                                    {% else %}
                                    {{'No Apto'}}
                                    {% endif %}</td>
                                <td>{{i.4}}</td>
                                <td>{{i.3.fecha_inspeccion}}</td>
                                <td>{{i.3.proxima_inspeccion}}</td>
                                <td>{{i.3.numero_inspeccion}}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                    </table>
                            <nav aria-label="Page navigation">
                                <ul class="pagination">
                                    {% if pageIns.has_previous %}
                                        <li class="page-item"><a class="page-link" href="?page=1">&laquo; First</a></li>
                                        <li class="page-item"><a class="page-link" href="?page={{ pageIns.previous_page_number }}">Previous</a></li>
                                    {% endif %}
                                    {% for i in nums %}
                                        <li class="page-item"><a class="page-link" href="?page={{ forloop.counter }}">{{ forloop.counter }}</a></li>
                                    {% endfor %}
                                    {% if pageIns.has_next %}
                                        <li class="page-item"><a class="page-link" href="?page={{ pageIns.next_page_number }}">Next</a></li>
                                        <li class="page-item"><a class="page-link" href="?page={{ pageIns.paginator.num_pages }}">Last &raquo;</a></li>
                                    {% endif %}
                                </ul>
                            </nav>""")
                ),
                Tab(
                    'Certificado de inspección',
                    #Para poder visualizar el certificado en el Viewer PDF por defecto.
                    HTML("""<embed src="{{ MEDIA_URL }}{{inspectores.certificado_inspector}}#zoom=40&scrollbar=0&navpanes=0" 
                    content_type="application/pdf" width="700" height="600"></embed>"""),  #style="pointer-events: none"-Para evitar que l usuario pueda interactuar con el PDF
                ),
                Tab(
                    'Carnet',
                    #Para poder visualizar el certificado en el Viewer PDF por defecto.
                    HTML("""<embed src="{{ MEDIA_URL }}{{inspectores.carnet_inspector}}#zoom=90&scrollbar=0&navpanes=0" 
                    content_type="application/pdf" width="700" height="600"></embed>"""),  #style="pointer-events: none"-Para evitar que l usuario pueda interactuar con el PDF
                ),
                Tab('Configuración',
                    'Phone_number',
                    'Enterprise',
                    'foto_inspector',
                    ButtonHolder(
                        Reset('reset', 'Limpiar campos', css_class='btn btn-secondary mt-2'),
                        #Botón enviado hacia HTML que esta conectado a un menú modal llamado UpdateConfirmation ese menú tiene el botón para cancelar, y aceptar tiene el submit que realiza el POST
                        HTML('<button type="button" class="btn btn-success mt-2" data-toggle="modal" data-target="#UpdateConfirmation">Actualizar</button>'),              
                    ),
                    ButtonHolder(
                        HTML("""<a class = "pl-0 m-0" href="{% url 'password' %}">"""),
                        Button('password', 'Cambiar contraseña', css_class='btn btn-primary mt-2'),
                    )     
                ),
                
            )   
    )


class SearchInspectorForm(forms.Form):
    codigo_inspector  = forms.CharField(widget=forms.NumberInput, label='Código de inspector')


class InspectionSheetFormEslingas(forms.Form):
    eslingas_absorbedor_fields = [
        'presenta_hoyos_desgarres', 
        'costuras_sueltas_reventadas', 
        'deterioro', 
        'presenta_suciedad', 
        'quemaduras_soldadura_cigarrillo',
        'salpicadura_rigidez_cintas',
        'otros_eslingas_absorbedor',
        ] 
    eslingas_absorbedor_labels = [ 
        '¿Presentan hoyos o desgarres?', 
        'Costuras Sueltas o reventadas?', 
        '¿Deterioro?', 
        '¿Presentan Suciedad?', 
        '¿Quemadura por soldadura o cigarrillo?',  
        '¿Salpicadura de pintura y rigidez en cintas?',
        '¿Otros?',
        ]
    eslingas_cinta_reata_fields = [
        'deshilachadas', 
        'desgastadas', 
        'talladuras', 
        'salpicadura_rigidez', 
        'torsion',
        'otros_eslingas_cinta',
        ] 
    eslingas_cinta_reata_labels = [ 
        '¿Están deshilachadas?', 
        '¿Desgastadas?', 
        '¿Tienen Talladuras?', 
        '¿Salpicadura por pintura y rigidez en la reata?', 
        '¿Hay torsión?',  
        '¿Otros?',
        ]
    eslingas_metalicas_fields = [
        'metalicas_completas', 
        'corrosion_oxido', 
        'compuertas_ganchos',
        'deformacion_fisuras_golpes_hundimientos', 
        'otros_metalicas',
        ]
    eslingas_metalicas_labels = [
        '¿Completas?', 
        '¿Presentan Corrosión y óxido?', 
        '¿Las compuertas de ganchos abren y cierran correctamente?', 
        '¿Deformación, fisuras, golpes, hundimientos?',
        '¿Otros?',
        ]
    eslingas_costuras_etiquetas_fields = [
        'costuras_completas_continuas', 
        'visibles', 
        'otros_costura',
        ]
    eslingas_costuras_etiquetas_labels = [
        '¿Completas y continuas?', 
        '¿Son visibles?', 
        '¿Otros?',
        ]
    eslingas_absorbedor_observacion_fields = [
        'presenta_hoyos_desgarres_observacion', 
        'costuras_sueltas_reventadas_observacion', 
        'deterioro_observacion', 
        'presenta_suciedad_observacion', 
        'quemaduras_soldadura_cigarrillo_observacion',
        'salpicadura_rigidez_cintas_observacion',
        'otros_eslingas_absorbedor_observacion'
        ] 
    eslingas_cinta_reata_observacion_fields = [
        'deshilachadas_observacion', 
        'desgastadas_observacion', 
        'talladuras_observacion', 
        'salpicadura_rigidez_observacion', 
        'torsion_observacion', 
        'otros_eslingas_cinta_observacion',
        ] 
    eslingas_metalicas_observacion_fields = [
        'metalicas_completas_observacion', 
        'corrosion_oxido_observacion', 
        'compuertas_ganchos_observacion',
        'deformacion_fisuras_golpes_hundimientos_observacion', 
        'otros_metalicas_observacion',
        ]
    eslingas_costuras_etiquetas_observacion_fields = [
        'costuras_completas_continuas_observacion', 
        'visibles_observacion', 
        'otros_eslingas_costuras_observacion',
        ]

    db_columns = eslingas_absorbedor_fields+eslingas_cinta_reata_fields\
        +eslingas_metalicas_fields+eslingas_costuras_etiquetas_fields
    
    db_columns_labels = eslingas_absorbedor_labels+eslingas_cinta_reata_labels\
        +eslingas_metalicas_labels+eslingas_costuras_etiquetas_labels

    db_columns_observacion = eslingas_absorbedor_observacion_fields\
        +eslingas_cinta_reata_observacion_fields\
        +eslingas_metalicas_observacion_fields+eslingas_costuras_etiquetas_observacion_fields
    
    imagen_eslingas_absorbedor = forms.ImageField(
        required=False, 
        label='Subir una foto del absorbedor del equipo'
        ) 

    imagen_eslingas_cinta_reata = forms.ImageField(
        required=False, 
        label='Subir una foto de la cintas/ reatas del equipo'
        ) 
    imagen_eslingas_costuras = forms.ImageField(
        required=False, 
        label='Subir una foto de las costuras y etiquetas'
        )
    imagen_eslingas_metalicas = forms.ImageField(
        required=False, 
        label='Subir una foto de las partes metálicas del equipo'
        )
    fecha_proxima_inspeccion = forms.DateField(
        widget=DateInput(), 
        label='Fecha próxima inspección'
        )
    comentarios_adicionales = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
        required= False
        )
    
    CHOICES = [('1', 'Apto y puede continuar'),
               ('2', 'No apto y debe ser retirado')
              ]

    SI_NO = [('1', 'SI'),
             ('0', 'NO')
            ]

    veredicto = forms.ChoiceField(
            choices=CHOICES, 
            widget=forms.RadioSelect,
            )
    
    for db_col, label in zip(db_columns,db_columns_labels):
        # if db_columns == 'index' or db_columns == 'id':
        #     continue

        locals()[db_col] = forms.ChoiceField(
            choices=SI_NO, 
            widget=forms.RadioSelect, 
            label=label
            )

        # locals()[db_col] = forms.BooleanField(label=label, required=False)

    for db_col in db_columns_observacion:
        # if db_columns == 'index' or db_columns == 'id':
        #     continue
        locals()[db_col] = forms.CharField(
            widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
            required=False
            )


class InspectionSheetFormLineasAnclajes(forms.Form):
    
    lineas_metalicas_fields = [
        'metalicas_completas', 
        'fisuras',
        'corrosion_oxido',
        'golpes_hundimientos',
        'compuertas_ganchos',  
        'otros_metalicas',
        ]
    lineas_metalicas_labels = [
        '¿Completas?', 
        '¿Tiene fisuras?',
        '¿Presentan Corrosión y óxido?', 
        '¿Golpes, hundimientos?',
        '¿las compuertas de ganchos abren y cierran correctamente?', 
        '¿Otros?',
        ]
    lineas_cinta_reata_cuerda_fields = [
        'deshilachadas', 
        'quemadura_soldadura_cigarrillo_etc',
        'torsion_talladuras', 
        'salpicadura_rigidez', 
        'ruptura', 
        'otros_lineas_cinta',
        ] 
    lineas_cinta_reata_cuerda_labels = [ 
        '¿Están deshilachadas?', 
        '¿Quemaduras por soldadura, cigarrillo, etc?',
        '¿Hay Torsión o talladuras?', 
        '¿Salpicadura de pintura y rigidez en cinta?', 
        '¿Ruptura?',  
        '¿Otros?',
        ]
    lineas_costuras_etiquetas_fields = [
        'costuras_completas_continuas', 
        'visibles', 
        'otros_lineas_costuras',
        ]
    lineas_costuras_etiquetas_labels = [
        '¿Completas y continuas?', 
        '¿Visibles?', 
        '¿Otros?',
        ]
    
    lineas_metalicas_observacion = [
        'metalicas_completas_observacion', 
        'fisuras_observacion',
        'corrosion_oxido_observacion',
        'golpes_hundimientos_observacion',
        'compuertas_ganchos_observacion',  
        'otros_metalicas_observacion',
        ]
    lineas_cinta_reata_cuerda_observacion = [
        'deshilachadas_observacion', 
        'quemadura_soldadura_cigarrillo_etc_observacion',
        'torsion_talladuras_observacion', 
        'salpicadura_rigidez_observacion', 
        'ruptura_observacion',
        'otros_lineas_cinta_observacion',
        ] 
    lineas_costuras_etiquetas_observacion = [
        'costuras_completas_continuas_observacion', 
        'visibles_observacion', 
        'otros_lineas_costuras_observacion',
        ]
    

    db_columns = lineas_metalicas_fields+lineas_cinta_reata_cuerda_fields\
        +lineas_costuras_etiquetas_fields
    
    db_columns_labels = lineas_metalicas_labels+lineas_cinta_reata_cuerda_labels\
        +lineas_costuras_etiquetas_labels

    db_columns_observacion = lineas_metalicas_observacion\
        +lineas_cinta_reata_cuerda_observacion\
        +lineas_costuras_etiquetas_observacion

    imagen_lineas_metalicas = forms.ImageField(
        required=False, 
        label='Subir una foto de las partes metálicas y plasticas del equipo'
        )
    imagen_lineas_cinta_reata = forms.ImageField(
        required=False, 
        label='Subir una foto de la cintas/ reatas/ cuerda del equipo'
        ) 
    imagen_lineas_costuras = forms.ImageField(
        required=False, 
        label='Subir una foto de las costuras y etiquetas'
        )
    fecha_proxima_inspeccion = forms.DateField(
        widget=DateInput(), 
        label='Fecha próxima inspección'
        )
    comentarios_adicionales = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
        required= False
        )
    
    CHOICES = [('1', 'Apto y puede continuar'),
               ('2', 'No apto y debe ser retirado')
              ]

    SI_NO = [('1', 'SI'),
             ('0', 'NO')
            ]

    veredicto = forms.ChoiceField(
            choices=CHOICES, 
            widget=forms.RadioSelect,
            )
    
    for db_col, label in zip(db_columns,db_columns_labels):
        # if db_columns == 'index' or db_columns == 'id':
        #     continue

        locals()[db_col] = forms.ChoiceField(
            choices=SI_NO, 
            widget=forms.RadioSelect, 
            label=label
            )

        # locals()[db_col] = forms.BooleanField(label=label, required=False)

    for db_col in db_columns_observacion:
        # if db_columns == 'index' or db_columns == 'id':
        #     continue
        locals()[db_col] = forms.CharField(
            widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
            required=False
            )


class InspectionSheetFormCascos(forms.Form):
    
    casquete_fields = [
        'fisuras_golpes_hundimientos_casquete', 
        'quemaduras_deteriorquimicos',
        'rayadura_decoloracion',
        'otros_casquete',
        ]
    casquete_labels = [
        '¿Tiene fisuras, golpes, hundiminetos?', 
        '¿Presenta Quemaduras o deterioro por Quimicos?',
        '¿Presentan Rayadura o decoloración?',  
        '¿Otros?',
        ]
    suspencion_fields = [
        'completo_suspencion', 
        'fisuras_golpes_hundimientos_suspencion',
        'torsion_estiramiento',  
        'otros_suspencion',
        ] 
    suspencion_labels = [ 
        '¿Completo?', 
        '¿Tiene fisuras, golpes, hundimiento?',
        '¿Hay Torsión o estiramiento?', 
        '¿Otros?',
        ]
    barbuquejo_fields = [
        'completo_barbuquejo', 
        'cinta_deshilachada_rotas', 
        'salpicadura_pintura_rigidez_cinta',
        'otros_barbuquejo',
        ]
    barbuquejo_labels = [
        '¿Completas?', 
        '¿La cintas están deshilachadas o rotas?', 
        '¿Salpicaduras de pintura y rigidez en cinta?',
        '¿Otros?',
        ]
    
    
    casquete_observacion = [
        'fisuras_golpes_hundimientos_casquete_observacion', 
        'quemaduras_deteriorquimicos_observacion',
        'rayadura_decoloracion_observacion',
        'otros_casquete_observacion',
        ]
    suspencion_observacion = [
        'completo_suspencion_observacion', 
        'fisuras_golpes_hundimientos_suspencion_observacion',
        'torsion_estiramiento_observacion',  
        'otros_suspencion_observacion',
        ] 
    barbuquejo_observacion = [
        'completo_barbuquejo_observacion', 
        'cinta_deshilachada_rotas_observacion', 
        'salpicadura_pintura_rigidez_cinta_observacion',
        'otros_barbuquejo_observacion',
        ]
    

    db_columns = casquete_fields+suspencion_fields\
        +barbuquejo_fields
    
    db_columns_labels = casquete_labels+suspencion_labels\
        +barbuquejo_labels

    db_columns_observacion = casquete_observacion\
        +suspencion_observacion\
        +barbuquejo_observacion

    imagen_casco_casquete = forms.ImageField(
        required=False, 
        label='Subir una foto del casquete'
        )
    imagen_casco_suspencion = forms.ImageField(
        required=False, 
        label='Subir una foto de la suspencion'
        ) 
    imagen_casco_barbuquejo = forms.ImageField(
        required=False, 
        label='Subir una foto del barbuquejo'
        )
    fecha_proxima_inspeccion = forms.DateField(
        widget=DateInput(), 
        label='Fecha próxima inspección'
        )
    comentarios_adicionales = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
        required= False
        )
    
    CHOICES = [('1', 'Apto y puede continuar'),
               ('2', 'No apto y debe ser retirado')
              ]

    SI_NO = [('1', 'SI'),
             ('0', 'NO')
            ]

    veredicto = forms.ChoiceField(
            choices=CHOICES, 
            widget=forms.RadioSelect,
            )
    
    for db_col, label in zip(db_columns,db_columns_labels):
        # if db_columns == 'index' or db_columns == 'id':
        #     continue

        locals()[db_col] = forms.ChoiceField(
            choices=SI_NO, 
            widget=forms.RadioSelect, 
            label=label
            )

        # locals()[db_col] = forms.BooleanField(label=label, required=False)

    for db_col in db_columns_observacion:
        # if db_columns == 'index' or db_columns == 'id':
        #     continue
        locals()[db_col] = forms.CharField(
            widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
            required=False
            )

class InspectionSheetFormAccesorios(forms.Form):
    
    mosquetones_fields = [
        'fisuras_golpes_hundimientos_mosquetones', 
        'quemaduras_deteriorquimicos',
        'oxidacion_corrocion_mosquetones',
        'bordes_filosos_rugosos_mosquetones',
        'compuerta_libre_mosquetones',
        'deformaciones_mosquetones',
        'otros_mosquetones',
        ]
    mosquetones_labels = [
        '¿Tiene fisuras, golpes, hundiminetos?', 
        '¿Presenta Quemaduras o deterioro por Quimicos?',
        '¿Presentan oxidación y corrosión?',
        '¿Presenta bordes filosos y rugosos que causen corte?',
        '¿La compuerta abre y cierra libremente?',
        '¿Tiene deformaciones?',
        '¿Otros?',
        ]
    arrestador_poleas_fields = [ 
        'fisuras_golpes_hundimientos_arrestador',
        'frenado_lisa',
        'oxidacion_corrocion_arrestador',
        'bordes_filosos_rugosos_arrestador',
        'compuerta_libre_arrestador',
        'deformaciones_arrestador',
        'otros_arrestador',
        ] 
    arrestador_poleas_labels = [
        '¿Tiene fisuras, golpes, hundiminetos?', 
        '¿La superficies de frenado se encuentran lisas?',
        '¿Presentan oxidación y corrosión?',
        '¿Presenta bordes filosos y rugosos que causen corte?',
        '¿La compuerta abre y cierra libremente?',
        '¿Tiene deformaciones?',  
        '¿Otros?',
        ]
    descendedores_anclajes_fields = [
        'fisuras_golpes_hundimientos_descendedor',
        'contacto_lisa',
        'oxidacion_corrocion_descendedor',
        'bordes_filosos_rugosos_descendedor',
        'desgaste_disminucionmetal',
        'deformaciones_descendedor',
        'otros_descendedor',
        ]
    descendedores_anclajes_labels = [
        '¿Tiene fisuras, golpes, hundiminetos?', 
        '¿Las superficies de contacto se encuentran lisas?',
        '¿Presentan oxidación y corrosión?',
        '¿Presenta bordes filosos y rugosos que causen corte?',
        '¿Presenta desgastes o disminución de metal?',
        '¿Tiene deformaciones?',  
        '¿Otros?',
        ]
    
    mosquetones_observacion = [
        'fisuras_golpes_hundimientos_mosquetones_observacion', 
        'quemaduras_deteriorquimicos_observacion',
        'oxidacion_corrocion_mosquetones_observacion',
        'bordes_filosos_rugosos_mosquetones_observacion',
        'compuerta_libre_mosquetones_observacion',
        'deformaciones_mosquetones_observacion',
        'otros_mosquetones_observacion',
        ]
    arrestador_poleas_observacion = [ 
        'fisuras_golpes_hundimientos_arrestador_observacion',
        'frenado_lisa_observacion',
        'oxidacion_corrocion_arrestador_observacion',
        'bordes_filosos_rugosos_arrestador_observacion',
        'compuerta_libre_arrestador_observacion',
        'deformaciones_arrestador_observacion',
        'otros_arrestador_observacion',
        ] 
    descendedores_anclajes_observacion = [
        'fisuras_golpes_hundimientos_descendedor_observacion',
        'contacto_lisa_observacion',
        'oxidacion_corrocion_descendedor_observacion',
        'bordes_filosos_rugosos_descendedor_observacion',
        'desgaste_disminucionmetal_observacion',
        'deformaciones_descendedor_observacion',
        'otros_descendedor_observacion',
        ]
    

    db_columns = mosquetones_fields+arrestador_poleas_fields\
        +descendedores_anclajes_fields
    
    db_columns_labels = mosquetones_labels+arrestador_poleas_labels\
        +descendedores_anclajes_labels

    db_columns_observacion = mosquetones_observacion+arrestador_poleas_observacion\
        +descendedores_anclajes_observacion

    imagen_accesorio_mosquetones = forms.ImageField(
        required=False, 
        label='Subir una foto del mosqueton'
        )
    imagen_accesorio_arrestador_polea = forms.ImageField(
        required=False, 
        label='Subir una foto del arrestador de caidas y poleas'
        ) 
    imagen_accesorio_descendedores_anclajes = forms.ImageField(
        required=False, 
        label='Subir una foto de los descendedores/ascendedores y anclajes'
        )
    fecha_proxima_inspeccion = forms.DateField(
        widget=DateInput(), 
        label='Fecha próxima inspección'
        )
    comentarios_adicionales = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
        required= False
        )
    
    CHOICES = [('1', 'Apto y puede continuar'),
               ('2', 'No apto y debe ser retirado')
              ]

    SI_NO = [('1', 'SI'),
             ('0', 'NO')
            ]

    veredicto = forms.ChoiceField(
            choices=CHOICES, 
            widget=forms.RadioSelect,
            )
    
    for db_col, label in zip(db_columns,db_columns_labels):
        # if db_columns == 'index' or db_columns == 'id':
        #     continue

        locals()[db_col] = forms.ChoiceField(
            choices=SI_NO, 
            widget=forms.RadioSelect, 
            label=label
            )

        # locals()[db_col] = forms.BooleanField(label=label, required=False)

    for db_col in db_columns_observacion:
        # if db_columns == 'index' or db_columns == 'id':
        #     continue
        locals()[db_col] = forms.CharField(
            widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
            required=False
            )
            
class InspectionSheetFormSillas(forms.Form):
    silla_cinta_reata_fields = [
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
        ]
    silla_cinta_reata_labels = [
        '¿Tienen hoyos o agujeros?', 
        '¿Están deshilachadas?', 
        '¿Cortadas o desgastadas?', 
        '¿Tienen talladuras?', 
        '¿Hay torsión?', 
        '¿Presentan suciedad?', 
        '¿Quemaduras por soldadura, cigarrilo, etc.?', 
        '¿Salpicadura por pintura y rigidez en cinta?', 
        '¿Sustancias químicas?', 
        '¿Otros?',
        ]
    silla_costuras_etiquetas_fields = [
        'costuras_completas_continuas', 
        'visibles', 
        'otros_silla_costuras',
        ]
    silla_costuras_etiquetas_labels = [
        '¿Completas y continuas?', 
        '¿Son visibles?', 
        '¿Otros?',
        ]
    silla_metalicas_fields = [
        'metalicas_completas', 
        'corrosion_oxido', 
        'deformacion', 
        'fisuras_golpes',
        'otros_metalicas',
        ]
    silla_metalicas_labels = [
        '¿Completas?', 
        '¿Presentan Corrosión y óxido?', 
        '¿Deformación?', 
        '¿Fisuras, golpes, hundimientos?',
        '¿Otros?',
        ]
    silla_madera_fields = [
        'golpes_rupturas', 
        'pollillas_gorgojos', 
        'humeda_pintura', 
        'otros_madera',
        ]
    silla_madera_labels = [
        '¿Tiene Golpes, Rupturas o Deformaciones?', 
        '¿Presentan Polillas o Gorgojos?', 
        '¿Exceso de humedad y pintura?', 
        '¿Otros?',
        ]

    silla_cinta_reata_observacion_fields = [
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
        ]
    silla_costuras_etiquetas_observacion_fields = [
        'costuras_completas_continuas_observacion',
        'visibles_observacion',   
        'otros_silla_costuras_observacion',
        ]
    silla_metalicas_observacion_fields = [
        'metalicas_completas_observacion', 
        'corrosion_oxido_observacion', 
        'deformacion_observacion', 
        'fisuras_golpes_observacion', 
        'otros_metalicas_observacion',
        ]
    silla_madera_observacion_fields = [
        'golpes_rupturas_observacion', 
        'pollillas_gorgojos_observacion', 
        'humeda_pintura_observacion', 
        'otros_madera_observacion',
        ]
    db_columns = silla_cinta_reata_fields+silla_costuras_etiquetas_fields\
        +silla_metalicas_fields+silla_madera_fields
    
    db_columns_labels = silla_cinta_reata_labels+silla_costuras_etiquetas_labels\
        +silla_metalicas_labels+silla_madera_labels

    db_columns_observacion = silla_cinta_reata_observacion_fields+silla_costuras_etiquetas_observacion_fields\
        +silla_metalicas_observacion_fields+silla_madera_observacion_fields
    
    imagen_silla_cinta_reata = forms.ImageField(
        required=False, 
        label='Subir una foto de la cintas/reatas del equipo'
        ) 
    imagen_silla_costuras = forms.ImageField(
        required=False, 
        label='Subir una foto de las costuras y etiquetas'
        )
    imagen_silla_metalicas = forms.ImageField(
        required=False, 
        label='Subir una foto de las partes metálicas y plasticas del equipo'
        )
    imagen_silla_madera = forms.ImageField(
        required=False, 
        label='Subir una foto de las partes de madera del equipo'
        )
    fecha_proxima_inspeccion = forms.DateField(
        widget=DateInput(), 
        label='Fecha próxima inspección'
        )
    comentarios_adicionales = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
        required= False
        )
    
    CHOICES = [('1', 'Apto y puede continuar'),
               ('2', 'No apto y debe ser retirado')
              ]

    SI_NO = [('1', 'SI'),
             ('0', 'NO')
            ]

    veredicto = forms.ChoiceField(
            choices=CHOICES, 
            widget=forms.RadioSelect,
            )
    
    for db_col, label in zip(db_columns,db_columns_labels):
        # if db_columns == 'index' or db_columns == 'id':
        #     continue

        locals()[db_col] = forms.ChoiceField(
            choices=SI_NO, 
            widget=forms.RadioSelect, 
            label=label
            )

        # locals()[db_col] = forms.BooleanField(label=label, required=False)

    for db_col in db_columns_observacion:
        # if db_columns == 'index' or db_columns == 'id':
        #     continue
        locals()[db_col] = forms.CharField(
            widget=forms.Textarea(attrs={'rows':2, 'cols':40}), 
            required=False
            )
    
    