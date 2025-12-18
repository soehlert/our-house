document.addEventListener('DOMContentLoaded', function () {
    const makeSelect = document.getElementById('id_make');
    const modelInput = document.getElementById('id_model'); // The text input
    const modelDatalist = document.getElementById('model-list'); // The datalist
    const modelUrlTemplate = makeSelect.dataset.modelUrl;

    if (!makeSelect || !modelInput || !modelDatalist || !modelUrlTemplate) {
        console.error('Required elements for vehicle form not found.');
        return;
    }

    makeSelect.addEventListener('change', function () {
        const selectedMake = this.value;

        // Clear previous options
        modelDatalist.innerHTML = '';

        if (selectedMake) {
            const url = modelUrlTemplate.replace('PLACEHOLDER', selectedMake);

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.models && data.models.length > 0) {
                        data.models.forEach(function (model) {
                            const option = document.createElement('option');
                            option.value = model;
                            modelDatalist.appendChild(option);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error fetching vehicle models:', error);
                });
        }
    });

    // It's good practice to clear the model input if the make changes
    makeSelect.addEventListener('change', function() {
        modelInput.value = '';
    });
});
