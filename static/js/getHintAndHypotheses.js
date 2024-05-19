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
    // Получаем ссылку на контейнер, где будут наши элементы
    let competenciesContainer = document.querySelector('.myCompetenciesInputForms');
    let addButton = document.querySelector('.btnAddikDiv #addCompetencies');

    // Добавляем обработчик событий на кнопку "+"
    addButton.addEventListener('click', function() {
        // Создаем новый элемент
        let newCompetency = document.createElement('div');
        newCompetency.className = 'enumerationCompetencies';
        newCompetency.innerHTML = `
            <input type="text" class="myCompetenciesInput" name="name" />
            <button class="deletik" id="deleteCompetencies">-</button>
        `;

        // Добавляем обработчик событий на кнопку "-" внутри нового элемента
        newCompetency.querySelector('#deleteCompetencies').addEventListener('click', function() {
            // Удаляем элемент при нажатии на "-"
            competenciesContainer.removeChild(newCompetency);
        });

        // Добавляем новый элемент в контейнер перед кнопкой "+"
        competenciesContainer.insertBefore(newCompetency, addButton.parentNode);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Получаем ссылку на контейнер, где будут наши элементы
    let interestsContainer = document.querySelector('.myInterestsInputForms');
    let addButtonInterests = document.querySelector('.btnAddikDiv #addInterests');

    // Добавляем обработчик событий на кнопку "+"
    addButtonInterests.addEventListener('click', function() {
        // Создаем новый элемент
        let newInterest = document.createElement('div');
        newInterest.className = 'enumerationInterests';
        newInterest.innerHTML = `
            <input type="text" class="myInterestsInput" name="name" />
            <button class="deletik" id="deleteInterests">-</button>
        `;

        // Добавляем обработчик событий на кнопку "-" внутри нового элемента
        newInterest.querySelector('#deleteInterests').addEventListener('click', function() {
            // Удаляем элемент при нажатии на "-"
            interestsContainer.removeChild(newInterest);
        });

        // Добавляем новый элемент в контейнер перед кнопкой "+"
        interestsContainer.insertBefore(newInterest, addButtonInterests.parentNode);
    });
});


function toggleInfo(element) {
    const ideaContainer = element.closest('.ideaContainer');
    const infoIdea = ideaContainer.querySelector('.infoIdea');
    
    if (infoIdea && infoIdea.innerHTML.trim() !== '') {
        ideaContainer.classList.toggle('open');
    }
}