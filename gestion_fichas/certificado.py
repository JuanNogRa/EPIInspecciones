
# from reportlab.pdfgen import canvas
 
# c = canvas.Canvas("fileName.pdf")
# c.drawString(100,750,"This is my first PDF file in Reportlab!")
# c.save()



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import B4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

pdfmetrics.registerFont(TTFont('Monotype Corsiva', 'staticfiles/gestion_fichas/fonts/MTCORSVA.TTF'))
pdfmetrics.registerFont(TTFont('Amiri', 'staticfiles/gestion_fichas/fonts/Amiri-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Angsa', 'staticfiles/gestion_fichas/fonts/angsa.ttf'))
pdfmetrics.registerFont(TTFont('MyriadPro Semibold', 'staticfiles/gestion_fichas/fonts/MyriadPro-Semibold.ttf'))
pdfmetrics.registerFont(TTFont('MyriadPro Regular', 'staticfiles/gestion_fichas/fonts/MyriadPro-Regular.ttf'))
pdfmetrics.registerFont(TTFont('ArialMT', 'staticfiles/gestion_fichas/fonts/ARIALMT.ttf'))
class Certificado:
	def foot2(self,pdf,doc):
		width,height = B4
		pdf.saveState()
		pdf.setFont('Times-Roman',9)
		if self.flagShape=='0':
			pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
		elif self.flagShape=='1':
			pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
	
	def chunks(self, lst, n):
		for i in range(0, len(lst), n):
			yield lst[i:i + n]
	
	def get_doc(self, pdf, buffer, inspector):
		name=str(inspector.user.first_name)+' '+str(inspector.user.last_name)
		cedula=int(str(inspector.user))
		ciudad=str(inspector.ciudad.ciudad)
		lugar=str(inspector.lugar)
		fecha=inspector.fecha
		codigo=str(inspector.ciudad.codigo)

		c = canvas.Canvas(buffer, pagesize=B4, bottomup=1)
	# Add image border template`
		image_path = 'staticfiles/gestion_fichas/img/background.png'
		c.drawImage(image_path, 0, 0, width=250*mm, height=353*mm)

		# Body Text
		c.setFont("Monotype Corsiva", 20, leading=None)
		c.drawCentredString(250*mm/2, 353*mm-122.198*mm, 'En cumplimiento de la resolución 4272 de 2021')
		c.drawCentredString(250*mm/2, 353*mm-130.665*mm, 'título IV, capítulo I, artículo 61, punto G.')

		# Participant Name Text
		c.setFont("Amiri", 25, leading=None)
		c.drawCentredString(250*mm/2, 353*mm-162.850*mm, name.upper())

		# More body Text ...
		c.setFont("Angsa", 22, leading=None)
		c.drawCentredString(250*mm/2, 353*mm-180.762*mm, 'con documento de identidad '+f"{cedula:,}".replace(',', '.'))
		c.drawCentredString(250*mm/2, 353*mm-(180.762+8.467)*mm, 'cursó y aprobó la acción de formación de:')

		# More body Text
		c.setFont("Angsa", 22, leading=None)
		c.drawCentredString(250*mm/2, 353*mm-240.777*mm, 'en la ciudad de '+ciudad+',')
		c.drawCentredString(250*mm/2, 353*mm-(240.777+9)*mm, 'en el '+lugar)
		c.drawCentredString(250*mm/2, 353*mm-(240.777+18)*mm, 'El día '+fecha.strftime('%d de %B del %Y'))
		c.drawCentredString(250*mm/2, 353*mm-(240.777+35)*mm, 'Con duración de 8 horas.')

		c.setFont("Angsa", 20, leading=None)
		c.drawCentredString(250*mm*.315, 353*mm-308.7*mm, 'GERENTE GENERAL DE E.P.I SAS')
		c.setFont("Angsa", 20, leading=None)
		c.drawCentredString(250*mm*.75, 353*mm-300.7*mm, codigo+'-'+str(cedula)+'-'+fecha.strftime('%m%y'))
		c.setFont("Angsa", 18, leading=None)
		c.drawCentredString(250*mm*.75, 353*mm-305.7*mm, 'Número de Registro')

		c.showPage()
		c.save()

class Carnet:
	def foot2(self,pdf,doc):
		width,height = B4
		pdf.saveState()
		pdf.setFont('Times-Roman',9)
		if self.flagShape=='0':
			pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 1)
		elif self.flagShape=='1':
			pdf.drawString(width-1*inch, 0.1 * inch,'Página '+"%d" % doc.page+' de '+"%d" % 3)
	
	def chunks(self, lst, n):
		for i in range(0, len(lst), n):
			yield lst[i:i + n]
	
	def get_doc(self, pdf, buffer, inspector):
		name=str(inspector.user.first_name)+' '+str(inspector.user.last_name)
		cedula=int(str(inspector.user))
		fecha=inspector.fecha
		codigo=str(inspector.ciudad.codigo)

		c = canvas.Canvas(buffer, pagesize=letter, bottomup=1)
		# Add image border template`
		image_path = 'staticfiles/gestion_fichas/img/background_carnet.png'
		c.drawImage(image_path, 0, 0, width=215.89999*mm, height=279.39999*mm)

		# Body Text
		c.setFont("MyriadPro Semibold",10, leading=None)
		c.drawCentredString(20.703*mm*2.5, 279.39999*mm-36.011*mm*1.5, name.upper())
		c.drawCentredString(20.703*mm*2.5, 279.39999*mm-36.011*mm*1.5-4*mm, "CC "+f"{cedula:,}".replace(',', '.'))
		
		
		c.setFont("ArialMT", 7, leading=None)
		
		c.setFillColorRGB(255, 255, 255)
		c.drawCentredString(78.940*mm*1.85, 279.39999*mm-55.728*mm*1.51, 'Teléfonos: (602) 5245331 - 4415331 Cali, Colombia      www.episafety.com')
		
		c.setFont("MyriadPro Regular",8, leading=None)
		c.setFillColorRGB(0, 0, 0)
		c.rotate(90)
		c.drawCentredString((279.39999*mm-44.852*mm*1.7), -66.208*mm*1.3, fecha.strftime('%d/%m/%Y'))
		
		c.setFont("MyriadPro Regular",10, leading=None)
		c.setFillColorRGB(0, 0, 0)
		c.drawCentredString((279.39999*mm-42*mm*1.6), -66.208*mm*1.35, codigo+'-'+str(cedula)+'-'+fecha.strftime('%m%y'))

		c.showPage()
		c.save()