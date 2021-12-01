// misses.js shows/hides missed blocks
function toggleMisses() {
    var misses = document.getElementById("misses");
    var toggle = document.getElementById('tgl');
    if (misses.style.display === "none") {
        misses.style.display = "inline-block";
        toggle.innerHTML = "Hide?"
    } else {
        misses.style.display = "none";
        toggle.innerHTML = "Show?"
    }
}
