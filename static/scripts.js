document.addEventListener('DOMContentLoaded', function() {
    // Modal functions
    window.openModal = function() {
        document.getElementById('infoModal').style.display = 'block';
    }

    window.closeModal = function() {
        document.getElementById('infoModal').style.display = 'none';
    }

    // Close modal when clicking outside
    const infoModal = document.getElementById('infoModal');
    if (infoModal) {
        infoModal.addEventListener('click', function(e) {
            if (e.target === infoModal) {
                closeModal();
            }
        });
    }
});
