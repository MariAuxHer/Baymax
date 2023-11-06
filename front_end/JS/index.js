import { log_conversations, session } from "./utils.js";
const messages = document.getElementById("messages")

document.addEventListener('DOMContentLoaded', async function() {
    session().then(async (result) => {

        // logged in
        if (result === true) {
            const conversations = await log_conversations() 
            
            // Display most recent conversation
            try {
                for (let i = conversations[0].interaction_set.length - 1; i >= 0; i--) {
                    const promptElement = document.createElement('p')
                    promptElement.setAttribute('class', 'right')
                    promptElement.innerHTML = conversations[0].interaction_set[i].prompt
    
                    const LLMresponseElement = document.createElement('p')
                    LLMresponseElement.setAttribute('class', 'left')
                    LLMresponseElement.innerHTML = conversations[0].interaction_set[i].LLMresponse
                    
                    messages.appendChild(promptElement)
                    messages.appendChild(LLMresponseElement)
                }
            } catch {
                console.log("No conversation to display, falling back to default message.")
                messages.appendChild(first_message())
            }
        } 
        // not logged in
        else {
            console.log("default home page behavior")

            messages.appendChild(first_message())
        }
    })
});

function first_message() {
    const welcome_message = document.createElement('p')
    welcome_message.setAttribute('class', 'left')
    welcome_message.innerHTML = "Hello, it's me"

    return welcome_message
}

