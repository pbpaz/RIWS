# Galibooks

Este proyecto ha sido desarrollado por Pablo Braga, Jose Daniel García y Diego García para la asignatura RIWS. Se trata de un sistema de scraping, indexación y presentación a través de una interfaz web de los contenido indexados, que son libros de diferentes páginas web.

## Ejecución del proyecto

Tras clonar el repositorio, podremos hacer lo siguiente

> NOTA: Dados los materiales que hay en este repositorio sería posible llevar a cabo un scrapeado nuevo y un procesado de los datos de las páginas con el objetivo de crear un índice actualizado. Sin embargo este tutorial de ejecución partirá de la base de que se utilizan los datos scrapeados previamente accesibles en la carpeta data.
 
### Despliegue del contenedor de elastic

primeramente deberemos lanzar el contenedor de Elastic para la ejecución de nuestro índice ejecutando los siguientes comandos:

> Nota: para este paso es necesario tener docker corriendo en el ordenador.


```bash
#Desde el directorio raíz del proyecto
cd docker
docker-compose up
```

### Creación de índice e inserción de documentos

Para ello deberemos situarnos en la carpeta elastic dentro del directorio riws y ejecutar los scripts de python:

```bash
#Desde el directorio raíz del proyecto
cd riws
cd elastic
python create_index.py
python insert_documents.py
```

### Lanzamiento del frontend

Para este paso, deberemos situarnos en la carpeta del frontend y ejecutar los siguientes comandos:

```bash
#Desde el directorio raíz del proyecto
cd app-search-reference-ui-react-master
yarn
yarn start
```