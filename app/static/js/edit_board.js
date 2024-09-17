$(document).ready(function() {
    $(document).on('click', 'h5.card-title', function() {
        let $h5 = $(this);
        let currentText = $h5.text();
        let boardId = $h5.data('board-id');
        let $input = $('<input>', {
            type: 'text',
            class: 'form-control',
            value: currentText,
        });

        $h5.replaceWith($input);
        $input.focus(); 

        function updateBoardTitle() {
            let newText = $input.val(); 
            let $newH5 = $('<h5>', {
                class: 'card-title',
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
                    console.log('Название доски обновлено');
                },
                error: function(error) {
                    console.log('Ошибка при обновлении названия доски');
                }
            });
        }

        $input.on('keydown', function(e) {
            if (e.key === 'Enter') {
                updateBoardTitle();  
            }
        });

        $input.on('blur', function() {
            updateBoardTitle(); 
        });
    });
});