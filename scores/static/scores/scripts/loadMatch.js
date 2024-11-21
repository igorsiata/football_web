export function loadMatchByTeam(team_id) {
  fetch(`/load_matches?id=${team_id}`)
    .then((response) => response.json())
    .then((data) => {
      renderMatchesFromTemplate(data.matches);
    });
}

export function loadMatchByDate(match_date){
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
          const league_text = document.createElement("h4");
          league_text.style.marginLeft = "20px";
          league_text.style.marginTop = "30px";
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

function renderMatchesFromTemplate(matches) {
  const template = document.getElementById("match_template");
  const container = document.getElementById("matches");
  matches.forEach((match) => {
    const clone = template.content.cloneNode(true);
    clone.getElementById("home_team_logo").src = match.home_team.logo;
    clone.getElementById("away_team_logo").src = match.away_team.logo;
    clone.getElementById("match_date").textContent = match.date;
    
    clone.getElementById("home_team").textContent = match.home_team.tla + " " + match.score_home;
    clone.getElementById("away_team").textContent =match.score_away + " " + match.away_team.tla;
    // Link to team page
    clone.getElementById("home_team").onclick = function() {
      window.location.href = `/teams/${match.home_team.id}`;  
    };

    clone.getElementById("away_team").onclick = function() {
      window.location.href = `/teams/${match.away_team.id}`;  
    };
    clone.getElementById("home_team_logo").onclick = function() {
      window.location.href = `/teams/${match.home_team.id}`;  
    };

    clone.getElementById("away_team_logo").onclick = function() {
      window.location.href = `/teams/${match.away_team.id}`;  
    };
    
    // Color winner to green
    if (match.score_away> match.score_home){
      clone.getElementById("away_team").style.color = "#228B22";
      clone.getElementById("home_team").style.color = "#8B0000";
    }else if(match.score_home> match.score_away){
      clone.getElementById("home_team").style.color = "#228B22";
      clone.getElementById("away_team").style.color = "#8B0000";
    }
    else{
      clone.getElementById("home_team").style.color = "#ba8e23";
      clone.getElementById("away_team").style.color = "#ba8e23";
    }
    if(!match.score_away & !match.score_home){
      clone.getElementById("home_team").textContent = match.home_team.tla + " - ";
      clone.getElementById("away_team").textContent =" - " + match.away_team.tla;
      clone.getElementById("home_team").style.color = "gray";
      clone.getElementById("away_team").style.color = "gray";
    }
    container.appendChild(clone);
  });
}
