def generate_config_php(db_config: dict) -> str:
    return f"""<?php
class Database {{
    private $host = '{db_config['host']}';
    private $db_name = '{db_config['dbname']}';
    private $username = '{db_config['username']}';
    private $password = '{db_config['password']}';
    private $conn;

    public function getConnection() {{
        $this->conn = null;
        try {{
            $this->conn = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name,
                                  $this->username, $this->password);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        }} catch(PDOException $exception) {{
            echo "Error de conexión: " . $exception->getMessage();
        }}
        return $this->conn;
    }}
}}
?>"""
