import os
from .parser import SQLParser
from .db_config import generate_config_php
from .generators.model_generator import generate_model
from .generators.controller_generator import generate_controller
from .generators.view_generator import (
    generate_view_index, generate_view_create, generate_view_edit
)
from .generators.layout_generator import (
    generate_layout, generate_login_view, generate_logout_view
)
from .generators.index_generator import generate_index_file
from .generators.readme_generator import generate_readme


class CRUDGenerator:
    def __init__(self, sql_file_path: str, output_dir: str = "generated_crud"):
        self.sql_file_path = sql_file_path
        self.output_dir = output_dir
        # self.tables now contains { 'table_name': {'columns': [...], 'foreign_keys': [...]}}
        self.tables = {}
        self.db_config = {
            'host': 'localhost',
            'dbname': 'mi_base',
            'username': 'root',
            'password': ''
        }

    def parse_sql_file(self):
        parser = SQLParser(self.sql_file_path)
        self.tables = parser.parse()

    def create_directory_structure(self):
        # Base directories
        dirs = [
            self.output_dir,
            f"{self.output_dir}/config",
            f"{self.output_dir}/models",
            f"{self.output_dir}/views",
            f"{self.output_dir}/controllers"
        ]
        # Create view directories for each table
        for table_name in self.tables.keys():
            dirs.append(f"{self.output_dir}/views/{table_name}")

        for d in dirs:
            os.makedirs(d, exist_ok=True)
            print(f"📁 Directorio creado: {d}")

    def generate_all_files(self):
        # Generate Database configuration file
        with open(f"{self.output_dir}/config/Database.php", 'w', encoding='utf-8') as f:
            f.write(generate_config_php(self.db_config))

        # Generate Login, Logout, and Main Layout views
        with open(f"{self.output_dir}/login.php", 'w', encoding='utf-8') as f:
            f.write(generate_login_view())
        
        with open(f"{self.output_dir}/logout.php", 'w', encoding='utf-8') as f:
            f.write(generate_logout_view())

        # Generate main layout file within the 'views' folder
        with open(f"{self.output_dir}/views/layout.php", 'w', encoding='utf-8') as f:
            f.write(generate_layout(self.tables))

        # Generate index.php for routing
        with open(f"{self.output_dir}/index.php", 'w', encoding='utf-8') as f:
            f.write(generate_index_file(self.tables))

        # Generate Models, Controllers, and Views for each table
        for table_name, table_data in self.tables.items():
            columns = table_data['columns']
            foreign_keys = table_data['foreign_keys'] # Get foreign keys

            class_name = ''.join(w.capitalize() for w in table_name.split('_'))

            # Models
            # Pass foreign_keys to generate_model so it can create JOIN queries
            with open(f"{self.output_dir}/models/{class_name}.php", 'w', encoding='utf-8') as f:
                f.write(generate_model(table_name, columns, foreign_keys))

            # Controllers
            with open(f"{self.output_dir}/controllers/{class_name}Controller.php", 'w', encoding='utf-8') as f:
                f.write(generate_controller(table_name, columns, foreign_keys))

            # Views
            with open(f"{self.output_dir}/views/{table_name}/index.php", 'w', encoding='utf-8') as f:
                # Pass foreign_keys to generate_view_index for displaying joined data
                f.write(generate_view_index(table_name, columns, foreign_keys))

            with open(f"{self.output_dir}/views/{table_name}/create.php", 'w', encoding='utf-8') as f:
                # Pass foreign_keys to generate_view_create for dropdowns
                f.write(generate_view_create(table_name, columns, foreign_keys))

            with open(f"{self.output_dir}/views/{table_name}/edit.php", 'w', encoding='utf-8') as f:
                # Pass foreign_keys to generate_view_edit for dropdowns and pre-selection
                f.write(generate_view_edit(table_name, columns, foreign_keys))

        # Generate README
        with open(f"{self.output_dir}/README.md", 'w', encoding='utf-8') as f:
            f.write(generate_readme(self.tables, self.output_dir))
