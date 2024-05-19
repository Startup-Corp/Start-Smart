// Функция для показа всплывающей подсказки
function showTooltip(btnId, tooltipId) {
    document.getElementById(btnId).addEventListener('mouseover', function() {
        var tooltip = document.getElementById(tooltipId);
        tooltip.classList.remove('hide');
        tooltip.classList.add('show');
    });

    document.getElementById(btnId).addEventListener('mouseout', function() {
        var tooltip = document.getElementById(tooltipId);
        tooltip.classList.remove('show');
        tooltip.classList.add('hide');
    });
}


showTooltip('hintBtnTitle', 'toolchik1');
showTooltip('hintBtnProblem', 'toolchik2');
showTooltip('hintBtnDeci', 'toolchik3');