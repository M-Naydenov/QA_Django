const startingMinutes = 10;
let time = startingMinutes * 60;

const countDownElement = document.getElementById("pkt-counter");

setInterval(updateCountdown, 1000);

function updateCountdown() {

    const minutes = Math.floor(time/60);
    let seconds = Math.floor(time%60);

    seconds = seconds <10 ? '0' + seconds : seconds;

    countDownElement.innerHTML = `${minutes}:${seconds}`;
    time--;
}