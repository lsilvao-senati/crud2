def generate_controller(table_name: str, columns: list, foreign_keys: list) -> str:
    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    primary_key = next((col['name'] for col in columns if col.get('primary_key')), 'id')

    set_attributes_create = []
    for col in columns:
        if not col.get('auto_increment'):
            set_attributes_create.append(f"${table_name}->{col['name']} = $_POST['{col['name']}'] ?? null;")


    set_attributes_update = []
    for col in columns:
        set_attributes_update.append(f"${table_name}->{col['name']} = $_POST['{col['name']}'] ?? null;")

    # Lógica para obtener datos de tablas relacionadas para los SELECTs (claves foráneas)
    related_data_fetch = []
    # El nombre de la instancia del modelo actual, ej. $posts si table_name es 'posts'
    model_instance_var_name = f"${table_name}"

    for fk in foreign_keys:
        referenced_table_name = fk['referenced_table']
        # Nombre del método en el modelo actual, ej. getAllCategories
        method_to_call = f"getAll{''.join(word.capitalize() for word in referenced_table_name.split('_'))}"
        # Clave para $this->data, ej. 'categories_options' o 'categories'
        # La vista espera: foreach (${referenced_table_name}s as ${referenced_table_name}_item)
        # Entonces, la clave en $this->data debe ser referenced_table_name + "s"
        data_key_for_view = f"{referenced_table_name}s"

        related_data_fetch.append(f'''
        // Obtener datos para el SELECT de {fk['local_column']} (tabla {referenced_table_name})
        // Se utiliza el método {method_to_call}() del modelo ({class_name}.php)
        // Asegurarse que {model_instance_var_name} está instanciado antes de esta línea.
        $this->data['{data_key_for_view}'] = {model_instance_var_name}->{method_to_call}();''')

    return f"""<?php
require_once 'config/Database.php';
require_once 'models/{class_name}.php';

class {class_name}Controller {{
    private $data = []; // Propiedad para almacenar datos para pasar a las vistas

    public function index() {{
        ${table_name} = new {class_name}();
        $stmt = ${table_name}->readAll();
        $data_rows = []; // Inicializar como array vacío

        // Verificar si $stmt es una instancia válida de PDOStatement
        if ($stmt instanceof PDOStatement) {{
            $data_rows = $stmt->fetchAll(PDO::FETCH_ASSOC); // Obtener todas las filas como un array asociativo
        }} else {{
            // Registrar el error si $stmt no es un PDOStatement (puedes ajustar el manejo de errores)
            error_log("Error: readAll() para {table_name} no devolvió un PDOStatement.");
            // Opcional: agregar un mensaje de error a $this->data para mostrar en la vista
            $this->data['error_message'] = "Error al cargar los datos de {class_name}.";
        }}

        // Pasar el array de filas a la vista
        $this->data['{table_name}s'] = $data_rows; 

        $title = "Gestión de {class_name}";
        extract($this->data); // Esto convertirá $this->data['{table_name}s'] en ${table_name}s
        include 'views/{table_name}/index.php';
    }}

    public function create() {{
        $title = "Crear Nuevo {class_name}";
        // Instanciar el modelo principal ANTES de obtener datos relacionados
        ${table_name} = new {class_name}();
        {' '.join(related_data_fetch)} // Incluir lógica para obtener datos relacionados
        extract($this->data); // Extraer datos relacionados si los hay
        include 'views/{table_name}/create.php';
    }}

    public function store() {{
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {{
            ${table_name} = new {class_name}();
            {' '.join(set_attributes_create)}
            if (${table_name}->create()) {{
                header("Location: index.php?controller={table_name}&action=index&msg=created");
                exit();
            }} else {{
                header("Location: index.php?controller={table_name}&action=create&error=1");
                exit();
            }}
        }}
    }}

    public function edit() {{
        ${table_name} = new {class_name}();
        ${table_name}->{primary_key} = $_GET['id'] ?? 0;
        ${table_name}->readOne();
        $this->data['{table_name}'] = ${table_name}; // Pasar el objeto de la tabla actual

        $title = "Editar {class_name}";
        {' '.join(related_data_fetch)} // Incluir lógica para obtener datos relacionados para la vista de edición
        extract($this->data); // Pasar todos los datos (incluyendo el objeto de la tabla actual y las tablas relacionadas)
        include 'views/{table_name}/edit.php';
    }}

    public function update() {{
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {{
            ${table_name} = new {class_name}();
            {' '.join(set_attributes_update)}
            if (${table_name}->update()) {{
                header("Location: index.php?controller={table_name}&action=index&msg=updated");
                exit();
            }} else {{
                header("Location: index.php?controller={table_name}&action=edit&id=" . $_POST['{primary_key}'] . "&error=1");
                exit();
            }}
        }}
    }}

    public function delete() {{
        ${table_name} = new {class_name}();
        ${table_name}->{primary_key} = $_GET['id'] ?? 0;
        if (${table_name}->delete()) {{
            header("Location: index.php?controller={table_name}&action=index&msg=deleted");
            exit();
        }} else {{
            header("Location: index.php?controller={table_name}&action=index&error=1");
            exit();
        }}
    }}
}}
?>"""
