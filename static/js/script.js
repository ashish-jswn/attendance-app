document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);

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
        // Display results
        let resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `<p>${data.message}</p>`;
        if (data.uncertain_students && data.uncertain_students.length > 0) {
            resultsDiv.innerHTML += `<p>Uncertain Students: ${data.uncertain_students.join(', ')}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('results').innerHTML = `<p>Error: ${error.message}</p>`;
    });
});