const aiBtn = document.getElementById('aiInspireBtn');
const aiMsgDiv = document.getElementById('aiMessageBlock');

const BACKEND_URL = 'https://fullstack-back.twc1.net';

aiBtn.addEventListener('click', async () => {
    aiBtn.disabled = true;
    aiMsgDiv.innerHTML = '<span class="loader"></span> Нейросеть генерирует мысль...';
    
    try {
        const response = await fetch(`${BACKEND_URL}/api/ai-tip`);
        
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error(`Сервер вернул ошибку ${response.status} (не JSON)`);
        }

        if (!response.ok) {
            throw new Error('Не удалось получить ответ от ИИ');
        }
        
        const data = await response.json();
        const aiText = data.ai_phrase || '✨ Упс! Но искусство кода всегда вдохновляет.';
        aiMsgDiv.innerHTML = `🤖 ✦ ${aiText} ✦`;
    } catch (error) {
        console.error(error);
        aiMsgDiv.innerHTML = '✨ Упс! Но искусство кода всегда вдохновляет.';
    } finally {
        aiBtn.disabled = false;
    }
});


const form = document.getElementById('feedbackForm');
const statusDiv = document.getElementById('formStatus');
const submitBtn = document.getElementById('sendBtn');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const email = document.getElementById('email').value.trim();
    const comment = document.getElementById('message').value.trim(); 

    if (!name || !phone || !email || !comment) {
        statusDiv.innerHTML = '<span style="color:#FFAA87;">❌ Заполните все поля формы</span>';
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\- ]?[0-9]{3}[\s\- ]?[0-9]{2}[\s\- ]?[0-9]{2}$/;

    if (!emailRegex.test(email)) {
        statusDiv.innerHTML = '<span style="color:#FFAA87;">❌ Введите корректный адрес почты (например, user@mail.ru)</span>';
        return;
    }

    if (!phoneRegex.test(phone)) {
        statusDiv.innerHTML = '<span style="color:#FFAA87;">❌ Введите корректный номер телефона (например, +79991234567)</span>';
        return;
    }
    statusDiv.innerHTML = '<div><span class="loader"></span> Отправка заявки...</div>';
    submitBtn.disabled = true;


    const payload = { name, phone, email, comment };

    try {
        const response = await fetch(`${BACKEND_URL}/api/send_mail`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error(`Ошибка сервера (${response.status}). На бэкенде закрыты порты или упал SMTP.`);
        }

        const result = await response.json();

        if (!response.ok) {
            if (response.status === 422 && result.detail) {
                if (Array.isArray(result.detail)) {
                    throw new Error(result.detail[0].msg);
                }
                throw new Error(result.detail.detail || result.detail);
            }
            if (response.status === 429) {
                throw new Error("Слишком много запросов. Подождите минуту.");
            }
            throw new Error(result.message || 'Ошибка отправки');
        }

        statusDiv.innerHTML = '<span style="color:#B0FFB0;">✅ Успешно! Заявка принята, копия письма отправляется вам.</span>';
        form.reset();

    } catch (err) {
        statusDiv.innerHTML = `<span style="color:#FFA5A5;">❌ Ошибка: ${err.message}</span>`;
    } finally {
        submitBtn.disabled = false;
        
        setTimeout(() => {
            if (statusDiv.innerHTML.includes('✅')) {
                statusDiv.innerHTML = '';
            }
        }, 7000);
    }
});
