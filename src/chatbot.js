// --- Referencias a elementos del DOM ---
const chatWindow = document.getElementById('chat-window');
const chatLog = document.getElementById('chat-log');
const chatBubbleBtn = document.getElementById('chat-bubble-btn');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatFooter = document.getElementById('chat-footer');

// --- Variables de estado y datos ---
let userData = { fullName: "", department: "" };
let conversationStep = "awaiting_full_name";
let lastProblemKey = "";
let optionsShownCount = 0; // **NUEVO:** Contador para el menú de opciones

// --- Asignación de Eventos ---
chatBubbleBtn.addEventListener('click', toggleChat);
sendBtn.addEventListener('click', handleUserInput);
userInput.addEventListener('keydown', (event) => { if (event.key === 'Enter') handleUserInput(); });

// --- Base de datos de soluciones ---
const solutions = {
    teclado_mouse: `<strong>Solución para Teclado y Mouse:</strong><br><br>1. Revisa la conexión USB y prueba en otro puerto.<br>2. Si es inalámbrico, comprueba las baterías.<br>3. Reinicia el equipo.`,
    impresora: `<strong>Solución para problemas de Impresora:</strong><br><br>1. Asegúrate de que la impresora esté encendida.<br>2. Confirma que tenga papel y tinta/tóner.<br>3. Reinicia la impresora.<br>4. Si es una impresora de red, verifica que tu equipo y la impresora tengan conexión a la red.`,
    internet: `<strong>Solución para problemas de Internet:</strong><br><br>1. Reinicia tu Módem y Router.<br>2. Verifica el cableado de red.<br>3. Si persiste, contacta a tu proveedor.`,
    contacto_ti: `<strong>Contacto con Soporte de TI:</strong><br><br>Para problemas de lentitud, por favor, genera un ticket de soporte enviando un email a: <strong>soporte.ti@tuempresa.com</strong>`
};

// --- Lógica del Chat ---
function toggleChat() {
    chatWindow.classList.toggle('hidden-chat');
    // Si la ventana se abre, se resetea la sesión
    if (!chatWindow.classList.contains('hidden-chat')) {
        resetSession();
    }
}

// **NUEVO:** Función para resetear el estado del chat
function resetSession() {
    chatLog.innerHTML = ''; // Limpia el historial del chat
    optionsShownCount = 0;
    conversationStep = "awaiting_full_name";
    userData = { fullName: "", department: "" };
    startIdentificationProcess();
}

function startIdentificationProcess() {
    chatFooter.style.display = 'block';
    addBotMessage("¡Hola! 👋 Soy tu asistente de TI. Por favor, dime tu <strong>nombre y apellido</strong>.");
    userInput.focus();
}

function handleUserInput() {
    const text = userInput.value.trim();
    if (text === "") return;
    addUserMessage(text);
    userInput.value = "";

    if (conversationStep === 'awaiting_full_name') {
        userData.fullName = text;
        addBotMessage(`¡Gracias, ${userData.fullName}! Ahora, dime a qué <strong>departamento</strong> perteneces.`);
        conversationStep = 'awaiting_department';
    } else if (conversationStep === 'awaiting_department') {
        userData.department = text;
        addBotMessage(`¡Listo! Te he registrado como <strong>${userData.fullName}</strong> del departamento de <strong>${userData.department}</strong>.`);
        conversationStep = 'problem_solving';
        setTimeout(showInitialOptions, 800);
    }
}

function showInitialOptions() {
        chatFooter.style.display = 'none';
        optionsShownCount++; // Aumenta el contador cada vez que se llama

        // **NUEVO:** Lógica para limitar las visualizaciones
        if (optionsShownCount > 2) {
            addBotMessage("Gracias por usar el asistente. Si necesitas más ayuda, no dudes en contactar directamente a TI. ¡Que tengas un buen día!");
            setTimeout(() => chatFooter.style.display = 'none', 100); // Se asegura que el input quede oculto
            return;
        }

        const optionsHtml = `
        <div class="chat chat-start" id="options-bubble">
                <div class="chat-bubble">
                    <p class="font-bold mb-2">${optionsShownCount === 1 ? 'Ahora sí, ¿cómo puedo ayudarte?' : '¿Hay algo más en lo que pueda ayudarte?'}</p>
                    <div class="flex flex-col space-y-2 items-start">
                        <button class="btn btn-sm btn-outline" onclick="selectOption('teclado_mouse', 'Problemas con Teclado / Mouse ⌨️🖱️')">Teclado / Mouse</button>
                        <button class="btn btn-sm btn-outline" onclick="selectOption('impresora', 'Problemas con la Impresora 🖨️')">Impresora</button>
                        <button class="btn btn-sm btn-outline" onclick="selectOption('internet', 'No tengo Conexión a Internet 🌐')">Internet</button>
                        <button class="btn btn-sm btn-outline" onclick="selectOption('contacto_ti', 'Mi equipo está lento / Otros 💻')">Equipo Lento / Otros</button>
                    </div>
                </div>
        </div>`;
    addMessageToLog(optionsHtml);
}

function selectOption(problemKey, userText) {
    lastProblemKey = problemKey;
    const oldOptions = document.getElementById('options-bubble') || document.getElementById('feedback-bubble');
    if (oldOptions) { oldOptions.remove(); }
    addUserMessage(userText);
    setTimeout(() => {
        const solutionHtml = solutions[problemKey];
        addBotMessage(solutionHtml);
        setTimeout(askForFeedback, 1500);
    }, 600);
}

function askForFeedback() {
    const feedbackHtml = `
        <div class="chat chat-start" id="feedback-bubble">
            <div class="chat-bubble">
                <p class="font-bold mb-2">¿Pude resolver tu problema?</p>
                <div class="flex space-x-2">
                    <button class="btn btn-sm btn-success" onclick="handleFeedback('yes')">Sí, gracias</button>
                    <button class="btn btn-sm btn-error" onclick="handleFeedback('no')">No, necesito más ayuda</button>
                </div>
            </div>
        </div>`;
    addMessageToLog(feedbackHtml);
}

function handleFeedback(response) {
    const feedbackBubble = document.getElementById('feedback-bubble');
    if (feedbackBubble) { feedbackBubble.remove(); }
    
    if (response === 'yes') {
        addUserMessage("Sí, gracias");
        addBotMessage("¡Excelente! Estoy para servirte. 😊");
    } else {
        addUserMessage("No, necesito más ayuda");
        const ticketMessage = `Entendido. He generado un ticket de soporte para el departamento de TI con tus datos:<br>
                                <strong>- Solicitante:</strong> ${userData.fullName}<br>
                                <strong>- Departamento:</strong> ${userData.department}<br>
                                <strong>- Problema:</strong> ${lastProblemKey.replace(/_/g, ' ')}<br><br>
                                Pronto se pondrán en contacto contigo.`;
        addBotMessage(ticketMessage);
    }
    // En lugar de llamar a offerMoreHelp, llamamos a showInitialOptions directamente
    setTimeout(showInitialOptions, 2000);
}

function addUserMessage(text) {
    const messageHtml = `<div class="chat chat-end"><div class="chat-bubble chat-bubble-info">${text}</div></div>`;
    addMessageToLog(messageHtml);
}

function addBotMessage(htmlContent) {
    const messageHtml = `
        <div class="chat chat-start">
            <div class="chat-image avatar">
                <div class="w-10 rounded-full"><img alt="Avatar del Asistente" src="Imagenes/bot.jpg" /></div>
            </div>
            <div class="chat-bubble">${htmlContent}</div>
        </div>`;
    addMessageToLog(messageHtml);
}

function addMessageToLog(html) {
    chatLog.insertAdjacentHTML('beforeend', html);
    chatLog.scrollTop = chatLog.scrollHeight;
}