function openRoomModal(roomId, roomName) {
    const modal = document.getElementById('roomModal');
    const modalRoomName = document.getElementById('modalRoomName');
    const modalOutletCount = document.getElementById('modalOutletCount');
    const modalOutletGrid = document.getElementById('modalOutletGrid');
    const modalLoading = document.getElementById('modalLoading');
    const modalError = document.getElementById('modalError');
    const modalAddOutletBtn = document.getElementById('modalAddOutletBtn');

    if (!modal || !modalRoomName || !modalOutletCount || !modalOutletGrid ||
        !modalLoading || !modalError || !modalAddOutletBtn) {
        console.error('Required modal elements not found');
        return;
    }

    modalRoomName.textContent = roomName;
    modalAddOutletBtn.href = `${window.outletCreateUrl}?room=${roomId}/`;
    modal.classList.remove('hidden');
    modalLoading.classList.remove('hidden');
    modalError.classList.add('hidden');
    modalOutletGrid.innerHTML = '';

    fetch(`${window.outletRoomApiUrl.replace(0, roomId)}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            modalLoading.classList.add('hidden');
            modalOutletCount.textContent = `${data.outlets.length} outlet${data.outlets.length !== 1 ? 's' : ''}`;

            if (data.outlets.length > 0) {
                modalOutletGrid.innerHTML = data.outlets.map(outlet => createOutletCard(outlet)).join('');
            } else {
                modalOutletGrid.innerHTML = createEmptyState(roomName);
            }
        })
        .catch(error => {
            console.error('Error loading outlets:', error);
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

function createOutletCard(outlet) {
    const detailUrl = `${window.outletDetailUrl}${outlet.id}/`;
    const editUrl = window.outletUpdateUrl.replace('OUTLET_ID', outlet.id);

    return `
        <div class="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
            <div class="p-4">
                <h3 class="text-lg font-medium text-gray-900 mb-2 capitalize">${outlet.location_description || outlet.device_type_display}</h3>
                <div class="flex items-center gap-2 mb-3">
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getDeviceTypeBadgeClass(outlet.device_type)}">${outlet.device_type_display.toUpperCase()}</span>
                    ${outlet.circuit && outlet.circuit.protection_type && outlet.circuit.protection_type !== 'none' ? 
                      `<span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium ${getProtectionColor(outlet.circuit.protection_type)}">${getProtectionLabel(outlet.circuit.protection_type)}</span>` : 
                      ''
                    }
                </div>
                ${outlet.circuit ? createCircuitInfo(outlet.circuit) : createNoCircuitInfo()}
                ${outlet.position_number ? `<p class="text-xs text-gray-500 mb-3">Position: ${outlet.position_number}</p>` : ''}
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
            <h3 class="mt-2 text-sm font-medium text-gray-900">No outlets in ${roomName}</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by adding an outlet to this room.</p>
        </div>
    `;
}

function getDeviceTypeBadgeClass(deviceType) {
    switch(deviceType) {
        case 'RECEPTACLE': return 'bg-blue-100 text-blue-800';
        case 'SWITCH': return 'bg-green-100 text-green-800';
        case 'LIGHT': return 'bg-yellow-100 text-yellow-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeRoomModal();
    }
});
