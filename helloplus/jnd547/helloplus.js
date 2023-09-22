
let number;

window.onload = function() {
    number = Math.floor(Math.random() * 10);
    console.log(number);
}

var submitButton = document.getElementById("check_answer");
submitButton.onclick = function() {
    var input = document.getElementById("answerbox").value;

    var outcome = document.getElementById("outcome_text")
    if (input == number) {
        outcome.textContent = "You win!";
    }
    else {
        outcome.textContent = "You lose. The number was " + number;
    }
} 

