const form = document.getElementById('detect-form');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const risk_level = document.getElementById('risk-level');
const flagged_words = document.getElementById('flagged-words');
const urlsList = document.getElementById('urls-list');
const submitButton = document.querySelector('button[type="submit"]');

const formActionUrl = '/phishing/scan/email/';

// Fallback for alertify if not loaded
if (typeof alertify === 'undefined') {
    window.alertify = {
        error: (msg) => alert(msg),
        success: (msg) => alert(msg)
    };
}

form.onsubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    submitButton.disabled = true;

    // Show loader
    loading.classList.remove('hidden');
    result.classList.add('hidden');

    try {
        const response = await fetch(formActionUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();

        // Wait 30 seconds before showing result
        await new Promise(resolve => setTimeout(resolve, 10000));

        // Hide loader, show result
        loading.classList.add('hidden');
        result.classList.remove('hidden');

        // Fill in result section
        const level = data.risk_level || "Unknown";
        risk_level.textContent = level;

        // Apply colors
        if (level.toUpperCase() === "HIGH") risk_level.style.color = "red";
        else if (level.toUpperCase() === "MEDIUM") risk_level.style.color = "gold";
        else if (level.toUpperCase() === "LOW") risk_level.style.color = "green";

        flagged_words.textContent = (data.flagged_words && data.flagged_words.join(", ")) || "None";

        urlsList.innerHTML = "";
        if (data.urls && data.urls.length > 0) {
            data.urls.forEach(url => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = url;
                a.target = "_blank";
                a.textContent = url;
                a.className = "text-pink-600 hover:text-pink-800 underline";
                li.appendChild(a);
                urlsList.appendChild(li);
            });
        } else {
            urlsList.innerHTML = "<li class='text-gray-500'>No URLs detected</li>";
        }

        // Show success message
        alertify.success("Email scanning completed successfully!");

        form.reset();
    } catch (error) {
        console.error('Error:', error);
        alertify.error("An error occurred: " + error.message);
        loading.classList.add('hidden');
        result.classList.add('hidden');
    } finally {
        submitButton.disabled = false;
    }
};