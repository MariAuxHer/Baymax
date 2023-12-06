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
window.onload = loadStates(6252001);  // Load the states of US