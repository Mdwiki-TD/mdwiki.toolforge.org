document.getElementById('myForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission
    $("#load").show();

    // Create a FormData object from the form
    let formData = new FormData(this);

    // Send a POST request to the PHP page
    await fetch('do_text.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('command').innerHTML = data.command;
        document.getElementById('result').innerHTML = data.result;
        document.getElementById('newtext').value = data.newtext;
    })
    .catch(error => {
        console.error('Error:', error);
    });
    $("#load").hide();
});
