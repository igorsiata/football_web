import { renderMatchesFromTemplate } from "./loadMatch.js";
import {followTeam} from "./followTeam.js"

document.addEventListener("DOMContentLoaded", () => {
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    let csrftoken = "";
    if (csrfTokenElement) {
        csrftoken = csrfTokenElement.value;
    } else {
        console.error("CSRF token not found.");
    }
  const teams = document.getElementsByClassName("prof_team_page");
  for(let team of teams){
    var team_id = team.dataset.teamId;
    team.querySelector("button").addEventListener('click',()=>{
        followTeam(team, csrftoken);
    })
    loadRecentMatchesByTeam(team_id,3,team.querySelector(".prof_team_matches"));
  }
});

function loadRecentMatchesByTeam(team_id, max_res, container){
    fetch(`/load_matches?id=${team_id}&max=${max_res}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(container);
      renderMatchesFromTemplate(data.matches, container);
    });
  }

