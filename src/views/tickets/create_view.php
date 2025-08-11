<h2>Crear Nuevo Ticket</h2>

<?php if (isset($error)): ?>
    <p class="error"><?php echo htmlspecialchars($error); ?></p>
<?php endif; ?>

<form action="crear_ticket.php" method="POST">

    <div>
        <label for="titulo">Título de la solicitud:</label>
        <input type="text" id="titulo" name="titulo" required>
        <small>Un resumen breve y claro del cambio deseado.</small>
    </div>

    <div>
        <label for="tipo">Tipo de solicitud:</label>
        <select id="tipo" name="tipo" required>
            <option value="mejora">Mejora</option>
            <option value="error">Corrección de error (Bug)</option>
            <option value="nueva_funcionalidad">Nueva funcionalidad</option>
        </select>
    </div>

    <div>
        <label for="prioridad">Prioridad:</label>
        <select id="prioridad" name="prioridad" required>
            <option value="baja">Baja</option>
            <option value="media">Media</option>
            <option value="alta">Alta</option>
        </select>
    </div>

    <div>
        <label for="descripcion">Descripción detallada:</label>
        <textarea id="descripcion" name="descripcion" rows="6" required></textarea>
        <small>Explica el problema o la necesidad. Describe el "qué" y el "por qué" de tu solicitud.</small>
    </div>

    <fieldset>
        <legend>Información Técnica (Opcional)</legend>
        <div>
            <label for="modulo_afectado">Sistema o Módulo afectado:</label>
            <input type="text" id="modulo_afectado" name="modulo_afectado">
            <small>Ej: "Módulo de Reportes", "Página de inicio de sesión".</small>
        </div>
        <div>
            <label for="pasos_reproducir">Pasos para reproducir el error (si es un bug):</label>
            <textarea id="pasos_reproducir" name="pasos_reproducir" rows="6"></textarea>
            <small>Describe el camino exacto para que el equipo técnico pueda replicar el problema.</small>
        </div>
    </fieldset>

    <button type="submit">Enviar Solicitud</button>
</form>
