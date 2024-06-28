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
1) Una vez clonado el repositorio, cree un entorno virual dentro de la carpeta  con "python -m venv SkillSeeker". Entre a SkillSeeker/cripts y ejecute ./activate)

2) Ejecute pip install -r requirements.txt en la cmd para asegurarse de instalar todo lo que ocupa el programa. Debe tener uvicorn instalado (si no, pip install uvicorn).
3)Hay 2 formas de Iniciar el programa. "python main.py" ejecutara el programa junto al formulario Online, el link se mostrara en la consola. No se pueden editar archivos en este estado(Se puede pero no se actualizara hasta reiniciar el programa). La otra forma es "uvicorn src.main:app --reload" que si permiter actualizar a tiempo real pero no se creara el formulario Online.
4) La primera ejecución del programa con "python main.py" dara error dado que no hay una cuenta de ngrok conectada(Se inicia antes para instalar ngrok en el sistema).
5)Crearse una cuenta gratuita en ngrok.com.
6)En el Dashboard ir Getting Started/Your Authtoken.
7)En la consola ejecutar ngrok config add-authtoken $YOUR_AUTHTOKEN .
(El Token se encuentra ahí mismo).
8)Volver a ejecutar el programa.
4) Para la ejecución de los test, abra otra consola aparte. Mientras tenga corriendo la ejecución del programa, ejecute: 
python -m unittest tests.test_history
python -m unittest tests.test_request
5) Las respuestas que dan son los test que fueron ejecutados y los estados de los tests.

Video Hito 4: https://youtu.be/c8SgnkVqJ3U