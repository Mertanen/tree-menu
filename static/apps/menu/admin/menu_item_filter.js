document.addEventListener('DOMContentLoaded', function() {
    const menuField = document.getElementById('id_menu');
    const parentField = document.getElementById('id_parent');
    const selectedParentId = parentField.value;

    // Инициализация при загрузке формы
    if (menuField.value) {
        fetchParentItems(menuField.value, selectedParentId);
    }

    menuField.addEventListener('change', function() {
        const menuId = this.value;
        fetchParentItems(menuId, null); // При смене меню, родительский элемент сбрасывается
    });

    function fetchParentItems(menuId, selectedParentId = null) {
        const url = window.location.origin + '/admin/get_menu_items/?menu_id=' + menuId;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                parentField.innerHTML = '<option value="">---------</option>';
                data.forEach(item => {
                    const isSelected = selectedParentId == item.id ? 'selected' : '';
                    parentField.innerHTML += `<option value="${item.id}" ${isSelected}>${item.title}</option>`;
                });
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных:', error);
            });
    }
});

