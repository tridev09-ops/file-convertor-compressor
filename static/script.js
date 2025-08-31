const input = document.getElementById("fileInput");
const size = document.getElementById("size");
const form = document.getElementById("compressForm");
const qualityDropdown= document.getElementById("qualityDropdown");

let orderedFiles = [];

input.addEventListener("change", (event) => {
    const files = Array.from(event.target.files);
    orderedFiles = []; // reset

    files.forEach((file, i) => {
        orderedFiles.push(file);
        //document.write(file.name)
    });
});

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData();

    orderedFiles.forEach(file => {
        formData.append("files", file);
    });

    formData.append("size", parseInt(size.value))
    
    formData.append("quality", qualityDropdown.value)
    
    fetch("/compress",
        {
            method: "POST",
            body: formData
        })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "";
        a.click();
        window.URL.revokeObjectURL(url);
    });
});