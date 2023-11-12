import { log_conversations, session, post_prompt, post_conversation } from "./utils.js";

const messages = document.getElementById("messages")

// keeps track of which conversation the user is looking at (null)
// means that the user is looking at the empty conversation screen (where 
// they may randomly prompt and create a new conversation)
let conversation_url = null; 

document.addEventListener('DOMContentLoaded', async () => {
    session().then(async (result) => {

        // logged in
        if (result === true) {
            // adjust navbar
            const login_button = document.getElementById('toLoginPage')
            login_button.remove()

            const conversations = await log_conversations() 
            
            // Display most recent conversation
            try {
                load_conversation(conversations[0].url)
            } catch {
                console.log("No conversation to display, falling back to default message.")
                default_page()
            }

            const panel = document.getElementById('panelContainer')

            // create default conversation button
            const default_button = document.createElement('button')
            default_button.setAttribute('id', 'default_button')
            default_button.addEventListener('click', () => {
                default_page()
            })
            panel.appendChild(default_button)

            // populate the panel with buttons
            for (let i = 0; i < conversations.length; i++) {
                const button = document.createElement('button')
                button.setAttribute('id', panel.id + '_button_' + i)
                button.addEventListener('click', () => {
                    load_conversation(conversations[i].url)
                    conversation_url = conversations[i].url
                })

                panel.appendChild(button)
            }
        } 
        // not logged in
        else {
            window.location.pathname = 'html/login.html'
        }
    })
});

document.addEventListener('submit', async (event) => {
    event.preventDefault()

    const text = document.getElementById('prompt_text').innerHTML
    
    if (text!== "") {
        add_prompt(text)
        if (conversation_url) { 
            // make sure we dont send an empty prompt // though it doesn't technically break anything it is still something we should validate
            const interaction = await post_prompt(conversation_url, text)

            if (interaction) {
                add_LLMresponse(interaction.LLMresponse)
            } else {
                add_LLMresponse("post_prompt didnt come back with anything")
                console.error("post_prompt didnt come back with anything")
            } 
        } else {
            const conversation = await post_conversation(text, text)

            if (conversation) {
                if (conversation.interaction_set[0]) {
                    add_LLMresponse(conversation.interaction_set[0].LLMresponse)
                    conversation_url = conversation.url
                } else {
                    add_LLMresponse("post_conversation didnt come back with a DEFAULT INTERACTION")
                    console.error("post_conversation didnt come back with a DEFAULT INTERACTION")
                }
            } else {
                add_LLMresponse("post_conversation didnt come back with anything")
                console.error("post_conversation didnt come back with anything")
            }
        } 
    }
})

function default_page() {
    messages.innerHTML = ""
    add_LLMresponse("Hello, it's me")
    conversation_url = null; 
}

async function load_conversation(url) {
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })

    if (response.ok) {
        console.log("LOAD_CONVERSATION Conversation Fetched")

        const json = await response.json()

        try {
            print_conversation(json)
        } catch {
            console.log("No conversation to display, falling back to default message.")
            messages.appendChild(first_message())
        }
    } else {
        console.error("Failed to get conversation")
    }
}

async function print_conversation(conversation_obj) {
    messages.innerHTML = ""
    for (let i = conversation_obj.interaction_set.length - 1; i >= 0; i--) {                    
        add_prompt(conversation_obj.interaction_set[i].prompt)
        add_LLMresponse(conversation_obj.interaction_set[i].LLMresponse)
    }
    conversation_url = conversation_obj.url; 
}

/*
 * Adds a LLMResponse (string) to the left side of the window chat starting from the bottom
 */ 
function add_LLMresponse(LLMresponse) {
    const LLMresponseElement = document.createElement('p')
    LLMresponseElement.setAttribute('class', 'left')
    LLMresponseElement.innerHTML = LLMresponse
    messages.appendChild(LLMresponseElement)
}

function add_prompt(prompt) {
    const promptElement = document.createElement('p')
    promptElement.setAttribute('class', 'right')
    promptElement.innerHTML = prompt
    messages.appendChild(promptElement)
}

