# El Buen Sabor - API de Reservas de Restaurante

![Imagen de un restaurante elegante](https://placehold.co/1200x400/333333/FFFFFF?text=El+Buen+Sabor)

"El Buen Sabor" es el backend para un sistema de reservas de restaurantes desarrollado con FastAPI, PostgreSQL, y Docker, siguiendo los principios de Arquitectura Hexagonal y Diseño Guiado por Dominio (DDD).

## Características

* **Autenticación y Autorización:** Sistema seguro basado en OAuth2 (Password Flow) y JWT, con roles de Cliente y Administrador.
* **Gestión de Restaurantes:** Operaciones CRUD para restaurantes y sus mesas (restringido a administradores).
* **Sistema de Reservas:** Permite a los clientes agendar, cancelar y ver sus reservas, con validaciones de horario y disponibilidad.
* **Menú y Pre-órdenes:** Los clientes pueden ver el menú y pre-ordenar platos al momento de hacer su reserva.
* **Dashboard:** Endpoints para que los administradores puedan ver estadísticas clave sobre reservas, platos y ocupación.
* **Notificaciones (Simuladas):** Notificaciones en consola para eventos importantes como creación o cancelación de reservas.

## Arquitectura del Proyecto

La estructura del proyecto se basa en la **Arquitectura Hexagonal** y **DDD**. Esto significa que el núcleo de la lógica de negocio (el dominio) es independiente de las tecnologías externas como la base de datos o la API web.

* **/src**: Contiene todo el código fuente de la aplicación.
    * **/shared**: Código compartido por todos los módulos, como la configuración de la base de datos y las excepciones personalizadas.
    * **/auth | /restaurants | /reservations | /menu | /dashboard**: Cada uno de estos es un **módulo de negocio** autocontenido.
        * **/domain**: Contiene las entidades (modelos) y la lógica de negocio pura. No depende de ninguna otra capa.
        * **/infrastructure**: Implementaciones concretas de las interfaces definidas en el dominio (ej. repositorios que interactúan con PostgreSQL) y servicios externos (ej. seguridad, JWT).
        * **/api**: Define los endpoints de FastAPI (los "adaptadores" de entrada), manejando las solicitudes HTTP y llamando a la lógica del dominio.
    * **/notifications**: Un módulo simple para simular notificaciones.
    * **/alembic**: Contiene las migraciones de la base de datos gestionadas por Alembic.
* **/tests**: Contiene los tests unitarios y de integración, buscando una alta cobertura del código.

Esta separación de responsabilidades hace que el código sea más mantenible, escalable y fácil de probar.

## Cómo Ejecutar el Proyecto con Docker

Para levantar el proyecto, solo necesitas tener Docker y Docker Compose instalados.

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO>
    ```

2.  **Construye y levanta los contenedores:**
    Este comando construirá la imagen para la aplicación de FastAPI y levantará los servicios de la API y la base de datos PostgreSQL.
    ```bash
    docker-compose up --build
    ```

3.  **Ejecuta las migraciones de la base de datos:**
    En otra terminal, ejecuta el siguiente comando para aplicar las migraciones y crear las tablas en la base de datos.
    ```bash
    docker-compose exec web alembic upgrade head
    ```

4.  **Crea un usuario Administrador (Opcional pero recomendado):**
    Para acceder a las rutas de administrador, puedes crear un usuario con ese rol. Conéctate al contenedor de la base de datos y crea el usuario manualmente.

5.  **¡Listo! La API estará disponible en `http://localhost:8000`**
    Puedes acceder a la documentación interactiva de Swagger UI en `http://localhost:8000/docs`.

## Stack Tecnológico

* **Backend:** FastAPI
* **Base de Datos:** PostgreSQL
* **ORM/Modelado:** SQLModel
* **Migraciones:** Alembic
* **Contenerización:** Docker & Docker Compose
* **Testing:** Pytest
* **Autenticación:** JWT, OAuth2, Passlib, Bcrypt

