let taskList = document.getElementById('task-list');

let sortable = new Sortable(taskList, {
    animation: 150,
    onEnd: function(evt) {
        let task_order = [];
        let tasks = taskList.children;

        for (let i = 0; i < tasks.length; i++) {
            task_order.push({
                id: tasks[i].getAttribute('data-task-id'),
                position: i + 1
            });
        }
        console.log(task_order)

        fetch('/update-task-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}' 
            },
            body: JSON.stringify(task_order)
        }).then(response => {
            if (!response.ok) {
                alert('Ошибка обновления позиции');
            }
        });
    }
});