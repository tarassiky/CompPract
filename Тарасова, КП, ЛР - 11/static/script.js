async function decryptFile() {
    const form = document.getElementById('decypherForm');
    const formData = new FormData(form);
    const resultDiv = document.getElementById('result');
    resultDiv.textContent = "Decrypting..."; // Feedback to the user

    try {
        const response = await fetch('/decypher', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }

        const data = await response.text(); // Get the plain text decryption result
        resultDiv.textContent = `Decrypted: ${data}`;

    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    }
}
async function generateKeys() {
    const keyPairDiv = document.getElementById('keyPair');
    keyPairDiv.textContent = "Generating keys...";

    try {
        const response = await fetch('/generate_keys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        keyPairDiv.innerHTML = `
        <label>Public Key (PEM):</label><br>
        <textarea id="publicKey" rows="5" cols="50">${data.public_key}</textarea><br><br>
        <label>Private Key (PEM):</label><br>
        <textarea id="privateKey" rows="5" cols="50">${data.private_key}</textarea><br><br>
        `;

    } catch (error) {
        keyPairDiv.textContent = `Error: ${error.message}`;
    }
}

async function encryptMessage() {
    const publicKey = document.getElementById('publicKey');
    const message = document.getElementById('message');
    const encryptionResultDiv = document.getElementById('encryptionResult');

    if (!publicKey || !publicKey.value || !message || !message.value) {
        encryptionResultDiv.textContent = "Please generate a key pair and enter a message.";
        return;
    }
    encryptionResultDiv.textContent = "Encrypting...";

    try {
        const response = await fetch('/encrypt_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                public_key: publicKey.value,
                message: message.value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }
        const blob = await response.blob();
        const downloadUrl = URL.createObjectURL(blob);
        encryptionResultDiv.innerHTML = `<a href="${downloadUrl}" download="secret.bin">Download Encrypted File</a>`;

    } catch (error) {
        encryptionResultDiv.textContent = `Error: ${error.message}`;
    }
}