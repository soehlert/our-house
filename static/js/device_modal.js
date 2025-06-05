function openRoomModal(roomId, roomName) {
    const modal = document.getElementById('roomModal');
    const modalRoomName = document.getElementById('modalRoomName');
    const modalDeviceCount = document.getElementById('modalDeviceCount'); // Updated
    const modalDeviceGrid = document.getElementById('modalDeviceGrid'); // Updated
    const modalLoading = document.getElementById('modalLoading');
    const modalError = document.getElementById('modalError');
    const modalAddDeviceBtn = document.getElementById('modalAddDeviceBtn'); // Updated

    if (!modal || !modalRoomName || !modalDeviceCount || !modalDeviceGrid ||
        !modalLoading || !modalError || !modalAddDeviceBtn) {
        console.error('Required modal elements not found');
        return;
    }

    modalRoomName.textContent = roomName;
    modalAddDeviceBtn.href = `${window.deviceCreateUrl}?room=${roomId}/`; // Updated
    modal.classList.remove('hidden');
    modalLoading.classList.remove('hidden');
    modalError.classList.add('hidden');
    modalDeviceGrid.innerHTML = '';

    fetch(`${window.deviceRoomApiUrl.replace(0, roomId)}`) // Updated
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            modalLoading.classList.add('hidden');
            modalDeviceCount.textContent = `${data.devices.length} device${data.devices.length !== 1 ? 's' : ''}`; // Updated

            if (data.devices.length > 0) { // Updated
                modalDeviceGrid.innerHTML = data.devices.map(device => createDeviceCard(device)).join(''); // Updated
            } else {
                modalDeviceGrid.innerHTML = createEmptyState(roomName);
            }
        })
        .catch(error => {
            console.error('Error loading devices:', error); // Updated
            modalLoading.classList.add('hidden');
            modalError.classList.remove('hidden');
        });
}

function closeRoomModal() {
    const modal = document.getElementById('roomModal');
    if (modal) {
        modal.classList.add('hidden');
    }
    if (document.activeElement && document.activeElement.blur) {
        document.activeElement.blur();
    }
}

function createDeviceCard(device) { // Updated function name and parameter
    const detailUrl = `${window.deviceDetailUrl}${device.id}/`; // Updated
    const editUrl = window.deviceUpdateUrl.replace('DEVICE_ID', device.id); // Updated

    return `
        <div class="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
            <div class="p-4">
                <h3 class="text-lg font-medium text-gray-900 mb-2 capitalize">${device.location_description || device.device_type_display}</h3>
                <div class="flex items-center gap-2 mb-3">
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getDeviceTypeBadgeClass(device.device_type)}">${device.device_type_display.toUpperCase()}</span>
                    ${device.protection_type && device.protection_type !== 'none' ? 
                      `<span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium ${getProtectionColor(device.protection_type)}">${getProtectionLabel(device.protection_type)}</span>` : 
                      ''
                    }
                </div>
                ${device.circuit ? createCircuitInfo(device.circuit) : createNoCircuitInfo()}
                ${device.position_number ? `<p class="text-xs text-gray-500 mb-3">Position: ${device.position_number}</p>` : ''}
                ${device.attached_appliance ? 
                  `<span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-700">${device.attached_appliance.name}</span>` : 
                  ''
                }
                <div class="flex space-x-2 mt-3">
                    <a href="${detailUrl}" class="px-3 py-1 text-sm font-medium text-green-600 bg-white border border-green-600 rounded hover:bg-green-50">View</a>
                    <a href="${editUrl}" class="px-3 py-1 text-sm font-medium text-blue-600 bg-white border border-blue-600 rounded hover:bg-blue-50">Edit</a>
                </div>
            </div>
        </div>
    `;
}

function createCircuitInfo(circuit) {
    return `
        <p class="text-sm text-gray-600 mb-1">Type: ${circuit.pole_type_display}</p>
        <div class="flex items-center text-sm text-gray-600 mb-2">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            <span>Circuit ${circuit.circuit_number}</span>
        </div>
    `;
}

function getProtectionColor(protectionType) {
    const colors = {
        'gfci': 'bg-blue-100 text-blue-700',
        'afci': 'bg-green-100 text-green-700',
        'dual_function': 'bg-purple-100 text-purple-700'
    };
    return colors[protectionType] || 'bg-gray-100 text-gray-700';
}

function getProtectionLabel(protectionType) {
    const labels = {
        'gfci': 'GFCI',
        'afci': 'AFCI',
        'dual_function': 'Dual Function'
    };
    return labels[protectionType] || 'Unknown';
}

function createNoCircuitInfo() {
    return `
        <div class="flex items-center text-sm text-red-600 mb-3">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            <span class="font-medium">No Circuit Assigned</span>
        </div>
    `;
}

function createEmptyState(roomName) {
    return `
        <div class="col-span-full text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No devices in ${roomName}</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by adding a device to this room.</p>
        </div>
    `;
}

function getDeviceTypeBadgeClass(deviceType) {
    switch(deviceType) {
        case 'Receptacle': return 'bg-blue-100 text-blue-800'; // Updated to match your model choices
        case 'Switch': return 'bg-green-100 text-green-800';
        case 'Light': return 'bg-yellow-100 text-yellow-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeRoomModal();
    }
});
