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


document.addEventListener('DOMContentLoaded', function() {
    function setupDynamicList(containerSelector, addButtonSelector, itemClassName, inputClassName, deleteButtonId) {
        // Получаем ссылку на контейнер, где будут наши элементы
        let container = document.querySelector(containerSelector);
        let addButton = document.querySelector(addButtonSelector);

        // Добавляем обработчик событий на кнопку "+"
        addButton.addEventListener('click', function() {
            // Создаем новый элемент
            let newItem = document.createElement('div');
            newItem.className = itemClassName;
            newItem.innerHTML = `
                <input type="text" class="${inputClassName}" name="name" />
                <button class="deletik" id="${deleteButtonId}">-</button>
            `;

            // Добавляем обработчик событий на кнопку "-" внутри нового элемента
            newItem.querySelector(`#${deleteButtonId}`).addEventListener('click', function() {
                // Удаляем элемент при нажатии на "-"
                container.removeChild(newItem);
            });

            // Добавляем новый элемент в контейнер перед кнопкой "+"
            container.insertBefore(newItem, addButton.parentNode);
        });
    }

    // Вызовы функции для компетенций и интересов
    setupDynamicList('.myCompetenciesInputForms', '.btnAddikDiv #addCompetencies', 'enumerationCompetencies', 'myCompetenciesInput', 'deleteCompetencies');
    setupDynamicList('.myInterestsInputForms', '.btnAddikDiv #addInterests', 'enumerationInterests', 'myInterestsInput', 'deleteInterests');
});



function toggleInfo(element) {
    const ideaContainer = element.closest('.ideaContainer');
    const infoIdea = ideaContainer.querySelector('.infoIdea');
    
    if (infoIdea && infoIdea.innerHTML.trim() !== '') {
        ideaContainer.classList.toggle('open');
    }
}