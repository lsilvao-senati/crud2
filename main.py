from crud_generator.generator import CRUDGenerator


def get_user_input():
    """Solicita datos al usuario de forma interactiva"""
    import os

    print("🚀 Generador de Sistema CRUD en PHP")
    print("=" * 50)
    
    # Solicitar archivo SQL
    while True:
        sql_file = input("📄 Ingresa la ruta del archivo SQL: ").strip()
        if not sql_file:
            print("❌ La ruta del archivo no puede estar vacía")
            continue
        if not os.path.exists(sql_file):
            print(f"❌ El archivo '{sql_file}' no existe. Intenta nuevamente.")
            continue
        break
    
    # Solicitar directorio de salida
    output_dir = input("📁 Directorio de salida (presiona Enter para 'generated_crud'): ").strip()
    if not output_dir:
        output_dir = "generated_crud"
    
    print("\n🔧 Configuración de Base de Datos")
    print("-" * 30)
    
    # Configuración de base de datos
    host = input("🌐 Host de la base de datos (presiona Enter para 'localhost'): ").strip()
    if not host:
        host = "localhost"
    
    dbname = input("💾 Nombre de la base de datos: ").strip()
    while not dbname:
        print("❌ El nombre de la base de datos es obligatorio")
        dbname = input("💾 Nombre de la base de datos: ").strip()
    
    username = input("👤 Usuario de la base de datos (presiona Enter para 'root'): ").strip()
    if not username:
        username = "root"
    
    password = input("🔒 Contraseña (presiona Enter si no tiene): ").strip()

    print("\n📝 Resumen de configuración:")
    print(f"   Archivo SQL: {sql_file}")
    print(f"   Directorio de salida: {output_dir}")
    print(f"   Host: {host}")
    print(f"   Base de datos: {dbname}")
    print(f"   Usuario: {username}")
    print(f"   Contraseña: {'(sin contraseña)' if not password else '********'}")

    confirm = input("\n✅ ¿Continuar con esta configuración? (s/n): ").strip().lower()
    if confirm not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return None
    
    return {
        'sql_file': sql_file,
        'output_dir': output_dir,
        'host': host,
        'dbname': dbname,
        'username': username,
        'password': password
    }

if __name__ == "__main__":
    try:
        # Obtener datos del usuario
        config = get_user_input()
        if not config:
            exit(0)
        
        # Crear instancia del generador
        generator = CRUDGenerator(config['sql_file'], config['output_dir'])
        
        # Configurar base de datos
        generator.db_config = {
            'host': config['host'],
            'dbname': config['dbname'],
            'username': config['username'],
            'password': config['password']
        }
        
        # Procesar archivo SQL
        print(f"\n📄 Analizando archivo SQL: {config['sql_file']}")
        generator.parse_sql_file()
        
        if not generator.tables:
            print("❌ No se encontraron tablas en el archivo SQL")
            exit(1)
        
        print(f"✅ Se encontraron {len(generator.tables)} tabla(s)")
        
        # ¡NUEVA LÍNEA AQUÍ! Asegurarse de que la estructura de directorios exista antes de generar archivos
        generator.create_directory_structure()

        # Generar sistema CRUD
        print("⚙️ Generando archivos del sistema CRUD...")
        generator.generate_all_files()
        
        print(f"✅ Sistema CRUD generado exitosamente en: {generator.output_dir}")

    except Exception as e:
        print(f"❌ Error durante la generación: {e}")