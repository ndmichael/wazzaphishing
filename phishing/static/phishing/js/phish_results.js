const form = document.getElementById('detect-form');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const resultMessage = document.getElementById('result-message');
const formContainer = document.getElementById('form-container');
const submitButton = document.querySelector('button[type="submit"]');
const risk_level = document.getElementById('risk-level');
const flagged_words = document.getElementById('flagged-words');
const urlsList = document.getElementById('urls-list');

const formActionUrl = '/phishing/scan/email/';
form.onsubmit = async (event) => {

    event.preventDefault();
    const formData = new FormData(form);
    submitButton.disabled = true;

//     // Update UI
//     loading.classList.add('visible');
//     loading.classList.remove('hidden');
//     formContainer.classList.add('hidden');
//     formContainer.classList.remove('visible');

    try {
        const response = await fetch(formActionUrl, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }
        else{
            const data = await response.json();
            

            result.classList.add('visible');
            result.classList.remove('hidden');

            // Update the analysis report
            level =  data.risk_level;
            risk_level.textContent =level
            alert(data.risk_percent)
            // alert(data.risk_prediction)
            
            // Apply colors based on risk level
            if (level.toUpperCase() === "HIGH") {
                risk_level.style.color = "red";
            } else if (level.toUpperCase() === "MEDIUM") {
                risk_level.style.color = "black";
            } else if (level.toUpperCase() === "LOW") {
                risk_level.style.color = "green";
            }
            flagged_words.textContent = data.flagged_words.join(", ");

            // Display URLs
            urlsList.innerHTML = '';
            data.urls.forEach(url => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = url;
                link.target = "_blank";
                link.textContent = url;
                listItem.appendChild(link);
                urlsList.appendChild(listItem);
            });
        }
        
    } catch (error) {
        alert("Error occured")
        loading.classList.add('hidden');
        loading.classList.remove('visible');
        formContainer.classList.add('visible');
        formContainer.classList.remove('hidden');
        // resultMessage.textContent = `An error occurred: ${error.message}`;
        // result.classList.add('visible');
        // result.classList.remove('hidden');
    } finally {
        // Reset loading state
        submitButton.disabled = false;
    }
};
