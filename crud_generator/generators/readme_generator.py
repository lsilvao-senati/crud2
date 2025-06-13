def generate_readme(tables: dict, output_dir: str) -> str:
    table_list_markdown = '\n'.join(
        [f"- **{''.join(word.capitalize() for word in tn.split('_'))}** (`{tn}`)" for tn in tables.keys()]
    )

    return f"""# Generador de Sistema CRUD en PHP

Este es un sistema CRUD (Create, Read, Update, Delete) generado automáticamente a partir de una base de datos SQL.

## 🚀 Inicio Rápido

1.  **Requisitos**:
    * Servidor web (Apache, Nginx, etc.)
    * PHP (versión 7.4 o superior recomendada)
    * Base de datos MySQL/MariaDB

2.  **Configuración de la Base de Datos**:
    * Asegúrate de que tu base de datos esté configurada en `config/Database.php`.
    * Importa tu archivo `.sql` en tu base de datos.

3.  **Despliegue**:
    * Copia todo el contenido de la carpeta `{output_dir}` a la raíz de tu servidor web (ej. `htdocs/` en XAMPP, `www/` en WAMP, etc.).

4.  **Acceso**:
    * Abre tu navegador y ve a `http://localhost/tu_ruta_del_proyecto/login.php` (o la URL correspondiente).
    * **Credenciales predeterminadas de inicio de sesión (pueden modificarse en `login.php`):**
        * Usuario: `admin`
        * Contraseña: `admin`

## 📁 Estructura del Proyecto

La estructura del sistema está organizada en carpetas para separar controladores, vistas y modelos siguiendo el patrón MVC.

## 📊 Tablas Incluidas

{table_list_markdown}

## 🛠️ Personalización

Puedes modificar los archivos de configuración, vistas y controladores según las necesidades específicas de tu proyecto.

---

Generado automáticamente por el sistema CRUD Generator.
"""
