# API Course Manager in Django

Este proyecto es una API REST construida con **Django** que permite gestionar cursos. La idea es simular el backend de plataformas como Udemy o universidades. La API interactúa con una base de datos **MySQL**.

## Características

### Usuarios
- **Crear usuario**: Añade un nuevo usuario. ```generics.ListCreateAPIView```
- **Consultar usuarios**: Obtiene todos los usuarios. ```generics.ListCreateAPIView```
- **Consultar un usuario**: Obtiene los datos de un usuario específico. ```generics.RetrieveDestroyAPIView```
- **Eliminar usuario**: Elimina un usuario específico y sus datos asociados. ```generics.RetrieveDestroyAPIView```
- **Cambiar contraseña**: Permite cambiar la contaseña a un usuario. ```generics.UpdateAPIView```

### Categorías
- **Consultar las categorías**: Obtiene todas las categorías disponibles a las que se puede asociar un curso. ```generics.ListCreateAPIView```
- **Consultar una categoría**: Obtiene los datos asociados a una categoría específica. ```generics.ListCreateAPIView```

### Cursos
- **Crear un curso**: Añade un nuevo curso. ```viewsets.ModelViewSet```
- **Consultar los cursos**: Obtiene todos los cursos. ```viewsets.ModelViewSet```
- **Consultar un curso**: Obtiene los datos asociados a un curso específico. ```viewsets.ModelViewSet```
- **Actualizar un curso**: Permite cambiar los datos de un curso específico. ```viewsets.ModelViewSet```
- **Eliminar un curso**: Borra un curso específico. ```viewsets.ModelViewSet```

### Estudiantes
- **Asignar un estudiante a un curso**: Permite asignar un estudiante a un curso que esté cursando. ```generics.ListCreateAPIView```
- **Consultar los estudiantes de un curso**: Devuelve la lista de estudiantes de un curso específico. ```generics.ListCreateAPIView```
- **Eliminar a un estudiante de un curso**: Borra la relación entre un estudiante y un curso.  ```generics.DestroyAPIView```

### Ayuda
- **Sugerencias de cursos**: Permite encontrar cursos de las mismas categorías que el estudiante está cursando para recomendar nuevos cursos. ```APIView```

## Configuración

### Requisitos previos
- Python 3.8+
- Django
- Mysql

### Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/DanielCaldes/Django-Avanzado.git
   cd course_management
   ```

2. Crea y activa el entorno virtual (ejemplo con conda):

   ```bash
   conda create --name nombre_del_entorno python=3.x
   conda activate nombre_del_entorno
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crea una base de datos MySQL con la configuración siguiente, si quisieras modificar algo, puedes cambiar los datos en ```settings.py```:
   ```settings
   "NAME": "course_management",
   "USER" : "admin",
   "PASSWORD":"1234",
   "HOST":"localhost",
   "PORT":"3307"  # Normalmente será 3306, si tu configuración es diferente cambia el puerto.
   ```

### Ejecución

1. Inicia el servidor de Django:
   ```bash
   python manage.py runserver
   ```

2. Accede a la documentación interactiva de la API en Swagger o Redoc:
   - Swagger: http://127.0.0.1:8000/swagger/
   - Redoc: http://127.0.0.1:8000/redoc/

## Endpoints

### **Usuarios**

#### 1. Crear un usuario

- **Método**: POST  
  ```url  
  /api/users/
  ```
- **Descripción**: Crea un nuevo usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
     "username": "Cristina_Romero_Palacios",
     "email": "cRomeroPalacios@alumno.gmail.com",
     "is_professor":false,
     "password":"cristinaRomero"
   }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "User created successfully",
    "id": 22
  }
  ```

#### 2. Obtener la lista de usuarios

- **Método**: GET  
  ```url  
  /api/users/
  ```
- **Descripción**: Obtiene la lista de usuarios, con posibilidad de filtrado por grupo (professors/students).
- **Respuesta**:
  ```json  
  [
     {
       "id": 2,
       "username": "Juan_Ruiz_Lopez",
       "email": "jRuizLopez@profesor.mail.com",
       "professor": true
     },
     {
       "id": 3,
       "username": "Pedro_Sanchez_Castejon",
       "email": "pSanchezCastejon@alumno.mail.com",
       "professor": false
     }
  ]
  ```

#### 3. Obtener un usuario por ID

- **Método**: GET  
  ```url  
  /api/users/{user_id}/
  ```
- **Descripción**: Obtiene los detalles de un usuario por su ID.
- **Respuesta**:
  ```json  
  {
     "id": 2,
     "username": "Juan_Ruiz_Lopez",
     "email": "jRuizLopez@profesor.mail.com",
     "professor": true
   }
  ```

#### 4. Eliminar un usuario por ID

- **Método**: DELETE  
  ```url  
  /api/users/{user_id}/
  ```
- **Descripción**: Elimina un usuario por su ID.
- **Respuesta**:
  ```json  
  {}
  ```

#### 5. Resetear la contraseña de un usuario

- **Método**: PUT  
  ```url  
  /api/users/{user_id}/password/
  ```
- **Descripción**: Actualiza la contraseña de un usuario.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "new_password": "4321231"
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "La contraseña ha sido actualizada correctamente."
  }
  ```


### **Categorías**

#### 1. Ver todas las categorías

- **Método**: GET  
  ```url  
  /api/courses/categories/
  ```
- **Descripción**: Obtiene una lista de todas las categorías disponibles.
- **Respuesta**:
  ```json  
  [
    {
      "id": 1,
      "name": "Tecnología"
    },
    {
      "id": 2,
      "name": "Ciencias Sociales"
    }
  ]
  ```

#### 2. Consultar una categoría por ID

- **Método**: GET  
  ```url  
  /api/courses/categories/{category_id}/
  ```
- **Descripción**: Obtiene los detalles de una categoría específica por su ID.
- **Respuesta**:
  ```json  
  {
    "id": 1,
    "name": "Tecnología"
  }
  ```


### **Cursos**

#### 1. Realizar operaciones sobre cursos

- **Método**: GET, POST, PUT, DELETE  
  ```url  
  /api/courses/
  ```
- **Descripción**: Permite realizar operaciones CRUD sobre los cursos.
- **Respuesta**:
  ```json  
  {
    "id": 1,
    "name": "Curso de Tecnología",
    "description": "Curso introductorio de tecnología",
    "categories": ["Tecnología", "Ciencias"]
  }
  ```

#### 2. Ver la lista de estudiantes en un curso

- **Método**: GET  
  ```url  
  /api/courses/{course_id}/students/
  ```
- **Descripción**: Obtiene la lista de estudiantes en un curso específico.
- **Respuesta**:
  ```json  
  [
    {
      "id": 1,
      "username": "student_name",
      "email": "student_email@example.com"
    }
  ]
  ```

#### 3. Añadir un estudiante a un curso

- **Método**: POST  
  ```url  
  /api/courses/{course_id}/students/
  ```
- **Descripción**: Agrega un estudiante a un curso.
- **Cuerpo de la solicitud** (JSON):
  ```json  
  {
    "user_id": 1
  }
  ```
- **Respuesta**:
  ```json  
  {
    "message": "Student added successfully to the course."
  }
  ```

#### 4. Eliminar un estudiante de un curso

- **Método**: DELETE  
  ```url  
  /api/courses/{course_id}/students/{student_id}/
  ```
- **Descripción**: Elimina a un estudiante de un curso específico.
- **Respuesta**:
  ```json  
  {
    "message": "Student removed from the course."
  }
  ```
  

### **Sugerencias de Cursos**

#### 1. Obtener sugerencias de cursos para un usuario

- **Método**: GET  
  ```url  
  /api/users/{user_id}/suggestions/
  ```
- **Descripción**: Obtiene sugerencias de cursos para un usuario basadas en las categorías de los cursos en los que está inscrito.
- **Respuesta**:
  ```json  
  {
    "suggested_courses": [
      {
        "name": "Curso de Ciencia de Datos",
        "description": "Aprende sobre análisis de datos",
        "categories": ["Tecnología", "Ciencias"]
      }
    ]
  }
  ```
