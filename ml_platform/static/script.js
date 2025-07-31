// Переключение списка тем по модулям
function toggleTopics(id) {
    const list = document.getElementById(id);
    list.style.display = list.style.display === 'none' ? 'block' : 'none';
  }
  
  // Получаем элементы
  const askBtn = document.getElementById('ask-button');
  const chatPopup = document.getElementById('chat-popup');
  const chatMessages = document.getElementById('chat-messages');
  const inputField = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-button');
  const closeButton = document.getElementById('close-chat');
  
  // Функция добавления сообщения в чат
  function addMessage(content, sender = 'user') {
    const msg = document.createElement('div');
    msg.className = 'message ' + sender;
    msg.textContent = content;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  
  // Отображение кнопки "Объясни" при выделении текста
  document.addEventListener('mouseup', function (e) {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 0) {
      const x = e.pageX;
      const y = e.pageY;
      askBtn.style.left = `${x + 10}px`;
      askBtn.style.top = `${y}px`;
      askBtn.style.display = 'block';
      askBtn.dataset.text = selectedText;
    } else {
      askBtn.style.display = 'none';
    }
  });
  
  // Обработка клика по кнопке "Объясни" при выделении
  askBtn.addEventListener('click', function () {
    const selected = askBtn.dataset.text;
    chatPopup.style.display = 'flex';
    addMessage(selected, 'user');
    addMessage("Запрос отправлен...", 'bot');
  
    fetch('/ask_ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: selected })
    })
      .then(res => res.json())
      .then(data => {
        const lastBotMessage = chatMessages.querySelector('.message.bot:last-child');
        if (lastBotMessage) {
          lastBotMessage.textContent = data.answer;
        }
      });
  });
  
  // Обработка отправки текста вручную через кнопку "Объясни иначе"
  sendButton.addEventListener('click', () => {
    const userText = inputField.value.trim();
    if (!userText) return;
  
    addMessage(userText, 'user');
    inputField.value = '';
    chatPopup.style.display = 'flex';
    addMessage("Обрабатываю...", 'bot');
  
    fetch('/ask_ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: userText })
    })
      .then(res => res.json())
      .then(data => {
        const lastBotMessage = chatMessages.querySelector('.message.bot:last-child');
        if (lastBotMessage) {
          lastBotMessage.textContent = data.answer;
        }
      });
  });
  
  // Отправка по клавише Enter
  inputField.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      sendButton.click();
    }
  });
  
  // Закрытие чата
  closeButton.addEventListener('click', function () {
    chatPopup.style.display = 'none';
  });

const chat = document.getElementById('chat-popup');
const cat = chat.querySelector('.spacecat-wrapper_main');

const observer = new ResizeObserver(entries => {
  for (const entry of entries) {
    const height = entry.contentRect.height;
    cat.style.top = `${-Math.min(50 + (height - 340) * 0.3, 120)}px`; 
    // максимум поднимаем до -120px, регулируй по вкусу
  }
});

observer.observe(chat);

  

