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
            f"            ['local_column' => '{fk['local_column']}', 'referenced_table' => '{fk['referenced_table']}', 'referenced_column' => '{fk['referenced_column']}']"
        )
    php_foreign_keys_data = "[\n" + ",\n".join(php_fks_list_items) + "\n        ]"

    # CORREGIDO: Generar métodos auxiliares para obtener datos de tablas relacionadas
    helper_methods = ""
    referenced_tables = set()
    for fk in foreign_keys:
        table = fk['referenced_table']
        if table not in referenced_tables:
            referenced_tables.add(table)
            method_name = f"getAll{table.capitalize()}"
            helper_methods += f"""
    // Método para obtener todos los registros de {table} (para formularios)
    public function {method_name}() {{
        $query = "SELECT id, nombre FROM {table} ORDER BY nombre";
        $stmt = $this->conn->prepare($query);
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

            // Alias para mostrar el nombre de la tabla relacionada
            $alias_for_display = $referenced_table_name . "_nombre";
            
            // Seleccionar la columna 'nombre' de la tabla referenciada (asumiendo que tienen 'nombre')
            $select_columns[] = "`" . $referenced_table_name . "`.`nombre` AS `" . $alias_for_display . "`";
            
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
}}
?>"""