# Práctica 4.1 — CI con GitHub Actions (Flask) | Guía desde 0 (para un compañero)

## 1 Objetivo
En esta práctica se trabaja con una aplicación **Flask** y se configura **CI/CD** con **GitHub Actions**. 
- **CI (Integración Continua)**: automatizar la ejecución de **tests** cada vez que se hace un `push` a la rama `main`.
- **CD (Entrega/Despliegue)**:
   - El repositorio incluye workflows para construir/publicar una imagen Docker y desplegar en AWS.
   - **En AWS Academy (cuentas de estudiante) no es posible completar el despliegue automático a AWS**, pero **sí** se puede realizar la **parte de CI**.

Cumpliendo:
- **CI funciona** (tests automáticos con push)
- Se han añadido **tests adicionales**
- La parte de **AWS/CD** queda **documentada** como no realizable con AWS Academy

## 2 Estructura del proyecto
```
ci-cd-flask/
├─ .github/
│ └─ workflows/
│ ├─ ci-cd-preproduction.yml
│ └─ ci-cd-preproduction-aws.yaml
├─ src/
│ └─ app.py
├─ tests/
│ └─ test.py
├─ Dockerfile
├─ requirements.txt
└─ README.md
```

## 3 Crear Fork en GitHub

### 3.1 Crear fork
1. Abrimos el repositorio del profesor:
   - `https://github.com/josejuansanchez/ci-cd-flask`
2. Pulsamos **Fork** → se crea una copia en nuestra cuenta (ejemplo):
   - `https://github.com/<TU_USUARIO>/ci-cd-flask`


## 4 Clonar nuestro fork en la máquina virtual (EC2/VM)

### 4.1 Clonar repositorio
Desde la VM:

```
cd ~
git clone https://github.com/<TU_USUARIO>/<TU_REPO>.git
cd <TU_REPO>
```

### 4.2 Comprobar el contenido
```
pwd
ls
```
## 5 Crear entorno virtual (venv) e instalar dependencias
### 5.1 Instalar soporte para venv
En algunas versiones de Ubuntu, venv requiere paquete adicional:
```
sudo apt update
sudo apt install -y python3.12-venv
```

### 5.2 Crear entorno virtual
```
python3 -m venv venv
```
### 5.3 Activar entorno virtual
```
source venv/bin/activate
```

### 5.4 Instalar dependencias
```
pip install -r requirements.txt
```

### 5.5 Salir del entorno virtual (si se necesita)
```
deactivate
```

## 6 Ejecutar tests en local (antes de subir)
### 6.1 Ejecutar todos los tests
Desde la raíz del proyecto:

```
python3 -m unittest discover -s tests -p "*.py" -v
```

## 7 Añadir tests adicionales
### 7.1 Editar el archivo de tests
Archivo: tests/test.py
- Añadimos tests adicionales en el mismo archivo, separados por un comentario para mantener orden.

```
import unittest
from src.app import app


class BasicTests(unittest.TestCase):

    def setUp(self):
        # Crea un cliente de prueba usando la aplicación Flask
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        # Envía una solicitud GET a la ruta '/'
        result = self.app.get('/')

        # Verifica que la respuesta sea "Hello, World!"
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode(), "Hello, World!")

# Tests adicionales (Práctica 4.1)

class ExtraTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_not_found_returns_404(self):
        result = self.app.get('/ruta-que-no-existe')
        self.assertEqual(result.status_code, 404)

    def test_home_content_type(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        # Aceptamos HTML/texto o JSON
        self.assertTrue(
            "text" in result.content_type or "html" in result.content_type or "json" in result.content_type
        )

    def test_home_not_empty(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(len(result.data) > 0)


if __name__ == "__main__":
    unittest.main()

```

### 7.2 Ejecutar tests tras los cambios
```
python3 -m unittest discover -s tests -p "*.py" -v
```

- Debe mostrar OK.

## 8 Subir cambios a GitHub (commit + push)
### 8.1 Ver cambios
```
git status
```
### 9.2 Añadir archivo y hacer commit
```
git add tests/test.py
```
```
git commit -m "Add extra tests"
```

### 8.3 Subir al repositorio (push)
```
git push
```

## 9 GitHub Actions (CI)
### 9.1 Habilitar Actions en el fork
En GitHub: Pestaña Actions
- Si aparece mensaje de seguridad por fork, pulsar:
“I understand my workflows, go ahead and enable them”

### 9.2 Ver ejecución automática de CI
Una vez hecho el push, GitHub Actions lanza el workflow automáticamente.
PASOS:
1. Repositorio → Actions
2. Abrir la ejecución más reciente
3. Ver el job test en verde


### 1 Workflow de CI ejecutado en GitHub Actions (Actions)

![CI en GitHub Actions](img/4.1ci%20funcionando.png)

### 2 Tests ejecutados en la máquina virtual (unittest)

![Tests OK en consola](img/4.1%20test.png)

### 3 Preparación del entorno (venv + instalación de dependencias)

![Entorno virtual y requirements](img/4.1%20entorno.png)

#### María del Mar López Montoya | 2ºDAW
