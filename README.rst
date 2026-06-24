Sistema de Gestión para Tienda de Productos Lácteos
====================================================

Aplicación web para administrar inventario, ventas, clientes y reportes
de un negocio de productos lácteos.

Tecnologías
-----------

- Python 3.10+
- Flask + Flask-AppBuilder
- SQLAlchemy + Flask-Migrate
- Bootstrap (tema Flatly)

Roles del sistema
-----------------

- **Super Administrador**: acceso total, gestión de usuarios y configuración.
- **Administrador**: catálogo, inventario, clientes y reportes.
- **Vendedor**: consulta de productos/stock, ventas y clientes.

Instalación
-----------

.. code-block:: bash

   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

Configuración
-------------

Por defecto usa SQLite (`lacteos.db`). Para MySQL/PostgreSQL define la variable
``DATABASE_URL``.

Ejecución
---------

.. code-block:: bash

   set FLASK_APP=run.py
   flask fab create-admin
   python run.py

Luego abre http://127.0.0.1:8080

Datos iniciales (opcional)
--------------------------

.. code-block:: bash

   python scripts/seed_data.py

Módulos incluidos
-----------------

- Categorías, envases y productos
- Ingresos y ventas con actualización automática de stock
- Inventario con alertas de agotado, stock bajo y vencimiento
- Clientes
- Reportes de ventas, inventario y movimientos
- Auditoría de creación/modificación y historial de movimientos
