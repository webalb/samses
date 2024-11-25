document.addEventListener("DOMContentLoaded", function () {
    // Function to generate registration number
    function generateRegistrationNumber() {
        const date = new Date();
        const year = date.getFullYear();
        const uniqueId = Math.floor(1000 + Math.random() * 9000);  // Random 4-digit ID
        return `MOE-${year}-${uniqueId}`;
    }

    // Function to generate accreditation number
    function generateAccreditationNumber() {
        const date = new Date();
        const year = date.getFullYear();
        const uniqueId = Math.floor(1000 + Math.random() * 9000);  // Random 4-digit ID
        return `ACCR-${year}-${uniqueId}`;
    }

    // Add Generate button for Registration Number
    const regField = document.getElementById("id_registration_number");
    const regButton = document.createElement("button");
    regButton.innerText = "Generate";
    regButton.type = "button";
    regButton.addEventListener("click", function () {
        regField.value = generateRegistrationNumber();
    });
    regField.parentNode.appendChild(regButton);

    // Add Generate button for Accreditation Number
    const accField = document.getElementById("id_accreditation_number");
    const accButton = document.createElement("button");
    accButton.innerText = "Generate";
    accButton.type = "button";
    accButton.addEventListener("click", function () {
        accField.value = generateAccreditationNumber();
    });
    accField.parentNode.appendChild(accButton);
});
