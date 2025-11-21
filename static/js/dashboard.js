document.addEventListener('DOMContentLoaded', function() {
    const joinButtons = document.querySelectorAll('.join-session');
    const leaveButtons = document.querySelectorAll('.leave-session');

    joinButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sessionId = this.getAttribute('data-session-id');
            this.disabled = true;
            fetch(`/join_session/${sessionId}`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.disabled = false;
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert(data.message || 'Failed to join session.');
                    }
                })
                .catch(error => {
                    this.disabled = false;
                    console.error('Error:', error);
                    alert('An error occurred while joining the session.');
                });
        });
    });

    leaveButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!confirm('Are you sure you want to leave this session?')) {
                return;
            }
            const sessionId = this.getAttribute('data-session-id');
            this.disabled = true;
            fetch(`/leave_session/${sessionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.disabled = false;
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert(data.message || 'Failed to leave session.');
                    }
                })
                .catch(error => {
                    this.disabled = false;
                    console.error('Error:', error);
                    alert('An error occurred while leaving the session.');
                });
        });
    });

    const deleteButtons = document.querySelectorAll('.delete-session');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!confirm('Are you sure you want to delete this session? All attendance records will be removed.')) {
                return;
            }
            const sessionId = this.getAttribute('data-session-id');
            this.disabled = true;

            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/sessions/${sessionId}/delete`;
            document.body.appendChild(form);
            form.submit();
        });
    });

    // Filter Panel Toggle
    const filterToggle = document.getElementById('filterToggle');
    const filterPanel = document.getElementById('filterPanel');
    
    if (filterToggle && filterPanel) {
        filterToggle.addEventListener('click', function() {
            filterPanel.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // Filter Functionality
    const applyFiltersBtn = document.getElementById('applyFilters');
    const clearFiltersBtn = document.getElementById('clearFilters');
    const searchBar = document.getElementById('searchBar');
    const filterTag = document.getElementById('filterTag');
    
    function applyFilters() {
        const courseFilter = document.getElementById('filterCourse').value.toLowerCase();
        const locationFilter = document.getElementById('filterLocation').value.toLowerCase();
        const yearFilter = document.getElementById('filterYear').value;
        const termFilter = document.getElementById('filterTerm').value;
        const professorFilter = document.getElementById('filterProfessor').value.toLowerCase();
        const tagFilter = filterTag ? filterTag.value.toLowerCase() : '';
        const searchQuery = searchBar ? searchBar.value.toLowerCase() : '';
        
        const sessionCards = document.querySelectorAll('#joinSessionsList .session_card');
        const noResultsMessage = document.getElementById('noResultsMessage');
        let visibleCount = 0;
        
        sessionCards.forEach(card => {
            const courseName = card.getAttribute('data-course-name').toLowerCase();
            const locationAddress = card.getAttribute('data-location-address').toLowerCase();
            const courseYear = card.getAttribute('data-course-year');
            const courseTerm = card.getAttribute('data-course-term');
            const professorName = card.getAttribute('data-professor-name').toLowerCase();
            const cardTagsValue = card.getAttribute('data-tags') || '';
            const cardTags = cardTagsValue ? cardTagsValue.toLowerCase().split(',') : [];
            const cardText = card.textContent.toLowerCase();
            
            // Check if card matches all filters
            const matchesCourse = !courseFilter || courseName.includes(courseFilter);
            const matchesLocation = !locationFilter || locationAddress.includes(locationFilter);
            const matchesYear = !yearFilter || courseYear === yearFilter;
            const matchesTerm = !termFilter || courseTerm === termFilter;
            const matchesProfessor = !professorFilter || professorName.includes(professorFilter);
            const matchesTag = !tagFilter || cardTags.includes(tagFilter);
            const matchesSearch = !searchQuery || cardText.includes(searchQuery);
            
            if (matchesCourse && matchesLocation && matchesYear && matchesTerm && matchesProfessor && matchesTag && matchesSearch) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show/hide no results message
        if (noResultsMessage) {
            noResultsMessage.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    }
    
    function clearFilters() {
        document.getElementById('filterCourse').value = '';
        document.getElementById('filterLocation').value = '';
        document.getElementById('filterYear').value = '';
        document.getElementById('filterTerm').value = '';
        document.getElementById('filterProfessor').value = '';
        if (filterTag) filterTag.value = '';
        if (searchBar) searchBar.value = '';
        
        applyFilters();
    }
    
    // Event listeners for filter controls
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', applyFilters);
    }
    
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', clearFilters);
    }
    
    // Apply filters when search bar changes
    if (searchBar) {
        searchBar.addEventListener('input', applyFilters);
    }
    
    // Apply filters when any filter changes
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', applyFilters);
    });
});
