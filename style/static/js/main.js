const totalQuestions = 2;
let currentQuestion = 1;

const profileBtn = document.getElementById('profileBtn');
const dropdownMenu = document.getElementById('dropdownMenu');

profileBtn.addEventListener('click', function(event) {
    event.stopPropagation();
    dropdownMenu.classList.toggle('hidden');
});

window.addEventListener('click', function(event) {
    if (!dropdownMenu.contains(event.target) && !profileBtn.contains(event.target)) {
        if (!dropdownMenu.classList.contains('hidden')) {
            dropdownMenu.classList.add('hidden');
        }
    }
});


function goToQuestion(qNumber) {
    document.getElementById(`soal-${currentQuestion}`).classList.remove('active');

    updateNavButtonState(currentQuestion);

    currentQuestion = qNumber;

    document.getElementById(`soal-${currentQuestion}`).classList.add('active');

    const activeBtn = document.getElementById(`btn-nav-${currentQuestion}`);
    if (activeBtn) {
        activeBtn.className = "h-10 w-full rounded border border-blue-600 bg-blue-600 text-white font-medium transition text-sm";
    }
}

function prevQuestion() {
    if (currentQuestion > 1) goToQuestion(currentQuestion - 1);
}

function nextQuestion() {
    if (currentQuestion < totalQuestions) goToQuestion(currentQuestion + 1);
}

function markAnswered(qNumber) {
    const btn = document.getElementById(`btn-nav-${qNumber}`);
    if (btn) {
        btn.setAttribute('data-answered', 'true');
    }
}

function updateNavButtonState(qNumber) {
    const btn = document.getElementById(`btn-nav-${qNumber}`);
    if (!btn) return;

    const isAnswered = btn.getAttribute('data-answered') === 'true';

    if (isAnswered) {
        btn.className = "h-10 w-full rounded border border-green-500 bg-green-500 text-white font-medium hover:opacity-80 transition text-sm";
    } else {
        btn.className = "h-10 w-full rounded border border-gray-300 bg-white text-gray-700 font-medium hover:bg-gray-100 transition text-sm";
    }
}

let timeInSeconds = 90 * 60;
function startTimer() {
    const timerDisplay = document.getElementById('timerDisplay');

    const interval = setInterval(function() {
        let hours = Math.floor(timeInSeconds / 3600);
        let minutes = Math.floor((timeInSeconds % 3600) / 60);
        let seconds = timeInSeconds % 60;

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        timerDisplay.textContent = `${hours}:${minutes}:${seconds}`;

        if (timeInSeconds <= 300) {
            timerDisplay.classList.add('animate-pulse');
        }

        if (timeInSeconds <= 0) {
            clearInterval(interval);
            timerDisplay.textContent = "00:00:00";
            alert("Waktu habis! Jawaban akan dikumpulkan otomatis.");
        }

        timeInSeconds--;
    }, 1000);
}

window.onload = startTimer;

