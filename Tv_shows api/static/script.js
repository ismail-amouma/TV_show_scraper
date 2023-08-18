document.addEventListener("DOMContentLoaded", function() {
    const newLink = document.getElementById("newLink");
    const inputOverlay = document.getElementById("inputOverlay");
    const submitButton = document.getElementById("submitButton");
    const userInput = document.getElementById("userInput");
    const closeButton = document.getElementById("closeButton"); // Add this line
    const scrapingText = document.getElementById("scrapingText"); // Add this line

    newLink.addEventListener("click", function() {
        inputOverlay.style.display = "block";
    });

    closeButton.addEventListener("click", function() { // Add this block
        inputOverlay.style.display = "none";
        userInput.value = ''; // Clear the input field
    });

    submitButton.addEventListener("click", function() {
        const url = userInput.value;

        const formData = new FormData();
        formData.append('url', url);

        // Update the button text to "Scraping..."
        submitButton.innerText = "Scraping...";

        fetch("/submit", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Reset the button text and close the input overlay
            submitButton.innerText = "Get";
            inputOverlay.style.display = "none";
            userInput.value = ''; // Clear the input field
            location.reload();
        })
        .catch(error => {
            console.error("Error:", error);
            // Reset the button text in case of an error
            submitButton.innerText = "Get";
        });
    });
});
