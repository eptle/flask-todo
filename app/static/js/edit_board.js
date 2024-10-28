$(document).ready(function() {
    $(document).on('dblclick', 'h5.card-title', function() {
        let $h5 = $(this);
        let boardId = $h5.data('board-id');
        let currentText = $h5.text();
        let $input = $('<input>', {
            type: 'text',
            class: 'card-title',
            value: currentText,
        });

        $h5.replaceWith($input);
        $input.focus(); 

        function updateTask() {
            let newText = $input.val();
            if (newText === '') {
                newText = 'Board';
            }
            let $newH5 = $('<h5>', {
                class: 'card-title w-50',
                text: newText,
                'data-board-id': boardId  
            });

            $input.replaceWith($newH5);  
            $.ajax({
                url: '/edit-board',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    board_id: boardId,
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

        $input.on('blur', function() {
            updateTask(); 
        });
    });
});