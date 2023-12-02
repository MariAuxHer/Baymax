import { loadCountries, loadStates, loadCities } from "./utils.js";

// Initial call to load countries when the page loads
window.onload = loadCountries;