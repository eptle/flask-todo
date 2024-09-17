$(document).ready(function() {
    $(document).on('click', 'p.sort-task', function() {
        let $p = $(this);
        let currentText = $p.text();
        let $input = $('<input>', {
            type: 'text',
            class: 'form-control',
            value: currentText,
        });

        $p.replaceWith($input);
        $input.focus(); 

        function updateTask() {
            let newText = $input.val(); 
            let $newP = $('<p>', {
                class: 'sort-task',
                text: newText  
            });

            $input.replaceWith($newP);  

            let taskId = $newP.closest('li').data('task-id');
            $.ajax({
                url: '/edit-task',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    task_id: taskId,
                    new_title: newText
                }),
                success: function(response) {
                    console.log('Задача обновлена');
                },
                error: function(error) {
                    console.log('Ошибка при обновлении задачи');
                }
            });
        }

        $input.on('keydown', function(e) {
            if (e.key === 'Enter') {
                updateTask(); 
            }
        });

        // Обработка потери фокуса (blur)
        $input.on('blur', function() {
            updateTask(); 
        });
    });
});