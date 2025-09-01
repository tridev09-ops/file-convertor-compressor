const convertForm = document.querySelector("#convertForm")
const convertInput = document.querySelector("#convertForm #fileInput")
const extDropdown = document.querySelector("#extDropdown")

const compressForm = document.querySelector("#compressForm")
const compressInput = document.querySelector("#compressForm #fileInput")
const size = document.querySelector("#size")
const qualityDropdown = document.querySelector("#qualityDropdown")

let orderedFiles = []
let exts = []
const image_ext = ['jpg', 'png', 'jpeg']
const video_ext = ['mp4', 'mkv', 'avi']

size.style.display = 'none'
qualityDropdown.style.display = 'none'

const appendFiles = (event) => {
    const files = Array.from(event.target.files)
    orderedFiles = [] // reset
    exts=[]
    
    files.forEach((file, i) => {
        orderedFiles.push(file)
        exts.push(file.name.slice(file.name.indexOf('.')+1))
    })
    size.style.display = 'none'
    qualityDropdown.style.display = 'none'

    if (image_ext.includes(exts[0])) {
        size.style.display = 'flex'
        extDropdown.innerHTML = `
        <option value="jpg">jpg</option>
        <option value="png">png</option>
        <option value="jpeg">jpeg</option>
        `
    } else if (video_ext.includes(exts[0])) {
        qualityDropdown.style.display = 'flex'
        extDropdown.innerHTML = `
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
        formData.append("ext", extDropdown.value)
    }else if (route == "/compress") {
        if (image_ext.includes(exts[0])) {
            formData.append("size", parseInt(size.value))
        } else if (video_ext.includes(exts[0])) {
            formData.append("quality", qualityDropdown.value)
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
