let tg = window.Telegram.WebApp;
let currentFlower = "";

function openOrder(name, price, qty) {
    currentFlower = name;
    document.getElementById('shop').classList.add('hidden');
    document.getElementById('orderForm').classList.remove('hidden');
    document.getElementById('selectedFlower').innerText = name + " - " + price + "₸";
}

function sendData() {
    let data = {
        flower: currentFlower,
        address: document.getElementById('address').value,
        count: document.getElementById('count').value,
        budget: document.getElementById('budget').value
    };
    tg.sendData(JSON.stringify(data)); // Отправляем данные боту
    tg.close();
}