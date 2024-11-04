# mosquitto_server
Esto es un proyecto sobre utilizar el protocolo mqtt, se envian datos con un microcontrolador esp32, se envia los datos por mqtt, lo recibe nuestro servidor rocky linuxv8 y este grafica los datos con grafana


# microcontrolador esp32
se utiliza un micro esp32 para tomar datos de sensores de medidas, en este proyecto el microcontrolador va a mandar datos random(aletorios) por el protocolo mqtt para el envio de datos por el topico "sensor/datos". El sentido de este proyecto es implementar un servicio en nuestro servidor rocky linux v8 para tomar dichos datos con el servicio mosquitto implementado en el servidor para luego graficar los datos con grafana


# instalacion de mosquitto para rocky linux server v8
## Instalación y Configuración de Mosquitto en Rocky Linux 8

Este documento proporciona una guía paso a paso para instalar Mosquitto, configurarlo con autenticación de usuario y contraseña, y suscribirse a un tópico en Rocky Linux 8.

### Paso 1: Actualizar el sistema

Primero, asegúrate de que el sistema esté actualizado ejecutando el siguiente comando:
```
sudo dnf update -y
```
### paso 2: instalar mosquitto
```
sudo dnf install mosquitto mosquitto-clients -y
```
### Paso 3: Configurar Mosquitto con Autenticación

- Crear archivo de contraseñas:
Para configurar Mosquitto con autenticación, crea un archivo de contraseñas. Reemplaza username con el nombre de usuario que desees.
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd username
```
- Editar el archivo de configuración de Mosquitto:
Abre el archivo de configuración de Mosquitto para habilitar la autenticación.
```
sudo nano /etc/mosquitto/mosquitto.conf
```
- Añade las siguientes líneas al final del archivo para permitir únicamente conexiones autenticadas y especificar el archivo de contraseñas:
```
allow_anonymous false
password_file /etc/mosquitto/passwd
```
- Reiniciar el servicio de Mosquitto:
Después de editar la configuración, reinicia el servicio para aplicar los cambios:
```
sudo systemctl restart mosquitto
```
- Habilitar el servicio Mosquitto al iniciar el sistema:
Para que Mosquitto se inicie automáticamente con el sistema, usa el siguiente comando:
```
sudo systemctl enable mosquitto
```
## suscribirse a un topico 
- Suscribirse a un Tópico
Una vez que Mosquitto esté configurado con autenticación, puedes suscribirte a un tópico específico usando las herramientas de cliente de Mosquitto.

Comando para suscribirse a un tópico:

Para suscribirte al tópico sensores/temperatura, usa el siguiente comando. Asegúrate de reemplazar username y password con las credenciales que creaste.
```
mosquitto_sub -h localhost -t "sensores/temperatura" -u "username" -P "password"
```
donde :
-h especifica la dirección del servidor (en este caso, localhost porque Mosquitto está instalado localmente).
-t especifica el tópico al que deseas suscribirte.
-u y -P son el usuario y la contraseña configurados.
- Publicar un Mensaje en el Tópico (Opcional)
Para verificar que la suscripción funciona, puedes publicar un mensaje en el mismo tópico desde otra terminal usando el siguiente comando:
```
mosquitto_pub -h localhost -t "sensores/temperatura" -m "Prueba de mensaje" -u "username" -P "password"
```
Esto debería mostrar el mensaje en la terminal donde te suscribiste al tópico sensores/temperatura.


# instalacion y configuracion de grafana para rocky linux 
### paso 1: instalar grafana
```
sudo dnf install grafana -y
```
### paso 2: Iniciar y habilitar el servicio de Grafana:
```
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```
### paso 3: opcion para utilizar con firewall (Abrir el puerto de Grafana (3000) en el firewall:)
```
sudo firewall-cmd --add-port=3000/tcp --permanent
sudo firewall-cmd --reload
```
### paso 4: accerder a grafana 
Acceder a Grafana: Abre un navegador web y accede a Grafana usando la dirección http://<tu-IP>:3000.

Usuario y contraseña predeterminados: admin para ambos.

### paso 5: instalar plugins de mqtt 
Grafana necesita un plugin para recibir y graficar datos desde un broker MQTT.

- Instalar el plugin de MQTT:

Ejecuta el siguiente comando para instalar el plugin de MQTT para Grafana:
```
sudo grafana-cli plugins install grafana-mqtt-datasource
```
- Luego, reinicia el servicio de Grafana para aplicar el nuevo plugin:
```
sudo systemctl restart grafana-server
```
### paso 6 :Configurar el plugin MQTT en Grafana:

Ve a Configuración > Data Sources en la interfaz de Grafana.
- Haz clic en Add Data Source y selecciona MQTT.
- Configura el plugin con los detalles de tu broker MQTT:
- Broker Address: mqtt://<IP_del_broker>:1883
- Topic: El tópico del que quieres recibir datos (ej. sensores/temperatura).
- Autenticación: Si configuraste usuario y contraseña, ingrésalos aquí.

### Paso 7: Configurar un Panel en Grafana para Mostrar Datos de MQTT
- Crear un nuevo dashboard:
- En Grafana, ve a Dashboards > New Dashboard y crea uno nuevo.
- Añadir un panel para graficar datos:
- Haz clic en Add New Panel.
- Selecciona la fuente de datos MQTT que configuraste anteriormente.
- Configura el panel para mostrar el tópico de datos que envías a través de MQTT (por ejemplo, sensores/temperatura).
- Ajusta las opciones de visualización, como el tipo de gráfico, el intervalo de actualización y los límites de eje si es necesario.
### Paso 8: Verificar la Conexión de MQTT y Visualizar Datos en Tiempo Real
Enviar datos de prueba al tópico MQTT:
En una terminal separada, publica datos en el mismo tópico al que se ha suscrito Grafana. Reemplaza <usuario> y <contraseña> con las credenciales de tu broker MQTT:
```
mosquitto_pub -h <IP_del_broker> -t "sensores/temperatura" -m '{"value": 25.5}' -u "<usuario>" -P "<contraseña>"
```
Verificar la visualización en Grafana:
Observa en el panel de Grafana cómo los datos publicados en MQTT se reflejan en tiempo real. Puedes ajustar el intervalo de actualización en el panel para ver los cambios en el gráfico a medida que envías nuevos datos.
