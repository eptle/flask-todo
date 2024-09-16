fetch('/edit-board', {
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