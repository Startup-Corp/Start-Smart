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


showTooltip('hintBtnProductTitle', 'tool-product');
showTooltip('hintBtnImageProduct', 'tool-image-product');
showTooltip('hintBtnFunnel', 'tool-funnel');
showTooltip('hintBtnMetrics', 'tool-metric');
showTooltip('hintBtnTargetValue', 'tool-target-value');
showTooltip('hintBtnAdditionalData', 'tool-additional-data');

