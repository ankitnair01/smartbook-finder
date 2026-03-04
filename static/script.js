function searchBooks(){

    const query = document.getElementById("searchInput").value;

    const loader = document.getElementById("loader");
    const results = document.getElementById("results");

    loader.style.display = "block";
    results.innerHTML = "";

    fetch(`/search?q=${query}`)
        .then(response => response.json())
        .then(data => {

            loader.style.display = "none";
            document.getElementById("results").scrollIntoView({
                 behavior: "smooth"
            });

            data.forEach(book => {

                const image = book.thumbnail ? book.thumbnail : "https://via.placeholder.com/120";

                const bookCard = `
                    <div class="book-card">
                        <img src="${image}" width="120">
                        <h3>${book.title}</h3>
                        <p>${book.authors}</p>
                        <p>${book.publishedDate}</p>
                        <a href="${book.previewLink}" target="_blank">More Info</a>
                    </div>
                `;

                results.innerHTML += bookCard;

            });

        });

}
document.getElementById("searchInput")
.addEventListener("keypress", function(event){

    if(event.key === "Enter"){
        searchBooks();
    }

});