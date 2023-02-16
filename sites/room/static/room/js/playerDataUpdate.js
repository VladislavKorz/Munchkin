
$(document).ready(function() {
    // Открытие модального окна при клике на имя игрока
    $('.player-date').on('click', function() {
        var $player = $(this).closest('.player');
        var $modal = $('#playerDataEditModal');

        // Заполнение полей модального окна
        $modal.find('.name').text($player.find('.player-name').text());
        $modal.find('.total').text($player.find('.total').text());
        $modal.find('.level').val($player.find('.level').text());
        $modal.find('.power').val($player.find('.power').text());

        // Открытие модального окна
        $player.addClass("active");
        $modal.modal('show');
    });

    // Закрытие модального окна и обновление значений на странице
    $("#playerDataEditModal").on("hide.bs.modal", function () {
        var $player = $('.player.active');
        var $modal = $('#playerDataEditModal');
        $player.removeClass("active");
        $player.find('.level').text($modal.find('.level').val());
        $player.find('.power').text($modal.find('.power').val());
        $player.find('.total').text($modal.find('.total').text());
    });

    // Увеличение и уменьшение уровня игрока
    $('.increase-level').on('click', function() {
        var $level = $(this).closest('.player').find('.level');
        var levelValue = parseInt($level.val());
        $level.val(levelValue + 1);
    });

    $('.decrease-level').on('click', function() {
    var $level = $(this).closest('.player').find('.level');
    var levelValue = parseInt($level.val());
        if (levelValue > 1) {
        $level.val(levelValue - 1);
        }
    });

    // Увеличение и уменьшение силы игрока
    $('.increase-power').on('click', function() {
        var $power = $(this).closest('.player').find('.power');
        var powerValue = parseInt($power.val());
        $power.val(powerValue + 1);
    });

    $('.decrease-power').on('click', function() {
        var $power = $(this).closest('.player').find('.power');
        var powerValue = parseInt($power.val());
        if (powerValue > 1) {
        $power.val(powerValue - 1);
        }
    });

    // Расчет общей силы игрока
    $('#playerDataEditModal').on('click', '.player-data-edit', function() {
        var $modal = $('#playerDataEditModal');
        var levelValue = parseInt($modal.find('.level').val());
        var powerValue = parseInt($modal.find('.power').val());
        var total = levelValue + powerValue;
        $modal.find('.total').text(total);
    });
});