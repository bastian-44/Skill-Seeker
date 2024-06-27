# Skill Seeker

## Proyecto Análisis y diseño de Software / Ingenieria de Software

###
* Grupo 2
* Paralelo 1

* Integrantes:

1) Bastián Arismendi 202173107-5

2) Rosario Bregante  202173078-8

3) Felipe Contreras  201621002-4

4) Javier Hormaechea  202003017-0


* -Cómo correr el código-
1) Una vez clonado el repositorio, cree un entorno virual dentro de la carpeta Skill Seeker con python -m venv env . Luego active el entorno virtual (entre por cmd al la carpeta env creada, luego a Scripts y ejecute ./activate)
2) Ejecute pip install -r requirements.txt en la cmd para asegurarse de instalar todo lo que ocupa el programa. Debe tener uvicorn instalado (si no, pip install uvicorn)
3) Para iniciar el programa ejecute *uvicorn src.main:app --reload*.
4) Para la ejecución de los test, abra otra consola aparte. Mientras tenga corriendo la ejecución del programa, ejecute: 
*python -m unittest tests.test_history*
*python -m unittest tests.test_request*
5) Las respuestas que dan son los test que fueron ejecutados y los estados de los tests.

Video Hito 4: https://youtu.be/c8SgnkVqJ3U
