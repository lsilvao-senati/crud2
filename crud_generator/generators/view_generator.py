def get_input_type(sql_type: str) -> str:
    # Determines the appropriate HTML input type based on the SQL data type.
    if sql_type in ['int', 'integer', 'bigint', 'smallint', 'tinyint']:
        return 'number'
    elif sql_type in ['date']:
        return 'date'
    elif sql_type in ['datetime', 'timestamp']:
        return 'datetime-local'
    elif sql_type in ['text', 'longtext']:
        return 'textarea'
    elif sql_type in ['boolean', 'bool']:
        return 'checkbox'
    else:
        return 'text'


def generate_view_index(table_name, columns, foreign_keys: list):
    # Generates the PHP code for the index (list) view of a table.
    # This view displays all records in a table format.

    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    primary_key = next((col['name'] for col in columns if col.get('primary_key')), 'id')

    # Generate table headers, including aliases for foreign key columns.
    headers_list = []
    for col in columns:
        is_fk_column = False
        for fk in foreign_keys:
            if fk['local_column'] == col['name']:
                # Use the referenced table name and display column as header.
                headers_list.append(f"                <th>{fk['referenced_table'].replace('_', ' ').title()} ({fk['display_column'].replace('_', ' ').title()})</th>")
                is_fk_column = True
                break
        if not is_fk_column:
            headers_list.append(f"                <th>{col['name'].replace('_', ' ').title()}</th>")
    headers_str = '\n'.join(headers_list)

    # Generate table rows, using the aliased names for foreign keys when applicable.
    rows_list = []
    for col in columns:
        is_fk_column = False
        for fk in foreign_keys:
            if fk['local_column'] == col['name']:
                # Access data using the alias generated in the model: referenced_table_display_column
                alias = f"{fk['referenced_table']}_{fk['display_column']}"
                rows_list.append(f"                        <td><?= htmlspecialchars($row['{alias}']) ?></td>")
                is_fk_column = True
                break
        if not is_fk_column:
            rows_list.append(f"                        <td><?= htmlspecialchars($row['{col['name']}']) ?></td>")
    rows_str = '\n'.join(rows_list)

    return f"""<?php
$title = "Gestión de {class_name}";
ob_start();
?>
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Gestión de {class_name}</h2>
    <a href="index.php?controller={table_name}&action=create" class="btn btn-success">
        <i class="bi bi-plus-circle"></i> Nuevo {class_name.replace('_', ' ').title()}
    </a>
</div>

<?php if (isset($msg) && $msg == 'created'): ?>
    <div class="alert alert-success">Registro creado exitosamente.</div>
<?php elseif (isset($msg) && $msg == 'updated'): ?>
    <div class="alert alert-success">Registro actualizado exitosamente.</div>
<?php elseif (isset($msg) && $msg == 'deleted'): ?>
    <div class="alert alert-danger">Registro eliminado exitosamente.</div>
<?php endif; ?>

<div class="card shadow-sm">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0">Lista de {class_name.replace('_', ' ').title()}</h5>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
{headers_str}
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (!empty(${table_name}s)): ?> <!-- Check if the data array is not empty -->
                        <?php foreach (${table_name}s as $row): ?> <!-- Iterate over the data array -->
                        <tr>
{rows_str}
                            <td>
                                <a href="index.php?controller={table_name}&action=edit&id=<?= htmlspecialchars($row['{primary_key}']) ?>" class="btn btn-sm btn-primary"><i class="bi bi-pencil"></i></a>
                                <a href="index.php?controller={table_name}&action=delete&id=<?= htmlspecialchars($row['{primary_key}']) ?>" class="btn btn-sm btn-danger" onclick="return confirm('¿Estás seguro de que quieres eliminar este registro?');"><i class="bi bi-trash"></i></a>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    <?php else: ?>
                        <tr>
                            <td colspan="{len(columns) + 1}" class="text-center">No hay registros.</td> <!-- Adjusted colspan for FK columns -->
                        </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php
$content = ob_get_clean();
include __DIR__ . '/../layout.php';
?>"""


def generate_view_create(table_name, columns, foreign_keys: list) -> str:
    # Generates the PHP code for the create (new record) view of a table.

    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    primary_key = next((col['name'] for col in columns if col.get('primary_key')), 'id')

    form_fields = []
    for col in columns:
        if col.get('auto_increment'):
            continue # Skip auto-increment columns in create form

        label = col['name'].replace('_', ' ').title()
        required_attr = 'required' if not col['nullable'] and not col.get('primary_key') else ''
        input_type = get_input_type(col['type'])

        # Check if the current column is a foreign key
        is_foreign_key = False
        fk_info = None
        for fk in foreign_keys:
            if fk['local_column'] == col['name']:
                is_foreign_key = True
                fk_info = fk
                break

        if is_foreign_key:
            # Generate a SELECT/dropdown for foreign keys
            referenced_table_name = fk_info['referenced_table']
            referenced_id_column = fk_info['referenced_column'] # Usually 'id' or the primary key of the referenced table
            
            # This requires fetching the data for the select box, which is done in the controller.
            # The view just needs to iterate over the passed data.
            field = f"""        <div class="mb-3">
            <label for="{col['name']}" class="form-label">{label}{' *' if required_attr else ''}</label>
            <select class="form-control" id="{col['name']}" name="{col['name']}" {required_attr}>
                <option value="">Seleccione un/a {label}</option>
                <?php foreach (${referenced_table_name}s as ${referenced_table_name}_item): ?>
                    <option value="<?= htmlspecialchars(${referenced_table_name}_item['{referenced_id_column}']) ?>">
                        <?= htmlspecialchars(${referenced_table_name}_item['{fk_info['display_column']}']) ?> </option>
                <?php endforeach; ?>
            </select>
        </div>"""
        elif input_type == 'textarea':
            field = f"""        <div class="mb-3">
            <label for="{col['name']}" class="form-label">{label}{' *' if required_attr else ''}</label>
            <textarea class="form-control" id="{col['name']}" name="{col['name']}" rows="3" {required_attr}></textarea>
        </div>"""
        elif input_type == 'checkbox':
             field = f"""        <div class="form-check mb-3">
            <input type="checkbox" class="form-check-input" id="{col['name']}" name="{col['name']}" value="1">
            <label class="form-check-label" for="{col['name']}">{label}</label>
        </div>"""
        else:
            field = f"""        <div class="mb-3">
            <label for="{col['name']}" class="form-label">{label}{' *' if required_attr else ''}</label>
            <input type="{input_type}" class="form-control" id="{col['name']}" name="{col['name']}" {required_attr}>
        </div>"""
        form_fields.append(field)

    return f"""<?php
$title = "Crear Nuevo {class_name}";
ob_start();
?>
<div class="card shadow-sm">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0">Crear Nuevo {class_name.replace('_', ' ').title()}</h5>
    </div>
    <div class="card-body">
        <form method="POST" action="index.php?controller={table_name}&action=store">
{chr(10).join(form_fields)}
            <button type="submit" class="btn btn-primary"><i class="bi bi-plus-circle"></i> Crear</button>
            <a href="index.php?controller={table_name}&action=index" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
<?php
$content = ob_get_clean();
include __DIR__ . '/../layout.php';
?>"""


def generate_view_edit(table_name, columns, foreign_keys: list) -> str:
    # Generates the PHP code for the edit (update record) view of a table.

    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    form_fields = []
    primary_key = next((col['name'] for col in columns if col.get('primary_key')), 'id')

    for col in columns:
        label = col['name'].replace('_', ' ').title()
        if col.get('auto_increment'):
            # The auto_increment field is the PK and is sent as hidden for the UPDATE
            field = f"""        <input type="hidden" name="{col['name']}" value="<?= ${table_name}->{col['name']} ?>">"""
        else:
            input_type = get_input_type(col['type'])
            required_attr = 'required' if not col.get('nullable') else ''

            is_foreign_key = False
            fk_info = None
            for fk in foreign_keys:
                if fk['local_column'] == col['name']:
                    is_foreign_key = True
                    fk_info = fk
                    break

            if is_foreign_key:
                referenced_table_name = fk_info['referenced_table']
                referenced_id_column = fk_info['referenced_column']
                
                field = f"""        <div class="mb-3">
            <label for="{col['name']}" class="form-label">{label}{' *' if required_attr else ''}</label>
            <select class="form-control" id="{col['name']}" name="{col['name']}" {required_attr}>
                <option value="">Seleccione un/a {label}</option>
                <?php foreach (${referenced_table_name}s as ${referenced_table_name}_item): ?>
                    <option value="<?= htmlspecialchars(${referenced_table_name}_item['{referenced_id_column}']) ?>"
                        <?= (${table_name}->{col['name']} == ${referenced_table_name}_item['{referenced_id_column}']) ? 'selected' : '' ?>>
                        <?= htmlspecialchars(${referenced_table_name}_item['{fk_info['display_column']}']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>"""
            elif input_type == 'textarea':
                field = f"""        <div class="mb-3">
            <label for="{col['name']}" class="form-label">{label}{' *' if required_attr else ''}</label>
            <textarea class="form-control" id="{col['name']}" name="{col['name']}" {required_attr}><?= htmlspecialchars(${table_name}->{col['name']}) ?></textarea>
        </div>"""
            elif input_type == 'checkbox':
                field = f"""        <div class="form-check mb-3">
            <input type="checkbox" class="form-check-input" id="{col['name']}" name="{col['name']}" value="1" <?= ${table_name}->{col['name']} ? 'checked' : '' ?>>
            <label class="form-check-label" for="{col['name']}">{label}</label>
        </div>"""
            else:
                # Handle date/datetime types if the value is null or empty
                if input_type in ['date', 'datetime-local']:
                    field = f"""        <div class="mb-3">
            <label for="{col['name']}" class="form-label">{label}{' *' if required_attr else ''}</label>
            <input type="{input_type}" class="form-control" id="{col['name']}" name="{col['name']}" value="<?= htmlspecialchars(${table_name}->{col['name']} ?? '') ?>" {required_attr}>
        </div>"""
                else:
                    field = f"""        <div class="mb-3">
            <label for="{col['name']}" class="form-label">{label}{' *' if required_attr else ''}</label>
            <input type="{input_type}" class="form-control" id="{col['name']}" name="{col['name']}" value="<?= htmlspecialchars(${table_name}->{col['name']}) ?>" {required_attr}>
        </div>"""
        form_fields.append(field)

    return f"""<?php
$title = "Editar {class_name}";
ob_start();
?>
<div class="card shadow-sm">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0">Editar {class_name.replace('_', ' ').title()}</h5>
    </div>
    <div class="card-body">
        <form method="POST" action="index.php?controller={table_name}&action=update">
{chr(10).join(form_fields)}
            <button type="submit" class="btn btn-primary"><i class="bi bi-save"></i> Actualizar</button>
            <a href="index.php?controller={table_name}&action=index" class="btn btn-secondary"><i class="bi bi-arrow-left"></i> Cancelar</a>
        </form>
    </div>
</div>
<?php
$content = ob_get_clean();
// CORRECTION HERE
include(__DIR__ . '/../layout.php');
?>"""
