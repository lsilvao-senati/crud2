<?php if (isset($ticket) && $ticket): ?>
    <h2>Ticket #<?php echo htmlspecialchars($ticket['id']); ?>: <?php echo htmlspecialchars($ticket['titulo']); ?></h2>

    <div class="ticket-details">
        <div class="ticket-meta">
            <p><strong>Solicitante:</strong> <?php echo htmlspecialchars($ticket['solicitante_nombre']); ?></p>
            <p><strong>Fecha de Creación:</strong> <?php echo htmlspecialchars($ticket['fecha_creacion']); ?></p>
            <p><strong>Última Actualización:</strong> <?php echo htmlspecialchars($ticket['fecha_actualizacion']); ?></p>
        </div>
        <div class="ticket-status">
            <p><strong>Tipo:</strong> <span class="badge type-<?php echo htmlspecialchars($ticket['tipo']); ?>"><?php echo htmlspecialchars(ucfirst($ticket['tipo'])); ?></span></p>
            <p><strong>Prioridad:</strong> <span class="badge priority-<?php echo htmlspecialchars($ticket['prioridad']); ?>"><?php echo htmlspecialchars(ucfirst($ticket['prioridad'])); ?></span></p>
            <p><strong>Estado:</strong> <span class="badge status-<?php echo htmlspecialchars($ticket['estado']); ?>"><?php echo htmlspecialchars(ucfirst($ticket['estado'])); ?></span></p>
        </div>
    </div>

    <div class="ticket-content">
        <h3>Descripción</h3>
        <p><?php echo nl2br(htmlspecialchars($ticket['descripcion'])); ?></p>
    </div>

    <?php if (!empty($ticket['modulo_afectado']) || !empty($ticket['pasos_reproducir'])): ?>
    <div class="ticket-technical-info">
        <h3>Información Técnica</h3>
        <?php if (!empty($ticket['modulo_afectado'])): ?>
            <p><strong>Módulo Afectado:</strong> <?php echo htmlspecialchars($ticket['modulo_afectado']); ?></p>
        <?php endif; ?>
        <?php if (!empty($ticket['pasos_reproducir'])): ?>
            <h4>Pasos para reproducir el error:</h4>
            <pre><?php echo htmlspecialchars($ticket['pasos_reproducir']); ?></pre>
        <?php endif; ?>
    </div>
    <?php endif; ?>

    <a href="tickets.php?action=list">Volver a la lista</a>

<?php else: ?>
    <h2>Ticket no encontrado</h2>
    <p>El ticket que buscas no existe o no tienes permiso para verlo.</p>
    <a href="tickets.php?action=list">Volver a la lista</a>
<?php endif; ?>
