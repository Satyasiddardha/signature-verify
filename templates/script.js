document.getElementById('verificationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const originalFile = document.getElementById('originalSignature').files[0];
    const forgedFile = document.getElementById('forgedSignature').files[0];

    if (!originalFile || !forgedFile) {
        document.getElementById('result').innerText = "Please upload both signatures.";
        document.getElementById('result').style.color = 'red';
        return;
    }

    const reader1 = new FileReader();
    const reader2 = new FileReader();

    reader1.onload = function(e) {
        const originalImage = e.target.result;
        reader2.onload = function(e) {
            const forgedImage = e.target.result;
            verifySignatures(originalImage, forgedImage);
        };
        reader2.readAsDataURL(forgedFile);
    };
    reader1.readAsDataURL(originalFile);
});

function verifySignatures(originalImage, forgedImage) {
    fetch('/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            originalSignature: originalImage,
            forgedSignature: forgedImage
        }),
    })
    .then(response => response.json())
    .then(data => {
        const resultText = data.result;
        const resultColor = resultText.includes("genuine") ? 'green' : 'red';

        document.getElementById('result').innerText = resultText;
        document.getElementById('result').style.color = resultColor;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred.';
        document.getElementById('result').style.color = 'red';
    });
}
