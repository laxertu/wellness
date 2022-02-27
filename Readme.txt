Instalación

* Instalar las dependencias: pip install -r requirements.txt

* Ejecutar install.py: python3 install.py [ruta al fichero csv]
Genera la base de datos con SqlLite y importa los datos desde el csv que se pasa por parámetro

* Levantar el servicio web
flask run

Documentación

Se han creado tres puntos de entrada:

* http://127.0.0.1:5000/login
Realiza un login ficticio, sin credenciales, retorna un token bearer a enviar en cabecera en las demás peticiones

* http://127.0.0.1:5000/get_values?fields=[field1]&field=[field2]&dt_from=[Y-m-d H:M:S]&dt_to=[Y-m-d H:M:S]
Retorna los datos fila por fila en el intervalo de tiempo especificado
ejemplo:
http://127.0.0.1:5000/get_values?fields=power&fields=maximeter&dt_from=2019-08-01 00:00:00&dt_to=2019-08-04 01:00:00

* http://127.0.0.1:5000/get_sum_values?fields=[field1]&field=[field2]&dt_from=[Y-m-d]&dt_to=[Y-m-d]
Retorna los datos agregados por suma en el intervalo de tiempo especificado
ejemplo
http://127.0.0.1:5000/get_sum_values?fields=power&fields=maximeter&dt_from=2019-08-01&dt_to=2019-08-04

* http://127.0.0.1:5000/get_avg_values?fields=[field1]&field=[field2]&dt_from=[Y-m-d]&dt_to=[Y-m-d]
Retorna los datos agregados por promedio en el intervalo de tiempo especificado
ejemplo
http://127.0.0.1:5000/get_avg_values?fields=power&fields=maximeter&dt_from=2019-08-01&dt_to=2019-08-04

Los posibles valores de "fields" se corresponden con las columnas de la tabla en base de datos:
'energy', 'reactive_energy', 'power', 'maximeter', 'reactive_power', 'voltage', 'intensity', 'power_factor'

**

Estos métodos deberían de ser suficientes para generar la visualización propuesta en el ejercicio. Para "datos eléctricos mes en curso"
se puede usar la suma pasando en intervalo correspondiente, aunque se podría añadir un metodo especifico para ello por
cuestiones de optimización.

Un punto a mejorar seguramente sea el sistema de logueo, para que escriba en disco en lugar de por pantalla

