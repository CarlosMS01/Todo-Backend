document.getElementById('toggle-theme').addEventListener('click', () => {
  document.body.classList.toggle('dark');
});

function enableDragAndDrop() {
  const tasks = document.querySelectorAll('.task');
  tasks.forEach(task => {
    task.setAttribute('draggable', true);

    task.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', task.dataset.id);
    });
  });

  const container = document.getElementById('task-list');
  container.addEventListener('dragover', e => e.preventDefault());

  container.addEventListener('drop', async e => {
    e.preventDefault();
    const id = e.dataTransfer.getData('text/plain');
    // Aquí podrías actualizar el orden o estado en la API
    console.log(`Tarea soltada: ${id}`);
  });
}

document.querySelectorAll('#filters button').forEach(btn => {
  btn.addEventListener('click', () => {
    const estado = btn.dataset.filter;
    document.querySelectorAll('.task').forEach(task => {
      task.style.display = task.dataset.status === estado ? 'block' : 'none';
    });
  });
});


async function fetchTasks() {
  const res = await fetch('https://tu-backend-en-render.com/api/tasks', {
    credentials: 'include' // 🔐 envía cookies automáticamente
  });
  const tasks = await res.json();
  renderTasks(tasks);
}
