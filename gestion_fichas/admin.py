from django.contrib import admin
from django import forms


from gestion_fichas.models import EquiposArnes, InspeccionAccesorioMetalicos, InspeccionArnes, InspeccionCascoSeguridad, InspeccionEslinga, InspeccionLineasAnclajes, InspeccionSillasPerchas, ReferenciasArnes, ReferenciasEslingas, ReferenciasCascoSeguridad, \
                                    ReferenciasLineasAnclajes, ReferenciasAccesorioMetalicos,  ReferenciasSillasPerchas, EquiposEslinga, EquiposLineasAnclajes, EquiposCascoSegurida, EquiposAccesorioMetalicos, EquiposSillasPerchas, CiudadCodigo
from gestion_fichas.models import LineasTipo
from gestion_fichas.models import CustomUser, Inspectores

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class EquiposArnes_admin(admin.ModelAdmin):
    
    list_display   = (
        "numero_producto", "user", "fecha_puesta_en_uso", "referencias_arnes_id",
        "veredicto", "personal_a_cargo", "fecha_fabricacion", 'image_tag'
        )

    list_filter    = ("fecha_fabricacion",'veredicto')
    date_hierarchy = "fecha_fabricacion"
    search_fields  = ("personal_a_cargo",)


class EquiposEslinga_admin(admin.ModelAdmin):
    
    list_display   = (
        "numero_producto", "user", "fecha_puesta_en_uso", "referencias_eslingas_id",
        "veredicto", "personal_a_cargo", "fecha_fabricacion", 'image_tag'
        )
    
    list_filter    = ("fecha_fabricacion",'veredicto')
    date_hierarchy = "fecha_fabricacion"
    search_fields  = ("personal_a_cargo",)

class EquiposLineas_admin(admin.ModelAdmin):
    
    list_display   = (
        "numero_producto", "user", "fecha_puesta_en_uso", "referencias_anclajes_id",
        "veredicto", "personal_a_cargo", "fecha_fabricacion", 'image_tag'
        )
    
    list_filter    = ("fecha_fabricacion",'veredicto')
    date_hierarchy = "fecha_fabricacion"
    search_fields  = ("personal_a_cargo",)

class EquiposCasco_admin(admin.ModelAdmin):
    
    list_display   = (
        "numero_producto", "user", "fecha_puesta_en_uso", "referencias_casco_id",
        "veredicto", "personal_a_cargo", "fecha_fabricacion", 'image_tag'
        )
    
    list_filter    = ("fecha_fabricacion",'veredicto')
    date_hierarchy = "fecha_fabricacion"
    search_fields  = ("personal_a_cargo",)

class EquiposAccesorioMetalicos_admin(admin.ModelAdmin):
    
    list_display   = (
        "numero_producto", "user", "fecha_puesta_en_uso", "referencias_accesorio_metalicos_id",
        "veredicto", "personal_a_cargo", "fecha_fabricacion", 'image_tag'
        )
    
    list_filter    = ("fecha_fabricacion",'veredicto')
    date_hierarchy = "fecha_fabricacion"
    search_fields  = ("personal_a_cargo",)

class EquiposSillasPerchas_admin(admin.ModelAdmin):
    
    list_display   = (
        "numero_producto", "user", "fecha_puesta_en_uso", "referencias_sillas_id",
        "veredicto", "personal_a_cargo", "fecha_fabricacion", 'image_tag'
        )
    
    list_filter    = ("fecha_fabricacion",'veredicto')
    date_hierarchy = "fecha_fabricacion"
    search_fields  = ("personal_a_cargo",)

class ReferenciasArnes_admin(admin.ModelAdmin):

    list_display   = ("referencia", 'image_tag', "descripcion","tipo","talla","material","peso_maximo_kg","resistencia_kn","pdf")
    #list_filter    = ("equipos_tipo",)

    search_fields  = ("referencia", "tipo")

    
class ReferenciasEslingas_admin(admin.ModelAdmin):

    list_display   = ("referencia", 'image_tag', "descripcion","tipo","material","peso_maximo_kg","resistencia_kn","pdf")
    #list_filter    = ("equipos_tipo",)

    search_fields  = ("referencia", "tipo")

class ReferenciasLineasAnclajes_admin(admin.ModelAdmin):

    list_display   = ("referencia", 'image_tag', "descripcion","tipo","material","peso_maximo_kg","resistencia_kn","pdf")
    #list_filter    = ("equipos_tipo",)

    search_fields  = ("referencia", "tipo")

class ReferenciasCascoSegurida_admin(admin.ModelAdmin):

    list_display   = ("referencia", 'image_tag', "descripcion","tipo","clase","pdf")
    #list_filter    = ("equipos_tipo",)

    search_fields  = ("referencia", "tipo")

class ReferenciasAccesorioMetalicos_admin(admin.ModelAdmin):

    list_display   = ("referencia", 'image_tag', "descripcion","diametro_cable","material","resistencia_kn","pdf")
    #list_filter    = ("equipos_tipo",)

    search_fields  = ("referencia", "tipo")

class ReferenciasSillasPerchas_admin(admin.ModelAdmin):

    list_display   = ("referencia", 'image_tag', "resistencia_kn","pdf")
    #list_filter    = ("equipos_tipo",)

    search_fields  = ("referencia", "tipo")

class EquiposTipo_admin(admin.ModelAdmin):

    #form = formfield_for_foreignkey_ReferenciasArnes

    list_display   = ("nombre","lineas_tipo","descripcion")

class LineasTipo_admin(admin.ModelAdmin):

    #form = formfield_for_foreignkey_ReferenciasArnes

    list_display   = ("nombre","descripcion")

class Inspector_admin(admin.StackedInline):
    

    fieldsets = (
        (Inspectores, {
            'fields': ('phone', 'empresa', 'ciudad', 'lugar', 'fecha', 'certificado_inspector', 'carnet_inspector', 'foto_inspector')
        }),
    )
    
    add_fieldsets = (
        (Inspectores, {
            'fields': ('phone', 'empresa', 'ciudad', 'lugar', 'fecha', 'certificado_inspector', 'carnet_inspector', 'foto_inspector')
        }),
    )
    #form = formfield_for_foreignkey_ReferenciasArnes
    model = Inspectores

class InspeccionArnes_admin(admin.ModelAdmin):


    list_display  = (
        "user",
        "get_numero_producto",
        'image_tag',
        "fecha_inspeccion",
        "proxima_inspeccion",
        "numero_inspeccion",
        'reata_tienen_hoyos_agujeros',
        'reata_deshilachadas',
        'reata_cortadas_desgastadas',
        'reata_talladuras',
        'reata_torsion',
        'reata_suciedad',
        'reata_quemadura',
        'reata_salpicadura_rigidez',
        'reata_sustancia_quimica',
        'otros_arnes_cinta',
        'costuras_completas_continuas',
        'costuras_visibles',
        'costuras_indicador_impacto_activado',
        'otros_arnes_costuras',
        'metalicas_completas',
        'metalicas_corrosion_oxido',
        'metalicas_deformacion',
        'metalicas_fisuras_golpes_hundimiento',
        'otros_metalicas',
        
        )

    def get_numero_producto(self, obj):

        return obj.equipos_arnes.numero_producto

    
    get_numero_producto.short_description = 'Numero Producto'
    #list_editable  = ("fecha_fabricacion","numero_producto",)
    list_filter    = ("fecha_inspeccion",)
    date_hierarchy = "fecha_inspeccion"

class InspeccionEslingas_admin(admin.ModelAdmin):


    list_display  = (
        "user",
        "get_numero_producto",
        'image_tag',
        "fecha_inspeccion",
        "proxima_inspeccion",
        "numero_inspeccion",
        'absorbedor_hoyos_desgarres', 
        'absorbedor_costuras_sueltas_reventadas', 
        'absorbedor_deterioro', 
        'absorbedor_suciedad', 
        'absorbedor_quemaduras_soldadura_cigarrillo',
        'absorbedor_salpicadura_rigidez',
        'otros_absorbedor',
        'reata_deshilachadas', 
        'reata_desgastadas', 
        'reata_talladuras', 
        'reata_salpicadura_rigidez', 
        'reata_torsion',
        'otros_cinta',
        'metalicas_completas', 
        'metalicas_corrosion_oxido', 
        'metalicas_compuertas',
        'metalicas_deformacion_fisuras_golpes_hundimiento', 
        'otros_metalicas',
        'costuras_completas_continuas', 
        'costuras_visibles', 
        'otros_costuras',
        )

    def get_numero_producto(self, obj):

        return obj.equipos_eslingas.numero_producto

    get_numero_producto.short_description = 'Numero Producto'
    #list_editable  = ("fecha_fabricacion","numero_producto",)
    list_filter    = ("fecha_inspeccion",)
    date_hierarchy = "fecha_inspeccion"

class InspeccionLineas_admin(admin.ModelAdmin):


    list_display  = (
        "user",
        "get_numero_producto",
        'image_tag',
        "fecha_inspeccion",
        "proxima_inspeccion",
        "numero_inspeccion",
        'metalicas_completas', 
        'metalicas_fisuras',
        'metalicas_corrosion_oxido',
        'metalicas_golpes_hundimiento',
        'metalicas_compuertas_ganchos',  
        'otros_metalicas',
        'reata_deshilachadas', 
        'reata_quemadura',
        'reata_torsion_talladuras', 
        'reata_salpicadura_rigidez', 
        'reata_ruptura', 
        'otros_lineas_cinta',
        'costuras_completas_continuas', 
        'costuras_visibles', 
        'otros_lineas_costuras',
        )

    def get_numero_producto(self, obj):

        return obj.equipos_lineas_anclajes.numero_producto

    get_numero_producto.short_description = 'Numero Producto'
    #list_editable  = ("fecha_fabricacion","numero_producto",)
    list_filter    = ("fecha_inspeccion",)
    date_hierarchy = "fecha_inspeccion"

class InspeccionCasco_admin(admin.ModelAdmin):


    list_display  = (
        "user",
        "get_numero_producto",
        'image_tag',
        "fecha_inspeccion",
        "proxima_inspeccion",
        "numero_inspeccion",
        'casquete_fisuras_golpes_hundimiento', 
        'casquete_quemaduras_deterioro_quimicos',
        'casquete_rayadura_decoloracion',
        'otros_casquete',
        'suspencion_completo', 
        'suspencion_fisuras_golpes_hundimientos',
        'suspencion_torsion_estiramiento',  
        'otros_suspencion',
        'barbuquejo_completo', 
        'barbuquejo_cinta_deshilachada_rotas', 
        'barbuquejo_salpicadura_pintura_rigidez_cinta',
        'otros_barbuquejo',
        )

    def get_numero_producto(self, obj):

        return obj.equipos_cascos.numero_producto

    get_numero_producto.short_description = 'Numero Producto'
    #list_editable  = ("fecha_fabricacion","numero_producto",)
    list_filter    = ("fecha_inspeccion",)
    date_hierarchy = "fecha_inspeccion"

class InspeccionAccesorio_admin(admin.ModelAdmin):


    list_display  = (
        "user",
        "get_numero_producto",
        'image_tag',
        "fecha_inspeccion",
        "proxima_inspeccion",
        "numero_inspeccion",
        'mosquetones_fisuras_golpes_hundimiento', 
        'mosquetones_quemaduras_deterioro_quimicos',
        'mosquetones_oxidacion_corrocion_mosquetones',
        'mosquetones_bordes_filosos_rugosos',
        'mosquetones_compuerta_libre',
        'mosquetones_deformaciones',
        'otros_mosquetones',
        'arrestador_poleas_fisuras_golpes_hundimientos',
        'arrestador_poleas_frenado_lisa',
        'arrestador_poleas_oxidacion_corrocion',
        'arrestador_poleas_bordes_filosos_rugosos',
        'arrestador_poleas_compuerta_libre',
        'arrestador_poleas_deformaciones',
        'otros_arrestador_poleas',
        'descendedores_anclajes_fisuras_golpes_hundimientos',
        'descendedores_anclajes_contacto_lisa',
        'descendedores_anclajes_oxidacion_corrocion',
        'descendedores_anclajes_bordes_filosos_rugosos',
        'descendedores_anclajes_desgaste_disminucion_metal',
        'descendedores_anclajes_deformaciones',
        'otros_descendedores_anclajes',
        )

    def get_numero_producto(self, obj):

        return obj.equipos_accesorios_metalicos.numero_producto

    get_numero_producto.short_description = 'Numero Producto'
    #list_editable  = ("fecha_fabricacion","numero_producto",)
    list_filter    = ("fecha_inspeccion",)
    date_hierarchy = "fecha_inspeccion"

class InspeccionSilla_admin(admin.ModelAdmin):


    list_display  = (
        "user",
        "get_numero_producto",
        'image_tag',
        "fecha_inspeccion",
        "proxima_inspeccion",
        "numero_inspeccion",
        'reata_tienen_hoyos_agujeros', 
        'reata_deshilachadas',
        'reata_desgastadas',
        'reata_talladuras',
        'reata_torsion',
        'reata_suciedad',
        'reata_quemadura',
        'reata_salpicadura_rigidez',
        'reata_sustancia_quimica',
        'otros_cinta_reata',
        'costuras_completas_continuas',
        'costuras_visibles',
        'otros_silla_costuras',
        'metalicas_completas',
        'metalicas_corrosion',
        'metalicas_deformacion',
        'metalicas_fisuras_golpes',
        'otros_metalicas',
        'madera_golpes_rupturas', 
        'madera_polillas', 
        'madera_exceso_humeda', 
        'otros_madera',
        )

    def get_numero_producto(self, obj):

        return obj.equipos_sillas_perchas.numero_producto

    get_numero_producto.short_description = 'Numero Producto'
    #list_editable  = ("fecha_fabricacion","numero_producto",)
    list_filter    = ("fecha_inspeccion",)
    date_hierarchy = "fecha_inspeccion"

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:

        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    
    class Meta:

        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
#donde esta el tuto para implementar la extención del formulario 
# https://cpadiernos.github.io/how-to-add-fields-to-the-user-model-in-django.html 
class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
                )
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Información adicional', {
            'fields': ('is_inspector', 'is_register')
        })
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
                )
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Información adicional', {
            'fields': ('is_inspector', 'is_register')
        })
    )
    list_display=('username','email','first_name','last_name','is_staff','is_inspector','is_register')
    inlines = [
        Inspector_admin
    ]
    
    class Meta:

            fields = '__all__'
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.


    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    filter_horizontal = ()

class CiudadCodigo_admin(admin.ModelAdmin):

    #form = formfield_for_foreignkey_ReferenciasArnes

    list_display   = ("ciudad","departamento", "codigo")
    
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(EquiposArnes,EquiposArnes_admin)

admin.site.register(EquiposEslinga,EquiposEslinga_admin)

admin.site.register(EquiposLineasAnclajes,EquiposLineas_admin)

admin.site.register(EquiposCascoSegurida,EquiposCasco_admin)

admin.site.register(EquiposAccesorioMetalicos,EquiposAccesorioMetalicos_admin)

admin.site.register(EquiposSillasPerchas,EquiposSillasPerchas_admin)

admin.site.register(ReferenciasArnes,ReferenciasArnes_admin)

admin.site.register(ReferenciasEslingas,ReferenciasEslingas_admin)

admin.site.register(ReferenciasLineasAnclajes,ReferenciasLineasAnclajes_admin)

admin.site.register(ReferenciasCascoSeguridad,ReferenciasCascoSegurida_admin)

admin.site.register(ReferenciasAccesorioMetalicos,ReferenciasAccesorioMetalicos_admin)

admin.site.register(ReferenciasSillasPerchas,ReferenciasSillasPerchas_admin)

admin.site.register(LineasTipo,LineasTipo_admin)

admin.site.register(InspeccionArnes,InspeccionArnes_admin)

admin.site.register(InspeccionEslinga,InspeccionEslingas_admin)

admin.site.register(InspeccionLineasAnclajes,InspeccionLineas_admin)

admin.site.register(InspeccionCascoSeguridad,InspeccionCasco_admin)

admin.site.register(InspeccionAccesorioMetalicos,InspeccionAccesorio_admin)

admin.site.register(InspeccionSillasPerchas,InspeccionSilla_admin)

admin.site.register(CiudadCodigo,CiudadCodigo_admin)
