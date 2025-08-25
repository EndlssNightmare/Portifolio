// Pagination functionality for Cybersecurity Portfolio

class Pagination {
    constructor(containerId, itemsPerPage = 10) {
        this.container = document.getElementById(containerId);
        this.itemsPerPage = itemsPerPage;
        this.currentPage = 1;
        this.totalItems = 0;
        this.totalPages = 0;
        this.items = [];
        
        if (this.container) {
            this.init();
        }
    }
    
    init() {
        // Get all items from the container
        this.items = Array.from(this.container.querySelectorAll('.writeup-card, .project-card'));
        this.totalItems = this.items.length;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        
        // Create pagination controls
        this.createPaginationControls();
        
        // Show first page
        this.showPage(1);
    }
    
    createPaginationControls() {
        if (this.totalPages <= 1) return;
        
        const paginationContainer = document.createElement('div');
        paginationContainer.className = 'pagination-container d-flex justify-content-center mt-4';
        
        // Generate page numbers
        const pageNumbers = this.generatePageNumbers();
        
        paginationContainer.innerHTML = `
            <nav aria-label="Page navigation">
                <ul class="pagination pagination-lg">
                    <li class="page-item">
                        <button class="page-link" id="prevPage" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </button>
                    </li>
                    ${pageNumbers}
                    <li class="page-item">
                        <button class="page-link" id="nextPage" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </button>
                    </li>
                </ul>
            </nav>
        `;
        
        // Insert pagination after the container
        this.container.parentNode.insertBefore(paginationContainer, this.container.nextSibling);
        
        // Add event listeners
        document.getElementById('prevPage').addEventListener('click', () => {
            this.previousPage();
        });
        
        document.getElementById('nextPage').addEventListener('click', () => {
            this.nextPage();
        });
        
        // Add event listeners for page number buttons
        for (let i = 1; i <= this.totalPages; i++) {
            const pageBtn = document.getElementById(`page-${i}`);
            if (pageBtn) {
                pageBtn.addEventListener('click', () => {
                    this.goToPage(i);
                });
            }
        }
        
        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                this.previousPage();
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                this.nextPage();
            }
        });
    }
    
    generatePageNumbers() {
        let pageNumbers = '';
        const maxVisiblePages = 7; // Show max 7 page numbers
        
        if (this.totalPages <= maxVisiblePages) {
            // Show all page numbers
            for (let i = 1; i <= this.totalPages; i++) {
                pageNumbers += `
                    <li class="page-item">
                        <button class="page-link page-number" id="page-${i}" data-page="${i}">
                            ${i}
                        </button>
                    </li>
                `;
            }
        } else {
            // Show first page, last page, and pages around current
            const currentPage = this.currentPage;
            const halfVisible = Math.floor(maxVisiblePages / 2);
            
            // Always show first page
            pageNumbers += `
                <li class="page-item">
                    <button class="page-link page-number" id="page-1" data-page="1">
                        1
                    </button>
                </li>
            `;
            
            if (currentPage > halfVisible + 2) {
                pageNumbers += `
                    <li class="page-item disabled">
                        <span class="page-link">...</span>
                    </li>
                `;
            }
            
            // Show pages around current page
            const start = Math.max(2, currentPage - halfVisible);
            const end = Math.min(this.totalPages - 1, currentPage + halfVisible);
            
            for (let i = start; i <= end; i++) {
                pageNumbers += `
                    <li class="page-item">
                        <button class="page-link page-number" id="page-${i}" data-page="${i}">
                            ${i}
                        </button>
                    </li>
                `;
            }
            
            if (currentPage < this.totalPages - halfVisible - 1) {
                pageNumbers += `
                    <li class="page-item disabled">
                        <span class="page-link">...</span>
                    </li>
                `;
            }
            
            // Always show last page
            if (this.totalPages > 1) {
                pageNumbers += `
                    <li class="page-item">
                        <button class="page-link page-number" id="page-${this.totalPages}" data-page="${this.totalPages}">
                            ${this.totalPages}
                        </button>
                    </li>
                `;
            }
        }
        
        return pageNumbers;
    }
    
    showPage(pageNumber) {
        if (pageNumber < 1 || pageNumber > this.totalPages) return;
        
        this.currentPage = pageNumber;
        
        // Hide all items
        this.items.forEach(item => {
            item.style.display = 'none';
        });
        
        // Show items for current page
        const startIndex = (pageNumber - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        
        for (let i = startIndex; i < endIndex && i < this.totalItems; i++) {
            this.items[i].style.display = 'block';
            this.items[i].style.animation = 'fadeInUp 0.6s ease';
        }
        
        // Update pagination controls
        this.updatePaginationControls();
        
        // Scroll to top of container
        this.container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    updatePaginationControls() {
        const prevBtn = document.getElementById('prevPage');
        const nextBtn = document.getElementById('nextPage');
        
        if (prevBtn) prevBtn.disabled = this.currentPage === 1;
        if (nextBtn) nextBtn.disabled = this.currentPage === this.totalPages;
        
        // Update button styles
        if (prevBtn) {
            prevBtn.parentElement.classList.toggle('disabled', this.currentPage === 1);
        }
        if (nextBtn) {
            nextBtn.parentElement.classList.toggle('disabled', this.currentPage === this.totalPages);
        }
        
        // Update page number buttons
        for (let i = 1; i <= this.totalPages; i++) {
            const pageBtn = document.getElementById(`page-${i}`);
            if (pageBtn) {
                pageBtn.parentElement.classList.toggle('active', i === this.currentPage);
                pageBtn.parentElement.classList.remove('disabled');
            }
        }
    }
    
    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.showPage(this.currentPage + 1);
        }
    }
    
    previousPage() {
        if (this.currentPage > 1) {
            this.showPage(this.currentPage - 1);
        }
    }
    
    goToPage(pageNumber) {
        this.showPage(pageNumber);
    }
    
    // Method to refresh pagination when items are filtered or added
    refresh(items = null) {
        if (items) {
            this.items = items;
            this.totalItems = items.length;
        } else {
            this.items = Array.from(this.container.querySelectorAll('.writeup-card:not([style*="display: none"]), .project-card:not([style*="display: none"])'));
            this.totalItems = this.items.length;
        }
        
        const newTotalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        const pageChanged = this.totalPages !== newTotalPages;
        this.totalPages = newTotalPages;
        
        // Remove existing pagination controls
        const existingPagination = document.querySelector('.pagination-container');
        if (existingPagination) {
            existingPagination.remove();
        }
        
        // Recreate pagination controls if there are pages to show
        if (this.totalPages > 1) {
            this.createPaginationControls();
        }
        
        // Show appropriate page
        if (pageChanged && this.currentPage > this.totalPages) {
            // If we're on a page that no longer exists, go to the last page
            this.showPage(this.totalPages);
        } else {
            this.showPage(this.currentPage);
        }
    }
}

// Initialize pagination when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize pagination for index.html (10 items per page)
    const indexContainer = document.getElementById('indexContainer');
    if (indexContainer && (window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/'))) {
        window.paginationInstance = new Pagination('indexContainer', 10);
    }
    
    // Initialize pagination for writeups.html (30 items per page)
    const writeupsContainer = document.getElementById('writeupsContainer');
    if (writeupsContainer && window.location.pathname.includes('writeups.html')) {
        window.paginationInstance = new Pagination('writeupsContainer', 30);
    }
});

// Export for use in other scripts
window.Pagination = Pagination;

// Global function to refresh pagination when new content is added
window.refreshPagination = function() {
    if (window.paginationInstance) {
        window.paginationInstance.refresh();
    }
};

// Auto-refresh pagination when DOM changes (for dynamically added content)
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // Check if any writeup cards were added
            const addedCards = Array.from(mutation.addedNodes).some(node => 
                node.nodeType === 1 && (
                    node.classList?.contains('writeup-card') || 
                    node.classList?.contains('project-card') ||
                    node.querySelector?.('.writeup-card, .project-card')
                )
            );
            
            if (addedCards && window.paginationInstance) {
                // Small delay to ensure all content is loaded
                setTimeout(() => {
                    window.paginationInstance.refresh();
                }, 100);
            }
        }
    });
});

// Start observing when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const containers = document.getElementById('indexContainer') || document.getElementById('writeupsContainer');
    if (containers) {
        observer.observe(containers, {
            childList: true,
            subtree: true
        });
    }
});
