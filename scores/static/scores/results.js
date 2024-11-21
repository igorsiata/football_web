import { loadMatchByDate } from "./loadMatch.js";

let currentDate = new Date();

document.addEventListener("DOMContentLoaded",()=>{
    updateDate();
    


    document.getElementById("prev_day").addEventListener('click',()=>{
        currentDate.setDate(currentDate.getDate()-1);
        updateDate();
    })
    document.getElementById("next_day").addEventListener('click',()=>{
        currentDate.setDate(currentDate.getDate()+1);
        updateDate();
    })
})

function updateDate(){
    document.getElementById("curr_day").textContent = currentDate.toJSON().slice(0, 10);
    document.getElementById("matches").innerHTML = "";
    loadMatchByDate(document.getElementById("curr_day").textContent)
    
}
    