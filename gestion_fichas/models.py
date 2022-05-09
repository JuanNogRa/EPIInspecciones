# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove ` ` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models,connections

from django.core.files import File
from django.contrib.auth.models import AbstractUser
from django.conf import settings #To foreignk key
# importing necessery django classes

import tempfile
from io import BytesIO
from PIL import Image, ImageDraw
import qrcode

import datetime
from django.utils.html import format_html,mark_safe

from django.db import  models
from django.db.models.fields import AutoField
from django.utils.text import slugify
import os.path
import six


#date
now = datetime.datetime.now()
only_date = now.date()
date = only_date.strftime("/%Y/%m")
LINK = 'http://164.92.73.232/hv/'

LINL_PDF = 'http://164.92.73.232/media'

# LINK = 'http://andrewgomz.pythonanywhere.com/hv/'

# LINL_PDF = 'http://andrewgomz.pythonanywhere.com/'

class LoadDataQuerySet(models.QuerySet):
    """A QuerySet with an additional load_data method which inserts data quickly in bulk."""

    def _convert_instance_to_line(self, fields, instance, connection):
        """Convert an object to a single line to be placed in the temporary file."""
        # Convert each field value to a database value.
        #
        # Escape the enclosure and escape characters since they are not handled
        # automatically.
        db_prep_values = [
            six.text_type(self.model._meta.get_field(field_name).get_db_prep_value(
                getattr(instance, field_name), connection)).replace('\\', '\\\\').replace('"', '\\"')
            for field_name in fields
        ]

        # Comma separate the wrapped values.
        return ','.join(map(lambda v: '"' + v + '"', db_prep_values)) + '\n'

    def load_data(self, objs):
        """
        Inserts each of the instances into the database. This does *not* call
        save() on each of the instances, does not send any pre/post save
        signals, and does not set the primary key attribute if it is an
        autoincrement field. Multi-table models are not supported.

        Write the data to a temporary file, then insert that data into MySQL via a LOAD DATA call.

        :param tuple fields: A tuple of string field names.
        :param list objs: The list of objects to insert.
        :returns: The number of inserted records.
        :rtype int:
        """

        # This is based on by bulk_create.
        self._for_write = True
        connection = connections[self.db]
        fields = self.model._meta.concrete_fields
        fields = [f.name for f in fields if not isinstance(f, AutoField)]

        # The table name and field names cannot be parameterized when executing
        # a SQL statement with the Django ORM. The name of the file where data
        # is loaded from can be parameterized, however.
        #
        # The result of this is a partially formatted string to be fed into MySQL.
        load_data_statement = """
            LOAD DATA LOCAL INFILE %s INTO TABLE {mysql_table_name} CHARACTER SET utf8 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n' ({fields});
            """.format(
                mysql_table_name=self.model._meta.db_table,
                fields=', '.join(fields)
            ).strip()

        # Write each object to their own line in a temporary file and bulk
        # insert the data into MySQL using the LOAD DATA statement.
        with tempfile.NamedTemporaryFile(mode='w', suffix='.data', delete=True) as data_file:
            data_file.writelines(
                self._convert_instance_to_line(fields, obj, connection) for obj in objs
            )
            data_file.flush()

            with connection.cursor() as cursor:
                return cursor.execute(load_data_statement, [data_file.name])




# class CategoryChoiceField(forms.ModelChoiceField):
#      def label_from_instance(self, obj):
#          return "Referencia: {}".format(obj.referencia)

class LineaProducionConfeccion(models.Model):
    linea_numero = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'linea_produccion_confeccion'

    def __str__(self):
        return self.nombre

class EquiposArnes(models.Model):

    global date, LINK
    now = datetime.datetime.now()
    only_date = now.date()
    date_now = only_date.strftime("%d/%m/%Y")
    date_now_default = only_date.strftime("%Y-%m-%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING,default=None)
    numero_producto = models.CharField(max_length=7,unique=True)
    fecha_puesta_en_uso = models.DateField(default=date_now_default, blank=True)
    fecha_fabricacion = models.DateField()
    veredicto = models.BooleanField(default=True)
    codigo_interno = models.CharField(max_length=255,default=None, blank=True)
    personal_a_cargo = models.CharField(max_length=255,default=None, blank=True)
    codigo_qr = models.ImageField(upload_to='codigos_qr'+str(date), default = ' ')
    referencias_arnes = models.ForeignKey('ReferenciasArnes', models.DO_NOTHING,default=None)
    empresa = models.CharField(max_length=255, default=None, blank=True)
    telefono = models.CharField(max_length=255, default=None, blank=True)
    correo = models.CharField(max_length=255, default=None, blank=True)
    #pdf = models.FileField(upload_to= 'PDF'+str(date), default = '/media/Ficha_inspeccion.pdf' )

    def save(self, *args, **kwargs):

        url = LINK+str(self.numero_producto)+"/1"
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.numero_producto}-1.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr.url))

    image_tag.short_description = 'Codigo_qr'

    objects = LoadDataQuerySet.as_manager()
    def __str__(self):

        return self.numero_producto

    class Meta:

     db_table = 'equipos_arnes'

class EquiposEslinga(models.Model):

    global date, LINK
    now = datetime.datetime.now()
    only_date = now.date()
    date_now = only_date.strftime("%d/%m/%Y")
    date_now_default = only_date.strftime("%Y-%m-%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING,default=None)
    numero_producto = models.CharField(max_length=7,unique=True)
    fecha_puesta_en_uso = models.DateField(default=date_now_default, blank=True)
    fecha_fabricacion = models.DateField()
    veredicto = models.BooleanField(default=True)
    codigo_interno = models.CharField(max_length=255,default=None, blank=True)
    personal_a_cargo = models.CharField(max_length=255,default=None, blank=True)
    referencias_eslingas = models.ForeignKey('ReferenciasEslingas', models.DO_NOTHING,default=None)
    codigo_qr = models.ImageField(upload_to='codigos_qr'+str(date), default = ' ')
    empresa = models.CharField(max_length=255,default=None, blank=True)
    empresa = models.CharField(max_length=255,default=None, blank=True)
    telefono = models.CharField(max_length=255,default=None, blank=True)
    correo = models.CharField(max_length=255,default=None, blank=True)
    #pdf = models.FileField(upload_to= 'PDF'+str(date), default = '/media/Ficha_inspeccion.pdf' )

    def save(self, *args, **kwargs):

        url = LINK+str(self.numero_producto)+"/2"
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.numero_producto}-2.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr.url))

    image_tag.short_description = 'Codigo_qr'

    objects = LoadDataQuerySet.as_manager()
    def __str__(self):

        return self.numero_producto

    class Meta:

     db_table = 'equipos_eslingas'

class EquiposLineasAnclajes(models.Model):

    global date, LINK
    now = datetime.datetime.now()
    only_date = now.date()
    date_now = only_date.strftime("%d/%m/%Y")
    date_now_default = only_date.strftime("%Y-%m-%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING,default=None)
    numero_producto = models.CharField(max_length=7,unique=True)
    fecha_puesta_en_uso = models.DateField(default=date_now_default, blank=True)
    fecha_fabricacion = models.DateField()
    veredicto = models.BooleanField(default=True)
    codigo_interno = models.CharField(max_length=255,default=None, blank=True)
    personal_a_cargo = models.CharField(max_length=255,default=None, blank=True)
    referencias_anclajes = models.ForeignKey('ReferenciasLineasAnclajes', models.DO_NOTHING,default=None)
    empresa = models.CharField(max_length=255,default=None, blank=True)
    codigo_qr = models.ImageField(upload_to='codigos_qr'+str(date), default = ' ')
    empresa = models.CharField(max_length=255,default=None, blank=True)
    telefono = models.CharField(max_length=255,default=None, blank=True)
    correo = models.CharField(max_length=255,default=None, blank=True)
    #pdf = models.FileField(upload_to= 'PDF'+str(date), default = '/media/Ficha_inspeccion.pdf' )

    def save(self, *args, **kwargs):

        url = LINK+str(self.numero_producto)+"/3"
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.numero_producto}-3.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr.url))

    image_tag.short_description = 'Codigo_qr'

    objects = LoadDataQuerySet.as_manager()
    def __str__(self):

        return self.numero_producto

    class Meta:

     db_table = 'equipos_lineas_anclajes'


class EquiposCascoSegurida(models.Model):

    global date, LINK
    now = datetime.datetime.now()
    only_date = now.date()
    date_now = only_date.strftime("%d/%m/%Y")
    date_now_default = only_date.strftime("%Y-%m-%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING,default=None)
    numero_producto = models.CharField(max_length=7,unique=True)
    fecha_puesta_en_uso = models.DateField(default=date_now_default, blank=True)
    fecha_fabricacion = models.DateField()
    veredicto = models.BooleanField(default=True)
    codigo_interno = models.CharField(max_length=255,default=None, blank=True)
    personal_a_cargo = models.CharField(max_length=255,default=None, blank=True)
    referencias_casco = models.ForeignKey('ReferenciasCascoSeguridad', models.DO_NOTHING,default=None)
    codigo_qr = models.ImageField(upload_to='codigos_qr'+str(date), default = ' ')
    #pdf = models.FileField(upload_to= 'PDF'+str(date), default = '/media/Ficha_inspeccion.pdf' )
    empresa = models.CharField(max_length=255,default=None, blank=True)
    telefono = models.CharField(max_length=255,default=None, blank=True)
    correo = models.CharField(max_length=255,default=None, blank=True)
    
    def save(self, *args, **kwargs):

        url = LINK+str(self.numero_producto)+"/4"
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.numero_producto}-4.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr.url))

    image_tag.short_description = 'Codigo_qr'

    objects = LoadDataQuerySet.as_manager()
    def __str__(self):

        return self.numero_producto

    class Meta:

     db_table = 'equipos_cascos'


class EquiposAccesorioMetalicos(models.Model):

    global date, LINK
    now = datetime.datetime.now()
    only_date = now.date()
    date_now = only_date.strftime("%d/%m/%Y")
    date_now_default = only_date.strftime("%Y-%m-%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING,default=None)
    numero_producto = models.CharField(max_length=7,unique=True)
    fecha_puesta_en_uso = models.DateField(default=date_now_default, blank=True)
    fecha_fabricacion = models.DateField()
    veredicto = models.BooleanField(default=True)
    codigo_interno = models.CharField(max_length=255,default=None, blank=True)
    personal_a_cargo = models.CharField(max_length=255,default=None, blank=True)
    referencias_accesorio_metalicos = models.ForeignKey('ReferenciasAccesorioMetalicos', models.DO_NOTHING,default=None)
    codigo_qr = models.ImageField(upload_to='codigos_qr'+str(date), default = ' ')
    empresa = models.CharField(max_length=255,default=None, blank=True)
    empresa = models.CharField(max_length=255,default=None, blank=True)
    telefono = models.CharField(max_length=255,default=None, blank=True)
    correo = models.CharField(max_length=255,default=None, blank=True)
    #pdf = models.FileField(upload_to= 'PDF'+str(date), default = '/media/Ficha_inspeccion.pdf' )

    def save(self, *args, **kwargs):

        url = LINK+str(self.numero_producto)+"/5"
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.numero_producto}-5.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr.url))

    image_tag.short_description = 'Codigo_qr'

    objects = LoadDataQuerySet.as_manager()
    def __str__(self):

        return self.numero_producto

    class Meta:

     db_table = 'equipos_accesorios_metalicos'

class EquiposSillasPerchas(models.Model):

    global date, LINK
    now = datetime.datetime.now()
    only_date = now.date()
    date_now = only_date.strftime("%d/%m/%Y")
    date_now_default = only_date.strftime("%Y-%m-%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING,default=None)
    numero_producto = models.CharField(max_length=7,unique=True)
    fecha_puesta_en_uso = models.DateField(default=date_now_default, blank=True)
    fecha_fabricacion = models.DateField()
    veredicto = models.BooleanField(default=True)
    codigo_interno = models.CharField(max_length=255,default=None, blank=True)
    personal_a_cargo = models.CharField(max_length=255,default=None, blank=True)
    referencias_sillas = models.ForeignKey('ReferenciasSillasPerchas', models.DO_NOTHING,default=None)
    codigo_qr = models.ImageField(upload_to='codigos_qr'+str(date), default = ' ')
    #pdf = models.FileField(upload_to= 'PDF'+str(date), default = '/media/Ficha_inspeccion.pdf' )
    empresa = models.CharField(max_length=255,default=None, blank=True)
    telefono = models.CharField(max_length=255,default=None, blank=True)
    correo = models.CharField(max_length=255,default=None, blank=True)
    
    def save(self, *args, **kwargs):

        url = LINK+str(self.numero_producto)+"/6"
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.numero_producto}-6.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr.url))

    image_tag.short_description = 'Codigo_qr'

    objects = LoadDataQuerySet.as_manager()
    def __str__(self):

        return self.numero_producto

    class Meta:

     db_table = 'equipos_sillas_perchas'
     
class InspeccionArnes(models.Model):
    equipos_arnes = models.ForeignKey('EquiposArnes', models.DO_NOTHING, default=None)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING, default=None)
    veredicto = models.BooleanField(default=True)
    fecha_inspeccion = models.DateField()
    proxima_inspeccion = models.DateField()
    comentarios_adicionales = models.TextField(default='')

    numero_inspeccion = models.PositiveIntegerField()

    reata_tienen_hoyos_agujeros = models.BooleanField(default=False)
    reata_deshilachadas = models.BooleanField(default=False)
    reata_cortadas_desgastadas = models.BooleanField(default=False)
    reata_talladuras = models.BooleanField(default=False)
    reata_torsion = models.BooleanField(default=False)
    reata_suciedad = models.BooleanField(default=False)
    reata_quemadura = models.BooleanField(default=False)
    reata_salpicadura_rigidez = models.BooleanField(default=False)
    reata_sustancia_quimica = models.BooleanField(default=False)
    otros_arnes_cinta = models.BooleanField(default=False)
    reata_foto = models.ImageField(upload_to='arnes_cinta_reata'+str(date), default='empty.jpg')

    costuras_completas_continuas = models.BooleanField(default=False)
    costuras_visibles = models.BooleanField(default=False)
    costuras_indicador_impacto_activado = models.BooleanField(default=False)
    otros_arnes_costuras = models.BooleanField(default=False)
    costuras_foto = models.ImageField(upload_to='arnes_costuras_etiquetas'+str(date), default = 'empty.jpg')

    metalicas_completas = models.BooleanField(default=False)
    metalicas_corrosion_oxido = models.BooleanField(default=False)
    metalicas_deformacion = models.BooleanField(default=False)
    metalicas_fisuras_golpes_hundimiento = models.BooleanField(default=False)
    otros_metalicas = models.BooleanField(default=False)
    metalicas_foto = models.ImageField(upload_to='arnes_partes_metalicas'+str(date), default = 'empty.jpg')

    observacion_costuras_completas_continuas = models.CharField(max_length=255, default=None)
    observacion_costuras_visibles = models.CharField(max_length=255, default=None)
    observacion_costuras_indicador_impacto = models.CharField(max_length=255, default=None)
    observacion_costuras_otros = models.CharField(max_length=255, default=None)


    observacion_reata_hoyo = models.CharField(max_length=255, default=None)
    observacion_reata_deshilachadas = models.CharField(max_length=255, default=None)
    observacion_reata_cortadas_desgastadas = models.CharField(max_length=255, default=None)
    observacion_reata_talladuras = models.CharField(max_length=255, default=None)
    observacion_reata_torsion = models.CharField(max_length=255, default=None)
    observacion_reata_suciedad = models.CharField(max_length=255, default=None)
    observacion_reata_quemadura = models.CharField(max_length=255, default=None)
    observacion_reata_salpicadura_rigidez = models.CharField(max_length=255, default=None)
    observacion_reata_sustancia_quimica = models.CharField(max_length=255, default=None)
    observacion_reata_otros = models.CharField(max_length=255, default=None)

    observacion_metalicas_completas = models.CharField(max_length=255, default=None)
    observacion_metalicas_fisuras_golpes = models.CharField(max_length=255, default='')
    observacion_metalicas_corrosion_oxido = models.CharField(max_length=255, default=None)
    observacion_metalicas_deformacion = models.CharField(max_length=255, default=None)
    observacion_metalicas_otros = models.CharField(max_length=255, default=None)

    codigo_qr_pdf = models.ImageField(upload_to='codigos_qr_inspecciones/', default = ' ')
    def save(self, *args, **kwargs):
        
        url = LINL_PDF+str(self.equipos_arnes.id)+'/1/'+str(self.numero_inspeccion)+'/reporte_ficha_pdf/'
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (410, 410), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.equipos_arnes.id}-{self.numero_inspeccion}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr_pdf.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)
        new_image = compress(self.reata_foto)
        # set self.image to new_image
        self.reata_foto = new_image
        new_image = compress(self.costuras_foto)
        # set self.image to new_image
        self.costuras_foto = new_image
        new_image = compress(self.metalicas_foto)
        # set self.image to new_image
        self.metalicas_foto = new_image

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr_pdf.url))

    image_tag.short_description = 'Codigo_qr'

    class Meta:

        db_table = 'inspeccion_arnes'

class InspeccionEslinga(models.Model):
    equipos_eslingas = models.ForeignKey('EquiposEslinga', models.DO_NOTHING, default=None)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING, default=None)
    veredicto = models.BooleanField(default=True)
    fecha_inspeccion = models.DateField()
    proxima_inspeccion = models.DateField()
    comentarios_adicionales = models.TextField(default='')

    numero_inspeccion = models.PositiveIntegerField()

    absorbedor_hoyos_desgarres = models.BooleanField(default=False)
    absorbedor_costuras_sueltas_reventadas = models.BooleanField(default=False)
    absorbedor_deterioro = models.BooleanField(default=False)
    absorbedor_suciedad = models.BooleanField(default=False)
    absorbedor_quemaduras_soldadura_cigarrillo = models.BooleanField(default=False)
    absorbedor_salpicadura_rigidez = models.BooleanField(default=False)
    otros_absorbedor = models.BooleanField(default=False)
    absorbedor_foto = models.ImageField(upload_to='eslinga_absorbedor'+str(date), default = 'empty.jpg')

    reata_deshilachadas = models.BooleanField(default=False)
    reata_desgastadas = models.BooleanField(default=False)
    reata_talladuras = models.BooleanField(default=False)
    reata_salpicadura_rigidez = models.BooleanField(default=False)
    reata_torsion = models.BooleanField(default=False)
    otros_cinta = models.BooleanField(default=False)
    reata_foto = models.ImageField(upload_to='eslinga_cinta_reata'+str(date), default='empty.jpg')

    metalicas_completas = models.BooleanField(default=False)
    metalicas_corrosion_oxido = models.BooleanField(default=False)
    metalicas_compuertas = models.BooleanField(default=False)
    metalicas_deformacion_fisuras_golpes_hundimiento = models.BooleanField(default=False)
    otros_metalicas = models.BooleanField(default=False)
    metalicas_foto = models.ImageField(upload_to='eslinga_partes_metalicas'+str(date), default = 'empty.jpg')
        
    costuras_completas_continuas = models.BooleanField(default=False)
    costuras_visibles = models.BooleanField(default=False)
    otros_costuras = models.BooleanField(default=False)
    costuras_foto = models.ImageField(upload_to='eslinga_costuras_etiquetas'+str(date), default = 'empty.jpg')
    
    observacion_absorbedor_hoyos_desgarres = models.CharField(max_length=255, default=None)
    observacion_absorbedor_costuras_sueltas_reventadas = models.CharField(max_length=255, default=None)
    observacion_absorbedor_deterioro = models.CharField(max_length=255, default=None)
    observacion_absorbedor_suciedad = models.CharField(max_length=255, default=None)
    observacion_absorbedor_quemaduras_soldadura_cigarrillo = models.CharField(max_length=255, default=None)
    observacion_absorbedor_salpicadura_rigidez = models.CharField(max_length=255, default=None)
    observacion_otros_absorbedor = models.CharField(max_length=255, default=None)
    
    observacion_reata_deshilachadas = models.CharField(max_length=255, default=None)
    observacion_reata_desgastadas = models.CharField(max_length=255, default=None)
    observacion_reata_talladuras = models.CharField(max_length=255, default=None)
    observacion_reata_salpicadura_rigidez = models.CharField(max_length=255, default=None)
    observacion_reata_torsion = models.CharField(max_length=255, default=None)
    observacion_reata_otros = models.CharField(max_length=255, default=None)

    observacion_metalicas_completas = models.CharField(max_length=255, default=None)
    observacion_metalicas_corrosion_oxido = models.CharField(max_length=255, default=None)
    observacion_metalicas_compuertas = models.CharField(max_length=255, default=None)
    observacion_metalicas_deformacion_fisuras_golpes = models.CharField(max_length=255, default=None)
    observacion_metalicas_otros = models.CharField(max_length=255, default=None)

    observacion_costuras_completas_continuas = models.CharField(max_length=255, default=None)
    observacion_costuras_visibles = models.CharField(max_length=255, default=None)
    observacion_costuras_otros = models.CharField(max_length=255, default=None)

    codigo_qr_pdf = models.ImageField(upload_to='codigos_qr_inspecciones/', default = ' ')
    #pdf = models.FileField(upload_to='inspecciones/eslinga'+str(date))
    def save(self, *args, **kwargs):

        url = LINL_PDF+str(self.equipos_eslingas.id)+'/1/'+str(self.numero_inspeccion)
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (410, 410), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.equipos_eslingas.id}-{self.numero_inspeccion}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr_pdf.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)
        new_image = compress(self.absorbedor_foto)
        # set self.image to new_image
        self.absorbedor_foto = new_image
        new_image = compress(self.reata_foto)
        # set self.image to new_image
        self.reata_foto = new_image
        new_image = compress(self.metalicas_foto)
        # set self.image to new_image
        self.metalicas_foto = new_image
        new_image = compress(self.costuras_foto)
        # set self.image to new_image
        self.costuras_foto = new_image


    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr_pdf.url))

    image_tag.short_description = 'Codigo_qr'

    class Meta:

        db_table = 'inspeccion_eslingas'


class InspeccionLineasAnclajes(models.Model):
    equipos_lineas_anclajes = models.ForeignKey('EquiposLineasAnclajes', models.DO_NOTHING, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING, default=None)
    veredicto = models.BooleanField(default=True)
    fecha_inspeccion = models.DateField()
    proxima_inspeccion = models.DateField()
    comentarios_adicionales = models.TextField(default='')

    numero_inspeccion = models.PositiveIntegerField()


    metalicas_completas = models.BooleanField(default=False)
    metalicas_fisuras = models.BooleanField(default=False)
    metalicas_corrosion_oxido = models.BooleanField(default=False)
    metalicas_golpes_hundimiento = models.BooleanField(default=False)
    metalicas_compuertas_ganchos = models.BooleanField(default=False)
    otros_metalicas = models.BooleanField(default=False)
    metalicas_foto = models.ImageField(upload_to='lineas_anclajes_partes_metalicas'+str(date), default = 'empty.jpg')

    reata_deshilachadas = models.BooleanField(default=False)
    reata_quemadura = models.BooleanField(default=False)
    reata_torsion_talladuras = models.BooleanField(default=False)
    reata_salpicadura_rigidez = models.BooleanField(default=False)
    reata_ruptura = models.BooleanField(default=False)
    otros_lineas_cinta = models.BooleanField(default=False)
    reata_foto = models.ImageField(upload_to='lineas_anclajes_cinta_reata'+str(date), default='empty.jpg')
        
    costuras_completas_continuas = models.BooleanField(default=False)
    costuras_visibles = models.BooleanField(default=False)
    otros_lineas_costuras = models.BooleanField(default=False)
    costuras_foto = models.ImageField(upload_to='lineas_anclajes_costuras_etiquetas'+str(date), default = 'empty.jpg')

    observacion_metalicas_completas = models.CharField(max_length=255, default=None)
    observacion_metalicas_fisuras = models.CharField(max_length=255, default=None)
    observacion_metalicas_corrosion_oxido = models.CharField(max_length=255, default=None)
    observacion_metalicas_golpes_hundimientos = models.CharField(max_length=255, default=None)
    observacion_metalicas_compuertas_ganchos = models.CharField(max_length=255, default=None)
    observacion_metalicas_otros = models.CharField(max_length=255, default=None)

    observacion_reata_deshilachadas = models.CharField(max_length=255, default=None)
    observacion_reata_quemadura = models.CharField(max_length=255, default=None)
    observacion_reata_torsion_talladuras = models.CharField(max_length=255, default=None)
    observacion_reata_salpicadura_rigidez = models.CharField(max_length=255, default=None)
    observacion_reata_ruptura = models.CharField(max_length=255, default=None)
    observacion_otros_lineas_cinta = models.CharField(max_length=255, default=None)

    observacion_costuras_completas_continuas = models.CharField(max_length=255, default=None)
    observacion_costuras_visibles = models.CharField(max_length=255, default=None)
    observacion_costuras_otros = models.CharField(max_length=255, default=None)
    
    codigo_qr_pdf = models.ImageField(upload_to='codigos_qr_inspecciones/', default = ' ')
    def save(self, *args, **kwargs):

        url = LINL_PDF+str(self.equipos_lineas_anclajes.id)+'/1/'+str(self.numero_inspeccion)
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (410, 410), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.equipos_lineas_anclajes.id}-{self.numero_inspeccion}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr_pdf.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)
        new_image = compress(self.metalicas_foto)
        # set self.image to new_image
        self.metalicas_foto = new_image
        new_image = compress(self.reata_foto)
        # set self.image to new_image
        self.reata_foto = new_image
        new_image = compress(self.costuras_foto)
        # set self.image to new_image
        self.costuras_foto = new_image

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr_pdf.url))

    image_tag.short_description = 'Codigo_qr'

    class Meta:

        db_table = 'inspeccion_lineas_anclajes'


class InspeccionCascoSeguridad(models.Model):
    equipos_cascos = models.ForeignKey('EquiposCascoSegurida', models.DO_NOTHING, default=None)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING, default=None)
    veredicto = models.BooleanField(default=True)
    fecha_inspeccion = models.DateField()
    proxima_inspeccion = models.DateField()
    comentarios_adicionales = models.TextField(default='')

    numero_inspeccion = models.PositiveIntegerField()
    
    casquete_fisuras_golpes_hundimiento = models.BooleanField(default=False)
    casquete_quemaduras_deterioro_quimicos = models.BooleanField(default=False)
    casquete_rayadura_decoloracion = models.BooleanField(default=False)
    otros_casquete = models.BooleanField(default=False)
    casquete_foto = models.ImageField(upload_to='casco_casquete'+str(date), default = 'empty.jpg')

    suspencion_completo = models.BooleanField(default=False)
    suspencion_fisuras_golpes_hundimientos = models.BooleanField(default=False)
    suspencion_torsion_estiramiento = models.BooleanField(default=False)
    otros_suspencion = models.BooleanField(default=False)
    suspencion_foto = models.ImageField(upload_to='casco_suspencion'+str(date), default='empty.jpg')

    barbuquejo_completo = models.BooleanField(default=False)
    barbuquejo_cinta_deshilachada_rotas = models.BooleanField(default=False)
    barbuquejo_salpicadura_pintura_rigidez_cinta = models.BooleanField(default=False)
    otros_barbuquejo = models.BooleanField(default=False)
    barbuquejo_foto = models.ImageField(upload_to='casco_barbuquejo'+str(date), default = 'empty.jpg')

    observacion_casquete_fisuras_golpes_hundimiento = models.CharField(max_length=255, default=None)
    observacion_casquete_quemaduras_deterioro_quimicos = models.CharField(max_length=255, default=None)
    observacion_casquete_rayadura_decoloracion = models.CharField(max_length=255, default=None)
    observacion_casquete_otros = models.CharField(max_length=255, default=None)

    observacion_suspencion_completo = models.CharField(max_length=255, default=None)
    observacion_suspencion_fisuras_golpes_hundimientos = models.CharField(max_length=255, default=None)
    observacion_suspencion_torsion_estiramiento = models.CharField(max_length=255, default=None)
    observacion_suspencion_otros = models.CharField(max_length=255, default=None)

    observacion_barbuquejo_completo = models.CharField(max_length=255, default=None)
    observacion_barbuquejo_cinta_deshilachada_rotas = models.CharField(max_length=255, default=None)
    observacion_barbuquejo_salpicadura_pintura_rigidez_cinta = models.CharField(max_length=255, default=None)
    observacion_barbuquejo_otros = models.CharField(max_length=255, default=None)
    
    codigo_qr_pdf = models.ImageField(upload_to='codigos_qr_inspecciones/', default = ' ')
    def save(self, *args, **kwargs):

        url = LINL_PDF+str(self.equipos_cascos.id)+'/1/'+str(self.numero_inspeccion)
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (410, 410), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.equipos_cascos.id}-{self.numero_inspeccion}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr_pdf.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)
        new_image = compress(self.casquete_foto)
        # set self.image to new_image
        self.casquete_foto = new_image
        new_image = compress(self.suspencion_foto)
        # set self.image to new_image
        self.suspencion_foto = new_image
        # set self.image to new_image
        new_image = compress(self.barbuquejo_foto)
        # set self.image to new_image
        self.barbuquejo_foto = new_image
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr_pdf.url))

    image_tag.short_description = 'Codigo_qr'

    class Meta:

        db_table = 'inspeccion_casco'


class InspeccionAccesorioMetalicos(models.Model):
    equipos_accesorios_metalicos = models.ForeignKey('EquiposAccesorioMetalicos', models.DO_NOTHING, default=None)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING, default=None)
    veredicto = models.BooleanField(default=True)
    fecha_inspeccion = models.DateField()
    proxima_inspeccion = models.DateField()
    comentarios_adicionales = models.TextField(default='')

    numero_inspeccion = models.PositiveIntegerField()
    
    mosquetones_fisuras_golpes_hundimiento = models.BooleanField(default=False)
    mosquetones_quemaduras_deterioro_quimicos = models.BooleanField(default=False)
    mosquetones_oxidacion_corrocion_mosquetones = models.BooleanField(default=False)
    mosquetones_bordes_filosos_rugosos = models.BooleanField(default=False)
    mosquetones_compuerta_libre = models.BooleanField(default=False)
    mosquetones_deformaciones = models.BooleanField(default=False)
    otros_mosquetones = models.BooleanField(default=False)
    mosquetones_foto = models.ImageField(upload_to='accesorios_metalicos_mosquetones'+str(date), default = 'empty.jpg')
    
    arrestador_poleas_fisuras_golpes_hundimientos = models.BooleanField(default=False)
    arrestador_poleas_frenado_lisa = models.BooleanField(default=False)
    arrestador_poleas_oxidacion_corrocion = models.BooleanField(default=False)
    arrestador_poleas_bordes_filosos_rugosos = models.BooleanField(default=False)
    arrestador_poleas_compuerta_libre = models.BooleanField(default=False)
    arrestador_poleas_deformaciones = models.BooleanField(default=False)
    otros_arrestador_poleas = models.BooleanField(default=False)
    arrestador_poleas_foto = models.ImageField(upload_to='accesorios_metalicos_arrestador_poleas'+str(date), default='empty.jpg')

    descendedores_anclajes_fisuras_golpes_hundimientos = models.BooleanField(default=False)
    descendedores_anclajes_contacto_lisa = models.BooleanField(default=False)
    descendedores_anclajes_oxidacion_corrocion = models.BooleanField(default=False)
    descendedores_anclajes_bordes_filosos_rugosos = models.BooleanField(default=False)
    descendedores_anclajes_desgaste_disminucion_metal = models.BooleanField(default=False)
    descendedores_anclajes_deformaciones = models.BooleanField(default=False)
    otros_descendedores_anclajes = models.BooleanField(default=False)
    descendedores_anclajes_foto = models.ImageField(upload_to='accesorios_metalicos_descendedores_anclajes'+str(date), default='empty.jpg')

    observacion_mosquetones_fisuras_golpes_hundimiento = models.CharField(max_length=255, default=None)
    observacion_mosquetones_quemaduras_deterioro_quimicos = models.CharField(max_length=255, default=None)
    observacion_mosquetones_oxidacion_corrocion_mosquetones = models.CharField(max_length=255, default=None)
    observacion_mosquetones_bordes_filosos_rugosos = models.CharField(max_length=255, default=None)
    observacion_mosquetones_compuerta_libre = models.CharField(max_length=255, default=None)
    observacion_mosquetones_deformaciones = models.CharField(max_length=255, default=None)
    observacion_mosquetones_otros = models.CharField(max_length=255, default=None)

    observacion_arrestador_poleas_fisuras_golpes_hundimientos = models.CharField(max_length=255, default=None)
    observacion_arrestador_poleas_frenado_lisa = models.CharField(max_length=255, default=None)
    observacion_arrestador_poleas_oxidacion_corrocion = models.CharField(max_length=255, default=None)
    observacion_arrestador_poleas_bordes_filosos_rugosos = models.CharField(max_length=255, default=None)
    observacion_arrestador_poleas_compuerta_libre = models.CharField(max_length=255, default=None)
    observacion_arrestador_poleas_deformaciones = models.CharField(max_length=255, default=None)
    observacion_arrestador_poleas_otros = models.CharField(max_length=255, default=None)

    observacion_descendedores_anclajes_fisuras_golpes_hundimientos = models.CharField(max_length=255, default=None)
    observacion_descendedores_anclajes_frenado_lisa = models.CharField(max_length=255, default=None)
    observacion_descendedores_anclajes_oxidacion_corrocion = models.CharField(max_length=255, default=None)
    observacion_descendedores_anclajes_bordes_filosos_rugosos = models.CharField(max_length=255, default=None)
    observacion_descendedores_anclajes_desgaste_disminucion_metal = models.CharField(max_length=255, default=None)
    observacion_descendedores_anclajes_deformaciones = models.CharField(max_length=255, default=None)
    observacion_descendedores_anclajes_otros = models.CharField(max_length=255, default=None)
    
    codigo_qr_pdf = models.ImageField(upload_to='codigos_qr_inspecciones/', default = ' ')
    
    def save(self, *args, **kwargs):

        url = LINL_PDF+str(self.equipos_accesorios_metalicos.id)+'/1/'+str(self.numero_inspeccion)
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (410, 410), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.equipos_accesorios_metalicos.id}-{self.numero_inspeccion}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr_pdf.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)
        new_image = compress(self.mosquetones_foto)
        # set self.image to new_image
        self.mosquetones_foto = new_image
        new_image = compress(self.arrestador_poleas_foto)
        # set self.image to new_image
        self.arrestador_poleas_foto = new_image
        new_image = compress(self.descendedores_anclajes_foto)
        # set self.image to new_image
        self.descendedores_anclajes_foto = new_image
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr_pdf.url))

    image_tag.short_description = 'Codigo_qr'

    class Meta:

        db_table = 'inspeccion_accesorio_metalicos'

class InspeccionSillasPerchas(models.Model):
    equipos_sillas_perchas = models.ForeignKey('EquiposSillasPerchas', models.DO_NOTHING, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING, default=None)
    veredicto = models.BooleanField(default=True)
    fecha_inspeccion = models.DateField()
    proxima_inspeccion = models.DateField()
    comentarios_adicionales = models.TextField(default='')

    numero_inspeccion = models.PositiveIntegerField()
   
    reata_tienen_hoyos_agujeros = models.BooleanField(default=False)
    reata_deshilachadas = models.BooleanField(default=False)
    reata_desgastadas = models.BooleanField(default=False)
    reata_talladuras = models.BooleanField(default=False)
    reata_torsion = models.BooleanField(default=False)
    reata_suciedad = models.BooleanField(default=False)
    reata_quemadura = models.BooleanField(default=False)
    reata_salpicadura_rigidez = models.BooleanField(default=False)
    reata_sustancia_quimica = models.BooleanField(default=False)
    otros_cinta_reata = models.BooleanField(default=False)
    cinta_reata_foto = models.ImageField(upload_to='silla_percha_reata'+str(date), default = 'empty.jpg')
    
    costuras_completas_continuas = models.BooleanField(default=False)
    costuras_visibles = models.BooleanField(default=False)
    otros_silla_costuras = models.BooleanField(default=False)
    costuras_foto = models.ImageField(upload_to='silla_percha_costuras_etiquetas'+str(date), default = 'empty.jpg')
    
    metalicas_completas = models.BooleanField(default=False)
    metalicas_corrosion = models.BooleanField(default=False)
    metalicas_deformacion = models.BooleanField(default=False)
    metalicas_fisuras_golpes = models.BooleanField(default=False)
    otros_metalicas = models.BooleanField(default=False)
    metalicas_foto = models.ImageField(upload_to='silla_percha_metalicas'+str(date), default='empty.jpg')

    madera_golpes_rupturas = models.BooleanField(default=False)
    madera_polillas = models.BooleanField(default=False)
    madera_exceso_humeda = models.BooleanField(default=False)
    otros_madera = models.BooleanField(default=False)
    madera_foto = models.ImageField(upload_to='silla_percha_metalicas'+str(date), default='empty.jpg')

    observacion_reata_tienen_hoyos_agujeros = models.CharField(max_length=255, default=None)
    observacion_reata_deshilachadas = models.CharField(max_length=255, default=None)
    observacion_reata_cortadas_desgastadas = models.CharField(max_length=255, default=None)
    observacion_reata_talladuras = models.CharField(max_length=255, default=None)
    observacion_reata_torsion = models.CharField(max_length=255, default=None)
    observacion_reata_suciedad = models.CharField(max_length=255, default=None)
    observacion_reata_quemadura = models.CharField(max_length=255, default=None)
    observacion_reata_salpicadura_rigidez = models.CharField(max_length=255, default=None)
    observacion_reata_sustancia_quimica = models.CharField(max_length=255, default=None)
    observacion_reata_otros = models.CharField(max_length=255, default=None)

    observacion_costuras_completas_continuas = models.CharField(max_length=255, default=None)
    observacion_costuras_visibles = models.CharField(max_length=255, default=None)
    observacion_otros_silla_costuras = models.CharField(max_length=255, default=None)

    observacion_metalicas_completas = models.CharField(max_length=255, default=None)
    observacion_metalicas_corrosion_oxido = models.CharField(max_length=255, default=None)
    observacion_metalicas_deformacion = models.CharField(max_length=255, default=None)
    observacion_metalicas_fisuras_golpes = models.CharField(max_length=255, default=None)
    observacion_metalicas_otros = models.CharField(max_length=255, default=None)
    
    observacion_madera_golpes_rupturas = models.CharField(max_length=255, default=None)
    observacion_madera_polillas = models.CharField(max_length=255, default=None)
    observacion_madera_exceso_humeda = models.CharField(max_length=255, default=None)
    observacion_otros_madera = models.CharField(max_length=255, default=None)
    codigo_qr_pdf = models.ImageField(upload_to='codigos_qr_inspecciones/', default = ' ')
    def save(self, *args, **kwargs):

        url = LINL_PDF+str(self.equipos_sillas_perchas.id)+'/1/'+str(self.numero_inspeccion)
        qrcode_img = qrcode.make(url)
        canvas = Image.new('RGB', (410, 410), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.equipos_sillas_perchas.id}-{self.numero_inspeccion}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.codigo_qr_pdf.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)
        new_image = compress(self.cinta_reata_foto)
        # set self.image to new_image
        self.cinta_reata_foto = new_image
        new_image = compress(self.costuras_foto)
        # set self.image to new_image
        self.costuras_foto = new_image
        new_image = compress(self.metalicas_foto)
        # set self.image to new_image
        self.metalicas_foto = new_image
        new_image = compress(self.madera_foto)
        # set self.image to new_image
        self.madera_foto = new_image

    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.codigo_qr_pdf.url))

    image_tag.short_description = 'Codigo_qr'

    class Meta:

        db_table = 'inspeccion_sillas_perchas'



class ReferenciasArnes(models.Model):
    referencia = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    talla = models.CharField(max_length=255,default=None)
    material = models.CharField(max_length=255)
    peso_maximo_kg = models.PositiveIntegerField()
    resistencia_kn = models.FloatField()
    # default = /media/empty.jpg
    referencia_imagen = models.ImageField(upload_to='Referencias/Imagenes',default='empty.jpg')
    pdf = models.FileField(upload_to= 'Referencias/PDF',default=None)
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.referencia_imagen.url))


    image_tag.short_description = 'Imagen_referencia'

    class Meta:

        db_table = 'referencias_arnes'

class ReferenciasEslingas(models.Model):
    referencia = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    peso_maximo_kg = models.PositiveIntegerField(blank=True)
    resistencia_kn = models.FloatField(blank=True)
    # default = /media/empty.jpg
    referencia_imagen = models.ImageField(upload_to='Referencias/Imagenes',default='empty.jpg')
    pdf = models.FileField(upload_to= 'Referencias/PDF',default=None)
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.referencia_imagen.url))


    image_tag.short_description = 'Imagen_referencia'

    class Meta:

        db_table = 'referencias_eslingas'

class ReferenciasLineasAnclajes(models.Model):
    referencia = models.CharField(max_length=255, unique=True)
    linea_anclaje = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, blank=True)
    material = models.CharField(max_length=255)
    diametro_ancho = models.CharField(max_length=255)
    peso_maximo_kg = models.PositiveIntegerField(blank=True)
    resistencia_kn = models.FloatField()
    # default = /media/empty.jpg
    referencia_imagen = models.ImageField(upload_to='Referencias/Imagenes',default='empty.jpg')
    pdf = models.FileField(upload_to= 'Referencias/PDF',default=None)
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.referencia_imagen.url))


    image_tag.short_description = 'Imagen_referencia'

    class Meta:

        db_table = 'referencias_lineas_anclajes'

class ReferenciasCascoSeguridad(models.Model):
    referencia = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    clase = models.CharField(max_length=255)
    # default = /media/empty.jpg
    referencia_imagen = models.ImageField(upload_to='Referencias/Imagenes',default='empty.jpg')
    pdf = models.FileField(upload_to= 'Referencias/PDF',default=None)
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.referencia_imagen.url))


    image_tag.short_description = 'Imagen_referencia'

    class Meta:

        db_table = 'referencias_cascos'


class ReferenciasAccesorioMetalicos(models.Model):
    referencia = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255)
    diametro_cable = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    resistencia_kn = models.FloatField()
    # default = /media/empty.jpg
    referencia_imagen = models.ImageField(upload_to='Referencias/Imagenes',default='empty.jpg')
    pdf = models.FileField(upload_to= 'Referencias/PDF',default=None)
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.referencia_imagen.url))


    image_tag.short_description = 'Imagen_referencia'

    class Meta:

        db_table = 'referencias_accesorio_metalicos'

class ReferenciasSillasPerchas(models.Model):
    referencia = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255)
    resistencia_kn = models.FloatField()
    # default = /media/empty.jpg
    referencia_imagen = models.ImageField(upload_to='Referencias/Imagenes',default='empty.jpg')
    pdf = models.FileField(upload_to= 'Referencias/PDF',default=None)
    linea_producion = models.ForeignKey(LineaProducionConfeccion, on_delete=models.CASCADE, null=True)
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="50">'.format(self.referencia_imagen.url))


    image_tag.short_description = 'Imagen_referencia'

    class Meta:

        db_table = 'referencias_sillas_perchas'
"""
class Usuario(models.Model):
    usuario_priv_tipo = models.ForeignKey('UsuarioPrivTipo', models.DO_NOTHING,default=None)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    login = models.CharField(max_length=60, unique=True)
    clave = models.CharField(max_length=30)
    tipo = models.CharField(max_length=210)

    class Meta:

        db_table = 'usuario'


class UsuarioPrivTipo(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255)
    visualizar = models.BooleanField(default=False)
    descargar = models.BooleanField(default=False)
    agregar_usuarios = models.BooleanField(default=False)
    eliminar_usuarios = models.BooleanField(default=False)
    modificar_fichas = models.BooleanField(default=False)

    class Meta:

        db_table = 'usuario_priv_tipo'

"""
from django.core.exceptions import ValidationError
def only_int(value): 
    if value.isdigit()==False:
        raise ValidationError('ID contains characters')


# User class
class CustomUser(AbstractUser):

    # Define the extra fields
    # related to User here


    # More User fields according to need

    # define the custom permissions
    # related to User.

    """User model."""
    
    username = models.CharField(
        "Número de cédula de ciudadanía",
        max_length = 10,
        unique = True,
        help_text = ("Requiere 8 dígitos."),
        # customize the above string as you want
        validators = [only_int],
        error_messages = {
            'unique': ("El usuario con este número de cédula ya existe."),
        },
    )
    first_name = models.CharField('Nombre',max_length=30)
    last_name = models.CharField('Apellidos',max_length=40)
    is_inspector = models.BooleanField("Es inspector",default=False)
    is_register = models.BooleanField("Es registrador de equipos",default=False)
    email = models.EmailField(unique=True)
    class Meta:
        permissions = (
            ("can_create_inspection_sheets", "The user is an inspector and can create inspection sheets"),
            ("can_view_admin", "User can see the link referenced to the admin page"),
            ("can_view_profile", "The user can view his profile"),
            ("can_create_hv", "The user can create equipment life sheets"),
            ("can_view_hv", "The user can view equipment life sheets"),
            ("can_view_inspection_sheets", "The user can view inspection sheets"),
            ("can_add_equipments", "The user can add equipments"),
            ("can_add_inspectors", "The user can add inspectors"),
            )

    def __str__(self):

        return self.username
# Por medio de Signals despues de guardar se envia un correo con los datos https://www.youtube.com/watch?v=7dBbbIqWdCk y 
# https://localcoder.org/sending-emails-when-a-user-is-activated-in-the-django-admin#solution_2 y sobre todo siguiendo 
# https://ordinarycoders.com/blog/article/html-password-reset-email-template para poder enviar correos personalizados
from django.db.models.signals import post_save
from django import template
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from pathlib import Path
from django.contrib.staticfiles import finders


class CiudadCodigo(models.Model):
    ciudad = models.CharField(max_length=50, unique=True)
    departamento = models.CharField(max_length=50)
    codigo = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.ciudad

    class Meta:
        db_table = 'ciudad_codigo'

# Add other custom permissions according to need.
from .certificado import Certificado, Carnet
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
class Inspectores(models.Model):
    global date, LINK
    now = datetime.datetime.now()
    only_date = now.date()
    date_now = only_date.strftime("%d/%m/%Y")
    date_now_default = only_date.strftime("%Y-%m-%d")
    phone = models.CharField(max_length=255, blank=True)
    empresa = models.CharField(max_length=255, blank=True)
    certificado_inspector = models.FileField(upload_to='protected/certificados/', default=None, blank=True)
    carnet_inspector = models.FileField(upload_to='protected/certificados/', default=None, blank=True)
    foto_inspector = models.ImageField(upload_to='fotos_inspectores', default='default.jpg', blank=True)
    ciudad = models.ForeignKey(
        CiudadCodigo,
        on_delete=models.CASCADE,
        blank=True
    )
    lugar = models.CharField (max_length=255, default='Salón de Capacitación de EPI S.A.S', blank=True)
    fecha = models.DateField(verbose_name='Fecha del curso',default=date_now_default, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo_inspector = models.CharField(max_length=255, unique=True, blank=True)
    #Metodo de compresión de imagenes https://stackoverflow.com/questions/33077804/losslessly-compressing-images-on-django/33989023, la foto de perfil 
    #es guardada en la DB comprimida, una imagen que pesa 129kb pasa a pesar 14kb
    def save(self, *args, **kwargs):
        if self.user.is_inspector:
        # call the compress function
            
            new_image = compress(self.foto_inspector)
            # set self.image to new_image
            self.foto_inspector = new_image
            
            subject = "CERTIFICACIÓN CURSO DE INSPECCIÓN EPI Y HABILITACIÓN DE LA PLATAFORMA EPI"
            plaintext = template.loader.get_template('admin/password_reset_email.txt')
            htmltemp = template.loader.get_template('admin/account_creation_subject.html')
            image_path = 'media/iconos_imagenes/image002.jpg'
            self.codigo_inspector=str(self.ciudad.codigo)+'-'+str(self.user.username)+'-'+self.fecha.strftime('%m%y')
            c = { 
            "email":self.user.email,
            'domain':'164.92.73.232',
            'site_name': 'Inspecciones EPI',
            "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
            "user": self.user,
            'token': default_token_generator.make_token(self.user),
            'full_name': str(self.user.first_name)+" "+str(self.user.last_name),
            'username':self.user.username,
            'codigo':self.user.inspectores.codigo_inspector,
            'protocol': 'http',
            }
            text_content = plaintext.render(c)
            html_content = htmltemp.render(c)
            
            msg = EmailMultiAlternatives(subject, text_content, 'EPI Inspecciones', [self.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = 'html'  # set the primary content to be text/html
            msg.mixed_subtype = 'related' # it is an important part that ensures embedding of an image
            #Para añadir la imagen de la firma 
            #https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images
            #https://www.workaround.cz/howto-send-html-email-embedded-image-django/
            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read())
                msg.attach(image)
                image.add_header('Content-ID', f"<image_name>")
            # save
            fname=f'Certificados-{self.user.first_name}-{self.user.last_name}.pdf'
            if os.path.exists(fname):
                os.remove(os.path.join(settings.MEDIA_ROOT, fname))
            object_pdf =Certificado()
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4,bottomup=1)
            pdf.setTitle("Certificados")
            pdf.setAuthor("EPI SAS")
            object_pdf.get_doc(
                        pdf, 
                        buffer,
                        self
                        )
            pdf = buffer.getvalue()
            self.certificado_inspector.save(fname, File(buffer), save=False)
            msg.attach(fname, pdf,'application/pdf')
            buffer.close()
            fname=f'Carnet-{self.user.first_name}-{self.user.last_name}.pdf'
            if os.path.exists(fname):
                os.remove(os.path.join(settings.MEDIA_ROOT, fname))
            object_pdf_carnet =Carnet()
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4,bottomup=1)
            pdf.setTitle("Carnets")
            pdf.setAuthor("EPI SAS")
            object_pdf_carnet.get_doc(
                        pdf, 
                        buffer,
                        self
                        )
            pdf = buffer.getvalue()
            self.carnet_inspector.save(fname, File(buffer), save=False)
            msg.attach(fname, pdf,'application/pdf')
            buffer.close()
            
            #Archivos comprimidos en email https://djangocentral.com/sending-email-with-zip-files-using-python/
            with open('media/Curso_Inspeccion_Info.zip','rb') as file:
            # Attach the file with filename to the email
                msg.attach(MIMEApplication(file.read(), Name='Curso_Inspeccion_Info.zip'))
            msg.send()
            super().save(*args, **kwargs)
    def image_tag(self):

        return format_html('<img src="{}" / width="100" height="100">'.format(self.foto_inspector.url))

    image_tag.short_description = 'fotos inspectores'


    class Meta:

        db_table = 'inspectores'

#https://stackoverflow.com/questions/16041232/django-delete-filefield
from django.dispatch import receiver
@receiver(models.signals.post_delete, sender=Inspectores)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.foto_inspector:
        if os.path.isfile(instance.foto_inspector.path):
            os.remove(instance.foto_inspector.path)
    
    if instance.certificado_inspector:
        if os.path.isfile(instance.certificado_inspector.path):
            os.remove(instance.certificado_inspector.path)

    if instance.carnet_inspector:
        if os.path.isfile(instance.carnet_inspector.path):
            os.remove(instance.carnet_inspector.path)

@receiver(models.signals.pre_save, sender=Inspectores)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).foto_inspector
    except sender.DoesNotExist:
        return False

    new_file = instance.foto_inspector
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    try:
        old_file = sender.objects.get(pk=instance.pk).certificado_inspector
    except sender.DoesNotExist:
        return False

    new_file = instance.certificado_inspector
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    try:
        old_file = sender.objects.get(pk=instance.pk).carnet_inspector
    except sender.DoesNotExist:
        return False

    new_file = instance.carnet_inspector
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


def compress(image):
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO() 
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=70) 
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image

