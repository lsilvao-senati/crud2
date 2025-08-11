<h2>Registro de Usuario</h2>

<?php if (isset($error)): ?>
    <p class="error"><?php echo $error; ?></p>
<?php endif; ?>

<form action="registro.php" method="POST">
    <div>
        <label for="nombre_completo">Nombre Completo:</label>
        <input type="text" id="nombre_completo" name="nombre_completo" required>
    </div>
    <div>
        <label for="email">Correo Electrónico:</label>
        <input type="email" id="email" name="email" required>
    </div>
    <div>
        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password" required>
    </div>
    <div>
        <label for="password_confirm">Confirmar Contraseña:</label>
        <input type="password" id="password_confirm" name="password_confirm" required>
    </div>
    <div>
        <label for="rol">Rol:</label>
        <select id="rol" name="rol" required>
            <option value="cliente">Cliente</option>
            <option value="desarrollador">Desarrollador</option>
        </select>
    </div>
    <button type="submit">Registrarse</button>
</form>
