import { renderMatchesFromTemplate } from "./loadMatch.js";

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

function loadMatchByDate(match_date){
    fetch(`/load_matches?date=${match_date}`)
      .then((response) => response.json())
      .then((data) => {
        const container = document.getElementById("matches");
        let no_matches = true;
        for (const league in data.matches) {
          
          if(data.matches[league].length > 0){
            no_matches = false;
            // adding league header
            const league_header = document.createElement("div")
            league_header.style.display = "flex";
            league_header.style.margin = "20px auto"
            const league_text = document.createElement("h4");
            league_text.style.margin = "auto 0px";
            league_text.textContent = league;
            const img = document.createElement("img");
            img.src = data.leagues[league].logo_link;
            img.classList.add("league_logo");
            league_header.appendChild(img);
            league_header.appendChild(league_text);
            container.appendChild(league_header);
            
            // render matches
            renderMatchesFromTemplate(data.matches[league]);
          }
          
        }
        if(no_matches){
          container.innerHTML = "<h3>No matches were played on this day</h3>"
        }
        
        
      });
  }
    