import re

PREFERRED_DISPLAY_COLUMNS = ['nombre', 'name', 'title', 'titulo', 'descripcion', 'description', 'username', 'login', 'email']

class SQLParser:
    def __init__(self, sql_path):
        self.sql_path = sql_path

    def parse(self):
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        sql_content = ""

        for encoding in encodings:
            try:
                with open(self.sql_path, 'r', encoding=encoding) as f:
                    sql_content = f.read()
                print(f"✅ Archivo leído con codificación: {encoding}")
                break
            except UnicodeDecodeError:
                continue

        if not sql_content:
            raise Exception("❌ No se pudo leer el archivo SQL con una codificación válida")

        # Limpieza de comentarios y espacios
        sql_content = re.sub(r'--.*?$', '', sql_content, flags=re.MULTILINE)
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        sql_content = re.sub(r'\n{2,}', '\n', sql_content)
        sql_content = sql_content.strip()

        print(f"DEBUG: Contenido SQL limpio (primeras 1000 chars):\n{sql_content[:1000]}")
        print(f"DEBUG: Longitud total del contenido SQL limpio: {len(sql_content)}")

        tables = {}
        matches_found = 0

        for match in re.finditer(r'CREATE\s+TABLE\s+[`"]?(\w+)[`"]?\s*\((.*?)\)(?:;)?', sql_content, re.DOTALL | re.IGNORECASE):
            matches_found += 1
            table_name_raw = match.group(1)
            table_definition_content = match.group(2)

            print(f"DEBUG: Tabla '{table_name_raw}' encontrada.")

            columns, foreign_keys, primary_key_name = self.parse_table_definition_content(table_definition_content)

            if primary_key_name is None:
                for col in columns:
                    if col['name'].lower() == 'id':
                        col['primary_key'] = True
                        primary_key_name = 'id'
                        break
                if primary_key_name is None and columns:
                    columns[0]['primary_key'] = True
                    primary_key_name = columns[0]['name']

            tables[table_name_raw] = {
                'columns': columns,
                'foreign_keys': foreign_keys,
                'primary_key': primary_key_name
            }

        print(f"DEBUG: Se encontraron {matches_found} coincidencias de CREATE TABLE.")

        # Enhance foreign keys with display columns
        for table_name, table_data in tables.items():
            print(f"DEBUG: Processing foreign keys for table: {table_name}")
            for fk in table_data['foreign_keys']:
                referenced_table_name = fk['referenced_table']
                referenced_column_name = fk['referenced_column'] # This is the PK of the referenced table
                display_column_for_fk = referenced_column_name # Default to PK

                if referenced_table_name in tables:
                    columns_of_referenced_table = tables[referenced_table_name]['columns']
                    found_preferred = False
                    for preferred_name in PREFERRED_DISPLAY_COLUMNS:
                        for col_data in columns_of_referenced_table:
                            if col_data['name'].lower() == preferred_name.lower():
                                display_column_for_fk = col_data['name']
                                found_preferred = True
                                print(f"DEBUG: Found preferred display column '{display_column_for_fk}' for FK {fk['local_column']} -> {referenced_table_name}.{referenced_column_name}")
                                break
                        if found_preferred:
                            break
                    if not found_preferred:
                        print(f"DEBUG: No preferred display column found for FK {fk['local_column']} -> {referenced_table_name}.{referenced_column_name}. Defaulting to PK '{display_column_for_fk}'.")
                else:
                    print(f"WARN: Referenced table '{referenced_table_name}' not found in parsed tables. Cannot determine display column for FK from {table_name}.{fk['local_column']}.")

                fk['display_column'] = display_column_for_fk
                print(f"DEBUG: FK details for {table_name}.{fk['local_column']}: {fk}")


        return tables

    def parse_table_definition_content(self, content_str):
        columns = []
        foreign_keys = []
        primary_key_found = None

        lines = [line.strip() for line in content_str.split('\n') if line.strip()]

        for line_to_process in lines:
            if line_to_process.endswith(','):
                line_to_process = line_to_process[:-1].strip()

            if not line_to_process:
                continue

            # Broader check for FOREIGN KEY lines
            if line_to_process.strip().upper().startswith('FOREIGN KEY'):
                # Attempt to parse it for FK details using the existing detailed regex
                fk_match_detailed = re.match(
                    r'FOREIGN\s+KEY\s*\([`"]?(\w+)[`"]?\)\s*REFERENCES\s*[`"]?(\w+)[`"]?\s*\([`"]?(\w+)[`"]?\)(?:\s*ON\s+DELETE\s+\w+)?(?:\s*ON\s+UPDATE\s+\w+)?',
                    line_to_process,
                    re.IGNORECASE
                )
                if fk_match_detailed:
                    local_column, referenced_table, referenced_column = fk_match_detailed.groups()
                    foreign_keys.append({
                        'local_column': local_column,
                        'referenced_table': referenced_table,
                        'referenced_column': referenced_column
                        # display_column will be added later in the main parse method
                    })
                else:
                    print(f"DEBUG: Line started with FOREIGN KEY but did not match detailed FK regex: '{line_to_process}'")
                continue # Always continue to prevent falling through to column parsing

            # PRIMARY KEY (línea separada)
            pk_match = re.match(
                r'PRIMARY\s+KEY\s*\([`"]?(\w+)[`"]?\)',
                line_to_process,
                re.IGNORECASE
            )
            if pk_match:
                if primary_key_found is None:
                    primary_key_found = pk_match.group(1)
                continue

            # Otras restricciones que ignoramos
            constraint_keyword_match = re.match(r'^(UNIQUE|KEY|CONSTRAINT|INDEX)(?:\s.*)?$', line_to_process, re.IGNORECASE)
            if constraint_keyword_match:
                continue

            # Columnas normales
            col_match = re.match(
                r'[`"]?(\w+)[`"]?\s+(\w+)(?:\((\d+)(?:,\s*\d+)?\))?\s*(.*)',
                line_to_process,
                re.IGNORECASE
            )
            if col_match:
                col_name, sql_type, length, details = col_match.groups()

                is_primary_key_inline = 'PRIMARY KEY' in details.upper()
                if is_primary_key_inline and primary_key_found is None:
                    primary_key_found = col_name

                col_info = {
                    'name': col_name,
                    'type': sql_type.lower(),
                    'length': int(length) if length else None,
                    'nullable': 'NOT NULL' not in details.upper(),
                    'auto_increment': 'AUTO_INCREMENT' in details.upper() or 'IDENTITY' in details.upper(),
                    'primary_key': is_primary_key_inline
                }
                columns.append(col_info)
            else:
                print(f"DEBUG: Línea no procesada en definición de tabla: '{line_to_process}'")

        return columns, foreign_keys, primary_key_found
