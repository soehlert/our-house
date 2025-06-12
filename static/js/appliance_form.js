// Appliance form device filtering functionality
document.addEventListener('DOMContentLoaded', function() {
    const roomSelect = document.querySelector('select[name="room"]');
    const deviceSelect = document.querySelector('select[name="connected_device"]');

    if (!roomSelect || !deviceSelect) return;

    // Get device-room mapping from data attribute
    const deviceRoomMapping = JSON.parse(document.body.dataset.deviceRoomMapping || '{}');

    // Store all device options
    const allDeviceOptions = Array.from(deviceSelect.options).slice(1); // Skip empty option

    function filterDevices(preserveSelection = false) {
        const selectedRoomId = parseInt(roomSelect.value) || null;
        const currentSelection = preserveSelection ? deviceSelect.value : '';

        // Remove all options except the first (empty) one
        while (deviceSelect.options.length > 1) {
            deviceSelect.removeChild(deviceSelect.lastChild);
        }

        // Add back filtered options
        allDeviceOptions.forEach(option => {
            const deviceId = parseInt(option.value);
            const deviceRoomId = deviceRoomMapping[deviceId];

            if (!selectedRoomId || deviceRoomId === selectedRoomId) {
                const clonedOption = option.cloneNode(true);
                deviceSelect.appendChild(clonedOption);
            }
        });

        // Force the select to refresh its display so javascript filters after django adds the room totally
        deviceSelect.style.display = 'none';
        deviceSelect.offsetHeight; // Trigger reflow
        deviceSelect.style.display = '';
        deviceSelect.dispatchEvent(new Event('change'));

        // Restore selection if preserving
        if (preserveSelection && currentSelection) {
            deviceSelect.value = currentSelection;
        } else if (!preserveSelection) {
            deviceSelect.value = '';
        }
    }

    // Initial filter preserving existing selection
    filterDevices(true);

    // Filter when room changes, don't preserve selection
    roomSelect.addEventListener('change', () => {
        filterDevices(false);
    });
});
