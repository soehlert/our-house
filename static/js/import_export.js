// Import/Export form functionality
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const importForm = document.getElementById('importForm');

    // Handle file input display
    if (fileInput && fileName) {
        fileInput.addEventListener('change', function(e) {
            fileName.textContent = e.target.files[0]?.name || 'No file chosen';
        });
    }

    // Handle form submission
    if (importForm) {
        importForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');

            // Get import URL from data attribute
            const importUrl = document.body.dataset.importUrl;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing';

            console.log('Starting import request');

            fetch(importUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);

                // Reset form
                this.reset();
                if (fileName) {
                    fileName.textContent = 'No file chosen';
                }

                console.log('Reloading page');
                // Always reload to show the appropriate Django message
                window.location.reload();
            })
            .catch(error => {
                console.error('Import error:', error);
                // For network/parsing errors, show immediate feedback
                alert(`Import failed: ${error.message}`);
            })
            .finally(() => {
                // Reset button
                submitBtn.disabled = false;
                submitBtn.textContent = 'Import Data';
            });
        });
    }
});
