# EPI APP
# Descripción del Problema
Todo equipo de protección para alturas, debe ser sometido a inspecciones periódicas para comprobar el correcto funcionamiento de este, además verificar que su estado sea apto para el trabajo en alturas a realizar. Dado que fallas en el equipo pueden desencadenar una serie de accidentes que afectan la integridad de los usuarios de la empresa EPI en búsqueda de tener una trazabilidad de sus equipos producidos, tenía como proyecto planteado un aplicativo web para registrar las inspecciones realizadas por el personal calificado. En la empresa no se tenía ninguna plataforma digital para almacenar esta información pues todas las inspecciones realizadas se encuentran en formato físico por lo cual son propensas a perderse o deteriorarse con el tiempo, además el acceso a esta información es tedioso y difícil de manejar. Por ese motivo, se planteó la posibilidad de desarrollar un aplicativo web que permita el ingreso de las inspecciones realizadas y además sea posible acceder y visualizar las hojas de vida de los equipos de forma sencilla mediante la captura de un código QR situado en el equipo.

# Descripción de la solución:
En primer lugar, se diseñó el aplicativo utilizando la metodología de desarrollo de software RUP la cual define buenas prácticas de programación y permite que el código sea escalable y reutilizable. Además, se empleó la modelo vista controlador, que es una excelente practica pues permite estructuras sistemas robustos de forma clara y eficiente, pensando en que los sistemas sean escalables y que en el futuro necesitaran mantenimiento.
![alt text](https://espifreelancer.com/images/stack_Django_mtv.webp)*Modelo vista controlador (MVC) Django.*

Django es un framework de desarrollo web open-source, basado en el modelo MVC e implementado en python. Este framework fue seleccionado por su versatilidad pues es extremadamente escalable, lo hace de una forma rápida y flexible. Además, que provee un sistema de seguridad bastante robusto que ayuda a evitar muchos errores de seguridad comunes. Se selecciono MySQL como gestor de bases de datos, pues puede manejar grandes volúmenes de datos, el diagrama de identidad relación creado para el proyecto se muestra en la siguiente figura:

La base datos se estructuro de tal forma que fuese escalable para todos los equipos, dado que por cuestiones de tiempo únicamente se crearon las entidades correspondientes a los arneses. Pues cada equipo tiene su formato particular con diferentes campos, (cascos, líneas de vida, etc.) y la creación de muchas tablas viola principios de buenas prácticas de programación puesto que la introducción de nuevas características o información debe ser paulatina para proporcionar una facilidad al momento de corregir errores y estructurar el sistema. Sin embargo, el ingreso de nuevas tablas no presenta gran dificultad pues la base de datos se diseñó de forma que fuese escalable. Para cumplir con los requerimientos establecidos se utilizó múltiples herramientas software. Entre estas Javascript, html y css utilizadas para darle forma y dinamismo a las diferentes páginas del aplicativo. Sumado a ello se utilizó Bootsrap el cual es una librería que emplea las tres herramientas anteriormente mencionadas y permite lograr un aplicativo con diseño responsivo, es decir adaptable a cualquier dispositivo. A continuación, se presentan los cambios realizados desde la ultima versión.

# EPI-APP Actualizaciones realizadas por Juan Carlos Noguera Ramirez-UPDATE 01/26/2022
1. Tabs de navegación para el perfil del inspector con crispy_forms en forms.py.
2. Extensión de inspecciones a otros productos EPI.
3. Consulta de inspectores registrados en la plataforma EPI. Obteniendo foto de perfil, si esta “Habilitado” como inspector, nombre completo, correo electrónico, código de inspector y empresa de trabajo.
4. Recuperación de contraseñas usando el correo electrónico registrado en la base de datos de la aplicación.
5. Validación de username de la tabla CustomUser para que valide solo para valores numéricos de 10 dígitos cuando sea registrado por el administrados para que dicho campo sea la cédula de ciudadanía del inspector.

## Actualizaciones del perfil de inspector
1. Tabholder por medio de crispy_forms para dividir la interfaz en tres apartados "Registro de inspecciones", "Certificado de inspección" y "Configuración". El Orden antes era "Certificado de inspección", "Registro de inspecciones" y "Configuración" se cambio por facilidad de trabajo.
2. En el tab de "Certificado de inspección" muestra el archivo PDF sin cambiar de pagina estando indexado en tamaño "700"x"600". Falta por implementar la configuración en el servidor NGINX para que solo puede ser visto por el usuario logeado. Se añade links investigados para este proceso https://b0uh.github.io/protect-django-media-files-per-user-basis-with-nginx.html https://medium.com/analytics-vidhya/dajngo-with-nginx-gunicorn-aaf8431dc9e0 https://www.digitalocean.com/community/tutorials/como-configurar-django-con-postgres-nginx-y-gunicorn-en-ubuntu-18-04-es https://realpython.com/django-nginx-gunicorn/ https://wellfire.co/learn/nginx-django-x-accel-redirects/ https://pavanskipo.medium.com/how-to-serve-protected-content-using-x-accel-nginx-django-fd529e428531 https://github.com/cobusc/django-protected-media/blob/master/example/demo/settings.py http://jike.in/?qa=722548/python-serve-protected-media-files-with-django.
3. En la pestaña "Configuración", se puede actualizar en el lado cliente los datos del número de teléfono, empresa donde trabaja el inspector, foto de perfil y contraseña. Por medio de los ButtonHolder del paquete crispy_forms el forms.py renderiza los botones HTML con sus interacciones. En models.py esta el modelo de la base de datos y la tabla para esta parte de la APP es Inspectores, que tiene una relación uno a uno con la tabla custom de usuarios.
4. La APP ahora render en una tabla en boostraps 4 las ultimas entradas de inspecciones realizada por el usuario inspector registrado y habilitado, aplicando el concepto de pagination, para no imprimir todo en una sola tabla de longitud extensa. https://www.youtube.com/watch?v=wY_BNsxCEi4 https://docs.djangoproject.com/en/4.0/topics/pagination/ https://getbootstrap.com/docs/5.1/content/tables/.

## Actualizaciones extensión a otros productos EPI
1. Se extiende la base de datos añadiendo los modelos "accesorios_metalico", "cascos", "eslingas", "lineas_anclajes" y "sillas_perchas";, teniendo para cada uno un modelo para registrar los datos obtenidos del formulario de las inspecciones, las referencias del equipo y la información de fabrica de los equipos (provisionalmente sea estado trabajando como que el código de lote, se maneja por separado por cada equipo, falta definir si el lote es único por todos los equipos en EPI, si es así los diferentes modelos Django se reduce a uno solo).
2. Se realizan los formularios para cada equipo teniendo encuentra las particularidades que se tienen por equipo de la marca EPI.
3. El administrador puede registrar las referencias de los equipos y la información de fabricación de los demás equipos EPI (Lo mismo del literal 1, hasta no conocer como funciona el numero de lote la APP esta funcionando como si por equipo se tiene un código interno).

## Actualizaciones consulta de inspectores registrados en la plataforma EPI.
1. Se puede consultar como invitado (en este modo la plataforma muestra en el menú lateral herramientas que no tienen los invitados, y al hacer click en dichas herramientas es llevado a la pagina de Login, no pasa nada grave de seguridad pero altera la disposición de la pagina) o usuario registrado en la plataforma la foto de perfil del inspector, si esta “Habilitado” como inspector, nombre completo, correo electrónico, código de inspector y empresa de trabajo.

## Actualizaciones recuperación de contraseñas usando el correo electrónico registrado en la base de datos de la aplicación.
1. Se añade la herramienta de recuperación de contraseñas si es olvidada por el inspector por medio del correo electrónico que tenga registrado en la base de datos de la plataforma. La explicación del proceso esta en https://www.youtube.com/watch?v=JBhpo0o1Ajg https://dev.to/yahaya_hk/password-reset-views-in-django-2gf2. (Lo siguiente es personalizar el correo con los logotipos y firmas de la empresa EPI y configurar para cuando la APP sea puesta en producción/deploy).

# EPI-APP Actualizaciones realizadas por Juan Carlos Noguera Ramirez-UPDATE 01/29/2022
1. Ahora el certificado solo puede ser visto por el usuario asociado al mismo por medio de logica en Django en el archivo view.py y la configuración del servidor NGINX; en la carpeta "DeployGunicorn-NGINX" esta el archivo junto los archivos de configuración del servidor Gunicorn para realizar el proceso de Deploy. 

## Actualización seguridad del certificado
En el archivo view.py se realizo un query para acceder al path del certificado en la DB en el modelo de inspectores, se comparo con la variable pasada por medio de la url configurada en el archivo urls.py y se determina un booleano para saber si el usuario tiene acceso, los admin siempre tienen permisos; sino tiene permiso se indica con un mensaje para determinar que no puede acceder al archivo protegido y si el usuario tiene permiso se pasa de los objetos Python a sockets por el servidor Gunicorn y NGINX toma el socket y envia las cabeceras HTTPS a los navegadores, extendiendo el modelo MVC de Django.
![alt text](https://miro.medium.com/max/700/1*rYdZRYct2FKHiGxlJIvORg.png)*Request Flow.*

![alt text](https://files.realpython.com/media/Deploy-a-Django-App-With-Nginx--Gunicorn--HTTPS_Watermarked.8e99fe72a502.jpeg)*Esquema Django-App, Nginx, Gunicorn, HTTPS.*

Los archivos de configuración de NGINX debe de cambiarse el path para que apunte al proyecto Django. Se extiende que solo esten restringido por usuarios los archivos que tengan la url con "protected" si no tiene url con esa extensión se puede acceder al MEDIA FILE por todos los usuarios.

# EPI-APP Actualizaciones realizadas por Juan Carlos Noguera Ramirez-UPDATE 14/03/2022
1. La aplicación obtiene la imagen de la foto del inspector y la pone en el documento pdf de la inspección Arnes.
2. La aplicación almacena las inspecciones en disco junto el path de la misma en el DB para Arnes.
3. La aplicación permite acceder y visualizar los pdf por medio de la interacción de botones de los documentos de inspección almacenados en el DB para Arnes.
# EPI-APP Actualizaciones realizadas por Juan Carlos Noguera Ramirez-UPDATE 23/03/2022
1. Se extiende a los demás productos EPI lo desarrollado en la actualización 14/03/2022.
# EPI-APP Actualizaciones realizadas por Juan Carlos Noguera Ramirez-UPDATE 08/04/2022
1. Se regresa a que la inspección ya no se almacena en disco sino que siempre que se genere el reporte se consume recursos de CPU y RAM.
# EPI-APP Actualizaciones realizadas por Juan Carlos Noguera Ramirez-UPDATE 13/04/2022
1. Genera el certificado y el carnet después de guardar los datos de inspector.
