<h2>Iniciar Sesión</h2>

<?php
if (isset($GLOBALS['success_message'])): ?>
    <p class="success"><?php echo $GLOBALS['success_message']; ?></p>
<?php endif; ?>

<?php if (isset($error)): ?>
    <p class="error"><?php echo $error; ?></p>
<?php endif; ?>

<form action="login.php" method="POST">
    <div>
        <label for="email">Correo Electrónico:</label>
        <input type="email" id="email" name="email" required>
    </div>
    <div>
        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password" required>
    </div>
    <button type="submit">Entrar</button>
</form>
