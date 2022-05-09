from matplotlib.pyplot import flag
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak,\
    PageTemplate, Spacer, FrameBreak, NextPageTemplate, SimpleDocTemplate, \
    Table, LongTable, TableStyle, Image
from reportlab.lib.units import inch, cm
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import letter,A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER,TA_LEFT,TA_RIGHT
from reportlab.platypus.flowables import Flowable, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont

class verticalText(Flowable):

    '''Rotates a text in a table cell.'''

    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text
        self.pages = []

    def draw(self):
        canvas = self.canv
        canvas.rotate(90)
        fs = canvas._fontsize
        canvas.translate(1, -fs/1.2)  # canvas._leading?
        canvas.drawString(0, 0, self.text)
        self.pages.append(dict(self.__dict__))

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        return canv._leading, 1 + canv.stringWidth(self.text, fn, fs)

class ReportSheet:  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)                
  
    def foot2(self,pdf,doc):
        width,height = A4
        pdf.saveState()
        pdf.setFont('Times-Roman',9)
        if self.flagShape=='0':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
        elif self.flagShape=='1':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
    
    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
            
    class RotatedImage(Image):

        def wrap(self,availWidth,availHeight):
            h, w = Image.wrap(self,availHeight,availWidth)
            return w, h
        def draw(self):
            self.canv.rotate(90)
            Image.draw(self)

    def get_doc(self, pdf, buffer, inspection_info, equip_info, flag, Activate_photo):
        self.flagShape=flag
        width,height = A4
        
        doc = BaseDocTemplate(buffer,showBoundary=1, pagesize= A4)
        contents =[]
        styleSheet = getSampleStyleSheet()
        Title = "Hello world"
        TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.5*inch,showBoundary=1,id='normal')
        frame1 = Frame(0.2*inch,0.2*inch,(width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col1')
        frame2 = Frame(0.4*inch+(width-0.6*inch)/2,0.2*inch, (width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col2' )
        leftlogoframe = Frame(0.2*inch,height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        rightlogoframe = Frame((width-1.2*inch),height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')
        frame2later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,showBoundary = 1,id='col2later' )

        frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')
        
        firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

        laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)
        
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        styleH_2 = styles['Normal']
        bodyStyle = ParagraphStyle('Body',fontSize=11)
        para1 = Paragraph('Spam spam spam spam. ' * 300, bodyStyle)
        contents.append(NextPageTemplate('laterpages'))
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        
        logoleft = Image(archivo_imagen)
        logoleft._restrictSize(0.7*inch, 0.7*inch)
        logoleft.hAlign = 'LEFT'
        logoleft.vAlign = 'CENTER'
        
        style_bold = styles['Heading1']
        style_bold.fontSize=11
        #styleH_bold.alignment=TA_CENTER
        style_bold.leading = 11
        style_bold.fontName = 'Helvetica-Bold'

        

        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))

        style_normal= styles["Normal"]
        style_normal.fontSize=14
        #styleH_bold.alignment=TA_CENTER
        style_normal.leading = 11
        style_normal.fontName = 'Helvetica-Bold'


        style_normal_body= styles["Normal"]
        style_normal_body.fontSize=8
        #styleH_bold.alignment=TA_CENTER
        style_normal_body.leading = 9
        style_normal_body.fontName = 'Helvetica'

        style_small= styles["Italic"]
        style_small.fontSize = 6
        #stylesmallnment=TA_CENTER
        style_small.leading = 8
        style_small.fontName = 'Helvetica'
       
        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))
        
    
        Aspectos_inspeccionar = (Paragraph("ASPECTOS A INSPECCIONAR",style_normal))
    
        datos_table_cintas = (
                (verticalText('CINTAS/REATAS'),'Tienen hoyos o agujeros'),
                ('', 'Están deshilachadas'),
                ('', 'Cortadas o Desgastadas'),
                ('', 'Tienen talladuras'),
                ('', 'Hay torsión'),
                ('', 'Presentan suciedad'),
                ('', (Paragraph("Quemaduras por soldadura,cigarrilo, etc.",style_normal_body))),
                ('', (Paragraph("Salpicadura de pintura y rigidez en la reata.",style_normal_body))),
                ('', 'Sustancias químicas'),
                ('', 'Otros'),    
            )

        table_cintas = Table(data = datos_table_cintas,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                             
                            ],
                    hAlign='LEFT',
                    )

        datos_table_costuras = (
                (verticalText('COSTURAS'),verticalText('Y'),verticalText('ETIQUETAS'),'Completas y Continuas'),
                ('','','', 'Son Visibles'),
                ('','','',(Paragraph('Indicador de impacto activado',style_normal_body)) ),
                ('','','', 'Otros'),    
            )

        table_costuras = Table(data = datos_table_costuras,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-4,-1)),   
                            ('SPAN',(1,0),(-3,-1)), 
                            ('SPAN',(2,0),(-2,-1)),                           
                            ],
                    hAlign='LEFT',
                    )
        datos_table_metalicas = (
                (verticalText('PARTES'),verticalText('METÁLICAS'),verticalText('Y'),verticalText('PLASTICAS'),'Completas'),
                ('','','','', 'Presentan corrosión y oxido'),
                ('','','','', 'Deformación'),
                ('','','','',(Paragraph('Fisuras, golpes, hundimientos.',style_normal_body)) ),
                ('','','','', 'Otros'),    
            )

        table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.15*inch,0.15*inch,0.15*inch,0.15*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (3, 0), 'Helvetica', 8, 8),
                            ('FONT', (-1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-5,-1)),   
                            ('SPAN',(1,0),(-4,-1)), 
                            ('SPAN',(2,0),(-3,-1)),  
                            ('SPAN',(3,0),(-2,-1)),                         
                            ],
                    hAlign='LEFT',
                    )
        

        datos_table_aspectos = (
                ("EQUIPO",'PARTES',Aspectos_inspeccionar),
                (verticalText('ARNES'), table_cintas,''),
                (" ", table_costuras,''),
                (" ", table_metalicas,''),
                ('','VEREDICTO:',''),
                ('','Fecha de proxima inspección','')
            )

        table_aspectos = Table(data = datos_table_aspectos,colWidths=(
            0.5*inch,
            0.6*inch,1.58*inch
            ), 
            rowHeights=(
                0.39*inch, 
                3*inch, 
                1.2*inch, 
                1.5*inch,
                0.33*inch,
                0.17*inch)
                ,
            style = [
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    #('BOX',(0,0),(-1,-1),2,colors.black), 
                    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                    ('SPAN',(1,1),(2,1)),
                    ('SPAN',(0,1),(0,-1)),
                    ('SPAN',(-2,-1),(-1,-1)),
                    ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                    ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                    ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                    ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                    ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                    ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                    ('LEFTPADDING',(1,1),(-2,-1), 0),
                    ('RIGHTPADDING',(1,1),(-2,-1), 0),
                    ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                    ('TOPPADDING',(1,1),(-2,-1), 0),  
                    ('TOPPADDING',(0,0),(0,0), 0), 
                    ('SPAN',(-2,-2),(-1,-2)),
                    # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                    # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                    ],
                    )

        if flag=='1':
            
            contents.append(logoleft)
            contents.append(FrameBreak())
            datos_table_cintas = (
                    (verticalText('CINTAS/REATAS'),'Tienen hoyos o agujeros'),
                    ('', 'Están deshilachadas'),
                    ('', 'Cortadas o Desgastadas'),
                    ('', 'Tienen talladuras'),
                    ('', 'Hay torsión'),
                    ('', 'Presentan suciedad'),
                    ('', (Paragraph("Quemaduras por soldadura,cigarrilo, etc.",style_normal_body))),
                    ('', (Paragraph("Salpicadura de pintura y rigidez en la reata.",style_normal_body))),
                    ('', 'Sustancias químicas'),
                    ('', 'Otros'),    
                )

            table_cintas = Table(data = datos_table_cintas,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.39*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                             
                                ],
                        hAlign='LEFT',
                        )

            datos_table_costuras = (
                    (verticalText('COSTURAS'),verticalText('Y'),verticalText('ETIQUETAS'),'Completas y Continuas'),
                    ('','','', 'Son Visibles'),
                    ('','','',(Paragraph('Indicador de impacto activado',style_normal_body)) ),
                    ('','','', 'Otros'),    
                )

            table_costuras = Table(data = datos_table_costuras,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.39*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-4,-1)),   
                                ('SPAN',(1,0),(-3,-1)), 
                                ('SPAN',(2,0),(-2,-1)),                           
                                ],
                        hAlign='LEFT',
                        )
            datos_table_metalicas = (
                    (verticalText('PARTES'),verticalText('METÁLICAS'),verticalText('Y'),verticalText('PLASTICAS'),'Completas'),
                    ('','','','', 'Presentan corrosión y oxido'),
                    ('','','','', 'Deformación'),
                    ('','','','',(Paragraph('Fisuras, golpes, hundimientos.',style_normal_body)) ),
                    ('','','','', 'Otros'),    
                )

            table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.15*inch,0.15*inch,0.15*inch,0.15*inch,1.58*inch),rowHeights=(0.39*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (3, 0), 'Helvetica', 8, 8),
                                ('FONT', (-1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-5,-1)),   
                                ('SPAN',(1,0),(-4,-1)), 
                                ('SPAN',(2,0),(-3,-1)),  
                                ('SPAN',(3,0),(-2,-1)),                         
                                ],
                        hAlign='LEFT',
                        )
            

            datos_table_aspectos = (
                    ("EQUIPO",'PARTES',Aspectos_inspeccionar),
                    (verticalText('ARNES'), table_cintas,''),
                    (" ", table_costuras,''),
                    (" ", table_metalicas,''),
                    ('','VEREDICTO:',''),
                    ('','Fecha de proxima inspección','')
                )

            table_aspectos = Table(data = datos_table_aspectos,colWidths=(
                0.5*inch,
                0.6*inch,1.58*inch
                ), 
                rowHeights=(
                0.39*inch, 
                3.9*inch, 
                1.56*inch, 
                1.95*inch,
                0.33*inch,
                0.17*inch)
                ,
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(1,1),(2,1)),
                        ('SPAN',(0,1),(0,-1)),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                        ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                        ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                        ('LEFTPADDING',(1,1),(-2,-1), 0),
                        ('RIGHTPADDING',(1,1),(-2,-1), 0),
                        ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                        ('TOPPADDING',(1,1),(-2,-1), 0),  
                        ('TOPPADDING',(0,0),(0,0), 0), 
                        ('SPAN',(-2,-2),(-1,-2)),
                        # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                        ],
                        )
            inspection = inspection_info[0]
            
            qr_path = inspection['codigo_qr_pdf']
            
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            
        
            merged_all = inspection.copy()
            
            keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','reata_foto', 'metalicas_foto', 'costuras_foto']
            if Activate_photo:
                keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','reata_foto', 'metalicas_foto', 'costuras_foto', 'foto_inspector']
                imagen_avatar =  Image(settings.MEDIA_ROOT+inspection['foto_inspector'],width=60, height=80)
            for key in keys_to_remove:

                merged_all.pop(key)
           
            
            imagen_reata = Image(settings.MEDIA_ROOT+inspection['reata_foto'],width=170, height=150)
            #imagen_reata._restrictSize(0.7*inch, 0.7*inch)
            imagen_costuras = Image(settings.MEDIA_ROOT+inspection['costuras_foto'], width=170, height=150)
            imagen_metalicas = Image(settings.MEDIA_ROOT+inspection['metalicas_foto'], width=170, height=150)

            datos_table_boolean = [
                ('SI','NO')
                ]
            
            datos_table_observaciones = [
                ('Observaciones','')
                ]

            index_difference = 0 
            for  key in merged_all:
                
                value = merged_all[key]
                if index_difference >18:

                    datos_table_observaciones.append((Paragraph(value,style_small),''))
                
                else:

                    if value:

                        datos_table_boolean.append(('X',''))
                    
                    else: 
                        
                        datos_table_boolean.append(('','X'))
                    
                    index_difference += 1

            datos_table_observaciones.append(('',''))

            if inspection['veredicto']:

                datos_veredicto_fecha = (
                    ('X', Paragraph("Apto y puede continuar",style_small)),
                    ('', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    # inspection_info['proxima_inspeccion']
                    )
            else:

                datos_veredicto_fecha = (
                    ('', Paragraph("Apto y puede continuar",style_small)),
                    ('X', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    )
            #print("VEREDICTO",inspection[count]['veredicto'] )


            table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                            
                                ],
                        hAlign='LEFT'
                        )
            datos_table_boolean.append((table_veredicto_fecha, ''))

            table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch,
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch,
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            
            imagenes = [
            
                ['Reatas/cintas',''],
                [imagen_reata,''],
                ['',''],
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Costuras/etiquetas', ''),
                (imagen_costuras, ''),
                ('', ''), 
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Metalicas/plasticas', ''),
                (imagen_metalicas, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ]
           
            table_imagenes = Table(data = imagenes,colWidths=(2.4*inch), rowHeights=(
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch,
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch,
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(0,1),(1,1)),
                        ('SPAN',(0,1),(1,6)),
                        ('SPAN',(0,7),(1,7)),
                        ('SPAN',(0,8),(1,13)),
                        ('SPAN',(0,14),(1,14)),
                        ('SPAN',(0,15),(1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            style_observacion = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('SPAN',(0,0),(1, 0)),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),                     
                        ]

            for i in range(1,20):
                style_observacion.append(('SPAN',(0, i),(1, i)))
            
            table_observaciones = Table(data = datos_table_observaciones,colWidths=(1.6*inch), 
                style = style_observacion ,
                rowHeights=(
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch,
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch,
                0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.39*inch, 0.5*inch),
                hAlign='LEFT'
                )
            
            if Activate_photo=='True':
                
                datos_header = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'], ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'],''),
                    )
                tabla_head = LongTable(data = datos_header,colWidths=(2.68*inch,1.6*inch,1.*inch),
                    style = [
                            ('GRID',(0,0),(2,4),0.5,colors.grey),
                            
                            ('SPAN',(1,0),(2,0)),
                            ('SPAN',(1,1),(2,1)),
                            ('SPAN',(1,2),(2,2)),
                            ('SPAN',(1,3),(2,3)),
                            ('SPAN',(1,4),(2,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (2, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                datos_table_2 = (
                    (tabla_head,'','',imagen_avatar),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.*inch,1.6*inch),
                    style = [
                            
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            ('ALIGN', (1,0),(3,0), "RIGHT"), 
                            ('VALIGN', (1,0),(3,0), "MIDDLE"),
                            ('LEFTPADDING',(0,0),(0,0), 0),
                            ('RIGHTPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('TOPPADDING',(0,0),(0,0), 0),                     

                            ('TOPPADDING',(-5, -1),(-5,-1), 0),
                            
                            ('LEFTPADDING',(-4,-1),(-4,-1), 0),
                            ('RIGHTPADDING',(-4,-1),(-4,-1), 0),
                            ('BOTTOMPADDING',(-4,-1),(-4,-1), 0),
                            ('TOPPADDING',(-4,-1),(-4,-1), 0),

                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2, -1),(-2, -1), 0),
                            ('RIGHTPADDING',(-2, -1),(-2, -1), 0),
                            ('BOTTOMPADDING',(-2, -1),(-2, -1), 0),
                            ('TOPPADDING',(-2, -1),(-2, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            elif Activate_photo=='False':
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                    style = [
                            ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                            ('SPAN',(1,0),(3,0)),
                            ('SPAN',(1,1),(3,1)),
                            ('SPAN',(1,2),(3,2)),
                            ('SPAN',(1,3),(3,3)),
                            ('SPAN',(1,4),(3,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            

                            ('LEFTPADDING',(0,5),(0,5), 0),
                            ('RIGHTPADDING',(0,5),(0,5), 0),
                            ('BOTTOMPADDING',(0,5),(0,5), 0),
                            ('TOPPADDING',(0,5),(0,5), 0),
                            ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                            ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                            
                            ('TOPPADDING',(-4, -1),(-4,-1), 0),
                            
                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                            ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                            ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                            ('TOPPADDING',(-2,-1),(-2,-1), 0),

                            ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                            ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                            ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                            ('TOPPADDING',(-1, -1),(-1, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            contents.append(tabla)
            datos_tabla_comentarios = [
                    [Paragraph('Comentarios Adicionales:', ParagraphStyle('Heading',fontSize=12))],
                    [Paragraph(inspection['comentarios_adicionales'], bodyStyle)]
                ] 
           
            table_comentarios = Table(data = datos_tabla_comentarios)
            qr_code_data = [
                    [qr_code_image, table_comentarios],
                    
                    #["Escanee el código QR"],
                    ]

            table_qr = Table(data = qr_code_data,colWidths=(1.6*inch, 5.98*inch),
                    style = [
                            ('GRID',(0,0),(1,1),0.5,colors.grey),
                            ('TOPPADDING',(0, 0),(1, 0), 4),
                            ('VALIGN', (0, 0), (1, 0), "TOP"),                     
                            ],
                    hAlign='LEFT'
                    ,repeatRows=1
                    )

            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_aspectos, table_imagenes, ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        

                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            
            contents.append(tabla)
            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_qr, '', ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            contents.append(tabla)
            #contents.append(table_qr)

            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())


            doc.addPageTemplates([firstpage, laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)
            
            
        elif flag=='0':
            
            qr_path = equip_info[0]['codigo_qr']
        
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            inspection_info = list(self.chunks(inspection_info, 3))
            #print("Esta es", inspection_info)
            
            #print(inspection_info)
            index = 0 
            
            
            
                
            while (True):
                if index > (len(inspection_info)-1):
                    break
                contents.append(logoleft)
                contents.append(FrameBreak())
                group_inspections = []
                
                inspection = inspection_info[index]
                
                count = 0 
                fecha_inspecciones = ["FECHA INSPECCIÓN: "]
                responsables = ["RESPONSABLE DE LA INSPECCIÓN: "]
                
                while (True):
                    
                    
                    if ((count > 2) or (count > len(inspection)-1)):

                        break
                    
                    merged_all = inspection[count].copy()
                    
                    
                    keys_to_remove = ["fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto']

                    for key in keys_to_remove:

                        merged_all.pop(key)

                    
                    datos_table_boolean = [
                        ('SI','NO')
                        ]
                    
                    for  key in merged_all:
                        
                        value = merged_all[key]
                        
                        if value:

                            datos_table_boolean.append(('X',''))
                        
                        else: 
                            
                            datos_table_boolean.append(('','X'))
                    
                    if inspection[count]['veredicto']:

                        datos_veredicto_fecha = (
                            ('X', Paragraph("Apto y puede continuar",style_small)),
                            ('', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            # inspection_info['proxima_inspeccion']
                            )
                    else:

                        datos_veredicto_fecha = (
                            ('', Paragraph("Apto y puede continuar",style_small)),
                            ('X', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            )
                    #print("VEREDICTO",inspection[count]['veredicto'] )


                    table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                        
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                        
                                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        ('SPAN',(-2,-1),(-1,-1)),
                                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        # ('LEFTPADDING',(0,0),(-1,-1), 0),
                                        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                        # ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                        # ('TOPPADDING',(0,0),(-1,-1), 0),
                                                                
                                        ],
                                hAlign='LEFT'
                                )
                    datos_table_boolean.append((table_veredicto_fecha, ''))

                    table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                        0.39*inch, 0.30*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                        0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                        0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('LEFTPADDING',(0,0),(-1,-1), 0),
                                ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                ('TOPPADDING',(0,0),(-1,-1), 0),
                                # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                                # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                                ],
                        hAlign='LEFT'
                        )

                    group_inspections.append(table_datos_boolean)

                    fecha_inspecciones.append(inspection[count]['fecha_inspeccion'])

                    responsables.append(
                        inspection[count]['first_name']+
                        " "+
                        inspection[count]['last_name'])
                    count += 1
                
                if not (len(group_inspections)%3 ==0):
                
                        while(True):
                            group_inspections.append('')
                            if (len(group_inspections)% 3 ==0):
                                break
                    
                    
                print("FINAAAAL", equip_info[0])
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    fecha_inspecciones,
                    responsables,
                    (table_aspectos, group_inspections[0], group_inspections[1], group_inspections[2]),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = Table(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
            
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                hAlign='LEFT'
                        )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
                
                #setFont('Helvetica', 10)
            
                #contents.append(tabla)
                
                contents.append(tabla)
                qr_code_data = [
                    [qr_code_image],
                    #["Escanee el código QR"],
                    ]

                table_qr = Table(data = qr_code_data,
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                
                                                       
                                ],
                        hAlign='LEFT'
                        )
                contents.append(table_qr)
                index += 1
                

            
            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())

            doc.addPageTemplates([firstpage,laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)


class ReportSheet_eslingas:  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)                
  
    def foot2(self,pdf,doc):
        width,height = A4
        pdf.saveState()
        pdf.setFont('Times-Roman',9)
        if self.flagShape=='0':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
        elif self.flagShape=='1':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
    
    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    class RotatedImage(Image):

        def wrap(self,availWidth,availHeight):
            h, w = Image.wrap(self,availHeight,availWidth)
            return w, h
        def draw(self):
            self.canv.rotate(90)
            Image.draw(self)

    def get_doc(self, pdf, buffer, inspection_info, equip_info, flag, Activate_photo):
        self.flagShape=flag
        width,height = A4
        
        doc = BaseDocTemplate(buffer,showBoundary=1, pagesize= A4)
        contents =[]
        styleSheet = getSampleStyleSheet()
        Title = "Hello world"
        TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.5*inch,showBoundary=1,id='normal')
        frame1 = Frame(0.2*inch,0.2*inch,(width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col1')
        frame2 = Frame(0.4*inch+(width-0.6*inch)/2,0.2*inch, (width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col2' )
        leftlogoframe = Frame(0.2*inch,height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        rightlogoframe = Frame((width-1.2*inch),height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')
        frame2later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,showBoundary = 1,id='col2later' )

        frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')
        
        firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

        laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)
        
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        styleH_2 = styles['Normal']
        bodyStyle = ParagraphStyle('Body',fontSize=11)
        para1 = Paragraph('Spam spam spam spam. ' * 300, bodyStyle)
        contents.append(NextPageTemplate('firstpage'))
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        
        logoleft = Image(archivo_imagen)
        logoleft._restrictSize(0.7*inch, 0.7*inch)
        logoleft.hAlign = 'LEFT'
        logoleft.vAlign = 'CENTER'
        
        style_bold = styles['Heading1']
        style_bold.fontSize=11
        #styleH_bold.alignment=TA_CENTER
        style_bold.leading = 11
        style_bold.fontName = 'Helvetica-Bold'

        

        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))

        style_normal= styles["Normal"]
        style_normal.fontSize=14
        #styleH_bold.alignment=TA_CENTER
        style_normal.leading = 11
        style_normal.fontName = 'Helvetica-Bold'


        style_normal_body= styles["Normal"]
        style_normal_body.fontSize=8
        #styleH_bold.alignment=TA_CENTER
        style_normal_body.leading = 9
        style_normal_body.fontName = 'Helvetica'

        style_small= styles["Italic"]
        style_small.fontSize = 6
        #stylesmallnment=TA_CENTER
        style_small.leading = 8
        style_small.fontName = 'Helvetica'
       
        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))
        
    
        Aspectos_inspeccionar = (Paragraph("ASPECTOS A INSPECCIONAR",style_normal))
    
        datos_table_absorbedor = (
                (verticalText('ABSORBEDOR'),'Presenta hoyos o desgarres'),
                ('', (Paragraph('Costuras sueltas o reventadas',style_normal_body))),
                ('', 'Deterioro'),
                ('', 'Presentan suciedad'),
                ('', (Paragraph('Quemaduras por soldadura o cigarrillo',style_normal_body))),
                ('', (Paragraph('Salpicadura de pintura y rigidez en cintas',style_normal_body))),
                ('', 'Otros'),    
            )

        table_absorbedor = Table(data = datos_table_absorbedor,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                             
                            ],
                    hAlign='LEFT',
                    )

        datos_table_cintas = (
                (verticalText('CINTAS/REATAS'),'Están deshilachadas'),
                ('', 'Desgastadas'),
                ('', 'Tienen talladuras'),
                ('', (Paragraph('Salpicadura de pintura rigidez en la reata',style_normal_body)) ),
                ('', 'Hay torsión'),
                ('', 'Otros'),    
            )

        table_cintas = Table(data = datos_table_cintas,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                           
                            ],
                    hAlign='LEFT',
                    )
        datos_table_metalicas = (
                (verticalText('PARTES'),verticalText('METÁLICAS'),'Completas'),
                ('','', 'Presentan corrosión y oxido'),
                ('','', (Paragraph('Las compuertas de ganchos abren y cierran correctamente',style_normal_body))),
                ('','', (Paragraph('Deformación, fisuras, golpes, hundimientos',style_normal_body))),
                ('','', 'Otros'),    
            )

        table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-3,-1)),   
                            ('SPAN',(1,0),(-2,-1)),                            
                            ],
                    hAlign='LEFT',
                    )
        
        datos_table_costuras = (
                (verticalText('COSTURAS'),verticalText('Y'),verticalText('ETIQUETAS'),'Completas y Continuas'),
                ('','','', 'Son Visibles'),
                ('','','', 'Otros'),    
            )

        table_costuras = Table(data = datos_table_costuras,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-4,-1)),   
                            ('SPAN',(1,0),(-3,-1)), 
                            ('SPAN',(2,0),(-2,-1)),                           
                            ],
                    hAlign='LEFT',
                    )

        datos_table_aspectos = (
                ('EQUIPO','PARTES',Aspectos_inspeccionar),
                (verticalText('ESLINGAS PARA DETENCIÓN DE CAÍDA, RESTRICCIÓN Y POSICIONAMIENTO'),table_absorbedor,''),
                (" ", table_cintas,''),
                (" ", table_metalicas,''),
                (" ", table_costuras,''),
                ('','VEREDICTO:',''),
                ('','Fecha de proxima inspección','')
            )

        table_aspectos = Table(data = datos_table_aspectos,colWidths=(
            0.5*inch,
            0.6*inch,1.58*inch
            ), 
            rowHeights=(
                0.39*inch, 
                2.1*inch, 
                1.8*inch,
                1.5*inch, 
                0.9*inch,
                0.33*inch,
                0.17*inch)
                ,
            style = [
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    #('BOX',(0,0),(-1,-1),2,colors.black), 
                    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                    ('SPAN',(1,1),(2,1)),
                    ('SPAN',(0,1),(0,-1)),
                    ('SPAN',(-2,-1),(-1,-1)),
                    ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                    ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                    ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                    ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                    ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                    ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                    ('LEFTPADDING',(1,1),(-2,-1), 0),
                    ('RIGHTPADDING',(1,1),(-2,-1), 0),
                    ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                    ('TOPPADDING',(1,1),(-2,-1), 0),  
                    ('TOPPADDING',(0,0),(0,0), 0), 
                    ('SPAN',(-2,-2),(-1,-2)),
                    # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                    # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                    ]
                    )

        if flag=='1':
            
            contents.append(logoleft)
            contents.append(FrameBreak())
            datos_table_absorbedor = (
                    (verticalText('ABSORBEDOR'),'Presenta hoyos o desgarres'),
                    ('', (Paragraph('Costuras sueltas o reventadas',style_normal_body))),
                    ('', 'Deterioro'),
                    ('', 'Presentan suciedad'),
                    ('', (Paragraph('Quemaduras por soldadura o cigarrillo',style_normal_body))),
                    ('', (Paragraph('Salpicadura de pintura y rigidez en cintas',style_normal_body))),
                    ('', 'Otros'),    
                )

            table_absorbedor = Table(data = datos_table_absorbedor,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.35*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                             
                                ],
                        hAlign='LEFT',
                        )

            datos_table_cintas = (
                    (verticalText('CINTAS/REATAS'),'Están deshilachadas'),
                    ('', 'Desgastadas'),
                    ('', 'Tienen talladuras'),
                    ('', (Paragraph('Salpicadura de pintura rigidez en la reata',style_normal_body)) ),
                    ('', 'Hay torsión'),
                    ('', 'Otros'),    
                )

            table_cintas = Table(data = datos_table_cintas,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.35*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                           
                                ],
                        hAlign='LEFT',
                        )
            datos_table_metalicas = (
                    (verticalText('PARTES'),verticalText('METÁLICAS'),'Completas'),
                    ('','', 'Presentan corrosión y oxido'),
                    ('','', (Paragraph('Las compuertas de ganchos abren y cierran correctamente',style_normal_body))),
                    ('','', (Paragraph('Deformación, fisuras, golpes, hundimientos',style_normal_body))),
                    ('','', 'Otros'),    
                )

            table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.35*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-3,-1)),   
                                ('SPAN',(1,0),(-2,-1)),                            
                                ],
                        hAlign='LEFT',
                        )
            
            datos_table_costuras = (
                    (verticalText('COSTURAS'),verticalText('Y'),verticalText('ETIQUETAS'),'Completas y Continuas'),
                    ('','','', 'Son Visibles'),
                    ('','','', 'Otros'),    
                )

            table_costuras = Table(data = datos_table_costuras,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.35*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-4,-1)),   
                                ('SPAN',(1,0),(-3,-1)), 
                                ('SPAN',(2,0),(-2,-1)),                           
                                ],
                        hAlign='LEFT',
                        )

            datos_table_aspectos = (
                    ('EQUIPO','PARTES',Aspectos_inspeccionar),
                    (verticalText('ESLINGAS PARA DETENCIÓN DE CAÍDA, RESTRICCIÓN Y POSICIONAMIENTO'),table_absorbedor,''),
                    (" ", table_cintas,''),
                    (" ", table_metalicas,''),
                    (" ", table_costuras,''),
                    ('','VEREDICTO:',''),
                    ('','Fecha de proxima inspección','')
                )


            table_aspectos = Table(data = datos_table_aspectos,colWidths=(
                0.5*inch,
                0.6*inch,1.58*inch
                ), 
                
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(1,1),(2,1)),
                        ('SPAN',(0,1),(0,-1)),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                        ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                        ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                        ('LEFTPADDING',(1,1),(-2,-1), 0),
                        ('RIGHTPADDING',(1,1),(-2,-1), 0),
                        ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                        ('TOPPADDING',(1,1),(-2,-1), 0),  
                        ('TOPPADDING',(0,0),(0,0), 0), 
                        ('SPAN',(-2,-2),(-1,-2)),
                        # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                        ],
                        )
            
            inspection = inspection_info[0]
            
            qr_path = inspection['codigo_qr_pdf']
            
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            
        
            merged_all = inspection.copy()
            
            
            keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto', 'absorbedor_foto', 'reata_foto', 'metalicas_foto', 'costuras_foto']
            if Activate_photo:
                keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','absorbedor_foto', 'reata_foto', 'metalicas_foto', 'costuras_foto', 'foto_inspector']
                imagen_avatar =  Image(settings.MEDIA_ROOT+inspection['foto_inspector'],width=60, height=80)
            for key in keys_to_remove:
                merged_all.pop(key)
           
            
            imagen_absorbedor = Image(settings.MEDIA_ROOT+inspection['absorbedor_foto'],width=170, height=120)
            #imagen_reata._restrictSize(0.7*inch, 0.7*inch)
            imagen_reata = Image(settings.MEDIA_ROOT+inspection['reata_foto'], width=170, height=120)
            imagen_metalicas = Image(settings.MEDIA_ROOT+inspection['metalicas_foto'], width=170, height=120)
            imagen_costuras = Image(settings.MEDIA_ROOT+inspection['costuras_foto'], width=170, height=120)

            datos_table_boolean = [
                ('SI','NO')
                ]
            
            datos_table_observaciones = [
                ('Observaciones','')
                ]

            index_difference = 0 
            for  key in merged_all:
                
                value = merged_all[key]
                if index_difference >20:

                    datos_table_observaciones.append((Paragraph(value,style_small),''))
                
                else:

                    if value:

                        datos_table_boolean.append(('X',''))
                    
                    else: 
                        
                        datos_table_boolean.append(('','X'))
                    
                    index_difference += 1

            datos_table_observaciones.append(('',''))

            if inspection['veredicto']:

                datos_veredicto_fecha = (
                    ('X', Paragraph("Apto y puede continuar",style_small)),
                    ('', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    # inspection_info['proxima_inspeccion']
                    )
            else:

                datos_veredicto_fecha = (
                    ('', Paragraph("Apto y puede continuar",style_small)),
                    ('X', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    )
            #print("VEREDICTO",inspection[count]['veredicto'] )


            table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                            
                                ],
                        hAlign='LEFT'
                        )
            datos_table_boolean.append((table_veredicto_fecha, ''))

            table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                0.39*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
                0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
                0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
                0.35*inch, 0.35*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            
            imagenes = [
            
                ('Absorbedor',''),
                (imagen_absorbedor,''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Cinta/reata', ''),
                (imagen_reata, ''),
                ('', ''), 
                ('', ''),
                ('', ''),
                ('', ''),
                ('Metalicas', ''),
                (imagen_metalicas, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Costuras/etiquetas', ''),
                (imagen_costuras, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ]
           
            table_imagenes = Table(data = imagenes,colWidths=(2.4*inch), rowHeights=(
                0.39*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
                0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
                0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 
                0.35*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(0,1),(1,1)),
                        ('SPAN',(0,1),(1,5)),
                        ('SPAN',(0,6),(1,6)),
                        ('SPAN',(0,7),(1,11)),
                        ('SPAN',(0,12),(1,12)),
                        ('SPAN',(0,13),(1,17)),
                        ('SPAN',(0,18),(1,18)),
                        ('SPAN',(0,19),(1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            style_observacion = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('SPAN',(0,0),(1, 0)),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),                     
                        ]

            for i in range(1,22):
                style_observacion.append(('SPAN',(0, i),(1, i)))
            
            table_observaciones = Table(data = datos_table_observaciones,colWidths=(1.6*inch), rowHeights=(
                0.39*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
                0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
                0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 
                0.35*inch, 0.5*inch),
                style = style_observacion ,
                hAlign='LEFT'
                )

            if Activate_photo=='True':
                
                datos_header = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'], ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'],''),
                    )
                tabla_head = LongTable(data = datos_header,colWidths=(2.68*inch,1.6*inch,1.*inch),
                    style = [
                            ('GRID',(0,0),(2,4),0.5,colors.grey),
                            
                            ('SPAN',(1,0),(2,0)),
                            ('SPAN',(1,1),(2,1)),
                            ('SPAN',(1,2),(2,2)),
                            ('SPAN',(1,3),(2,3)),
                            ('SPAN',(1,4),(2,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (2, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                datos_table_2 = (
                    (tabla_head,'','',imagen_avatar),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.*inch,1.6*inch),
                    style = [
                            
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            ('ALIGN', (1,0),(3,0), "RIGHT"), 
                            ('VALIGN', (1,0),(3,0), "MIDDLE"),
                            ('LEFTPADDING',(0,0),(0,0), 0),
                            ('RIGHTPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('TOPPADDING',(0,0),(0,0), 0),                     

                            ('TOPPADDING',(-5, -1),(-5,-1), 0),
                            
                            ('LEFTPADDING',(-4,-1),(-4,-1), 0),
                            ('RIGHTPADDING',(-4,-1),(-4,-1), 0),
                            ('BOTTOMPADDING',(-4,-1),(-4,-1), 0),
                            ('TOPPADDING',(-4,-1),(-4,-1), 0),

                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2, -1),(-2, -1), 0),
                            ('RIGHTPADDING',(-2, -1),(-2, -1), 0),
                            ('BOTTOMPADDING',(-2, -1),(-2, -1), 0),
                            ('TOPPADDING',(-2, -1),(-2, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            elif Activate_photo=='False':
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                    style = [
                            ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                            ('SPAN',(1,0),(3,0)),
                            ('SPAN',(1,1),(3,1)),
                            ('SPAN',(1,2),(3,2)),
                            ('SPAN',(1,3),(3,3)),
                            ('SPAN',(1,4),(3,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            

                            ('LEFTPADDING',(0,5),(0,5), 0),
                            ('RIGHTPADDING',(0,5),(0,5), 0),
                            ('BOTTOMPADDING',(0,5),(0,5), 0),
                            ('TOPPADDING',(0,5),(0,5), 0),
                            ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                            ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                            
                            ('TOPPADDING',(-4, -1),(-4,-1), 0),
                            
                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                            ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                            ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                            ('TOPPADDING',(-2,-1),(-2,-1), 0),

                            ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                            ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                            ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                            ('TOPPADDING',(-1, -1),(-1, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            contents.append(tabla)
            datos_tabla_comentarios = [
                    [Paragraph('Comentarios Adicionales:', ParagraphStyle('Heading',fontSize=12))],
                    [Paragraph(inspection['comentarios_adicionales'], bodyStyle)]
                ] 
           
            table_comentarios = Table(data = datos_tabla_comentarios)
            qr_code_data = [
                    [qr_code_image, table_comentarios],
                    
                    #["Escanee el código QR"],
                    ]

            table_qr = Table(data = qr_code_data,colWidths=(1.6*inch, 5.98*inch),
                    style = [
                            ('GRID',(0,0),(1,1),0.5,colors.grey),
                            ('TOPPADDING',(0, 0),(1, 0), 4),
                            ('VALIGN', (0, 0), (1, 0), "TOP"),                     
                            ],
                    hAlign='LEFT'
                    ,repeatRows=1
                    )

            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_aspectos, table_imagenes, ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        

                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            
            contents.append(tabla)
            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_qr, '', ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            contents.append(tabla)
            #contents.append(table_qr)

            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())


            doc.addPageTemplates([firstpage, laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)
            
        
        elif flag=='0':
            
            qr_path = equip_info[0]['codigo_qr']
        
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            inspection_info = list(self.chunks(inspection_info, 3))
            #print("Esta es", inspection_info)
            
            #print(inspection_info)
            index = 0 
            
            
            
                
            while (True):
                


                if index > (len(inspection_info)-1):
                    break
                contents.append(logoleft)
                contents.append(FrameBreak())
                group_inspections = []
                
                inspection = inspection_info[index]
                
                count = 0 
                fecha_inspecciones = ["FECHA INSPECCIÓN: "]
                responsables = ["RESPONSABLE DE LA INSPECCIÓN: "]
                
                while (True):
                    
                    
                    if ((count > 2) or (count > len(inspection)-1)):

                        break
                    
                    merged_all = inspection[count].copy()
                    
                    
                    keys_to_remove = ["fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto']

                    for key in keys_to_remove:

                        merged_all.pop(key)

                    
                    datos_table_boolean = [
                        ('SI','NO')
                        ]
                    
                    for  key in merged_all:
                        
                        value = merged_all[key]
                        
                        if value:

                            datos_table_boolean.append(('X',''))
                        
                        else: 
                            
                            datos_table_boolean.append(('','X'))
                    
                    if inspection[count]['veredicto']:

                        datos_veredicto_fecha = (
                            ('X', Paragraph("Apto y puede continuar",style_small)),
                            ('', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            # inspection_info['proxima_inspeccion']
                            )
                    else:

                        datos_veredicto_fecha = (
                            ('', Paragraph("Apto y puede continuar",style_small)),
                            ('X', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            )
                    #print("VEREDICTO",inspection[count]['veredicto'] )


                    table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                        
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                        
                                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        ('SPAN',(-2,-1),(-1,-1)),
                                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        # ('LEFTPADDING',(0,0),(-1,-1), 0),
                                        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                        # ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                        # ('TOPPADDING',(0,0),(-1,-1), 0),
                                                                
                                        ],
                                hAlign='LEFT'
                                )
                    datos_table_boolean.append((table_veredicto_fecha, ''))

                    table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                        0.39*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                        0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                        0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 
                        0.3*inch, 0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('LEFTPADDING',(0,0),(-1,-1), 0),
                                ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                ('TOPPADDING',(0,0),(-1,-1), 0),
                                # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                                # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                                ],
                        hAlign='LEFT'
                        )

                    group_inspections.append(table_datos_boolean)

                    fecha_inspecciones.append(inspection[count]['fecha_inspeccion'])

                    responsables.append(
                        inspection[count]['first_name']+
                        " "+
                        inspection[count]['last_name'])
                    count += 1
                
                if not (len(group_inspections)%3 ==0):
                
                        while(True):
                            group_inspections.append('')
                            if (len(group_inspections)% 3 ==0):
                                break
                    
                    
                print("FINAAAAL", equip_info[0])
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    fecha_inspecciones,
                    responsables,
                    (table_aspectos, group_inspections[0], group_inspections[1], group_inspections[2]),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = Table(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
            
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                hAlign='LEFT'
                        )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
                
                #setFont('Helvetica', 10)
            
                #contents.append(tabla)
                
                contents.append(tabla)
                qr_code_data = [
                    [qr_code_image],
                    #["Escanee el código QR"],
                    ]

                table_qr = Table(data = qr_code_data,
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                
                                                       
                                ],
                        hAlign='LEFT'
                        )
                contents.append(table_qr)
                index += 1
                

            
            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())
        
            doc.addPageTemplates([firstpage,laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)

class ReportSheet_lineas_anclajes:  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)                
  
    def foot2(self,pdf,doc):
        width,height = A4
        pdf.saveState()
        pdf.setFont('Times-Roman',9)
        if self.flagShape=='0':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
        elif self.flagShape=='1':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    class RotatedImage(Image):

        def wrap(self,availWidth,availHeight):
            h, w = Image.wrap(self,availHeight,availWidth)
            return w, h
        def draw(self):
            self.canv.rotate(90)
            Image.draw(self)

    def get_doc(self, pdf, buffer, inspection_info, equip_info, flag, Activate_photo):
        self.flagShape=flag
        width,height = A4
        
        doc = BaseDocTemplate(buffer,showBoundary=1, pagesize= A4)
        contents =[]
        styleSheet = getSampleStyleSheet()
        Title = "Hello world"
        TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.5*inch,showBoundary=1,id='normal')
        frame1 = Frame(0.2*inch,0.2*inch,(width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col1')
        frame2 = Frame(0.4*inch+(width-0.6*inch)/2,0.2*inch, (width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col2' )
        leftlogoframe = Frame(0.2*inch,height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        rightlogoframe = Frame((width-1.2*inch),height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')
        frame2later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,showBoundary = 1,id='col2later' )

        frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')
        
        firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

        laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)
        
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        styleH_2 = styles['Normal']
        bodyStyle = ParagraphStyle('Body',fontSize=11)
        para1 = Paragraph('Spam spam spam spam. ' * 300, bodyStyle)
        contents.append(NextPageTemplate('laterpages'))
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        
        logoleft = Image(archivo_imagen)
        logoleft._restrictSize(0.7*inch, 0.7*inch)
        logoleft.hAlign = 'LEFT'
        logoleft.vAlign = 'CENTER'
        
        style_bold = styles['Heading1']
        style_bold.fontSize=11
        #styleH_bold.alignment=TA_CENTER
        style_bold.leading = 11
        style_bold.fontName = 'Helvetica-Bold'

        

        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))

        style_normal= styles["Normal"]
        style_normal.fontSize=14
        #styleH_bold.alignment=TA_CENTER
        style_normal.leading = 11
        style_normal.fontName = 'Helvetica-Bold'


        style_normal_body= styles["Normal"]
        style_normal_body.fontSize=8
        #styleH_bold.alignment=TA_CENTER
        style_normal_body.leading = 9
        style_normal_body.fontName = 'Helvetica'

        style_small= styles["Italic"]
        style_small.fontSize = 6
        #stylesmallnment=TA_CENTER
        style_small.leading = 8
        style_small.fontName = 'Helvetica'
       
        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))
        
    
        Aspectos_inspeccionar = (Paragraph("ASPECTOS A INSPECCIONAR",style_normal))

        datos_table_metalicas = (
                (verticalText('PARTES'),verticalText('METALICAS'),'Completas'),
                ('','', 'Tiene fisuras'),
                ('','', 'Presenta corrosión y oxido'),
                ('','', 'Golpes, hundimientos'),
                ('','', (Paragraph('Las compuertas de ganchos abren y cierran correctamente',style_normal_body))),
                ('','', 'Otros'),    
            )

        table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-3,-1)),   
                            ('SPAN',(1,0),(-2,-1)),                        
                            ],
                    hAlign='LEFT',
                    )

        datos_table_cinta = (
                (verticalText('CINTA/'),verticalText('REATA/CUERDA'),'Están deshilachadas'),
                ('','', (Paragraph('Quemaduras por soldadura, cigarrillo, etc',style_normal_body))),
                ('','', 'Hay torsión o talladuras'),
                ('','', (Paragraph('Salpicadura de pintura y rigidez en cinta',style_normal_body))),
                ('','', 'Ruptura'),
                ('','', 'Otros'),    
            )

        table_cinta = Table(data = datos_table_cinta,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-3,-1)),   
                            ('SPAN',(1,0),(-2,-1)),                        
                            ],
                    hAlign='LEFT',
                    )

        datos_table_costura = (
                (verticalText('COSTURAS'),verticalText('Y'),verticalText('ETIQUETAS'),'Tiene deformaciones'),
                ('','','', 'Visibles'),
                ('','','', 'Otros'),  
            )

        table_costura = Table(data = datos_table_costura,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-4,-1)),   
                            ('SPAN',(1,0),(-3,-1)), 
                            ('SPAN',(2,0),(-2,-1)),                           
                            ],
                    hAlign='LEFT',
                    )
        
        

        datos_table_aspectos = (
                ('EQUIPO','PARTES',Aspectos_inspeccionar),
                (verticalText('LINEAS DE VIDA Y ANCLAJES'), table_metalicas,''),
                ('', table_cinta,''),
                ('', table_costura,''),
                ('','VEREDICTO:',''),
                ('','Fecha de proxima inspección','')
            )

        table_aspectos = Table(data = datos_table_aspectos,colWidths=(
            0.5*inch,
            0.6*inch,1.58*inch
            ), 
            rowHeights=(
                0.6*inch, 
                1.8*inch, 
                1.8*inch, 
                0.9*inch,
                0.33*inch,
                0.17*inch)
                ,
            style = [
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    #('BOX',(0,0),(-1,-1),2,colors.black), 
                    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                    ('SPAN',(1,1),(2,1)),
                    ('SPAN',(0,1),(0,-1)),
                    ('SPAN',(-2,-1),(-1,-1)),
                    ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                    ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                    ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                    ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                    ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                    ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                    ('LEFTPADDING',(1,1),(-2,-1), 0),
                    ('RIGHTPADDING',(1,1),(-2,-1), 0),
                    ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                    ('TOPPADDING',(1,1),(-2,-1), 0),  
                    ('TOPPADDING',(0,0),(0,0), 0), 
                    ('SPAN',(-2,-2),(-1,-2)),
                    # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                    # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                    ],
                    )
        
        if flag=='1':
            
            contents.append(logoleft)
            contents.append(FrameBreak())
            datos_table_metalicas = (
                    (verticalText('PARTES'),verticalText('METALICAS'),'Completas'),
                    ('','', 'Tiene fisuras'),
                    ('','', 'Presenta corrosión y oxido'),
                    ('','', 'Golpes, hundimientos'),
                    ('','', (Paragraph('Las compuertas de ganchos abren y cierran correctamente',style_normal_body))),
                    ('','', 'Otros'),    
                )

            table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.4*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-3,-1)),   
                                ('SPAN',(1,0),(-2,-1)),                        
                                ],
                        hAlign='LEFT',
                        )

            datos_table_cinta = (
                    (verticalText('CINTA/'),verticalText('REATA/CUERDA'),'Están deshilachadas'),
                    ('','', (Paragraph('Quemaduras por soldadura, cigarrillo, etc',style_normal_body))),
                    ('','', 'Hay torsión o talladuras'),
                    ('','', (Paragraph('Salpicadura de pintura y rigidez en cinta',style_normal_body))),
                    ('','', 'Ruptura'),
                    ('','', 'Otros'),    
                )

            table_cinta = Table(data = datos_table_cinta,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.4*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-3,-1)),   
                                ('SPAN',(1,0),(-2,-1)),                        
                                ],
                        hAlign='LEFT',
                        )

            datos_table_costura = (
                    (verticalText('COSTURAS'),verticalText('Y'),verticalText('ETIQUETAS'),'Tiene deformaciones'),
                    ('','','', 'Visibles'),
                    ('','','', 'Otros'),  
                )

            table_costura = Table(data = datos_table_costura,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.4*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-4,-1)),   
                                ('SPAN',(1,0),(-3,-1)), 
                                ('SPAN',(2,0),(-2,-1)),                           
                                ],
                        hAlign='LEFT',
                        )
            
            

            datos_table_aspectos = (
                    ('EQUIPO','PARTES',Aspectos_inspeccionar),
                    (verticalText('LINEAS DE VIDA Y ANCLAJES'), table_metalicas,''),
                    ('', table_cinta,''),
                    ('', table_costura,''),
                    ('','VEREDICTO:',''),
                    ('','Fecha de proxima inspección','')
                )

            table_aspectos = Table(data = datos_table_aspectos,colWidths=(
                0.5*inch,
                0.6*inch,1.58*inch
                ), 
                rowHeights=(
                0.6*inch, 
                2.4*inch, 
                2.4*inch, 
                1.2*inch,
                0.33*inch,
                0.17*inch)
                ,
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(1,1),(2,1)),
                        ('SPAN',(0,1),(0,-1)),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                        ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                        ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                        ('LEFTPADDING',(1,1),(-2,-1), 0),
                        ('RIGHTPADDING',(1,1),(-2,-1), 0),
                        ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                        ('TOPPADDING',(1,1),(-2,-1), 0),  
                        ('TOPPADDING',(0,0),(0,0), 0), 
                        ('SPAN',(-2,-2),(-1,-2)),
                        # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                        ],
                        )
            inspection = inspection_info[0]
            
            qr_path = inspection['codigo_qr_pdf']
            
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            
        
            merged_all = inspection.copy()
            
            
            keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','reata_foto', 'metalicas_foto', 'costuras_foto']
            if Activate_photo:
                keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','reata_foto', 'metalicas_foto', 'costuras_foto', 'foto_inspector']
                imagen_avatar =  Image(settings.MEDIA_ROOT+inspection['foto_inspector'],width=60, height=80)

            for key in keys_to_remove:

                merged_all.pop(key)

           
            
            imagen_metalicas = Image(settings.MEDIA_ROOT+inspection['metalicas_foto'],width=150, height=130)
            #imagen_reata._restrictSize(0.7*inch, 0.7*inch)
            imagen_reata = Image(settings.MEDIA_ROOT+inspection['reata_foto'],width=150, height=130)
            imagen_costura = Image(settings.MEDIA_ROOT+inspection['costuras_foto'],width=150, height=130)

            datos_table_boolean = [
                ('SI','NO')
                ]
            
            datos_table_observaciones = [
                ('Observaciones','')
                ]

            index_difference = 0 
            for  key in merged_all:
                
                value = merged_all[key]
                if index_difference >14:

                    datos_table_observaciones.append((Paragraph(value,style_small),''))
                
                else:

                    if value:

                        datos_table_boolean.append(('X',''))
                    
                    else: 
                        
                        datos_table_boolean.append(('','X'))
                    
                    index_difference += 1

            datos_table_observaciones.append(('',''))

            if inspection['veredicto']:

                datos_veredicto_fecha = (
                    ('X', Paragraph("Apto y puede continuar",style_small)),
                    ('', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    # inspection_info['proxima_inspeccion']
                    )
            else:

                datos_veredicto_fecha = (
                    ('', Paragraph("Apto y puede continuar",style_small)),
                    ('X', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    )
            #print("VEREDICTO",inspection[count]['veredicto'] )


            table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                            
                                ],
                        hAlign='LEFT'
                        )
            datos_table_boolean.append((table_veredicto_fecha, ''))

            table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                0.6*inch, 0.40*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch,
                0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 
                0.4*inch, 0.4*inch, 0.4*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            
            imagenes = [
            
                ['Metálicas',''],
                (imagen_metalicas,''),
                ('',''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Cinta/reata/cuerda', ''),
                (imagen_reata, ''),
                ('', ''), 
                ('', ''),
                ('', ''),
                ('', ''),
                ('Costura y etiquetas', ''),
                (imagen_costura, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ]
           
            table_imagenes = Table(data = imagenes,colWidths=(2.4*inch), rowHeights=(
                0.6*inch, 0.37*inch, 0.37*inch, 0.37*inch, 0.37*inch, 0.4*inch, 0.37*inch,
                0.37*inch, 0.37*inch, 0.37*inch, 0.4*inch, 0.37*inch, 0.37*inch, 0.37*inch,
                0.37*inch, 0.37*inch, 0.37*inch, 0.52*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(0,1),(1,1)),
                        ('SPAN',(0,1),(1,5)),
                        ('SPAN',(0,6),(1,6)),
                        ('SPAN',(0,7),(1,11)),
                        ('SPAN',(0,12),(1,12)),
                        ('SPAN',(0,13),(1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            style_observacion = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('SPAN',(0,0),(1, 0)),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),                     
                        ]

            for i in range(1,20):
                style_observacion.append(('SPAN',(0, i),(1, i)))
            
            table_observaciones = Table(data = datos_table_observaciones,colWidths=(1.6*inch), rowHeights=(
                0.6*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch,
                0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.4*inch, 
                0.4*inch, 0.4*inch, 0.5*inch),
                style = style_observacion ,
                hAlign='LEFT'
                )

            if Activate_photo=='True':
                
                datos_header = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'], ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'],''),
                    )
                tabla_head = LongTable(data = datos_header,colWidths=(2.68*inch,1.6*inch,1.*inch),
                    style = [
                            ('GRID',(0,0),(2,4),0.5,colors.grey),
                            
                            ('SPAN',(1,0),(2,0)),
                            ('SPAN',(1,1),(2,1)),
                            ('SPAN',(1,2),(2,2)),
                            ('SPAN',(1,3),(2,3)),
                            ('SPAN',(1,4),(2,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (2, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                datos_table_2 = (
                    (tabla_head,'','',imagen_avatar),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.*inch,1.6*inch),
                    style = [
                            
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            ('ALIGN', (1,0),(3,0), "RIGHT"), 
                            ('VALIGN', (1,0),(3,0), "MIDDLE"),
                            ('LEFTPADDING',(0,0),(0,0), 0),
                            ('RIGHTPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('TOPPADDING',(0,0),(0,0), 0),                     

                            ('TOPPADDING',(-5, -1),(-5,-1), 0),
                            
                            ('LEFTPADDING',(-4,-1),(-4,-1), 0),
                            ('RIGHTPADDING',(-4,-1),(-4,-1), 0),
                            ('BOTTOMPADDING',(-4,-1),(-4,-1), 0),
                            ('TOPPADDING',(-4,-1),(-4,-1), 0),

                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2, -1),(-2, -1), 0),
                            ('RIGHTPADDING',(-2, -1),(-2, -1), 0),
                            ('BOTTOMPADDING',(-2, -1),(-2, -1), 0),
                            ('TOPPADDING',(-2, -1),(-2, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            elif Activate_photo=='False':
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                    style = [
                            ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                            ('SPAN',(1,0),(3,0)),
                            ('SPAN',(1,1),(3,1)),
                            ('SPAN',(1,2),(3,2)),
                            ('SPAN',(1,3),(3,3)),
                            ('SPAN',(1,4),(3,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            

                            ('LEFTPADDING',(0,5),(0,5), 0),
                            ('RIGHTPADDING',(0,5),(0,5), 0),
                            ('BOTTOMPADDING',(0,5),(0,5), 0),
                            ('TOPPADDING',(0,5),(0,5), 0),
                            ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                            ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                            
                            ('TOPPADDING',(-4, -1),(-4,-1), 0),
                            
                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                            ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                            ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                            ('TOPPADDING',(-2,-1),(-2,-1), 0),

                            ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                            ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                            ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                            ('TOPPADDING',(-1, -1),(-1, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            contents.append(tabla)
            datos_tabla_comentarios = [
                    [Paragraph('Comentarios Adicionales:', ParagraphStyle('Heading',fontSize=12))],
                    [Paragraph(inspection['comentarios_adicionales'], bodyStyle)]
                ] 
           
            table_comentarios = Table(data = datos_tabla_comentarios)
            qr_code_data = [
                    [qr_code_image, table_comentarios],
                    
                    #["Escanee el código QR"],
                    ]

            table_qr = Table(data = qr_code_data,colWidths=(1.5*inch, 5.98*inch),
                    style = [
                            ('GRID',(0,0),(1,1),0.5,colors.grey),
                            ('TOPPADDING',(0, 0),(1, 0), 4),
                            ('VALIGN', (0, 0), (1, 0), "TOP"),                     
                            ],
                    hAlign='LEFT'
                    ,repeatRows=1
                    )

            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_aspectos, table_imagenes, ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        

                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            
            contents.append(tabla)
            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_qr, '', ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            contents.append(tabla)
            #contents.append(table_qr)

            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())


            doc.addPageTemplates([firstpage, laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)
        
        elif flag=='0':
            
            qr_path = equip_info[0]['codigo_qr']
        
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            inspection_info = list(self.chunks(inspection_info, 3))
            #print("Esta es", inspection_info)
            
            #print(inspection_info)
            index = 0 
            
            
            
                
            while (True):
                


                if index > (len(inspection_info)-1):
                    break
                contents.append(logoleft)
                contents.append(FrameBreak())
                group_inspections = []
                
                inspection = inspection_info[index]
                
                count = 0 
                fecha_inspecciones = ["FECHA INSPECCIÓN: "]
                responsables = ["RESPONSABLE DE LA INSPECCIÓN: "]
                
                while (True):
                    
                    
                    if ((count > 2) or (count > len(inspection)-1)):

                        break
                    
                    merged_all = inspection[count].copy()
                    
                    
                    keys_to_remove = ["fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto']

                    for key in keys_to_remove:

                        merged_all.pop(key)

                    
                    datos_table_boolean = [
                        ('SI','NO')
                        ]
                    
                    for  key in merged_all:
                        
                        value = merged_all[key]
                        
                        if value:

                            datos_table_boolean.append(('X',''))
                        
                        else: 
                            
                            datos_table_boolean.append(('','X'))
                    
                    if inspection[count]['veredicto']:

                        datos_veredicto_fecha = (
                            ('X', Paragraph("Apto y puede continuar",style_small)),
                            ('', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            # inspection_info['proxima_inspeccion']
                            )
                    else:

                        datos_veredicto_fecha = (
                            ('', Paragraph("Apto y puede continuar",style_small)),
                            ('X', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            )
                    #print("VEREDICTO",inspection[count]['veredicto'] )


                    table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                        
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                        
                                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        ('SPAN',(-2,-1),(-1,-1)),
                                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        # ('LEFTPADDING',(0,0),(-1,-1), 0),
                                        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                        # ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                        # ('TOPPADDING',(0,0),(-1,-1), 0),
                                                                
                                        ],
                                hAlign='LEFT'
                                )
                    datos_table_boolean.append((table_veredicto_fecha, ''))
                    Altura=0.3
                    table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                        0.6*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch,
                        Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch,
                        Altura*inch, Altura*inch, 0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('LEFTPADDING',(0,0),(-1,-1), 0),
                                ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                ('TOPPADDING',(0,0),(-1,-1), 0),
                                # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                                # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                                ],
                        hAlign='LEFT'
                        )

                    group_inspections.append(table_datos_boolean)

                    fecha_inspecciones.append(inspection[count]['fecha_inspeccion'])

                    responsables.append(
                        inspection[count]['first_name']+
                        " "+
                        inspection[count]['last_name'])
                    count += 1
                
                if not (len(group_inspections)%3 ==0):
                
                        while(True):
                            group_inspections.append('')
                            if (len(group_inspections)% 3 ==0):
                                break
                    
                    
                print("FINAAAAL", equip_info[0])
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    fecha_inspecciones,
                    responsables,
                    (table_aspectos, group_inspections[0], group_inspections[1], group_inspections[2]),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = Table(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
            
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                hAlign='LEFT'
                        )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
                
                #setFont('Helvetica', 10)
            
                #contents.append(tabla)
                
                contents.append(tabla)
                qr_code_data = [
                    [qr_code_image],
                    #["Escanee el código QR"],
                    ]

                table_qr = Table(data = qr_code_data,
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                
                                                       
                                ],
                        hAlign='LEFT'
                        )
                contents.append(table_qr)
                index += 1
                

            
            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())

            doc.addPageTemplates([firstpage,laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)

class ReportSheet_casco:  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)                

    
    def foot2(self,pdf,doc):
        width,height = A4
        pdf.saveState()
        pdf.setFont('Times-Roman',9)
        if self.flagShape=='0':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
        elif self.flagShape=='1':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
    
    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    class RotatedImage(Image):

        def wrap(self,availWidth,availHeight):
            h, w = Image.wrap(self,availHeight,availWidth)
            return w, h
        def draw(self):
            self.canv.rotate(90)
            Image.draw(self)

    def get_doc(self, pdf, buffer, inspection_info, equip_info, flag, Activate_photo):
        self.flagShape=flag
        width,height = A4
        
        doc = BaseDocTemplate(buffer,showBoundary=1, pagesize= A4)
        contents =[]
        styleSheet = getSampleStyleSheet()
        Title = "Hello world"
        TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.5*inch,showBoundary=1,id='normal')
        frame1 = Frame(0.2*inch,0.2*inch,(width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col1')
        frame2 = Frame(0.4*inch+(width-0.6*inch)/2,0.2*inch, (width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col2' )
        leftlogoframe = Frame(0.2*inch,height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        rightlogoframe = Frame((width-1.2*inch),height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')
        frame2later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,showBoundary = 1,id='col2later' )

        frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')
        
        firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

        laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)
        
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        styleH_2 = styles['Normal']
        bodyStyle = ParagraphStyle('Body',fontSize=11)
        para1 = Paragraph('Spam spam spam spam. ' * 300, bodyStyle)
        contents.append(NextPageTemplate('laterpages'))
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        
        logoleft = Image(archivo_imagen)
        logoleft._restrictSize(0.7*inch, 0.7*inch)
        logoleft.hAlign = 'LEFT'
        logoleft.vAlign = 'CENTER'
        
        style_bold = styles['Heading1']
        style_bold.fontSize=11
        #styleH_bold.alignment=TA_CENTER
        style_bold.leading = 11
        style_bold.fontName = 'Helvetica-Bold'

        

        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))

        style_normal= styles["Normal"]
        style_normal.fontSize=14
        #styleH_bold.alignment=TA_CENTER
        style_normal.leading = 11
        style_normal.fontName = 'Helvetica-Bold'


        style_normal_body= styles["Normal"]
        style_normal_body.fontSize=8
        #styleH_bold.alignment=TA_CENTER
        style_normal_body.leading = 9
        style_normal_body.fontName = 'Helvetica'

        style_small= styles["Italic"]
        style_small.fontSize = 6
        #stylesmallnment=TA_CENTER
        style_small.leading = 8
        style_small.fontName = 'Helvetica'
       
        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))
        
    
        Aspectos_inspeccionar = (Paragraph("ASPECTOS A INSPECCIONAR",style_normal))
    
        datos_table_casquete = (
                (verticalText('CASQUETE'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                ('', (Paragraph('Presenta quemaduras o deterioro por químicos',style_normal_body))),
                ('', (Paragraph('Presenta rayadura o decoloración',style_normal_body))),
                ('', 'Otros'),
            )

        table_casquete = Table(data = datos_table_casquete,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                             
                            ],
                    hAlign='LEFT',
                    )

        datos_table_suspencion = (
                (verticalText('SUSPENCIÓN'),'Completo'),
                ('', (Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                ('', 'Hay torsión o estiramiento'),
                ('', 'Otros'),
            )

        table_suspencion = Table(data = datos_table_suspencion,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                             
                            ],
                    hAlign='LEFT',
                    )
        datos_table_barbuquejo = (
                (verticalText('BARBUQUEJO'),'Completo'),
                ('', (Paragraph('La cinta están deshilachada o rotas',style_normal_body))),
                ('', (Paragraph('Salpicadura de pintura y rigidez en cinta',style_normal_body))),
                ('', 'Otros'),
            )

        table_barbuquejo = Table(data = datos_table_barbuquejo,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                             
                            ],
                    hAlign='LEFT',
                    )
        

        datos_table_aspectos = (
                ('EQUIPO','PARTES',Aspectos_inspeccionar),
                (verticalText('CASCOS DE SEGURIDAD'), table_casquete,''),
                ('', table_suspencion,''),
                ('', table_barbuquejo,''),
                ('','VEREDICTO:',''),
                ('','Fecha de proxima inspección','')
            )

        table_aspectos = Table(data = datos_table_aspectos,colWidths=(
            0.5*inch,
            0.6*inch,1.58*inch
            ), 
            rowHeights=(
                0.3*inch, 
                1.2*inch, 
                1.2*inch, 
                1.2*inch,
                0.33*inch,
                0.17*inch)
                ,
            style = [
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    #('BOX',(0,0),(-1,-1),2,colors.black), 
                    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                    ('SPAN',(1,1),(2,1)),
                    ('SPAN',(0,1),(0,-1)),
                    ('SPAN',(-2,-1),(-1,-1)),
                    ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                    ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                    ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                    ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                    ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                    ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                    ('LEFTPADDING',(1,1),(-2,-1), 0),
                    ('RIGHTPADDING',(1,1),(-2,-1), 0),
                    ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                    ('TOPPADDING',(1,1),(-2,-1), 0),  
                    ('TOPPADDING',(0,0),(0,0), 0), 
                    ('SPAN',(-2,-2),(-1,-2)),
                    # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                    # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                    ],
                    )
        
        if flag=='1':
            
            contents.append(logoleft)
            contents.append(FrameBreak())
            datos_table_casquete = (
                    (verticalText('CASQUETE'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                    ('', (Paragraph('Presenta quemaduras o deterioro por químicos',style_normal_body))),
                    ('', (Paragraph('Presenta rayadura o decoloración',style_normal_body))),
                    ('', 'Otros'),
                )

            table_casquete = Table(data = datos_table_casquete,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                             
                                ],
                        hAlign='LEFT',
                        )

            datos_table_suspencion = (
                    (verticalText('SUSPENCIÓN'),'Completo'),
                    ('', (Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                    ('', 'Hay torsión o estiramiento'),
                    ('', 'Otros'),
                )

            table_suspencion = Table(data = datos_table_suspencion,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                             
                                ],
                        hAlign='LEFT',
                        )
            datos_table_barbuquejo = (
                    (verticalText('BARBUQUEJO'),'Completo'),
                    ('', (Paragraph('La cinta están deshilachada o rotas',style_normal_body))),
                    ('', (Paragraph('Salpicadura de pintura y rigidez en cinta',style_normal_body))),
                    ('', 'Otros'),
                )

            table_barbuquejo = Table(data = datos_table_barbuquejo,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                             
                                ],
                        hAlign='LEFT',
                        )
            

            datos_table_aspectos = (
                    ('EQUIPO','PARTES',Aspectos_inspeccionar),
                    (verticalText('CASCOS DE SEGURIDAD'), table_casquete,''),
                    ('', table_suspencion,''),
                    ('', table_barbuquejo,''),
                    ('','VEREDICTO:',''),
                    ('','Fecha de proxima inspección','')
                )

            table_aspectos = Table(data = datos_table_aspectos,colWidths=(
                0.5*inch,
                0.6*inch,1.58*inch
                ), 
                rowHeights=(
                0.5*inch, 
                2*inch, 
                2*inch, 
                2*inch,
                0.33*inch,
                0.17*inch)
                ,
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(1,1),(2,1)),
                        ('SPAN',(0,1),(0,-1)),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                        ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                        ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                        ('LEFTPADDING',(1,1),(-2,-1), 0),
                        ('RIGHTPADDING',(1,1),(-2,-1), 0),
                        ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                        ('TOPPADDING',(1,1),(-2,-1), 0),  
                        ('TOPPADDING',(0,0),(0,0), 0), 
                        ('SPAN',(-2,-2),(-1,-2)),
                        # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                        ],
                        )
            inspection = inspection_info[0]
            
            qr_path = inspection['codigo_qr_pdf']
            
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            
        
            merged_all = inspection.copy()
            
            
            keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','casquete_foto', 'suspencion_foto', 'barbuquejo_foto']
            if Activate_photo:
                keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','casquete_foto', 'suspencion_foto', 'barbuquejo_foto', 'foto_inspector']
                imagen_avatar =  Image(settings.MEDIA_ROOT+inspection['foto_inspector'],width=60, height=80)
            for key in keys_to_remove:

                merged_all.pop(key)
           
            
            imagen_casquete = Image(settings.MEDIA_ROOT+inspection['casquete_foto'],width=150, height=130)
            #imagen_reata._restrictSize(0.7*inch, 0.7*inch)
            imagen_suspencion = Image(settings.MEDIA_ROOT+inspection['suspencion_foto'],width=150, height=130)
            imagen_barbuquejo = Image(settings.MEDIA_ROOT+inspection['barbuquejo_foto'],width=150, height=130)

            datos_table_boolean = [
                ('SI','NO')
                ]
            
            datos_table_observaciones = [
                ('Observaciones','')
                ]

            index_difference = 0 
            for  key in merged_all:
                
                value = merged_all[key]
                if index_difference > 11:

                    datos_table_observaciones.append((Paragraph(value,style_small),''))
                
                else:

                    if value:

                        datos_table_boolean.append(('X',''))
                    
                    else: 
                        
                        datos_table_boolean.append(('','X'))
                    
                    index_difference += 1

            datos_table_observaciones.append(('',''))

            if inspection['veredicto']:

                datos_veredicto_fecha = (
                    ('X', Paragraph("Apto y puede continuar",style_small)),
                    ('', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    # inspection_info['proxima_inspeccion']
                    )
            else:

                datos_veredicto_fecha = (
                    ('', Paragraph("Apto y puede continuar",style_small)),
                    ('X', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    )
            #print("VEREDICTO",inspection[count]['veredicto'] )


            table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                            
                                ],
                        hAlign='LEFT'
                        )
            datos_table_boolean.append((table_veredicto_fecha, ''))

            table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch,
                0.5*inch, 0.5*inch, .5*inch, .5*inch, .5*inch, .5*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            
            imagenes = [
            
                ('Casquete',''),
                (imagen_casquete,''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Suspención', ''),
                (imagen_suspencion, ''),
                ('', ''), 
                ('', ''),
                ('', ''),
                ('Barbuquejo', ''),
                (imagen_barbuquejo, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ]
           
            table_imagenes = Table(data = imagenes,colWidths=(2.4*inch), rowHeights=(
                0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch,
                0.5*inch, 0.5*inch, .5*inch, .5*inch, .5*inch, .5*inch, 0.5, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(0,1),(1,1)),
                        ('SPAN',(0,1),(1,4)),
                        ('SPAN',(0,5),(1,5)),
                        ('SPAN',(0,6),(1,9)),
                        ('SPAN',(0,10),(1,10)),
                        ('SPAN',(0,11),(1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            style_observacion = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('SPAN',(0,0),(1, 0)),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),                     
                        ]

            for i in range(1,20):
                style_observacion.append(('SPAN',(0, i),(1, i)))
            
            table_observaciones = Table(data = datos_table_observaciones,colWidths=(1.6*inch), rowHeights=(
               0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch,
               0.5*inch, 0.5*inch, .5*inch, .5*inch, .5*inch, .5*inch, 0.5*inch),
                style = style_observacion ,
                hAlign='LEFT'
                )

            if Activate_photo=='True':
                
                datos_header = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'], ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'],''),
                    )
                tabla_head = LongTable(data = datos_header,colWidths=(2.68*inch,1.6*inch,1.*inch),
                    style = [
                            ('GRID',(0,0),(2,4),0.5,colors.grey),
                            
                            ('SPAN',(1,0),(2,0)),
                            ('SPAN',(1,1),(2,1)),
                            ('SPAN',(1,2),(2,2)),
                            ('SPAN',(1,3),(2,3)),
                            ('SPAN',(1,4),(2,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (2, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                datos_table_2 = (
                    (tabla_head,'','',imagen_avatar),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.*inch,1.6*inch),
                    style = [
                            
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            ('ALIGN', (1,0),(3,0), "RIGHT"), 
                            ('VALIGN', (1,0),(3,0), "MIDDLE"),
                            ('LEFTPADDING',(0,0),(0,0), 0),
                            ('RIGHTPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('TOPPADDING',(0,0),(0,0), 0),                     

                            ('TOPPADDING',(-5, -1),(-5,-1), 0),
                            
                            ('LEFTPADDING',(-4,-1),(-4,-1), 0),
                            ('RIGHTPADDING',(-4,-1),(-4,-1), 0),
                            ('BOTTOMPADDING',(-4,-1),(-4,-1), 0),
                            ('TOPPADDING',(-4,-1),(-4,-1), 0),

                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2, -1),(-2, -1), 0),
                            ('RIGHTPADDING',(-2, -1),(-2, -1), 0),
                            ('BOTTOMPADDING',(-2, -1),(-2, -1), 0),
                            ('TOPPADDING',(-2, -1),(-2, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            elif Activate_photo=='False':
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                    style = [
                            ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                            ('SPAN',(1,0),(3,0)),
                            ('SPAN',(1,1),(3,1)),
                            ('SPAN',(1,2),(3,2)),
                            ('SPAN',(1,3),(3,3)),
                            ('SPAN',(1,4),(3,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            

                            ('LEFTPADDING',(0,5),(0,5), 0),
                            ('RIGHTPADDING',(0,5),(0,5), 0),
                            ('BOTTOMPADDING',(0,5),(0,5), 0),
                            ('TOPPADDING',(0,5),(0,5), 0),
                            ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                            ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                            
                            ('TOPPADDING',(-4, -1),(-4,-1), 0),
                            
                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                            ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                            ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                            ('TOPPADDING',(-2,-1),(-2,-1), 0),

                            ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                            ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                            ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                            ('TOPPADDING',(-1, -1),(-1, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            contents.append(tabla)
            datos_tabla_comentarios = [
                    [Paragraph('Comentarios Adicionales:', ParagraphStyle('Heading',fontSize=12))],
                    [Paragraph(inspection['comentarios_adicionales'], bodyStyle)]
                ] 
           
            table_comentarios = Table(data = datos_tabla_comentarios)
            qr_code_data = [
                    [qr_code_image, table_comentarios],
                    
                    #["Escanee el código QR"],
                    ]

            table_qr = Table(data = qr_code_data,colWidths=(1.5*inch, 5.98*inch),
                    style = [
                            ('GRID',(0,0),(1,1),0.5,colors.grey),
                            ('TOPPADDING',(0, 0),(1, 0), 4),
                            ('VALIGN', (0, 0), (1, 0), "TOP"),                     
                            ],
                    hAlign='LEFT'
                    ,repeatRows=1
                    )

            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_aspectos, table_imagenes, ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        

                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            
            contents.append(tabla)
            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_qr, '', ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            contents.append(tabla)
            #contents.append(table_qr)

            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())


            doc.addPageTemplates([firstpage, laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)
        
        elif flag=='0':
            
            qr_path = equip_info[0]['codigo_qr']
        
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            inspection_info = list(self.chunks(inspection_info, 3))
            #print("Esta es", inspection_info)
            
            #print(inspection_info)
            index = 0 
            
            
            
                
            while (True):
                


                if index > (len(inspection_info)-1):
                    break
                contents.append(logoleft)
                contents.append(FrameBreak())
                group_inspections = []
                
                inspection = inspection_info[index]
                
                count = 0 
                fecha_inspecciones = ["FECHA INSPECCIÓN: "]
                responsables = ["RESPONSABLE DE LA INSPECCIÓN: "]
                
                while (True):
                    
                    
                    if ((count > 2) or (count > len(inspection)-1)):

                        break
                    
                    merged_all = inspection[count].copy()
                    
                    
                    keys_to_remove = ["fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto']

                    for key in keys_to_remove:

                        merged_all.pop(key)

                    
                    datos_table_boolean = [
                        ('SI','NO')
                        ]
                    
                    for  key in merged_all:
                        
                        value = merged_all[key]
                        
                        if value:

                            datos_table_boolean.append(('X',''))
                        
                        else: 
                            
                            datos_table_boolean.append(('','X'))
                    
                    if inspection[count]['veredicto']:

                        datos_veredicto_fecha = (
                            ('X', Paragraph("Apto y puede continuar",style_small)),
                            ('', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            # inspection_info['proxima_inspeccion']
                            )
                    else:

                        datos_veredicto_fecha = (
                            ('', Paragraph("Apto y puede continuar",style_small)),
                            ('X', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            )
                    #print("VEREDICTO",inspection[count]['veredicto'] )


                    table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                        
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                        
                                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        ('SPAN',(-2,-1),(-1,-1)),
                                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        # ('LEFTPADDING',(0,0),(-1,-1), 0),
                                        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                        # ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                        # ('TOPPADDING',(0,0),(-1,-1), 0),
                                                                
                                        ],
                                hAlign='LEFT'
                                )
                    datos_table_boolean.append((table_veredicto_fecha, ''))
                    Altura=0.3
                    table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                        0.38*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch,
                        Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, 0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('LEFTPADDING',(0,0),(-1,-1), 0),
                                ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                ('TOPPADDING',(0,0),(-1,-1), 0),
                                # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                                # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                                ],
                        hAlign='LEFT'
                        )

                    group_inspections.append(table_datos_boolean)

                    fecha_inspecciones.append(inspection[count]['fecha_inspeccion'])

                    responsables.append(
                        inspection[count]['first_name']+
                        " "+
                        inspection[count]['last_name'])
                    count += 1
                
                if not (len(group_inspections)%3 ==0):
                
                        while(True):
                            group_inspections.append('')
                            if (len(group_inspections)% 3 ==0):
                                break
                    
                    
                print("FINAAAAL", equip_info[0])
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    fecha_inspecciones,
                    responsables,
                    (table_aspectos, group_inspections[0], group_inspections[1], group_inspections[2]),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = Table(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
            
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                hAlign='LEFT'
                        )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
                
                #setFont('Helvetica', 10)
            
                #contents.append(tabla)
                
                contents.append(tabla)
                qr_code_data = [
                    [qr_code_image],
                    #["Escanee el código QR"],
                    ]

                table_qr = Table(data = qr_code_data,
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                
                                                       
                                ],
                        hAlign='LEFT'
                        )
                contents.append(table_qr)
                index += 1
                

            
            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())

            doc.addPageTemplates([firstpage,laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)



class ReportSheet_accesorios:  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)                
  
    def foot2(self,pdf,doc):
        width,height = A4
        pdf.saveState()
        pdf.setFont('Times-Roman',9)
        if self.flagShape=='0':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
        elif self.flagShape=='1':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
    
    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    class RotatedImage(Image):

        def wrap(self,availWidth,availHeight):
            h, w = Image.wrap(self,availHeight,availWidth)
            return w, h
        def draw(self):
            self.canv.rotate(90)
            Image.draw(self)

    def get_doc(self, pdf, buffer, inspection_info, equip_info, flag, Activate_photo):
        self.flagShape=flag
        width,height = A4
        
        doc = BaseDocTemplate(buffer,showBoundary=1, pagesize= A4)
        contents =[]
        styleSheet = getSampleStyleSheet()
        Title = "Hello world"
        TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.5*inch,showBoundary=1,id='normal')
        frame1 = Frame(0.2*inch,0.2*inch,(width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col1')
        frame2 = Frame(0.4*inch+(width-0.6*inch)/2,0.2*inch, (width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col2' )
        leftlogoframe = Frame(0.2*inch,height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        rightlogoframe = Frame((width-1.2*inch),height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')
        frame2later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,showBoundary = 1,id='col2later' )

        frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')
        
        firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

        laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)
        
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        styleH_2 = styles['Normal']
        bodyStyle = ParagraphStyle('Body',fontSize=11)
        para1 = Paragraph('Spam spam spam spam. ' * 300, bodyStyle)
        contents.append(NextPageTemplate('laterpages'))
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        
        logoleft = Image(archivo_imagen)
        logoleft._restrictSize(0.7*inch, 0.7*inch)
        logoleft.hAlign = 'LEFT'
        logoleft.vAlign = 'CENTER'
        
        style_bold = styles['Heading1']
        style_bold.fontSize=11
        #styleH_bold.alignment=TA_CENTER
        style_bold.leading = 11
        style_bold.fontName = 'Helvetica-Bold'

        style_normal= styles["Normal"]
        style_normal.fontSize=14
        #styleH_bold.alignment=TA_CENTER
        style_normal.leading = 11
        style_normal.fontName = 'Helvetica-Bold'


        style_normal_body= styles["Normal"]
        style_normal_body.fontSize=8
        #styleH_bold.alignment=TA_CENTER
        style_normal_body.leading = 9
        style_normal_body.fontName = 'Helvetica'

        style_small= styles["Italic"]
        style_small.fontSize = 6
        #stylesmallnment=TA_CENTER
        style_small.leading = 8
        style_small.fontName = 'Helvetica'
       
        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))
        
    
        Aspectos_inspeccionar = (Paragraph("ASPECTOS A INSPECCIONAR",style_normal))
    
        datos_table_mosquetones = (
                (verticalText('MOSQUETONES'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                ('', (Paragraph('Presenta quemaduras o deterior por químicos',style_normal_body))),
                ('', (Paragraph('Presenta oxidación y corrosión',style_normal_body))),
                ('', (Paragraph('Presenta bordes filosos y rugosos que causen corte',style_normal_body))),
                ('', (Paragraph('La compuerta abre y cierra libremente',style_normal_body))),
                ('', 'Tiene deformaciones'),
                ('', 'Otros'),
            )

        table_mosquetones = Table(data = datos_table_mosquetones,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                             
                            ],
                    hAlign='LEFT',
                    )

        datos_table_arrestador = (
                (verticalText('ARRESTADOR DE CAIDAS'),verticalText('Y'),verticalText('POLEAS'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                ('','','', (Paragraph('La superficie de frenado se encuentran lisas',style_normal_body))),
                ('','','', (Paragraph('Presenta oxidación y corrosión',style_normal_body))),
                ('','','', (Paragraph('Presenta bordes filosos y rugosos que causen corte',style_normal_body))),
                ('','','', (Paragraph('La compuerta abre y cierra libremente',style_normal_body))),
                ('','','', 'Tiene deformaciones'),
                ('','','', 'Otros'),  
            )

        table_arrestador = Table(data = datos_table_arrestador,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-4,-1)),   
                            ('SPAN',(1,0),(-3,-1)), 
                            ('SPAN',(2,0),(-2,-1)),                           
                            ],
                    hAlign='LEFT',
                    )
        datos_table_descendedor = (
                (verticalText('DESCENDEDORES/'),verticalText('ASCENDEDORES Y ANCLAJES'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                ('','', (Paragraph('La superficie de contacto se encuentran lisas.',style_normal_body))),
                ('','', (Paragraph('Presenta oxidación y corrosión',style_normal_body))),
                ('','', (Paragraph('Presenta bordes filosos y rugosos que causen corte',style_normal_body))),
                ('','', (Paragraph('Presenta desgaste y disminución del metal',style_normal_body))),
                ('','', 'Tiene deformaciones'),
                ('','', 'Otros'),    
            )

        table_descendedor = Table(data = datos_table_descendedor,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-3,-1)),   
                            ('SPAN',(1,0),(-2,-1)),                        
                            ],
                    hAlign='LEFT',
                    )
        

        datos_table_aspectos = (
                ('EQUIPO','PARTES',Aspectos_inspeccionar),
                (verticalText('ACCESORIOS METALICOS'), table_mosquetones,''),
                ('', table_arrestador,''),
                ('', table_descendedor,''),
                ('','VEREDICTO:',''),
                ('','Fecha de proxima inspección','')
            )

        table_aspectos = Table(data = datos_table_aspectos,colWidths=(
            0.5*inch,
            0.6*inch,1.58*inch
            ), 
            rowHeights=(
                0.6*inch, 
                2.1*inch, 
                2.1*inch, 
                2.1*inch,
                0.33*inch,
                0.17*inch)
                ,
            style = [
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    #('BOX',(0,0),(-1,-1),2,colors.black), 
                    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                    ('SPAN',(1,1),(2,1)),
                    ('SPAN',(0,1),(0,-1)),
                    ('SPAN',(-2,-1),(-1,-1)),
                    ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                    ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                    ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                    ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                    ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                    ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                    ('LEFTPADDING',(1,1),(-2,-1), 0),
                    ('RIGHTPADDING',(1,1),(-2,-1), 0),
                    ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                    ('TOPPADDING',(1,1),(-2,-1), 0),  
                    ('TOPPADDING',(0,0),(0,0), 0), 
                    ('SPAN',(-2,-2),(-1,-2)),
                    # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                    # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                    ],
                    )
        
        if flag=='1':
            
            contents.append(logoleft)
            contents.append(FrameBreak())
            datos_table_mosquetones = (
                    (verticalText('MOSQUETONES'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                    ('', (Paragraph('Presenta quemaduras o deterior por químicos',style_normal_body))),
                    ('', (Paragraph('Presenta oxidación y corrosión',style_normal_body))),
                    ('', (Paragraph('Presenta bordes filosos y rugosos que causen corte',style_normal_body))),
                    ('', (Paragraph('La compuerta abre y cierra libremente',style_normal_body))),
                    ('', 'Tiene deformaciones'),
                    ('', 'Otros'),
                )

            table_mosquetones = Table(data = datos_table_mosquetones,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                             
                                ],
                        hAlign='LEFT',
                        )

            datos_table_arrestador = (
                    (verticalText('ARRESTADOR DE CAIDAS'),verticalText('Y'),verticalText('POLEAS'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                    ('','','', (Paragraph('La superficie de frenado se encuentran lisas',style_normal_body))),
                    ('','','', (Paragraph('Presenta oxidación y corrosión',style_normal_body))),
                    ('','','', (Paragraph('Presenta bordes filosos y rugosos que causen corte',style_normal_body))),
                    ('','','', (Paragraph('La compuerta abre y cierra libremente',style_normal_body))),
                    ('','','', 'Tiene deformaciones'),
                    ('','','', 'Otros'),  
                )

            table_arrestador = Table(data = datos_table_arrestador,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.3*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-4,-1)),   
                                ('SPAN',(1,0),(-3,-1)), 
                                ('SPAN',(2,0),(-2,-1)),                           
                                ],
                        hAlign='LEFT',
                        )
            datos_table_descendedor = (
                    (verticalText('DESCENDEDORES/'),verticalText('ASCENDEDORES Y ANCLAJES'),(Paragraph('Tiene fisuras, golpes, hundimientos',style_normal_body))),
                    ('','', (Paragraph('La superficie de contacto se encuentran lisas.',style_normal_body))),
                    ('','', (Paragraph('Presenta oxidación y corrosión',style_normal_body))),
                    ('','', (Paragraph('Presenta bordes filosos y rugosos que causen corte',style_normal_body))),
                    ('','', (Paragraph('Presenta desgaste y disminución del metal',style_normal_body))),
                    ('','', 'Tiene deformaciones'),
                    ('','', 'Otros'),    
                )

            table_descendedor = Table(data = datos_table_descendedor,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.3*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-3,-1)),   
                                ('SPAN',(1,0),(-2,-1)),                        
                                ],
                        hAlign='LEFT',
                        )
            

            datos_table_aspectos = (
                    ('EQUIPO','PARTES',Aspectos_inspeccionar),
                    (verticalText('ACCESORIOS METALICOS'), table_mosquetones,''),
                    ('', table_arrestador,''),
                    ('', table_descendedor,''),
                    ('','VEREDICTO:',''),
                    ('','Fecha de proxima inspección','')
                )

            table_aspectos = Table(data = datos_table_aspectos,colWidths=(
                0.5*inch,
                0.6*inch,1.58*inch
                ), 
                rowHeights=(
                    0.6*inch, 
                    2.1*inch, 
                    2.1*inch, 
                    2.1*inch,
                    0.33*inch,
                    0.17*inch)
                    ,
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(1,1),(2,1)),
                        ('SPAN',(0,1),(0,-1)),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                        ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                        ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                        ('LEFTPADDING',(1,1),(-2,-1), 0),
                        ('RIGHTPADDING',(1,1),(-2,-1), 0),
                        ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                        ('TOPPADDING',(1,1),(-2,-1), 0),  
                        ('TOPPADDING',(0,0),(0,0), 0), 
                        ('SPAN',(-2,-2),(-1,-2)),
                        # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                        ],
                        )
            inspection = inspection_info[0]
            
            qr_path = inspection['codigo_qr_pdf']
            
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            
        
            merged_all = inspection.copy()
            
            
            keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','mosquetones_foto', 'arrestador_poleas_foto', 'descendedores_anclajes_foto']
            if Activate_photo:
                keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','mosquetones_foto', 'arrestador_poleas_foto', 'descendedores_anclajes_foto', 'foto_inspector']
                imagen_avatar =  Image(settings.MEDIA_ROOT+inspection['foto_inspector'],width=60, height=80)
            for key in keys_to_remove:

                merged_all.pop(key)
           
            
            imagen_mosquetones = Image(settings.MEDIA_ROOT+inspection['mosquetones_foto'],width=170, height=150)
            #imagen_reata._restrictSize(0.7*inch, 0.7*inch)
            imagen_arrestador = Image(settings.MEDIA_ROOT+inspection['arrestador_poleas_foto'],width=170, height=150)
            imagen_descendedores = Image(settings.MEDIA_ROOT+inspection['descendedores_anclajes_foto'],width=170, height=150)

            datos_table_boolean = [
                ('SI','NO')
                ]
            
            datos_table_observaciones = [
                ('Observaciones','')
                ]

            index_difference = 0 
            for  key in merged_all:
                
                value = merged_all[key]
                if index_difference >20:

                    datos_table_observaciones.append((Paragraph(value,style_small),''))
                
                else:

                    if value:

                        datos_table_boolean.append(('X',''))
                    
                    else: 
                        
                        datos_table_boolean.append(('','X'))
                    
                    index_difference += 1

            datos_table_observaciones.append(('',''))

            if inspection['veredicto']:

                datos_veredicto_fecha = (
                    ('X', Paragraph("Apto y puede continuar",style_small)),
                    ('', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    # inspection_info['proxima_inspeccion']
                    )
            else:

                datos_veredicto_fecha = (
                    ('', Paragraph("Apto y puede continuar",style_small)),
                    ('X', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    )
            #print("VEREDICTO",inspection[count]['veredicto'] )


            table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                            
                                ],
                        hAlign='LEFT'
                        )
            datos_table_boolean.append((table_veredicto_fecha, ''))

            table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                0.6*inch, 0.30*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 
                0.3*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            
            imagenes = [
            
                ('Mosquetones',''),
                (imagen_mosquetones,''),
                ('',''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Arrestador de caidas y poleas', ''),
                (imagen_arrestador, ''),
                ('', ''), 
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Descendedores/Ascendedores y anclajes', ''),
                (imagen_descendedores, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ]
           
            table_imagenes = Table(data = imagenes,colWidths=(2.4*inch), rowHeights=(
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(0,1),(1,1)),
                        ('SPAN',(0,1),(1,7)),
                        ('SPAN',(0,8),(1,8)),
                        ('SPAN',(0,9),(1,15)),
                        ('SPAN',(0,16),(1,16)),
                        ('SPAN',(0,17),(1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            style_observacion = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('SPAN',(0,0),(1, 0)),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),                     
                        ]

            for i in range(1,22):
                style_observacion.append(('SPAN',(0, i),(1, i)))
            
            table_observaciones = Table(data = datos_table_observaciones,colWidths=(1.6*inch), rowHeights=(
                0.6*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.5*inch),
                style = style_observacion ,
                hAlign='LEFT'
                )

            if Activate_photo=='True':
                
                datos_header = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'], ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'],''),
                    )
                tabla_head = LongTable(data = datos_header,colWidths=(2.68*inch,1.6*inch,1.*inch),
                    style = [
                            ('GRID',(0,0),(2,4),0.5,colors.grey),
                            
                            ('SPAN',(1,0),(2,0)),
                            ('SPAN',(1,1),(2,1)),
                            ('SPAN',(1,2),(2,2)),
                            ('SPAN',(1,3),(2,3)),
                            ('SPAN',(1,4),(2,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (2, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                datos_table_2 = (
                    (tabla_head,'','',imagen_avatar),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.*inch,1.6*inch),
                    style = [
                            
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            ('ALIGN', (1,0),(3,0), "RIGHT"), 
                            ('VALIGN', (1,0),(3,0), "MIDDLE"),
                            ('LEFTPADDING',(0,0),(0,0), 0),
                            ('RIGHTPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('TOPPADDING',(0,0),(0,0), 0),                     

                            ('TOPPADDING',(-5, -1),(-5,-1), 0),
                            
                            ('LEFTPADDING',(-4,-1),(-4,-1), 0),
                            ('RIGHTPADDING',(-4,-1),(-4,-1), 0),
                            ('BOTTOMPADDING',(-4,-1),(-4,-1), 0),
                            ('TOPPADDING',(-4,-1),(-4,-1), 0),

                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2, -1),(-2, -1), 0),
                            ('RIGHTPADDING',(-2, -1),(-2, -1), 0),
                            ('BOTTOMPADDING',(-2, -1),(-2, -1), 0),
                            ('TOPPADDING',(-2, -1),(-2, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            elif Activate_photo=='False':
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                    style = [
                            ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                            ('SPAN',(1,0),(3,0)),
                            ('SPAN',(1,1),(3,1)),
                            ('SPAN',(1,2),(3,2)),
                            ('SPAN',(1,3),(3,3)),
                            ('SPAN',(1,4),(3,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            

                            ('LEFTPADDING',(0,5),(0,5), 0),
                            ('RIGHTPADDING',(0,5),(0,5), 0),
                            ('BOTTOMPADDING',(0,5),(0,5), 0),
                            ('TOPPADDING',(0,5),(0,5), 0),
                            ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                            ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                            
                            ('TOPPADDING',(-4, -1),(-4,-1), 0),
                            
                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                            ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                            ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                            ('TOPPADDING',(-2,-1),(-2,-1), 0),

                            ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                            ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                            ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                            ('TOPPADDING',(-1, -1),(-1, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            contents.append(tabla)
            datos_tabla_comentarios = [
                    [Paragraph('Comentarios Adicionales:', ParagraphStyle('Heading',fontSize=12))],
                    [Paragraph(inspection['comentarios_adicionales'], bodyStyle)]
                ] 
           
            table_comentarios = Table(data = datos_tabla_comentarios)
            qr_code_data = [
                    [qr_code_image, table_comentarios],
                    
                    #["Escanee el código QR"],
                    ]

            table_qr = Table(data = qr_code_data,colWidths=(1.5*inch, 5.98*inch),
                    style = [
                            ('GRID',(0,0),(1,1),0.5,colors.grey),
                            ('TOPPADDING',(0, 0),(1, 0), 4),
                            ('VALIGN', (0, 0), (1, 0), "TOP"),                     
                            ],
                    hAlign='LEFT'
                    ,repeatRows=1
                    )

            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_aspectos, table_imagenes, ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        

                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            
            contents.append(tabla)
            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_qr, '', ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            contents.append(tabla)
            #contents.append(table_qr)

            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())


            doc.addPageTemplates([firstpage, laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)
        
        elif flag=='0':
            
            qr_path = equip_info[0]['codigo_qr']
        
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=50, height=50)
            inspection_info = list(self.chunks(inspection_info, 3))
            #print("Esta es", inspection_info)
            
            #print(inspection_info)
            index = 0 
            
            
            
                
            while (True):
                


                if index > (len(inspection_info)-1):
                    break
                contents.append(logoleft)
                contents.append(FrameBreak())
                group_inspections = []
                
                inspection = inspection_info[index]
                
                count = 0 
                fecha_inspecciones = ["FECHA INSPECCIÓN: "]
                responsables = ["RESPONSABLE DE LA INSPECCIÓN: "]
                
                while (True):
                    
                    
                    if ((count > 2) or (count > len(inspection)-1)):

                        break
                    
                    merged_all = inspection[count].copy()
                    
                    
                    keys_to_remove = ["fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto']

                    for key in keys_to_remove:

                        merged_all.pop(key)

                    
                    datos_table_boolean = [
                        ('SI','NO')
                        ]
                    
                    for  key in merged_all:
                        
                        value = merged_all[key]
                        
                        if value:

                            datos_table_boolean.append(('X',''))
                        
                        else: 
                            
                            datos_table_boolean.append(('','X'))
                    
                    if inspection[count]['veredicto']:

                        datos_veredicto_fecha = (
                            ('X', Paragraph("Apto y puede continuar",style_small)),
                            ('', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            # inspection_info['proxima_inspeccion']
                            )
                    else:

                        datos_veredicto_fecha = (
                            ('', Paragraph("Apto y puede continuar",style_small)),
                            ('X', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            )
                    #print("VEREDICTO",inspection[count]['veredicto'] )


                    table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                        
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                        
                                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        ('SPAN',(-2,-1),(-1,-1)),
                                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        # ('LEFTPADDING',(0,0),(-1,-1), 0),
                                        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                        # ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                        # ('TOPPADDING',(0,0),(-1,-1), 0),
                                                                
                                        ],
                                hAlign='LEFT'
                                )
                    datos_table_boolean.append((table_veredicto_fecha, ''))
                    Altura=0.3
                    table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                        0.3*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch,
                        Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch,
                        Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch, Altura*inch,
                        Altura*inch, 0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('LEFTPADDING',(0,0),(-1,-1), 0),
                                ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                ('TOPPADDING',(0,0),(-1,-1), 0),
                                # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                                # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                                ],
                        hAlign='LEFT'
                        )

                    group_inspections.append(table_datos_boolean)

                    fecha_inspecciones.append(inspection[count]['fecha_inspeccion'])

                    responsables.append(
                        inspection[count]['first_name']+
                        " "+
                        inspection[count]['last_name'])
                    count += 1
                
                if not (len(group_inspections)%3 ==0):
                
                        while(True):
                            group_inspections.append('')
                            if (len(group_inspections)% 3 ==0):
                                break
                    
                    
                print("FINAAAAL", equip_info[0])
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    fecha_inspecciones,
                    responsables,
                    (table_aspectos, group_inspections[0], group_inspections[1], group_inspections[2]),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = Table(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
            
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                hAlign='LEFT'
                        )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
                
                #setFont('Helvetica', 10)
            
                #contents.append(tabla)
                
                contents.append(tabla)
                qr_code_data = [
                    [qr_code_image],
                    #["Escanee el código QR"],
                    ]

                table_qr = Table(data = qr_code_data,
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                
                                                       
                                ],
                        hAlign='LEFT'
                        )
                contents.append(table_qr)
                index += 1
                

            
            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())

            doc.addPageTemplates([firstpage,laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)

class ReportSheet_sillas:  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)                
  
    def foot2(self,pdf,doc):
        width,height = A4
        pdf.saveState()
        pdf.setFont('Times-Roman',9)
        if self.flagShape=='0':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
        elif self.flagShape=='1':
            pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
    
    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    class RotatedImage(Image):

        def wrap(self,availWidth,availHeight):
            h, w = Image.wrap(self,availHeight,availWidth)
            return w, h
        def draw(self):
            self.canv.rotate(90)
            Image.draw(self)

    def get_doc(self, pdf, buffer, inspection_info, equip_info, flag, Activate_photo):
        self.flagShape=flag
        width,height = A4
        
        doc = BaseDocTemplate(buffer,showBoundary=1, pagesize= A4)
        contents =[]
        styleSheet = getSampleStyleSheet()
        Title = "Hello world"
        TopCenter = Frame(0.4*inch,height-1.2*inch,width-0.8*inch,0.5*inch,showBoundary=1,id='normal')
        frame1 = Frame(0.2*inch,0.2*inch,(width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col1')
        frame2 = Frame(0.4*inch+(width-0.6*inch)/2,0.2*inch, (width-0.6*inch)/2, height-1.6*inch,showBoundary = 1,id='col2' )
        leftlogoframe = Frame(0.2*inch,height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        rightlogoframe = Frame((width-1.2*inch),height-1.2*inch,1*inch,1*inch,showBoundary = 1)
        frame1later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0,showBoundary = 1,id='col1later')
        frame2later = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,showBoundary = 1,id='col2later' )

        frame_params = Frame(0.4*inch,0.6*inch,width-0.8*inch, height-2*inch,leftPadding=0,topPadding=0, showBoundary = 1,id='col')
        
        firstpage = PageTemplate(id='firstpage',frames=[TopCenter,frame_params],onPage=self.foot2)

        laterpages = PageTemplate(id='laterpages',frames=[TopCenter,frame1later],onPage=self.foot2)
        
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        styleH_2 = styles['Normal']
        bodyStyle = ParagraphStyle('Body',fontSize=11)
        para1 = Paragraph('Spam spam spam spam. ' * 300, bodyStyle)
        contents.append(NextPageTemplate('laterpages'))
        archivo_imagen = settings.MEDIA_ROOT+'/iconos_imagenes/epi_logo.jpg'
        
        logoleft = Image(archivo_imagen)
        logoleft._restrictSize(0.7*inch, 0.7*inch)
        logoleft.hAlign = 'LEFT'
        logoleft.vAlign = 'CENTER'
        
        style_bold = styles['Heading1']
        style_bold.fontSize=11
        #styleH_bold.alignment=TA_CENTER
        style_bold.leading = 11
        style_bold.fontName = 'Helvetica-Bold'

        

        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))

        style_normal= styles["Normal"]
        style_normal.fontSize=14
        #styleH_bold.alignment=TA_CENTER
        style_normal.leading = 11
        style_normal.fontName = 'Helvetica-Bold'


        style_normal_body= styles["Normal"]
        style_normal_body.fontSize=8
        #styleH_bold.alignment=TA_CENTER
        style_normal_body.leading = 9
        style_normal_body.fontName = 'Helvetica'

        style_small= styles["Italic"]
        style_small.fontSize = 6
        #stylesmallnment=TA_CENTER
        style_small.leading = 8
        style_small.fontName = 'Helvetica'
       
        Fecha = (Paragraph("FECHA INSPECCIÓN",style_bold))
        Responsable = (Paragraph("RESPONSABLE DE LA INSPECCIÓN",style_bold))
        
    
        Aspectos_inspeccionar = (Paragraph("ASPECTOS A INSPECCIONAR",style_normal))
    
        datos_table_cintas = (
                (verticalText('CINTAS/REATAS'),'Tiene hoyos o agujeros'),
                ('', 'Están deshilachadas'),
                ('', 'Tienen talladuras'),
                ('', 'Hay torsión'),
                ('', 'Presentan suciedad'),
                ('', (Paragraph('Quemaduras por soldadura, cigarrillo, etc.',style_normal_body))),
                ('', (Paragraph('Salpicadura de pintura y rigidez en cinta.',style_normal_body))),
                ('', 'Sustancias químicas'),
                ('', 'Otros'),    
            )

        table_cintas = Table(data = datos_table_cintas,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-2,-1)),                             
                            ],
                    hAlign='LEFT',
                    )

        datos_table_costuras = (
                (verticalText('COSTURAS'),verticalText('Y'),verticalText('ETIQUETAS'),'Completas y Continuas'),
                ('','','', 'Son Visibles'),
                ('','','', 'Otros'),    
            )

        table_costuras = Table(data = datos_table_costuras,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-4,-1)),   
                            ('SPAN',(1,0),(-3,-1)), 
                            ('SPAN',(2,0),(-2,-1)),                           
                            ],
                    hAlign='LEFT',
                    )

        datos_table_metalicas = (
                (verticalText('PARTES'),verticalText('METÁLICAS'),verticalText('Y'),verticalText('PLASTICAS'),'Completas'),
                ('','','','', 'Presentan corrosión'),
                ('','','','', 'Deformación'),
                ('','','','',(Paragraph('Fisuras, golpes, hundimientos.',style_normal_body)) ),
                ('','','','', 'Otros'),    
            )

        table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.15*inch,0.15*inch,0.15*inch,0.15*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(1,0), 0),
                            ('FONT', (0, 0), (3, 0), 'Helvetica', 8, 8),
                            ('FONT', (-1, 0), (-1, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-5,-1)),   
                            ('SPAN',(1,0),(-4,-1)), 
                            ('SPAN',(2,0),(-3,-1)),  
                            ('SPAN',(3,0),(-2,-1)),                         
                            ],
                    hAlign='LEFT',
                    )

        datos_table_madera = (
                (verticalText('ELEMENTOS'),verticalText('DE MADERA'),(Paragraph('Tiene golpes, rupturas o deformaciones',style_normal_body))),
                ('', '', 'Presenta polillas o gorgojos'),
                ('', '', (Paragraph('Exceso de humeda y pintura',style_normal_body))),
                ('', '', 'Hay torsión'),
                ('', '', 'Otros'),    
            )

        table_madera = Table(data = datos_table_madera,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.3*inch),
                    style = [
                            ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                            #('BOX',(0,0),(-1,-1),2,colors.black), 
                            ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                            ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                            ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                            ('SPAN',(0,0),(-3,-1)),   
                            ('SPAN',(1,0),(-2,-1)),                        
                            ],
                    hAlign='LEFT',
                    )
        
        

        datos_table_aspectos = (
                ('EQUIPO','PARTES',Aspectos_inspeccionar),
                (verticalText('SILLAS/PERCHAS'),table_cintas,''),
                (" ", table_costuras,''),
                (" ", table_metalicas,''),
                (" ", table_madera,''),
                ('','VEREDICTO:',''),
                ('','Fecha de proxima inspección','')
            )

        table_aspectos = Table(data = datos_table_aspectos,colWidths=(
            0.5*inch,
            0.6*inch,1.58*inch
            ), 
            rowHeights=(
                0.39*inch, 
                2.7*inch, 
                0.9*inch,
                1.5*inch, 
                1.5*inch,
                0.33*inch,
                0.17*inch)
                ,
            style = [
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    #('BOX',(0,0),(-1,-1),2,colors.black), 
                    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                    ('SPAN',(1,1),(2,1)),
                    ('SPAN',(0,1),(0,-1)),
                    ('SPAN',(-2,-1),(-1,-1)),
                    ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                    ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                    ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                    ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                    ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                    ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                    ('LEFTPADDING',(1,1),(-2,-1), 0),
                    ('RIGHTPADDING',(1,1),(-2,-1), 0),
                    ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                    ('TOPPADDING',(1,1),(-2,-1), 0),  
                    ('TOPPADDING',(0,0),(0,0), 0), 
                    ('SPAN',(-2,-2),(-1,-2)),
                    # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                    # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                    ],
                    )

        if flag=='1':
            contents.append(logoleft)
            contents.append(FrameBreak())
            table_cintas = Table(data = datos_table_cintas,colWidths=(0.6*inch,1.58*inch),rowHeights=(0.3*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-2,-1)),                             
                                ],
                        hAlign='LEFT',
                        )


            table_costuras = Table(data = datos_table_costuras,colWidths=(0.2*inch,0.2*inch,0.2*inch,1.58*inch),rowHeights=(0.3*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (0, 0), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-4,-1)),   
                                ('SPAN',(1,0),(-3,-1)), 
                                ('SPAN',(2,0),(-2,-1)),                           
                                ],
                        hAlign='LEFT',
                        )


            table_metalicas = Table(data = datos_table_metalicas,colWidths=(0.15*inch,0.15*inch,0.15*inch,0.15*inch,1.58*inch),rowHeights=(0.3*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('BOTTOMPADDING',(0,0),(0,0), 0),
                                ('BOTTOMPADDING',(0,0),(1,0), 0),
                                ('FONT', (0, 0), (3, 0), 'Helvetica', 8, 8),
                                ('FONT', (-1, 0), (-1, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-5,-1)),   
                                ('SPAN',(1,0),(-4,-1)), 
                                ('SPAN',(2,0),(-3,-1)),  
                                ('SPAN',(3,0),(-2,-1)),                         
                                ],
                        hAlign='LEFT',
                        )


            table_madera = Table(data = datos_table_madera,colWidths=(0.3*inch,0.3*inch,1.58*inch),rowHeights=(0.3*inch),
                        style = [
                                ('GRID',(-1,0),(-1,-1),0.5,colors.grey),
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('FONT', (0, 0), (-1, -1), 'Helvetica', 7, 7),
                                ('FONT', (1, 0), (0, -1), 'Helvetica', 9, 9),
                                ('SPAN',(0,0),(-3,-1)),   
                                ('SPAN',(1,0),(-2,-1)),                        
                                ],
                        hAlign='LEFT',
                        )
            
            

            datos_table_aspectos = (
                    ('EQUIPO','PARTES',Aspectos_inspeccionar),
                    (verticalText('SILLAS/PERCHAS'),table_cintas,''),
                    (" ", table_costuras,''),
                    (" ", table_metalicas,''),
                    (" ", table_madera,''),
                    ('','VEREDICTO:',''),
                    ('','Fecha de proxima inspección','')
                )

            table_aspectos = Table(data = datos_table_aspectos,colWidths=(
                0.5*inch,
                0.6*inch,1.58*inch
                ), 
                rowHeights=(
                    0.39*inch, 
                    2.7*inch, 
                    0.9*inch,
                    1.5*inch, 
                    1.5*inch,
                    0.33*inch,
                    0.17*inch)
                    ,
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(1,1),(2,1)),
                        ('SPAN',(0,1),(0,-1)),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        ('VALIGN',(0, 1), (0, 1), "MIDDLE"),

                        ('ALIGN', (0, 0), (-1, 0), "CENTER"), 
                        ('VALIGN', (0, 0), (1, 0), "MIDDLE"),
                        ('LEFTPADDING',(1,1),(-2,-1), 0),
                        ('RIGHTPADDING',(1,1),(-2,-1), 0),
                        ('BOTTOMPADDING',(1,1),(-2,-1), 0),
                        ('TOPPADDING',(1,1),(-2,-1), 0),  
                        ('TOPPADDING',(0,0),(0,0), 0), 
                        ('SPAN',(-2,-2),(-1,-2)),
                        # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(-2,-1),(-1,-1),2,colors.blue),                          
                        ],
                        )
            
            
            inspection = inspection_info[0]
            
            qr_path = inspection['codigo_qr_pdf']
            
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=100, height=100)
            
        
            merged_all = inspection.copy()
            
            
            keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','cinta_reata_foto', 'costuras_foto', 'metalicas_foto', 'madera_foto']
            if Activate_photo:
                keys_to_remove = ['comentarios_adicionales','codigo_qr_pdf', "fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto','cinta_reata_foto', 'costuras_foto', 'metalicas_foto', 'madera_foto', 'foto_inspector']
                imagen_avatar =  Image(settings.MEDIA_ROOT+inspection['foto_inspector'],width=60, height=80)
            for key in keys_to_remove:

                merged_all.pop(key)
           
            
            imagen_reata = Image(settings.MEDIA_ROOT+inspection['cinta_reata_foto'],width=170, height=100)
            #imagen_reata._restrictSize(0.7*inch, 0.7*inch)
            imagen_costuras = Image(settings.MEDIA_ROOT+inspection['costuras_foto'], width=170, height=100)
            imagen_metalicas = Image(settings.MEDIA_ROOT+inspection['metalicas_foto'], width=170, height=100)
            imagen_madera = Image(settings.MEDIA_ROOT+inspection['madera_foto'], width=170, height=100)
            datos_table_boolean = [
                ('SI','NO')
                ]
            
            datos_table_observaciones = [
                ('Observaciones','')
                ]

            index_difference = 0 
            for  key in merged_all:
                
                value = merged_all[key]
                if index_difference >21:

                    datos_table_observaciones.append((Paragraph(value,style_small),''))
                
                else:

                    if value:

                        datos_table_boolean.append(('X',''))
                    
                    else: 
                        
                        datos_table_boolean.append(('','X'))
                    
                    index_difference += 1

            datos_table_observaciones.append(('',''))

            if inspection['veredicto']:

                datos_veredicto_fecha = (
                    ('X', Paragraph("Apto y puede continuar",style_small)),
                    ('', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    # inspection_info['proxima_inspeccion']
                    )
            else:

                datos_veredicto_fecha = (
                    ('', Paragraph("Apto y puede continuar",style_small)),
                    ('X', Paragraph("No apto y debe ser retirado",style_small)),
                    (inspection['proxima_inspeccion'], ''),
                    )
            #print("VEREDICTO",inspection[count]['veredicto'] )


            table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                            
                                ],
                        hAlign='LEFT'
                        )
            datos_table_boolean.append((table_veredicto_fecha, ''))

            table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                0.39*inch, 0.30*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            
            imagenes = [
            
                ['Reatas/cintas',''],
                [imagen_reata,''],
                ['',''],
                ('', ''),
                ('', ''),
                ('', ''),
                ('Costuras/etiquetas', ''),
                (imagen_costuras, ''),
                ('', ''), 
                ('', ''),
                ('', ''),
                ('', ''),
                ('Metalicas/plasticas', ''),
                (imagen_metalicas, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('Madera', ''),
                (imagen_madera, ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ('', ''),
                ]
           
            table_imagenes = Table(data = imagenes,colWidths=(2.4*inch), rowHeights=(
                0.39*inch, 0.30*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.5*inch),
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        
                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(0,1),(1,1)),
                        ('SPAN',(0,1),(1,5)),
                        ('SPAN',(0,6),(1,6)),
                        ('SPAN',(0,7),(1,11)),
                        ('SPAN',(0,12),(1,12)),
                        ('SPAN',(0,13),(1,17)),
                        ('SPAN',(0,18),(1,18)),
                        ('SPAN',(0,19),(1,-1)),
                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                        # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                        ],
                hAlign='LEFT'
                )
            style_observacion = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                        ('SPAN',(-2,-1),(-1,-1)),
                        ('SPAN',(0,0),(1, 0)),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),                     
                        ]

            for i in range(1,23):
                style_observacion.append(('SPAN',(0, i),(1, i)))
            
            table_observaciones = Table(data = datos_table_observaciones,colWidths=(1.6*inch), rowHeights=(
                0.39*inch, 0.30*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                0.3*inch, 0.3*inch, 0.5*inch),
                style = style_observacion ,
                hAlign='LEFT'
                )

            if Activate_photo=='True':
                
                datos_header = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'], ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'],''),
                    )
                tabla_head = LongTable(data = datos_header,colWidths=(2.68*inch,1.6*inch,1.*inch),
                    style = [
                            ('GRID',(0,0),(2,4),0.5,colors.grey),
                            
                            ('SPAN',(1,0),(2,0)),
                            ('SPAN',(1,1),(2,1)),
                            ('SPAN',(1,2),(2,2)),
                            ('SPAN',(1,3),(2,3)),
                            ('SPAN',(1,4),(2,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (2, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                datos_table_2 = (
                    (tabla_head,'','',imagen_avatar),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.*inch,1.6*inch),
                    style = [
                            
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            ('ALIGN', (1,0),(3,0), "RIGHT"), 
                            ('VALIGN', (1,0),(3,0), "MIDDLE"),
                            ('LEFTPADDING',(0,0),(0,0), 0),
                            ('RIGHTPADDING',(0,0),(0,0), 0),
                            ('BOTTOMPADDING',(0,0),(0,0), 0),
                            ('TOPPADDING',(0,0),(0,0), 0),                     

                            ('TOPPADDING',(-5, -1),(-5,-1), 0),
                            
                            ('LEFTPADDING',(-4,-1),(-4,-1), 0),
                            ('RIGHTPADDING',(-4,-1),(-4,-1), 0),
                            ('BOTTOMPADDING',(-4,-1),(-4,-1), 0),
                            ('TOPPADDING',(-4,-1),(-4,-1), 0),

                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2, -1),(-2, -1), 0),
                            ('RIGHTPADDING',(-2, -1),(-2, -1), 0),
                            ('BOTTOMPADDING',(-2, -1),(-2, -1), 0),
                            ('TOPPADDING',(-2, -1),(-2, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            elif Activate_photo=='False':
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                    ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                    (table_aspectos, table_datos_boolean, table_observaciones, ''),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                    style = [
                            ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                            ('SPAN',(1,0),(3,0)),
                            ('SPAN',(1,1),(3,1)),
                            ('SPAN',(1,2),(3,2)),
                            ('SPAN',(1,3),(3,3)),
                            ('SPAN',(1,4),(3,4)),
                            #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                            ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                            #('ALIGN', (1,3),(5,4), "CENTER"),
                            # ('ALIGN', (1,3),(5,4), "CENTER"), 
                            # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                            

                            ('LEFTPADDING',(0,5),(0,5), 0),
                            ('RIGHTPADDING',(0,5),(0,5), 0),
                            ('BOTTOMPADDING',(0,5),(0,5), 0),
                            ('TOPPADDING',(0,5),(0,5), 0),
                            ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                            ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                            
                            ('TOPPADDING',(-4, -1),(-4,-1), 0),
                            
                            ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                            ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                            ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                            ('TOPPADDING',(-3,-1),(-3,-1), 0),

                            ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                            ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                            ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                            ('TOPPADDING',(-2,-1),(-2,-1), 0),

                            ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                            ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                            ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                            ('TOPPADDING',(-1, -1),(-1, -1), 0)

                            #'SPAN',(0,7),(3,7)),
                            #('BACKGROUND', (0, 7), (3, 7), custom_color),
                            ],
                    hAlign='LEFT'
                    ,splitByRow=True
                    ,repeatRows=True
                            )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
                
            contents.append(tabla)
            datos_tabla_comentarios = [
                    [Paragraph('Comentarios Adicionales:', ParagraphStyle('Heading',fontSize=12))],
                    [Paragraph(inspection['comentarios_adicionales'], bodyStyle)]
                ] 
           
            table_comentarios = Table(data = datos_tabla_comentarios)
            qr_code_data = [
                    [qr_code_image, table_comentarios],
                    
                    #["Escanee el código QR"],
                    ]

            table_qr = Table(data = qr_code_data,colWidths=(1.5*inch, 5.98*inch),
                    style = [
                            ('GRID',(0,0),(1,1),0.5,colors.grey),
                            ('TOPPADDING',(0, 0),(1, 0), 4),
                            ('VALIGN', (0, 0), (1, 0), "TOP"),                     
                            ],
                    hAlign='LEFT'
                    ,repeatRows=1
                    )

            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_aspectos, table_imagenes, ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        

                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            
            contents.append(tabla)
            contents.append(FrameBreak())
            contents.append(logoleft)
            datos_table_2 = (

                ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                ("FECHA INSPECCIÓN: ",inspection['fecha_inspeccion'],''),
                ("RESPONSABLE DE LA INSPECCIÓN: ",inspection['first_name']+" "+ inspection['last_name'], ''),
                (table_qr, '', ''),
                )
            
            custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
            tabla = LongTable(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
                style = [
                        ('GRID',(0,0),(-1,-2),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        ('SPAN',(1,3),(3,3)),
                        ('SPAN',(1,4),(3,4)),
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                 hAlign='LEFT'
                ,splitByRow=True
                ,repeatRows=True
                        )
            tabla.alignment = TA_JUSTIFY

            styleH_2.fontSize=11
            styleH_2.alignment=TA_CENTER
            styleH_2.leading = 11
            styleH_2.fontName = "Times-Roman"
            
            #setFont('Helvetica', 10)
        
            #contents.append(tabla)
            contents.append(tabla)
            #contents.append(table_qr)

            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())


            doc.addPageTemplates([firstpage, laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)
        
        elif flag=='0':
            
            qr_path = equip_info[0]['codigo_qr']
        
            qr_code_image = Image(settings.MEDIA_ROOT+qr_path, width=50, height=50)
            inspection_info = list(self.chunks(inspection_info, 3))
            #print("Esta es", inspection_info)
            
            #print(inspection_info)
            index = 0 
            
            
            
                
            while (True):
                


                if index > (len(inspection_info)-1):
                    break
                contents.append(logoleft)
                contents.append(FrameBreak())
                group_inspections = []
                
                inspection = inspection_info[index]
                
                count = 0 
                fecha_inspecciones = ["FECHA INSPECCIÓN: "]
                responsables = ["RESPONSABLE DE LA INSPECCIÓN: "]
                
                while (True):
                    
                    
                    if ((count > 2) or (count > len(inspection)-1)):

                        break
                    
                    merged_all = inspection[count].copy()
                    
                    
                    keys_to_remove = ["fecha_inspeccion", "first_name",  'last_name','proxima_inspeccion', 'veredicto']

                    for key in keys_to_remove:

                        merged_all.pop(key)

                    
                    datos_table_boolean = [
                        ('SI','NO')
                        ]
                    
                    for  key in merged_all:
                        
                        value = merged_all[key]
                        
                        if value:

                            datos_table_boolean.append(('X',''))
                        
                        else: 
                            
                            datos_table_boolean.append(('','X'))
                    
                    if inspection[count]['veredicto']:

                        datos_veredicto_fecha = (
                            ('X', Paragraph("Apto y puede continuar",style_small)),
                            ('', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            # inspection_info['proxima_inspeccion']
                            )
                    else:

                        datos_veredicto_fecha = (
                            ('', Paragraph("Apto y puede continuar",style_small)),
                            ('X', Paragraph("No apto y debe ser retirado",style_small)),
                            (inspection[count]['proxima_inspeccion'], ''),
                            )
                    #print("VEREDICTO",inspection[count]['veredicto'] )


                    table_veredicto_fecha = Table(data = datos_veredicto_fecha,colWidths=(0.3*inch, 1.3*inch), rowHeights=(0.17*inch),
                                style = [
                                        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
                                        
                                        ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                        
                                        #('BOX',(0,0),(-1,-1),2,colors.black), 
                                        # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        ('SPAN',(-2,-1),(-1,-1)),
                                        # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                        # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                        #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                        # ('LEFTPADDING',(0,0),(-1,-1), 0),
                                        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                        # ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                        # ('TOPPADDING',(0,0),(-1,-1), 0),
                                                                
                                        ],
                                hAlign='LEFT'
                                )
                    datos_table_boolean.append((table_veredicto_fecha, ''))

                    table_datos_boolean = Table(data = datos_table_boolean,colWidths=(0.8*inch), rowHeights=(
                        0.39*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                        0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch,
                        0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 0.3*inch, 
                        0.3*inch, 0.3*inch, 0.5*inch),
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                ('ALIGN', (0, 0), (-1, -1), "CENTER"), 
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                
                                #('BOX',(0,0),(-1,-1),2,colors.black), 
                                # ('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('SPAN',(-2,-1),(-1,-1)),
                                # ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 8, 8),
                                # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold', 10, 10),
                                # ('ALIGN', (0, 1), (0, 1), "CENTER"), 
                                #('ALIGN', (0, 0), (-1, -1), "LEFT"),
                                ('LEFTPADDING',(0,0),(-1,-1), 0),
                                ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                                ('TOPPADDING',(0,0),(-1,-1), 0),
                                # # ('GRID',(-2,-2),(-1,-2),2,colors.blue),
                                # ('GRID',(0,0),(-2,-1),2,colors.blue),                          
                                ],
                        hAlign='LEFT'
                        )

                    group_inspections.append(table_datos_boolean)

                    fecha_inspecciones.append(inspection[count]['fecha_inspeccion'])

                    responsables.append(
                        inspection[count]['first_name']+
                        " "+
                        inspection[count]['last_name'])
                    count += 1
                
                if not (len(group_inspections)%3 ==0):
                
                        while(True):
                            group_inspections.append('')
                            if (len(group_inspections)% 3 ==0):
                                break
                    
                    
                print("FINAAAAL", equip_info[0])
                datos_table_2 = (

                    ('FECHA DE FABRICACIÓN DEL EPI:', equip_info[0]['fecha_fabricacion'],'', ''),
                    ('NUMERO DE PRODUCTO:',  equip_info[0]['numero_producto'].zfill(7),'', ''),
                    ('CÓDIGO INTERNO:',  equip_info[0]['codigo_interno'],'', ''),
                    fecha_inspecciones,
                    responsables,
                    (table_aspectos, group_inspections[0], group_inspections[1], group_inspections[2]),
                    )
                
                custom_color =colors.Color(red=(72.0/255),green=(217.0/255),blue=(134.0/255))
                tabla = Table(data = datos_table_2,colWidths=(2.68*inch,1.6*inch,1.6*inch,1.6*inch),
            
                style = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                        ('SPAN',(1,0),(3,0)),
                        ('SPAN',(1,1),(3,1)),
                        ('SPAN',(1,2),(3,2)),
                        
                        #('BACKGROUND', (0, 0), (-1, 0), custom_color), 
                        ('ALIGN', (1, 0), (3, 4), 'CENTER'),
                        #('ALIGN', (1,3),(5,4), "CENTER"),
                        # ('ALIGN', (1,3),(5,4), "CENTER"), 
                        # ('VALIGN', (1,3),(5,4), "MIDDLE"),
                        ('LEFTPADDING',(0,5),(0,5), 0),
                        ('RIGHTPADDING',(0,5),(0,5), 0),
                        ('BOTTOMPADDING',(0,5),(0,5), 0),
                        ('TOPPADDING',(0,5),(0,5), 0),
                        ('FONT', (0, 0), (0, 2), 'Helvetica-Bold', 9, 9),
                        ('FONT', (0, 2), (0, 4), 'Helvetica', 9, 9),
                        
                        ('TOPPADDING',(-4, -1),(-4,-1), 0),
                        
                        ('LEFTPADDING',(-3,-1),(-3,-1), 0),
                        ('RIGHTPADDING',(-3,-1),(-3,-1), 0),
                        ('BOTTOMPADDING',(-3,-1),(-3,-1), 0),
                        ('TOPPADDING',(-3,-1),(-3,-1), 0),

                        ('LEFTPADDING',(-2,-1),(-2,-1), 0),
                        ('RIGHTPADDING',(-2,-1),(-2,-1), 0),
                        ('BOTTOMPADDING',(-2,-1),(-2,-1), 0),
                        ('TOPPADDING',(-2,-1),(-2,-1), 0),

                        ('LEFTPADDING',(-1, -1),(-1, -1), 0),
                        ('RIGHTPADDING',(-1, -1),(-1, -1), 0),
                        ('BOTTOMPADDING',(-1, -1),(-1, -1), 0),
                        ('TOPPADDING',(-1, -1),(-1, -1), 0)

                        #'SPAN',(0,7),(3,7)),
                        #('BACKGROUND', (0, 7), (3, 7), custom_color),
                        ],
                hAlign='LEFT'
                        )
                tabla.alignment = TA_JUSTIFY

                styleH_2.fontSize=11
                styleH_2.alignment=TA_CENTER
                styleH_2.leading = 11
                styleH_2.fontName = "Times-Roman"
                
                #setFont('Helvetica', 10)
            
                #contents.append(tabla)
                
                contents.append(tabla)
                qr_code_data = [
                    [qr_code_image],
                    #["Escanee el código QR"],
                    ]

                table_qr = Table(data = qr_code_data,
                        style = [
                                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                                
                                
                                                       
                                ],
                        hAlign='LEFT'
                        )

                contents.append(table_qr)
                index += 1
                

            
            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())

            # contents.append(NextPageTemplate('laterpages'))
            # contents.append(PageBreak())

            doc.addPageTemplates([firstpage,laterpages])
            #doc.addPageTemplates([PageTemplate(frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2]), ])
            #doc.addPageTemplates([PageTemplate(id='OneCol',frames=Top,onPage=foot1),PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2)])

            doc.build(contents)
