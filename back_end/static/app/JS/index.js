import { log_conversations, session, post_prompt, post_conversation, update_name, delete_conversation } from "./utils.js";

const messages = document.getElementById("messages")
const button_text_size = 30

// keeps track of which conversation the user is looking at (null)
// means that the user is looking at the empty conversation screen (where 
// they may randomly prompt and create a new conversation)
let conversation_url = null; 
let convo_count = 1;

document.addEventListener('DOMContentLoaded', async () => {
    session().then(async (result) => {

        // logged in
        if (result === true) {
            const conversations = await log_conversations() 
            
            // Display most recent conversation
            try {
                conversation_url = conversations[0].url
            } catch {
                console.log("No conversation to display, keeping what should be the default page")
            }
 
            // populate the panel with buttons
            const panel = document.getElementById('panelContainer')
            for (let i = conversations.length - 1; i >= 0; i--) {
                update_name(conversations[i].url, "new name").then( (data) => {
                    console.log(data)
                })

                add_conversation_button(conversations[i].url)
            }
        } 
        // not logged in
        else {
            window.location.pathname = 'login'
        }
    })
});


document.getElementById('message_form').addEventListener('submit', async (event) => {
    event.preventDefault()
    console.log("calling event listener, message_form")
    // const text = document.getElementById('prompt_text').innerHTML
    const text = document.getElementById('message_textarea').value
    
    if (text!== "") {
        add_prompt(text)
        if (conversation_url) { 
            // make sure we dont send an empty prompt // though it doesn't technically break anything it is still something we should validate
            /*
                The post_prompt and post_conversation functions are presumably responsible for sending the data to your backend. 
                Ensure these functions correctly make AJAX calls to your API endpoints.
            */
            const interaction = await post_prompt(conversation_url, text)

            /*
                The add_LLMresponse function is used to display the LLM's response on the page. 
                Ensure this updates the page appropriately after the backend returns a response.
            */
            if (interaction) {
                add_LLMresponse(interaction.LLMresponse)
                console.log("LLMresponse" + interaction.LLMresponse)
            } else {
                add_LLMresponse("post_prompt didnt come back with anything")
                console.error("post_prompt didnt come back with anything")
            } 
        } else {
            console.log("no interaction")
            const conversation = await post_conversation(text, text)

            if (conversation) {
                if (conversation.interaction_set[0]) {
                    add_LLMresponse(conversation.interaction_set[0].LLMresponse)
                    conversation_url = conversation.url

                    add_conversation_button(conversation.url)
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

// panel.js
const coll = document.querySelectorAll(".collapsible");
coll.forEach((button) => {
    button.addEventListener("click", function () {
        const content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
});

document.getElementById("addConversation").addEventListener("click", function () {
  default_page()
});

function add_conversation_button(url) { 
    const panel = document.getElementById('panelContainer')
    const conversation_options = document.createElement('div')

    const conversation_button = document.createElement('button')
    conversation_button.className = "collapsible"
    conversation_button.textContent = "Conversation " + convo_count
    conversation_button.setAttribute('id', panel.id + '_conversation_button_' + convo_count)

    conversation_button.addEventListener('click', () => {
        conversation_url = url
        load_conversation(url)
    })

    /*const delete_button = document.createElement('button')
    delete_button.textContent = "def" // this line is temporary until we decide what it will look like
    delete_button.setAttribute('id', panel.id + '_delete_button_' + convo_count++)

    delete_button.addEventListener('click', () => {
        delete_conversation(url)
        conversation_options.remove()
        default_page(); 
    }) */

    const delete_button = document.createElement('button');
    delete_button.setAttribute('id', panel.id + '_delete_button_' + convo_count++);
    delete_button.className = 'delete-button'; 

    delete_button.addEventListener('click', () => {
        delete_conversation(url);
        conversation_options.remove();
        default_page(); 
    }) 



    conversation_options.appendChild(conversation_button)
    conversation_options.appendChild(delete_button)
    let parent = document.querySelector(".panel");
    let insert_anchor = document.querySelector(".panel_nav");
    parent.insertBefore(conversation_options, insert_anchor);
}


// helper
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

