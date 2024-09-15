let taskList = document.getElementById('task-list');
new Sortable(taskList, {
    animation: 150,
    onEnd: function (evt) {
        let items = document.querySelectorAll('#task-list li');
        let positions = [];
        items.forEach((item, index) => {
            positions.push({ id: item.dataset.taskId, position: index });
        });

        fetch('/update-task-positions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(positions),
        }).then(response => response.json()).then(data => {
            console.log('Updated successfully', data);
        });
    },
});