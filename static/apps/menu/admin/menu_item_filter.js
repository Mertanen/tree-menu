document.addEventListener('DOMContentLoaded', function() {
    const menuField = document.getElementById('id_menu');
    const parentField = document.getElementById('id_parent');
    const parentFieldWrapper = parentField.closest('.field-parent');

    if (!menuField.value) {
        parentFieldWrapper.style.display = 'none';
    }

    menuField.addEventListener('change', function() {
        const menuId = this.value;

        if (!menuId) {
            parentFieldWrapper.style.display = 'none';
            return;
        }

        parentFieldWrapper.style.display = 'block';

        const url = window.location.origin + '/admin/get_menu_items/?menu_id=' + menuId;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: ${response.status} ${response.statusText}`);
                }
                return response.json();  // Ожидаем JSON
            })
            .then(data => {
                parentField.innerHTML = '<option value="">---------</option>';
                data.forEach(item => {
                    parentField.innerHTML += `<option value="${item.id}">${item.title}</option>`;
                });
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных:', error);
            });
    });
});
