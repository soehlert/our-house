// Warranty alert management functionality
let dismissedAlerts = new Set();

function dismissAlert(applianceId) {
    dismissedAlerts.add(applianceId);

    const card = document.querySelector(`[data-appliance-id="${applianceId}"]`);
    if (card) {
        card.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';

        setTimeout(() => {
            card.style.display = 'none';
        }, 300);
    }

    // Get CSRF token and URLs from data attributes
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const dismissUrl = document.body.dataset.dismissUrl.replace('0', applianceId);

    fetch(dismissUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            setTimeout(() => {
                window.location.reload();
            }, 400);
        }
    })
    .catch(error => {
        console.error('Error dismissing alert:', error);
        dismissedAlerts.delete(applianceId);
        if (card) {
            card.style.display = 'block';
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
        }
    });
}

function restoreAlert(applianceId) {
    const dismissedCard = document.querySelector(`#dismissedSection [data-appliance-id="${applianceId}"]`);
    if (dismissedCard) {
        dismissedCard.style.transition = 'opacity 0.3s ease-out';
        dismissedCard.style.opacity = '0';
        setTimeout(() => {
            dismissedCard.remove();
        }, 300);
    }

    // Get CSRF token and URLs from data attributes
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const undismissUrl = document.body.dataset.undismissUrl.replace('0', applianceId);

    fetch(undismissUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error restoring alert:', error);
    });
}

// Initialize toggle functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Toggle dismissed section
    const toggleButton = document.getElementById('toggleDismissed');
    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            const dismissedSection = document.getElementById('dismissedSection');
            const toggleText = document.getElementById('toggleText');
            const isHidden = dismissedSection.classList.contains('hidden');

            if (isHidden) {
                dismissedSection.classList.remove('hidden');
                toggleText.textContent = toggleText.textContent.replace('Show', 'Hide');
            } else {
                dismissedSection.classList.add('hidden');
                toggleText.textContent = toggleText.textContent.replace('Hide', 'Show');
            }
        });
    }
});
