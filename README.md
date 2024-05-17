Para ejecutar el API es necesario crear un entoro virtual en caso de que no exista
  python -m venv venv  # En Windows
  python3 -m venv venv  # En MacOS/Linux
Activar el entorno virtual dentro del proyecto
  .\venv\Scripts\activate  # En Windows
  source venv/bin/activate  # En MacOS/Linux
Instalar Flask dentro del entorno virtual, en caso de no tenerlo descargado
  pip install flask
  flask --version # Para verificar
Tambien requests
  xxx
Configurar
  En Windows:
    set FLASK_APP=run.py
    set FLASK_ENV=development
  En Mac/Linux
    export FLASK_APP=run.py
    export FLASK_ENV=development
Ejecutar la aplicacion
  run flask
