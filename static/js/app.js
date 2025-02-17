let startTime, interval;
let movimientoTime = 0;
let tiemposInicio = {};  // Almacena el tiempo de inicio por cada tecla
let totalTime = 0;
const timerDisplay = document.getElementById('timer');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
let car = document.getElementById('car');
const tiempoParado = document.getElementById('tiempo_parado');
const tiempoMovimiento = document.getElementById('tiempo_movimiento');
const tiempoTotal = document.getElementById('tiempo_total');
const totalPagar = document.getElementById('total_pagar');

function iniciarTaximetro() {
    // Reiniciar los valores del info-container
    clearInterval(interval);
    tiempoParado.textContent = '00:00:00';
    tiempoMovimiento.textContent = '00:00:00';
    tiempoTotal.textContent = '00:00:00';
    totalPagar.textContent = '0.00€';

    movimientoTime = 0;  //  Reiniciar el tiempo de movimiento al iniciar
    fetch('/iniciar_taximetro', { method: 'POST' });
    startTime = Date.now();
    timerDisplay.classList.add('running'); //que se inicie la animacion. 
    interval = setInterval(updateTimer, 1000);
    document.addEventListener('keydown', girarCoche);
    document.addEventListener('keyup', resetearCoche);

    startBtn.disabled = true;
    stopBtn.disabled = false;
}

function finalizarTaximetro() {
    clearInterval(interval);
    const totalTime = (Date.now() - startTime) / 1000;
    document.removeEventListener('keydown', girarCoche);
    document.removeEventListener('keyup', resetearCoche);

    fetch('/finalizar_taximetro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tiempo_total: totalTime,
            tiempo_movimiento: movimientoTime
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('conductor').textContent = data.conductor;
        document.getElementById('tiempo_parado').textContent = formatTime(totalTime - movimientoTime).padStart(2, '0');
        document.getElementById('tiempo_movimiento').textContent = formatTime(movimientoTime);
        document.getElementById('tiempo_total').textContent = formatTime(totalTime);
        document.getElementById('total_pagar').textContent = `${data.total_pagar.toFixed(2)}€`;
    });

    // Resaltar el info-container momentáneamente
    infoContainer.classList.add('highlight');
    setTimeout(() => infoContainer.classList.remove('highlight'), 1000);

    startBtn.disabled = false;
    stopBtn.disabled = true;
    /*reiniciar timer*/
    timerDisplay.classList.remove('running');
    timerDisplay.textContent = '00:00:00';

    tiempoParado.textContent = '00:00:00';
    tiempoMovimiento.textContent = '00:00:00';
    tiempoTotal.textContent = '00:00:00';
    totalPagar.textContent = '0.00€';
    console.log(` tiempoMovimiento ${tiempoMovimiento}`);

}

function updateTimer() {
    let elapsedTime = Math.floor((Date.now() - startTime) / 1000);
    timerDisplay.textContent = formatTime(elapsedTime);
    tiempoTotal.textContent = formatTime(elapsedTime);
}

function formatTime(seconds) {
    let hours = String(Math.floor(seconds / 3600)).padStart(2, '0');
    let minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    let secs = (seconds % 60).toFixed(2).toString().padStart(2, '0');
    return `${hours}:${minutes}:${secs}`;
}

function girarCoche(event) {
    const key = event.key;
    if (key >= '0' && key <= '9') {
        if (!tiemposInicio[key]) {
            tiemposInicio[key] = Date.now();  // Registro del tiempo de inicio
        }
        if (key === '7') {
            car.style.transform = 'rotate(-45deg)';
        } else if (key === '8') {
            car.style.transform = 'rotate(0deg)';
        } else if (key === '9') {
            car.style.transform = 'rotate(45deg)';      
        } else {
            car.style.transform = 'rotate(0deg)';
        }
    }
}

function resetearCoche(event) {
    const key = event.key;
    if (key >= '0' && key <= '9' && tiemposInicio[key]) {
        const tiempoPresionado = (Date.now() - tiemposInicio[key]) / 1000;  // Tiempo presionado en segundos
        movimientoTime += tiempoPresionado;  // Acumula el tiempo de movimiento
        console.log(`Tecla ${key} presionada durante ${tiempoPresionado} segundos`);
        delete tiemposInicio[key];  // Elimina el registro para esa tecla
        car.style.transform = 'rotate(0deg)';  // Regresa el coche a su posición original
    }
}