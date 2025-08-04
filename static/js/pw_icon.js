function togglePassword(passwordID) {
    const input = document.getElementById(passwordID);
    const eyeSymbol = document.getElementById(`eye-symbol-${passwordID}`);
    const slashEyeSymbol = document.getElementById(`eye-slash-symbol-${passwordID}`);

    const isHidden = input.type === "password";
    input.type = isHidden ? "text" : "password";

    eyeSymbol.style.display = isHidden ? "none" : "inline";
    slashEyeSymbol.style.display = isHidden ? "inline" : "none";

}