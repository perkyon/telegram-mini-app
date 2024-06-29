document.getElementById('payButton').addEventListener('click', function() {
    const data = {
        user_id: window.Telegram.WebApp.initDataUnsafe.user.id,
        user_name: window.Telegram.WebApp.initDataUnsafe.user.username
    };
    Telegram.WebApp.sendData(JSON.stringify(data));
});

Telegram.WebApp.ready();
