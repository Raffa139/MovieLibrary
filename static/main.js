const handleMessage = () => {
    const msg = document.querySelector("#msg");
    const msgTimer = document.querySelector("#msg-timer");

    if (msg && msgTimer) {
        new ResizeObserver(changes => {
            [change] = changes;
            width = change.contentRect.width;

            if (width <= 0.25) {
                msg.classList.add("hidden");
            }
        }).observe(msgTimer)
    }
};

const hideModal = () => {
    const modal = document.querySelector("#modal");
    modal.classList.add("hidden");
};

window.onload = () => handleMessage();
