# TFG
Evaluacion de prestaciones de aplicaciones de Internet

# ORGANIZACION
1. mem: Memoria del TFG, actualmente solo plantilla.
2. cod: Cada una de estas carpetas contiene el código requerido (Servidor Java, Elastic, Requests...)
3. doc: Documentos de referencia, links, información importante.

# COD

1. Version_1: El servidor funciona y contesta peticiones a un nivel muy basico, esperando un delay, problema = El servidor se cierra solo.
2. Version_2: El servidor ya no se cierra solo pero resetea las conexiones, curl(56) connection reset from peer.
3. Version_3: El servidor esta completamente operativo al igual que un programa basico para mandar peticiones a este.
4. Version_4: El programa de requests ha sido mejorado para mandar un trafico de requests mas complicado.

# GRAFANA

Finalmente la aplicacion para generar dashboards será grafana.

1. Opcion mas probable: Analizar factores como CPU, Memoria, Disco, I/O. Tecnologías = Telegraf como Collector e InfluxDB como base de los datos.
