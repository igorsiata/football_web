let page_number = 0;
let all_news_loaded = false;
document.addEventListener("DOMContentLoaded", () => {
  page_number = 0;
  renderNews();
  document.querySelector("#load_button").addEventListener("click", () => {
    renderNews();
  });
  document.querySelector("#load_button").style.display = "none";
});

window.onscroll = () => {
  if (
    window.innerHeight + Math.round(window.scrollY) >=
    document.body.offsetHeight
  ) {
    renderNews();
  }
};
function newsLoaded() {
  if (
    window.innerHeight + Math.round(window.scrollY) >=
    document.body.offsetHeight
  ) {
    renderNews();
  }
}
function renderNewsFromTemplate(news_page) {
  const template = document.getElementById("news_template");
  const container = document.getElementById("news_posts");

  news_page.forEach((news) => {
    const clone = template.content.cloneNode(true);
    clone.querySelector(".news_title").textContent = news.title;
    clone.querySelector(".date").textContent = news.timestamp;
    clone.querySelector(".news_title").href = `news/${news.id}`;
    if (news.image_path === "None") {
      clone.querySelector(".news_header_image").style.display = "none";
    } else {
      clone.querySelector(".news_header_image").src = news.image_path;
    }
    clone.querySelector(".news_title").addEventListener("click", () => {
      console.log("clicked");
    });
    container.appendChild(clone);
  });
  container
    .querySelector(".news_header:last-of-type")
    .addEventListener("animationend", newsLoaded);
}

function renderNews() {
  page_number++;
  if (all_news_loaded) {
    return;
  }
  fetch(`/load_news/${page_number}`)
    .then((response) => response.json())
    .then((data) => {
      max_pages = data.max_pages;
      if (data.news.length === 0) {
        document.querySelector("#end_page").style.display = "block";
        document.querySelector("#load_button").style.display = "none";
        page_number--;
        all_news_loaded = true;
      } else {
        renderNewsFromTemplate(data.news);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
