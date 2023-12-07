import {loadStates, loadCounties, loadCities, fetchDoctors} from "./utils.js";


// Event listener for state selection change
document.getElementById('state').addEventListener('change', function() {
    let stateGeonameId = this.value; // Get the geonameId of the selected state
    // let countryCode = document.getElementById('country').value;
    if (stateGeonameId) {
        loadCounties(stateGeonameId); // Pass the state's geonameId to loadCities function
    } else {
        document.getElementById('county').innerHTML = '<option value="">Select County</option>';
        document.getElementById('city').innerHTML = '<option value="">Select City</option>'; 
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


async function submitForm() {
    let city = document.getElementById('city');
    city = city.options[city.selectedIndex].text;
    let specialty = document.getElementById('specialization').value;
    let max_doctors = document.getElementById('maximum').value;

    let doctorsList = await fetchDoctors(specialty, city, max_doctors);

    let doctorsListElement = document.getElementById('doctorsList');
    doctorsListElement.innerHTML = ''; // Clear existing content

    if (doctorsList && doctorsList.length > 0) {

        let listHtml = `
        <table>
            <tr>
                <th>Name</th>
                <th>Address</th>
                <th>Phone</th>
            </tr>
            ${doctorsList.map(doctor => `
                <tr>
                    <td>${doctor.Name}</td>
                    <td>${doctor.Address}</td>
                    <td>${doctor.Phone}</td>
                </tr>
            `).join('')}
        </table>
        `;

        doctorsListElement.innerHTML = listHtml;
    } else {
        doctorsListElement.innerHTML = '<p>No doctors found.</p>';
    }
}


// This function gets the value of a cookie by name
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// // The submitForm function with the CSRF token included in the headers
// function submitForm() {
//     // Get the CSRF token from the cookie
//     const csrftoken = getCookie('csrftoken');

//     // Get the selected city's text content and the specialization value from the form elements
//     const citySelect = document.getElementById('city');
//     const selectedCity = citySelect.options[citySelect.selectedIndex].text; // Corrected line
//     const selectedSpecialization = document.getElementById('specialization').value;

//     // Prepare the search criteria, assuming the city names in the database are stored in a case-insensitive manner
//     const searchCriteria = {
//         city: selectedCity,
//         specialization: selectedSpecialization
//     };

//     // Make an AJAX POST request to your local search endpoint
//     console.log("body: ", JSON.stringify(searchCriteria));
//     fetch('/search', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken
//         },
//         body: JSON.stringify(searchCriteria),
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         return response.json();
//     })
//     .then(data => {
//         // Handle the search results here
//         console.log(data);
//     })
//     .catch(error => {
//         console.error('Error during fetch:', error);
//     });
// }

window.onload = function() {
    loadStates(6252001); // Load the states of US
    document.getElementById('state').innerHTML = '<option value="">Select State/Province</option>';
    document.getElementById('county').innerHTML = '<option value="">Select County</option>';
    document.getElementById('city').innerHTML = '<option value="">Select City</option>'; // Ensure "Select City" is set on page load
    window.submitForm = submitForm;
};