let tg = window.Telegram.WebApp;
let selectedFlowerName = "";

// Подстраиваем Mini App под экран Телеграма
tg.expand();
tg.ready();

function openOrder(name, price) {
    selectedFlowerName = name;
    
    // Скрываем каталог, показываем форму
    document.getElementById('main-container').classList.add('hidden');
    document.getElementById('orderForm').classList.remove('hidden');
    
    // Подставляем данные выбранного цветка
    document.getElementById('selectedFlower').innerText = name;
    document.getElementById('selectedPrice').innerText = price.toLocaleString() + " ₸";
    
    // Прокручиваем наверх формы на всякий случай
    window.scrollTo(0, 0);
}

function closeOrder() {
    // Возвращаем всё обратно: скрываем форму, показываем каталог
    document.getElementById('orderForm').classList.add('hidden');
    document.getElementById('main-container').classList.remove('hidden');
    
    // Очищаем поля формы, чтобы при следующем заказе они были пустыми
    document.getElementById('address').value = "";
    document.getElementById('count').value = "1";
    document.getElementById('budget').value = "";
}

function sendData() {
    const address = document.getElementById('address').value.trim();
    const count = document.getElementById('count').value;
    const budget = document.getElementById('budget').value.trim();

    if (!address || address.length < 5) {
        tg.showAlert("Господин, пожалуйста, введите корректный адрес доставки.");
        return;
    }

    const orderData = {
        flower: selectedFlowerName,
        address: address,
        count: count,
        budget: budget ? budget : "Не указан"
    };

    // Отправляем данные боту и закрываем окно
    tg.sendData(JSON.stringify(orderData));
    tg.close();
}