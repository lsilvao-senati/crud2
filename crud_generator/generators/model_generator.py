def generate_model(table_name: str, columns: list, foreign_keys: list) -> str:
    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    primary_key = next((col['name'] for col in columns if col.get('primary_key')), 'id')

    # CORREGIDO: Solo incluir columnas reales de la tabla
    properties = [f"    public ${col['name']};" for col in columns]
    # Add properties for columns_data and foreign_keys_data to PHP class
    properties.append("    public $columns_data;")
    properties.append("    public $foreign_keys_data;")

    # CORREGIDO: Filtrar columnas que no son auto_increment Y que existen realmente
    real_columns = [col for col in columns if not col.get('auto_increment')]
    insert_fields = [f"{col['name']}=:{col['name']}" for col in real_columns]
    bind_params = [f"$stmt->bindParam(':{col['name']}', $this->{col['name']});" for col in real_columns]

    assign_row = [f"$this->{col['name']} = $row['{col['name']}'];" for col in columns]
    update_fields = [f"{col['name']}=:{col['name']}" for col in real_columns]

    # CORREGIDO: Incluir binding para primary key en update
    update_bindings = [f"$stmt->bindParam(':{col['name']}', $this->{col['name']});" for col in real_columns]
    update_bindings.append(f"$stmt->bindParam(':{primary_key}', $this->{primary_key});")

    # Build PHP arrays for columns_data and foreign_keys_data
    php_cols_list_items = []
    for col in columns:
        php_cols_list_items.append(
            f"            ['name' => '{col['name']}', 'type' => '{col['type']}', "
            f"'length' => {('null' if col['length'] is None else str(col['length']))}, "
            f"'nullable' => {'true' if col['nullable'] else 'false'}, "
            f"'auto_increment' => {'true' if col['auto_increment'] else 'false'}, "
            f"'primary_key' => {'true' if col['primary_key'] else 'false'}]"
        )
    php_columns_data = "[\n" + ",\n".join(php_cols_list_items) + "\n        ]"

    php_fks_list_items = []
    for fk in foreign_keys:
        php_fks_list_items.append(
            f"            ['local_column' => '{fk['local_column']}', 'referenced_table' => '{fk['referenced_table']}', 'referenced_column' => '{fk['referenced_column']}', 'display_column' => '{fk['display_column']}']"
        )
    php_foreign_keys_data = "[\n" + ",\n".join(php_fks_list_items) + "\n        ]"

    # CORREGIDO: Generar métodos auxiliares para obtener datos de tablas relacionadas
    helper_methods = ""
    # Usar un diccionario para evitar duplicados por si múltiples FKs apuntan a la misma tabla pero queremos un método por FK referenciada de forma única
    # En este caso, la lógica original de generar un método por tabla referenciada es más simple y se mantiene.
    # Si se quisiera un método por CADA FK (ej. getAuthorsAsEditor, getAuthorsAsReviewer), se necesitaría un enfoque diferente.
    # Por ahora, un método por tabla referenciada es suficiente.
    processed_referenced_tables_for_helpers = set()
    for fk in foreign_keys:
        referenced_table = fk['referenced_table']
        if referenced_table not in processed_referenced_tables_for_helpers:
            processed_referenced_tables_for_helpers.add(referenced_table)

            # Capitalizar el nombre de la tabla para el nombre del método
            # ej. 'user_roles' se convierte en 'UserRoles'
            method_name_suffix = ''.join(word.capitalize() for word in referenced_table.split('_'))
            method_name = f"getAll{method_name_suffix}"

            # Usar referenced_column para el valor y display_column para el texto
            value_column = fk['referenced_column']
            display_text_column = fk['display_column']

            helper_methods += f"""
    // Método para obtener todos los registros de {referenced_table} (para formularios)
    // Selecciona {value_column} como valor y {display_text_column} como texto.
    public function {method_name}() {{
        $query = "SELECT `{value_column}`, `{display_text_column}` FROM `{referenced_table}` ORDER BY `{display_text_column}`";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }}
"""

    static_helper_method = f"""
    /**
     * Método genérico para obtener todos los registros de una tabla específica.
     * Útil para llenar dropdowns o listados donde no hay una FK directa definida en el modelo actual.
     *
     * @param string $tableName El nombre de la tabla de la cual obtener los datos.
     * @param array $columnsToSelect Array de columnas a seleccionar. Por defecto ['*'].
     * @param string|null $orderByColumn Columna opcional por la cual ordenar los resultados.
     * @return array Retorna un array de registros asociativos.
     */
    public static function getAllFromTable(string $tableName, array $columnsToSelect = ['*'], ?string $orderByColumn = null): array {{
        $database = new Database();
        $conn = $database->getConnection();

        $selectClause = implode(", ", array_map(function($col) {{ return "`" . $col . "`"; }}, $columnsToSelect));

        $query = "SELECT " . $selectClause . " FROM `" . $tableName . "`";

        if ($orderByColumn !== null) {{
            $query .= " ORDER BY `" . $orderByColumn . "`";
        }}

        $stmt = $conn->prepare($query);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }}
"""

    return f"""<?php
require_once 'config/Database.php';

class {class_name} {{
{chr(10).join(properties)}

    private $conn;
    private $table_name = "{table_name}";
    private $primary_key = "{primary_key}";

    public function __construct() {{
        $database = new Database();
        $this->conn = $database->getConnection();
        // Inicializar las propiedades con los datos de columnas y claves foráneas
        $this->columns_data = {php_columns_data};
        $this->foreign_keys_data = {php_foreign_keys_data};
    }}

    public function create() {{
        $query = "INSERT INTO " . $this->table_name . " SET {', '.join(insert_fields)}";
        $stmt = $this->conn->prepare($query);
        {' '.join(bind_params)}
        return $stmt->execute();
    }}

    public function readAll() {{
        // Construir la consulta SELECT con JOINs para obtener datos de tablas relacionadas
        $select_columns = [];
        $joins = [];

        // Seleccionar todas las columnas de la tabla principal
        foreach ($this->columns_data as $col) {{
            $select_columns[] = $this->table_name . ".`".$col['name']."`";
        }}

        // Añadir JOINS y columnas de visualización para claves foráneas
        foreach ($this->foreign_keys_data as $fk_info) {{
            $referenced_table_name = $fk_info['referenced_table'];
            $local_column = $fk_info['local_column'];
            $referenced_column = $fk_info['referenced_column'];
            // NUEVO: Usar display_column recuperado de $this->foreign_keys_data
            $display_column_name = $fk_info['display_column'];

            // Alias para mostrar el nombre de la tabla relacionada y su columna de visualización
            // ej., 'categories_name' o 'users_username'
            $alias_for_display = $referenced_table_name . "_" . $display_column_name;
            
            // Seleccionar la columna de visualización de la tabla referenciada
            $select_columns[] = "`" . $referenced_table_name . "`.`" . $display_column_name . "` AS `" . $alias_for_display . "`";
            
            // Construir el JOIN
            $joins[] = "LEFT JOIN `" . $referenced_table_name . "` ON `" . $this->table_name . "`.`" . $local_column . "` = `" . $referenced_table_name . "`.`" . $referenced_column . "`";
        }}

        $final_select_clause = implode(", ", $select_columns);
        $final_join_clause = implode(" ", $joins);

        $query = "SELECT " . $final_select_clause . " FROM " . $this->table_name . " " . $final_join_clause . " ORDER BY " . $this->table_name . ".`" . $this->primary_key . "` DESC";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt;
    }}

    public function readOne() {{
        $query = "SELECT * FROM " . $this->table_name . " WHERE `" . $this->primary_key . "` = ? LIMIT 0,1";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->{primary_key});
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($row) {{
            {' '.join(assign_row)}
        }}
    }}

    public function update() {{
        $query = "UPDATE " . $this->table_name . " SET {', '.join(update_fields)} WHERE `" . $this->primary_key . "` = :{primary_key}";
        $stmt = $this->conn->prepare($query);
        {' '.join(update_bindings)}
        return $stmt->execute();
    }}

    public function delete() {{
        $query = "DELETE FROM " . $this->table_name . " WHERE `" . $this->primary_key . "` = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->{primary_key});
        return $stmt->execute();
    }}{helper_methods}
{static_helper_method}
}}
?>"""