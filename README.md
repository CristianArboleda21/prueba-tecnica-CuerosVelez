Configuración del proyecto.

Entorno virtual

El entorno virtual nos permite tener paquetes y librerías instaladas en un entorno separado a los paquetes y librerías del sistema global, generando su propio interprete y así trabajar en diferentes proyectos con dependencias distintas y que no interfieren entre si.

- Instalar entorno virtual en el computador:
    - Windows: `pip install pipenv`
    - Mac: `brew install pipenv`
- Dentro de la carpeta de prueba-tecnica, luego de clonar el proyecto debe iniciar el entorno virtual en la consola:
    - Comando: pipenv shell
- Instalar librerías y paquetes necesarios en el entorno virtual:
    - pipenv install

Luego de instalar los paquetes y las librerías, debe seleccionar como interprete del editor de código el entorno virtual que creo.

A continuación verán un ejemplo de como seleccionar un interprete en Visual Studio Code:

- El primer paso es ir a la parte de arriba de editor de código y buscar la opción “view” o “ver” en caso de que este en español.
- Cuando este en el panel de “view” buscaras la opción de “command palette” en español “paleta de comandos”.
- Luego de escoger la opción de “command palette” se abrirá un pequeño menú, en el cual pondremos los siguiente:
    - “Python: select interpreter” en español “Python: seleccionar intérprete”
- Después de darle a Python: select interpreter se abrirá un nuevo menú, donde estarán los diferentes entornos virtuales que hemos creado además de la versión de Python instalada en el equipo, este seria el entorno global
    - Cada entorno virtual aparece de la siguiente manera:
        - Python 3.12 → Siendo “3.12” la versión que se tiene descargada de Python en el computador
        - ({nombre proyecto}-DAdxjyGrT: Pipenv) → Primero aparece el nombre de la carpeta donde esta el proyecto, luego un identificador que se crea automáticamente (DAdxjyGrT) y por ultimo la biblioteca que uso para crear el entorno virtual (Pipenv)
        - Entonces se vería así: “Python 3.12 ({nombre proyecto}-DAdxjyGrT: Pipenv)”

Crear archivo secreto (.env):

- Variables necesarias para las credenciales de VTEX
    - TOKEN=” ” (Token de acceso necesario para obtener información de la API de Vtex)
    - ACCOUNT_NAME=” ” (Nombre que ira en el dominio de la URL de la API)
    - URL_ORDERS=” ” (URL para obtener todas las ordenes)
    - URL_ORDER=” ” (URL para obtener una orden en especifico)
- Variables necesarias para la base de datos
    - POSTGRESQL_NAME=” ” (Nombre de la base de datos)
    - POSTGRESQL_USER=” ” (Nombre del usuario con acceso a la base de datos)
    - POSTGRESQL_PASS=” “ (Contraseña de acceso a la base de datos)
    - POSTGRESQL_HOST=”” (Host en el que se alojara la base de datos)
    - POSTGRESQL_NAME=5432 (Puerto donde esta ejecutándose la base de datos)
    - DEBUG=True

Instrucciones de ejecución

Luego de la configuración del proyecto se deben seguir las siguientes instrucciones para ejecutarlo:

- Activar el entorno virtual en la consola dentro de la carpeta del proyecto, ejecutando el siguiente comando: pipenv shell
- Crear las migraciones a la base de datos, ejecutando los siguientes comandos:
    - Debe dirigirse en la terminal a la carpeta de contenga el archivo manage.py, luego ejecuta:
        - python [manage.py](http://manage.py) makemigrations api
        - python [manage.py](http://manage.py) migrate
    - Luego debe ejecutar el comando que leerá la información de la API de Vtex, para ello ya debes tener las variables de entorno necesarias para el API de Vtex (TOKEN, URL_ORDERS, URL_ORDER) configuradas y tener acceso a la API:
        - python [manage.py](http://manage.py) import_orders → Este comando obtiene la información del API y la guardara en la base de datos con campos más importantes

Antes de poner a correr el servidor y que todo este listo para que funcione nuestro BackEnd, debemos tener nuestro FrontEnd para ver como se muestran los datos que el BackEnd nos proporciona, para ellos hacemos lo siguiente:

- Accedemos por consola a la carpeta llamada “front-end”:
    - cd … → hasta llegar a la carpeta
- Luego, estando en front-end vamos a la carpeta llamada “pages”
    - cd pages
- Estando en pages, ejecutamos el siguiente comando:
    - start index.html → Abrirá el navegador con la pagina inicial del proyecto
    

Después de seguir estos pasos, todo esta listo para pueda ejecutar el proyecto sin problemas, para correr el servidor, seguimos los siguientes pasos:

- Regresamos a la carpeta que contiene el manage.py
    - cd .. → Así hasta volver a la carpeta “prueba_tecnica”
- Luego lanzamos el siguiente comando:
    - python [manage.py](http://manage.py) runserver
    

Con esto ya nuestro BackEnd esta corriendo, por lo tanto podemos empezar a navegar en el FrontEnd y ver como pinta los datos obtenidos por el servidor

Decisiones técnicas:

- Se usa Python con apoyo del framework (Django Rest Framework) para desarrollar el BackEnd de la API y para consumir las URLs de Vtex, ya que este facilita el análisis de datos con sus librerías especializadas para esta área y que para el desarrollo de la API era fundamental tener un proceso claro de como se obtiene la información proporcionada
- Utilizamos Panda, una librería de Python que nos permite analizar la base de datos y agrupar en tablas la información necesaria para cumplir con los escenarios planteados
- Para graficar usamos matplotlib, una librería de Python que nos permite graficar los datos provenientes de las información que obtuvimos mediante Panda
- Como motor de base de datos se usa PostgreSQL, nos brinda tipos de datos avanzados, tiene JSON indexado lo que permite que sean más rápidas las consultas, brindando ventaja en cuanto a que el análisis de datos sea mas eficiente
- La intencionalidad es mostrar el funcionamiento de la API, por lo tanto para la visualización de los datos se uso HTML, JavaScript y CSS básico

Ejemplos uso de la API:

Endpoints para el API de Vtex:

- Obtener todas las ordenes: Este endpoint devolverá una lista con todas las ordenes facturadas en enero del 2024:
    - http://localhost/api/orders
- Obtener una orden especifica: Este endpoint nos permitirá ver una orden especifica con toda su información
    - http://localhost/api/orders/{orderId}

Endpoints para el API Datos almacenados:

- Obtener los movimientos: Este endpoint devolverá una lista con todas las ordenes facturadas en enero del 2024, además de contar con un filtro por fechas de las ordenes:
    - Recibe dos parametros de busqueda:
        - start_date: Se envía una fecha en formato (YY-mm-dd) y seria la fecha para traer las ordenes que se hicieron a partir de esa fecha en adelante
        - end_date: Se envía una fecha en formato (YY-mm-dd) y seria la fecha para traer las ordenes que se hicieron hasta esa fecha
        
        Los parámetros de búsqueda no son obligatorios, se pueden enviar vacíos o no enviarlos, igual el endpoint te va a responder con todos los movimientos, sin hacer ningún tipo de filtro
        
        - Con parámetros de búsqueda:
            - http://127.0.0.1:8000/api/orders/movements?start_date=2024-01-25&end_date=2024-01-31
                         
            ![movimientos_con_param](https://github.com/user-attachments/assets/b9c4f43b-93f0-4306-9ec1-6cd2c9de821e)
            
            - Resultado:
              
                ![resul_movimientos_con_param](https://github.com/user-attachments/assets/86357fd1-b5cd-4558-a614-b11710d6a9c5)                
            
        - Sin parámetros de búsqueda:
            - http://127.0.0.1:8000/api/orders/movements
              
            ![movimientos_sin_param](https://github.com/user-attachments/assets/d4983eee-f7c6-4947-ba0e-3b3cb6f346a1)
            
            - Resultado:
              
                ![resul_movimientos_sin_param](https://github.com/user-attachments/assets/eb12cc6a-d940-4cf6-9a53-28a96b886053)                

            
- Obtener el detalle de una orden especifica: Este endpoint nos permitirá ver el detalle de una orden especifica con toda su información, por ejemplo: el id de la orden (id que se crea en la base de datos), orderId (id de la orden), fecha, destino, origen y sus productos
    - En la URL solo debemos el enviar el id de la orden que queremos ver el detalle, lo hacemos de la siguiente manera:
        - http://127.0.0.1:8000/api/orders/{id}/detail_order
          
        ![detalle_orden](https://github.com/user-attachments/assets/027e903a-29b0-4b61-ae16-ce2a0d43c4fc)
        
    - Resultado:
      
        ![resul_deta_orden](https://github.com/user-attachments/assets/055fbc47-45ea-4f61-8b68-fc3a066931a9)        

    
- Análisis de los productos que salen de cada bodega: Este endpoint donde se usa panda nos brinda la información del producto y de cuales bodegas ha sido despachado a diferentes lugares
    - http://127.0.0.1:8000/api/products/specific_products
      
        ![analisis_prod-bode](https://github.com/user-attachments/assets/13111334-b5bc-47b1-a647-14f2f5237f28)
        
    - Resultado:
      
        ![resultado_ana_prod_bod](https://github.com/user-attachments/assets/9579c614-e43d-47f9-9ba9-2ee31f207a31)        

- Grafica análisis de los productos que salen de cada bodega: Creamos este endpoint donde se usa panda y matplotlib, nos genera una grafica con la información de los productos y de cuales bodegas ha sido despachado a diferentes lugares
    - http://127.0.0.1:8000/api/products/specific_products_chart
      
      ![graf_prod_bode](https://github.com/user-attachments/assets/4ed058dc-eef8-4a87-9b3d-338992e8ae3c)
    
    - Resultado:
      
      ![Captura de pantalla 2025-05-25 144110](https://github.com/user-attachments/assets/2b9b18e7-4f7e-4eea-9a2c-f09d8366b6b1)    


- Análisis de las ciudades a las que ha enviado un producto: Este endpoint donde se usa panda nos brinda la información del producto y a cuales ciudades ha sido mandado
    - http://127.0.0.1:8000/api/products/city_destination_products
      
        ![analisis_prod-ciudades](https://github.com/user-attachments/assets/ff24ea53-583e-4d60-9c76-ce9b271c8bc4)
        
    - Resultado:
      
        ![resul_ana_prod_ciudad](https://github.com/user-attachments/assets/f0418ed8-c25b-4bf4-821b-98f0643c329f)

- Grafica análisis de los productos y las ciudades que son enviados: Creamos este endpoint donde se usa panda y matplotlib, nos genera una grafica con la información de los productos y de las ciudades hacia donde los han enviado
    - http://127.0.0.1:8000/api/products/city_destination_products_chart
      
        ![graf_prod_ciudad](https://github.com/user-attachments/assets/cfe0b696-2169-41db-ab6d-e6ceefb748d6)
        
    - Resultado:
      
      ![Captura de pantalla 2025-05-25 144406](https://github.com/user-attachments/assets/c8cf422c-a421-4451-b790-c79c0c32108a)


- Análisis de los almacenes que han hecho envíos a ciudades especificas: Este endpoint donde se usa panda nos brinda la información de los almacenes que han enviado productos a una ciudad
    - http://127.0.0.1:8000/api/warehouses/warehouses_city
      
        ![analisis_bode-ciudades](https://github.com/user-attachments/assets/155240e2-d054-4f07-ae58-9dfcfa2f0f70)
        
    - Resultado:
      
        ![resul_ana_bode_ciudad](https://github.com/user-attachments/assets/54b35748-bed3-4d73-b8f9-d1ee710da63d)
    
- Grafica análisis de los almacenes que han hecho envíos a ciudades especificas: Creamos este endpoint donde se usa panda y matplotlib, nos genera una grafica con la información de las ciudades donde un almacenen de los almacenes ha hecho envíos
    - http://127.0.0.1:8000/api/warehouses/warehouses_city_chart
      
        ![graf_bode_ciudad](https://github.com/user-attachments/assets/c7ad4609-2777-4178-b3e5-4052586c4d0c)
        
    - Resultado:
      
    ![Captura de pantalla 2025-05-25 144708](https://github.com/user-attachments/assets/e3fa49c6-5be4-40a9-aef8-c4f1f83cd4ca)
    

Explicación de las vistas:

- Vista principal:
  
    ![Captura de pantalla 2025-05-25 140016](https://github.com/user-attachments/assets/3f77114b-8446-49fc-8ec1-722738c2c5dd)
    
- Opción “API VTEX”:
  
    ![Captura de pantalla 2025-05-25 140056](https://github.com/user-attachments/assets/1045da1b-c35a-46ef-bbab-9dbac8b6438d)
    
    ![Captura de pantalla 2025-05-25 140112](https://github.com/user-attachments/assets/f8013bac-b095-4ed5-ac38-b291e142f993)

- Opción “API Datos almacenados”:
  
  ![Captura de pantalla 2025-05-25 140156](https://github.com/user-attachments/assets/bcdc774b-9a77-4af3-a040-7b1d41ee1e6b)

  ![Captura de pantalla 2025-05-25 140212](https://github.com/user-attachments/assets/93ea9fe7-abfc-4461-a1df-c30a70924a98)

- Opción “Movimientos”:

  ![Captura de pantalla 2025-05-25 140253](https://github.com/user-attachments/assets/bb4908e9-ac74-48d5-a5de-379d188125a4)

  ![Captura de pantalla 2025-05-25 140308](https://github.com/user-attachments/assets/8114eab7-a8d9-4826-b79c-b14f8d29ad35)

- Si queremos ver los productos de la orden:

  ![Captura de pantalla 2025-05-25 140349](https://github.com/user-attachments/assets/6aace821-8dd6-4ebf-901c-3a01f0679cd7)

  ![Captura de pantalla 2025-05-25 140405](https://github.com/user-attachments/assets/5722df6a-2941-46da-83a8-37d8129612f1)

- Opción “Bodegas”:

  ![Captura de pantalla 2025-05-25 140442](https://github.com/user-attachments/assets/92089bc5-9699-4136-a329-6bd5583d0038)

  ![Captura de pantalla 2025-05-25 140455](https://github.com/user-attachments/assets/c95fb5a1-405a-4c7c-97ca-6bc8d4e50f72)

- Opción “Cargar Datos”

  ![Captura de pantalla 2025-05-25 140537](https://github.com/user-attachments/assets/87ac5633-1f77-4a2b-9295-2b97564bdff3)

- Opción “Ver Gráfica Bodegas por Ciudad”
  
  ![Captura de pantalla 2025-05-25 140622](https://github.com/user-attachments/assets/577b8db6-348d-4de2-a149-d7e7be711a53)

- Opción ”Productos”

  ![Captura de pantalla 2025-05-25 140745](https://github.com/user-attachments/assets/40670f8f-0513-4029-a59b-62988736f750)

  ![Captura de pantalla 2025-05-25 140822](https://github.com/user-attachments/assets/6a344bfa-4590-49f8-8b0b-53237c9a07c3)

- Opción “Productos - Almacenes”

  ![Captura de pantalla 2025-05-25 140838](https://github.com/user-attachments/assets/8df14cdb-5c20-4d2c-92c7-1c92b8b54d3b)

  ![Captura de pantalla 2025-05-25 140909](https://github.com/user-attachments/assets/3c9cf7d6-9dd7-489f-a5a6-5cbdd66fa619)

  ![Captura de pantalla 2025-05-25 141042](https://github.com/user-attachments/assets/6f742cef-2b29-4c3f-93d8-f641ba5a3cf8)

- Opción “Productos - Ciudades”

  ![Captura de pantalla 2025-05-25 141131](https://github.com/user-attachments/assets/b98c650e-995d-4935-9024-525a26bb9e63)

  ![Captura de pantalla 2025-05-25 141144](https://github.com/user-attachments/assets/c22c4254-79be-4a0a-aea2-46164a4c8615)

  ![Captura de pantalla 2025-05-25 141203](https://github.com/user-attachments/assets/58a47790-c94c-48fc-a1a4-58fabb32cd90)

  
