import {loadStates, loadCounties, loadCities } from "./utils.js";

// Initial call to load countries when the page loads

// // Event listener for country selection change
// document.getElementById('country').addEventListener('change', function() {
//     let geonameId = this.value; // Get the geonameId of the selected country
//     if (geonameId) {
//         loadStates(geonameId); // Pass the geonameId to loadStates function
//     } else {
//         document.getElementById('state').innerHTML = '<option value="">Select State/Province</option>';
//     }
//     document.getElementById('city').innerHTML = '<option value="">Select City/County</option>';
// });

// Event listener for state selection change
document.getElementById('state').addEventListener('change', function() {
    let stateGeonameId = this.value; // Get the geonameId of the selected state
    // let countryCode = document.getElementById('country').value;
    if (stateGeonameId) {
        loadCounties(stateGeonameId); // Pass the state's geonameId to loadCities function
    } else {
        document.getElementById('county').innerHTML = '<option value="">Select County</option>';
    }
});

document.getElementById('county').addEventListener('change', function() {
    let countyGeonameId = this.value; // Get the geonameId of the selected state
    // let countryCode = document.getElementById('country').value;
    if (countyGeonameId) {
        loadCities(countyGeonameId); // Pass the state's geonameId to loadCities function
    } else {
        document.getElementById('city').innerHTML = '<option value="">Select City</option>';
    }
});
function updateResultsDropdown(data) {
    // Get the results dropdown element
    const resultsDropdown = document.getElementById('results');

    // Clear existing options
    resultsDropdown.innerHTML = '';

    // Check if data is not empty
    if (data && data.length > 0) {
        // Iterate over each result item
        data.forEach(item => {
            // Create an option element
            const option = document.createElement('option');
            option.value = item.name; // or any unique identifier of the item

            // Set the text content of the option
            option.innerHTML = `${item.name}<br>${item.address}<br>${item.phone}<br><br><br>`;

            // Append the option to the dropdown
            resultsDropdown.appendChild(option);
        });
    } else {
        // Handle empty data scenario
        const option = document.createElement('option');
        option.textContent = 'No results found';
        resultsDropdown.appendChild(option);
    }
}

// This function gets the value of a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// The submitForm function with the CSRF token included in the headers
function submitForm() {
    // Get the CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');

    // Get the selected city's text content and the specialization value from the form elements
    const citySelect = document.getElementById('city');
    const selectedCity = citySelect.options[citySelect.selectedIndex].text; // Corrected line
    const selectedSpecialization = document.getElementById('specialization').value;

    // Prepare the search criteria, assuming the city names in the database are stored in a case-insensitive manner
    const searchCriteria = {
        city: selectedCity,
        specialization: selectedSpecialization
    };

    // Make an AJAX POST request to your local search endpoint
    console.log("body: ", JSON.stringify(searchCriteria));
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(searchCriteria),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Handle the search results here
        console.log(data);
        updateResultsDropdown(data);
    })
    .catch(error => {
        console.error('Error during fetch:', error);
    });
}

window.onload = loadStates(6252001);  // Load the states of US
window.submitForm = submitForm;