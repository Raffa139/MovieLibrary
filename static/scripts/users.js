const handleProfilePictureInput = () => {
    const uploadHandle = document.querySelector("#profile-picture-upload-handle");
    const uploadInput = document.querySelector("#profile-picture-input");

    const handleFileChange = () => {
        [file] = uploadInput.files;

        const fileReader = new FileReader();
        fileReader.onload = (event) => {
            uploadHandle.src = event.target.result;
        };

        fileReader.readAsDataURL(file);
    };

    uploadInput.addEventListener("change", handleFileChange);
    uploadHandle.addEventListener("click", () => uploadInput.click());
};

handleProfilePictureInput();
