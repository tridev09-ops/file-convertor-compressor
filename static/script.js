const convertForm = document.querySelector("#convertForm")
const convertInput = document.querySelector("#convertForm #fileInput")
const ext = document.querySelector("#ext")

const compressForm = document.querySelector("#compressForm")
const compressInput = document.querySelector("#compressForm #fileInput")
const size = document.querySelector("#size")
const quality = document.querySelector("#quality")

const toggle = document.querySelector(".toggle")
const convertBtn = document.querySelector("#convertBtn")
const compressBtn = document.querySelector("#compressBtn")

let orderedFiles = []
let exts = []
const image_ext = ['jpg', 'png', 'jpeg']
const video_ext = ['mp4', 'mkv', 'avi']

const reset = ()=> {
    orderedFiles = []
    exts = []
    size.style.display = 'none'
    quality.style.display = 'none'
    ext.style.display = 'none'
    convertForm.style.display = 'none'
    compressForm.style.display = 'none'
}

reset()
convertForm.style.display = ''

const appendFiles = (event) => {
    const files = Array.from(event.target.files)
    orderedFiles = [] // reset
    exts = []

    files.forEach((file, i) => {
        orderedFiles.push(file)
        exts.push(file.name.slice(file.name.indexOf('.')+1))
    })

    if (image_ext.includes(exts[0])) {
        size.style.display = 'flex'
        ext.style.display = 'flex'
        ext.innerHTML = `
        <option value="jpg">jpg</option>
        <option value="png">png</option>
        <option value="jpeg">jpeg</option>
        `
    } else if (video_ext.includes(exts[0])) {
        quality.style.display = 'flex'
        ext.style.display = 'flex'
        ext.innerHTML = `
        <option value="mp3">mp3</option>
        <option value="mp4">mp4</option>
        <option value="mkv">mkv</option>
        `
    }
}

const submitForm = (event, route)=> {
    event.preventDefault()
    const formData = new FormData()

    orderedFiles.forEach(file => {
        formData.append("files", file)
    })

    if (route == "/convert") {
        formData.append("ext", ext.value)
    } else if (route == "/compress") {
        if (image_ext.includes(exts[0])) {
            formData.append("size", parseInt(size.value))
        } else if (video_ext.includes(exts[0])) {
            formData.append("quality", quality.value)
        }
    }

    fetch(route,
        {
            method: "POST",
            body: formData
        })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = ""
        a.click()
        window.URL.revokeObjectURL(url)
    })
}

convertInput.addEventListener("change", (event) => {
    appendFiles(event)
})
compressInput.addEventListener("change", (event) => {
    appendFiles(event)
})

convertForm.addEventListener("submit", (event) => {
    submitForm(event, "/convert")
})
compressForm.addEventListener("submit", (event) => {
    submitForm(event, "/compress")
})

convertBtn.addEventListener("click", ()=> {
    reset()
    convertForm.style.display = ''
    convertBtn.classList.add("active-value")
    compressBtn.classList.remove("active-value")
})

compressBtn.addEventListener("click", ()=> {
    reset()
    compressForm.style.display = ''
    compressBtn.classList.add("active-value")
    convertBtn.classList.remove("active-value")
})