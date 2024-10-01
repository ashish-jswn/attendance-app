document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);

    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<p>Processing...</p>`;  // Display the "Processing" message

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || 'An error occurred');
            });
        }
        return response.json();
    })
    .then(data => {
        // Clear the results div and display "Attendance Marked"
        resultsDiv.innerHTML = `<p>${data.message}</p>`;

        // Display buttons for downloading the Excel file and marked images
        let downloadButtons = `
            <button onclick="window.location.href='/download_excel'">Download Excel</button>
        `;
        
        if (data.marked_images && data.marked_images.length > 0) {
            data.marked_images.forEach(image => {
                downloadButtons += `<button onclick="window.location.href='/download_image/${image.split('/').pop()}'">Download Marked Image</button>`;
            });
        }

        resultsDiv.innerHTML += downloadButtons;
    })
    .catch(error => {
        console.error('Error:', error);
        resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    });
});
