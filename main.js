let jobs = document.getElementById("indiviudal-job");
const jobsContainer = document.getElementById("jobs");

async function getData() {
  try {
    let response = await fetch("http://127.0.0.1:5000");

    // Check if the request was successful (status code 200)
    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }

    let data = await response.json(); // Parse the response body as JSON

    const showInHtml = data.map((item) => {
      return `
      <a href=${item.URL} target=”_blank”>
        <ul class="jobs">
                <li>${item.job_title}</li>
                <li>${item.Company_Name}</li>
                <li>${item.Location}</li>
                <li>${item.Salary}</li>
                <button class="addToSaved">+</button>
              </ul>
        </a>
        `;
    });

    jobsContainer.innerHTML = showInHtml.join("");

    let addToSaved = document.querySelectorAll("addToSaved");
    addToSaved.addEventListener("click", function () {
      alert("hello");
    });
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// **Saved Jobs**
// use the data from the API to push certain items to a new list
// need to find a SQL database to store saved jobs
// will be displayed when user clicks on saved jobs

getData();
