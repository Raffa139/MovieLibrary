const clearMessageFromUrl = () => {
    const url = new URL(window.location.href);
    const searchParams = new URLSearchParams(url.search);
    ["msg", "msg_lvl"].forEach(param => searchParams.delete(param));
    url.search = searchParams.toString();
    window.history.replaceState({}, document.title, url.toString());
};

const handleMessage = () => {
    const msg = document.querySelector("#msg");
    const msgTimer = document.querySelector("#msg-timer");

    if (msg && msgTimer) {
        msgTimer.addEventListener("animationend", () => msg.classList.add("hidden"));
        clearMessageFromUrl();
    }
};

const hideModal = () => {
    const modal = document.querySelector("#modal");
    modal.classList.add("hidden");
};

window.onload = () => handleMessage();
