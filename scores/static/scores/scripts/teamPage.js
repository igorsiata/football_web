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
  const url = window.location.pathname;
  const id = url.split('/')[2];
  loadMatchByTeam(id);
  const team = document.getElementById("team_page");
  team.querySelector("button").addEventListener('click',()=>{
    followTeam(team, csrftoken);
})
});


function loadMatchByTeam(team_id) {
  fetch(`/load_matches?id=${team_id}`)
    .then((response) => response.json())
    .then((data) => {
      renderMatchesFromTemplate(data.matches);
    });
}
