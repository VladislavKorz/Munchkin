// Смена пола
$(document).on('click', '.player-gender', function () {
    let $player = $(this).closest('.player');
    let gender = $(this).find('.fa');
    let gender_val = 'O';
    let gender_class = 'fa-mars';
    if (gender.hasClass('fa-mars')) {
        gender_val = 'F';
        gender_class = 'fa-venus'
    } else {
        gender_val = 'M';
    }
    gender.removeClass('fa-mars').removeClass('fa-venus').addClass('fa-spinner');
    $.ajax({
        url: changeRoomPlayer_URL,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrf_token,
            user_room: $player.attr('player'),
            gender: gender_val,
        },
        success: function (data) {
            gender.removeClass('fa-spinner').addClass(gender_class);
            if (gender_val == 'M') {
                gender_val = 'он брутальный мужик'
            } else {
                gender_val = 'она храбрая женщина'
            }
        }
    });
});
