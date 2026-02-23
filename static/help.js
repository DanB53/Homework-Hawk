function showSection(section){
    console.log(section)
    document.getElementById(section).scrollIntoView(({
        behavior:"smooth",
        block:"start",
    }))
}
console.log("hu")