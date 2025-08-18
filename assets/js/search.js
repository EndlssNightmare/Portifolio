
// Client-side search functionality
function searchWriteups() {
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();
    const writeupCards = document.querySelectorAll(".writeup-card");
    
    writeupCards.forEach(card => {
        const title = card.querySelector(".card-title").textContent.toLowerCase();
        const description = card.querySelector(".card-text").textContent.toLowerCase();
        const tags = Array.from(card.querySelectorAll(".tag-badge")).map(tag => tag.textContent.toLowerCase());
        
        const matches = title.includes(searchTerm) || 
                       description.includes(searchTerm) || 
                       tags.some(tag => tag.includes(searchTerm));
        
        card.style.display = matches ? "block" : "none";
    });
}

// Add search input to pages if it doesn't exist
document.addEventListener("DOMContentLoaded", function() {
    const writeupsContainer = document.querySelector(".writeups-container");
    if (writeupsContainer && !document.getElementById("searchInput")) {
        const searchDiv = document.createElement("div");
        searchDiv.className = "mb-4";
        searchDiv.innerHTML = `
            <div class="input-group">
                <input type="text" class="form-control" id="searchInput" placeholder="Search writeups..." onkeyup="searchWriteups()">
                <button class="btn btn-outline-secondary" type="button" onclick="searchWriteups()">
                    <i class="fas fa-search"></i>
                </button>
            </div>
        `;
        writeupsContainer.parentNode.insertBefore(searchDiv, writeupsContainer);
    }
});
