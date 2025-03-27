const handleMessage = () => {
    const msg = document.querySelector("#msg");

    if (msg) {
        const timer = document.querySelector("#timer");
        let elapsedTime = 5;
        timer.innerHTML = elapsedTime;

        const timerInterval = setInterval(() => {
            elapsedTime -= 1;
            timer.innerHTML = elapsedTime;
        }, 1000);

        setTimeout(() => {
            msg.classList.add("hidden");
            clearInterval(timerInterval);
        }, (elapsedTime + 0.5) * 1000);
    }
}

const hideModal = () => {
    const modal = document.querySelector("#modal");
    modal.classList.add("hidden");
};

window.onload = () => handleMessage();
