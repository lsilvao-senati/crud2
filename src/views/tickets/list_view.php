<h2>Lista de Tickets</h2>

<?php if (isset($success_message)): ?>
    <p class="success"><?php echo htmlspecialchars($success_message); ?></p>
<?php endif; ?>

<?php if (empty($tickets)): ?>
    <p>No hay tickets para mostrar.</p>
<?php else: ?>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Solicitante</th>
                <th>Tipo</th>
                <th>Prioridad</th>
                <th>Estado</th>
                <th>Fecha de Creación</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($tickets as $ticket): ?>
                <tr>
                    <td><?php echo htmlspecialchars($ticket['id']); ?></td>
                    <td>
                        <a href="tickets.php?action=view&id=<?php echo $ticket['id']; ?>">
                            <?php echo htmlspecialchars($ticket['titulo']); ?>
                        </a>
                    </td>
                    <td><?php echo htmlspecialchars($ticket['solicitante_nombre']); ?></td>
                    <td><?php echo htmlspecialchars(ucfirst($ticket['tipo'])); ?></td>
                    <td><?php echo htmlspecialchars(ucfirst($ticket['prioridad'])); ?></td>
                    <td><?php echo htmlspecialchars(ucfirst($ticket['estado'])); ?></td>
                    <td><?php echo htmlspecialchars($ticket['fecha_creacion']); ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php endif; ?>
