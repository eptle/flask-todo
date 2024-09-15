let taskList = document.getElementById('task-list');
new Sortable(taskList, {
    animation: 150,
    ghostClass: 'blue-background-class'
});
