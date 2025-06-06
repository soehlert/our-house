// Appliance form device filtering functionality
document.addEventListener('DOMContentLoaded', function() {
    const roomSelect = document.querySelector('select[name="room"]');
    const deviceSelect = document.querySelector('select[name="connected_device"]');

    if (!roomSelect || !deviceSelect) return;

    // Get device-room mapping from data attribute
    const deviceRoomMapping = JSON.parse(document.body.dataset.deviceRoomMapping || '{}');

    // Store all device options
    const allDeviceOptions = Array.from(deviceSelect.options).slice(1); // Skip empty option

    function filterDevices() {
        const selectedRoomId = roomSelect.value;

        // Remove all options except the first (empty) one
        while (deviceSelect.options.length > 1) {
            deviceSelect.removeChild(deviceSelect.lastChild);
        }

        // Add back filtered options
        allDeviceOptions.forEach(option => {
            const deviceId = parseInt(option.value);
            const deviceRoomId = deviceRoomMapping[deviceId];

            if (!selectedRoomId || deviceRoomId == selectedRoomId) {
                deviceSelect.appendChild(option.cloneNode(true));
            }
        });

        // Reset selection
        deviceSelect.value = '';
    }

    roomSelect.addEventListener('change', filterDevices);
});
