import { loadMatchByTeam } from "./loadMatch.js";

document.addEventListener("DOMContentLoaded", () => {
  const url = window.location.pathname;
  const id = url.split('/')[2];
  loadMatchByTeam(id);
});
