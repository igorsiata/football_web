
export function followTeam(team_profile_container, csrftoken){
    
    const team_id = team_profile_container.dataset.teamId;
    fetch(`/toggle_follow/${team_id}`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }})
        .then(response => response.json())
        .then(data => {
            if(data.status ==="unfollowed"){
                team_profile_container.querySelector("button").innerHTML = "Follow";
            }else if(data.status==="followed"){
                team_profile_container.querySelector("button").innerHTML = "Unfollow";
            }
            console.log(data.status);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}