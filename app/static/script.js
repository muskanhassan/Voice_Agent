const stopBtn =
    document.getElementById("stop-btn");

const micBtn =
    document.getElementById("mic-btn");

const chatBox =
    document.getElementById("chat-box");

const voiceSelect =
    document.getElementById("voice");

let recognition;


// Add chat message
function addMessage(
    text,
    sender
) {

    const div =
        document.createElement("div");

    div.className =
        `message ${sender}`;

    div.innerText =
        text;

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


// Load browser voices
let voices = [];

function loadVoices() {

    voices =
        speechSynthesis
            .getVoices();

    console.log(
        "Voices loaded:",
        voices
    );
}

speechSynthesis.onvoiceschanged =
    loadVoices;

loadVoices();


// Speech Recognition
const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (!SpeechRecognition) {

    alert(
        "Please use Google Chrome."
    );

} else {

    recognition =
        new SpeechRecognition();

    recognition.continuous =
        true;

    recognition.interimResults =
        true;

    recognition.lang =
        "en-US";
}


// Speak text
function speakText(text) {

    // stop old speech
    window.speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(
            text
        );

    speech.lang =
        "en-US";

    // Female voice
    if (
        voiceSelect.value
        === "Female"
    ) {

        speech.voice =
            voices.find(v =>
                v.name.includes(
                    "Zira"
                )
            ) ||

            voices.find(v =>
                v.name.includes(
                    "Female"
                )
            ) ||

            voices.find(v =>
                v.lang.includes(
                    "en"
                )
            );
    }

    // Male voice
    else {

        speech.voice =
            voices.find(v =>
                v.name.includes(
                    "David"
                )
            ) ||

            voices.find(v =>
                v.name.includes(
                    "Male"
                )
            ) ||

            voices.find(v =>
                v.lang.includes(
                    "en"
                )
            );
    }

    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    window
        .speechSynthesis
        .speak(speech);
}


// Greeting on load
window.onload =
    function () {

        const greeting =
            "Hello, I am your AI Assistant.";

        addMessage(
            greeting,
            "ai"
        );

        setTimeout(() => {

            speakText(
                greeting
            );

        }, 1000);
    };


// Mic button
micBtn.addEventListener(
    "click",
    async () => {

        try {

            // ask mic permission
            await navigator
                .mediaDevices
                .getUserMedia({
                    audio: true
                });

            recognition.start();

            micBtn.innerHTML =
                "🎙 Listening...";

        } catch (error) {

            console.log(
                error
            );

            alert(
                "Microphone permission denied"
            );
        }
    }
);


// User speech result
recognition.onresult =
    async function (
        event
    ) {

        let text = "";

        for (
            let i = event.resultIndex;
            i <
            event.results.length;
            i++
        ) {

            if (
                event.results[i]
                    .isFinal
            ) {

                text =
                    event.results[i][0]
                        .transcript;
            }
        }

        if (!text) return;

        console.log(
            "User:",
            text
        );

        addMessage(
            text,
            "user"
        );

        await getAIReply(
            text
        );
    };


// Recognition ended
recognition.onend =
    function () {

        micBtn.innerHTML =
            "🎤 Start Talking";
    };


// Recognition error
recognition.onerror =
    function (
        event
    ) {

        console.log(
            "Mic Error:",
            event.error
        );

        if (
            event.error
            !== "no-speech"
        ) {

            alert(
                "Microphone error: "
                + event.error
            );
        }

        micBtn.innerHTML =
            "🎤 Start Talking";
    };


// Get AI reply
async function getAIReply(
    userText
) {

    try {

        const response =
            await fetch(
                "/chat",
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            message:
                                userText
                        })
                }
            );

        const data =
            await response.json();

        console.log(
            "AI:",
            data.reply
        );

        addMessage(
            data.reply,
            "ai"
        );

        speakText(
            data.reply
        );

    } catch (error) {

        console.log(
            error
        );

        addMessage(
            "AI connection error",
            "ai"
        );
    }
}


// Stop button
stopBtn.addEventListener(
    "click",
    () => {

        if (
            recognition
        ) {

            recognition.stop();
        }

        window
            .speechSynthesis
            .cancel();

        micBtn.innerHTML =
            "🎤 Start Talking";
    }
);