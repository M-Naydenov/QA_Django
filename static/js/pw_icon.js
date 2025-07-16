function togglePassword() {
    const input = document.getElementById("password");
    const eyeSymbol = document.getElementById("eye-symbol");
    const slashEyeSymbol = document.getElementById("eye-slash-symbol");

    const isHidden = input.type === "password";
    input.type = isHidden ? "text" : "password";

    eyeSymbol.style.display = isHidden ? "none" : "inline";
    slashEyeSymbol.style.display = isHidden ? "inline" : "none";
}