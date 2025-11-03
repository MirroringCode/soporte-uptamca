// --- Referencias a elementos del DOM ---
const chatWindow = document.getElementById('chat-window');
const chatLog = document.getElementById('chat-log');
const chatBubbleBtn = document.getElementById('chat-bubble-btn');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatFooter = document.getElementById('chat-footer');

// --- Variables de estado y datos ---
let userData = { id: null, fullName: "", department: "", departmentId: null };
let conversationStep = "awaiting_full_name";
let lastProblemKey = "";
let optionsShownCount = 0;
let currentTicketId = null; // Para guardar el ID del ticket actual

// --- Asignación de Eventos ---
chatBubbleBtn.addEventListener('click', toggleChat);
sendBtn.addEventListener('click', handleUserInput);
userInput.addEventListener('keydown', (event) => { if (event.key === 'Enter') handleUserInput(); });

// --- Base de datos de soluciones (Frontend) ---
const solutions = {
    teclado_mouse: `<strong>Solución para Teclado y Mouse:</strong><br><br>1. Revisa la conexión USB y prueba en otro puerto.<br>2. Si es inalámbrico, comprueba las baterías.<br>3. Reinicia el equipo.`,
    impresora: `<strong>Solución para problemas de Impresora:</strong><br><br>1. Asegúrate de que la impresora esté encendida.<br>2. Confirma que tenga papel y tinta/tóner.<br>3. Reinicia la impresora.<br>4. Si es una impresora de red, verifica que tu equipo y la impresora tengan conexión a la red.`,
    internet: `<strong>Solución para problemas de Internet:</strong><br><br>1. Reinicia tu Módem y Router.<br>2. Verifica el cableado de red.<br>3. Si persiste, contacta a tu proveedor.`,
    contacto_ti: `<strong>Contacto con Soporte de TI:</strong><br><br>Para problemas de lentitud, por favor, genera un ticket de soporte enviando un email a: <strong>soporte.ti@tuempresa.com</strong>`
};

// --- Lógica del Chat ---

function toggleChat() {
    chatWindow.classList.toggle('hidden-chat');
    if (!chatWindow.classList.contains('hidden-chat')) {
        resetSession();
    }
}

function resetSession() {
    chatLog.innerHTML = '';
    optionsShownCount = 0;
    conversationStep = "awaiting_full_name";
    userData = { id: null, fullName: "", department: "", departmentId: null };
    currentTicketId = null;
    startIdentificationProcess();
}

function startIdentificationProcess() {
    chatFooter.style.display = 'block';
    addBotMessage("¡Hola! 👋 Soy tu asistente de TI. Por favor, dime tu <strong>nombre y apellido</strong>.");
    userInput.focus();
}

async function handleUserInput() {
    const text = userInput.value.trim();
    if (text === "") return;
    addUserMessage(text);
    userInput.value = "";

    if (conversationStep === 'awaiting_full_name') {
        userData.fullName = text;
        addBotMessage(`¡Gracias! Ahora, dime a qué <strong>departamento</strong> perteneces.`);
        conversationStep = 'awaiting_department';
    } else if (conversationStep === 'awaiting_department') {
        userData.department = text;
        addBotMessage("Verificando tus datos, un momento por favor...");
        try {
            const response = await fetch('http://localhost:5500/verify-user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    fullName: userData.fullName,
                    department: userData.department
                })
            });
            const data = await response.json();
            if (data.success) {
                userData.id = data.employeeId;
                userData.departmentId = data.departmentId;
                addBotMessage(`¡Usuario verificado! Te he registrado como <strong>${userData.fullName}</strong>.`);
                conversationStep = 'problem_solving';
                setTimeout(showInitialOptions, 800);
            } else {
                addBotMessage(`<strong>Error:</strong> ${data.message}. Por favor, vuelve a intentarlo. Dime tu nombre y apellido.`);
                conversationStep = 'awaiting_full_name';
            }
        } catch (error) {
            console.error("Error de conexión:", error);
            addBotMessage("No pude conectarme con el servidor de verificación. Por favor, inténtalo más tarde.");
            conversationStep = 'awaiting_full_name';
        }
    }
}

function showInitialOptions() {
    chatFooter.style.display = 'none';
    optionsShownCount++;
    if (optionsShownCount > 2) {
        addBotMessage("Gracias por usar el asistente. Si necesitas más ayuda, puedes contactar directamente a TI. ¡Que tengas un buen día!");
        setTimeout(() => chatFooter.style.display = 'none', 100);
        return;
    }
    const optionsHtml = `
        <div class="chat chat-start" id="options-bubble">
            <div class="chat-bubble">
                <p class="font-bold mb-2">${optionsShownCount === 1 ? 'Ahora sí, ¿cómo puedo ayudarte?' : '¿Hay algo más en lo que pueda ayudarte?'}</p>
                <div class="flex flex-col space-y-2 items-start">
                    <button class="btn btn-sm btn-outline" onclick="selectOption('teclado/mouse', 'Problemas con Teclado / Mouse ⌨️🖱️')">Teclado / Mouse</button>
                    <button class="btn btn-sm btn-outline" onclick="selectOption('impresora', 'Problemas con la Impresora 🖨️')">Impresora</button>
                    <button class="btn btn-sm btn-outline" onclick="selectOption('internet', 'No tengo Conexión a Internet 🌐')">Internet</button>
                    <button class="btn btn-sm btn-outline" onclick="selectOption('contacto_ti', 'Mi equipo está lento / Otros 💻')">Equipo Lento / Otros</button>
                </div>
            </div>
        </div>`;
    addMessageToLog(optionsHtml);
}

// **MODIFICADO:** Ahora crea el ticket inmediatamente
async function selectOption(problemKey, userText) {
    lastProblemKey = problemKey;
    const oldOptions = document.getElementById('options-bubble') || document.getElementById('feedback-bubble');
    if (oldOptions) { oldOptions.remove(); }
    addUserMessage(userText);

    try {
        const response = await fetch('http://localhost:5500/create-ticket', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                employeeId: userData.id,
                departmentId: userData.departmentId,
                problemType: problemKey
            })
        });
        const data = await response.json();
        if (data.success) {
            currentTicketId = data.ticketId; // Guardamos el ID del ticket
            addBotMessage(`He generado el ticket de soporte N° **${currentTicketId}**. Mientras esperas, aquí tienes una posible solución:`);
        } else {
            addBotMessage("Hubo un error al generar tu ticket, pero aquí tienes una posible solución:");
        }
    } catch (error) {
        console.error("Error al crear ticket:", error);
        addBotMessage("No pude conectar con el servidor para crear el ticket, pero aquí tienes una posible solución:");
    }

    setTimeout(() => {
        const solutionHtml = solutions[problemKey];
        addBotMessage(solutionHtml);
        setTimeout(askForFeedback, 1500);
    }, 800);
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

// **MODIFICADO:** Ahora actualiza el estado del ticket en lugar de crear uno nuevo
async function handleFeedback(response) {
    const feedbackBubble = document.getElementById('feedback-bubble');
    if (feedbackBubble) { feedbackBubble.remove(); }
    
    let status = (response === 'yes') ? 'resolved' : 'escalated';

    if (response === 'yes') {
        addUserMessage("Sí, gracias");
        addBotMessage("¡Excelente! He marcado el ticket como **resuelto**. Estoy para servirte. 😊");
    } else {
        addUserMessage("No, necesito más ayuda");
        addBotMessage(`Entendido. El ticket N° **${currentTicketId}** queda abierto. El equipo de TI se pondrá en contacto contigo.`);
    }
    
    // **INICIO: LÓGICA PARA ACTUALIZAR EL TICKET EN EL BACKEND**
    try {
        await fetch('http://localhost:5500/update-ticket-status', { // Llama al nuevo endpoint
            method: 'POST', // Usamos POST por simplicidad, aunque PUT/PATCH sería más semántico
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticketId: currentTicketId,
                status: status
            })
        });
    } catch (error) {
        console.error("No se pudo actualizar el ticket:", error);
    }
    // **FIN: LÓGICA PARA ACTUALIZAR EL TICKET**

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
                <div class="w-10 rounded-full"><img alt="Avatar del Asistente" src="./img/bot.jpg" /></div>
            </div>
            <div class="chat-bubble">${htmlContent}</div>
        </div>`;
    addMessageToLog(messageHtml);
}
        
function addMessageToLog(html) {
    chatLog.insertAdjacentHTML('beforeend', html);
    chatLog.scrollTop = chatLog.scrollHeight;
}