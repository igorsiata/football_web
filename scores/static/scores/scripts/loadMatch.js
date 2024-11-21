export function renderMatchesFromTemplate(matches, container=document.getElementById("matches") ){
  const template = document.getElementById("match_template");
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
    if(match.score_away === null & match.score_home === null){
      clone.getElementById("home_team").textContent = match.home_team.tla + " - ";
      clone.getElementById("away_team").textContent =" - " + match.away_team.tla;
      clone.getElementById("home_team").style.color = "gray";
      clone.getElementById("away_team").style.color = "gray";
    }
    container.appendChild(clone);
  });
}
