let jobs = document.getElementById("indiviudal-job");
const jobsContainer = document.getElementById("jobs");
console.log(jobs);

async function getData() {
  try {
    let response = await fetch("http://127.0.0.1:5000");

    // Check if the request was successful (status code 200)
    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }

    let data = await response.json(); // Parse the response body as JSON

    const showInHtml = data.map((item) => {
      console.log(item);
      return `
      <a href=${item.URL} target=”_blank”>
        <ul class="jobs">
                <li>${item.job_title}</li>
                <li>${item.Company_Name}</li>
                <li>${item.Location}</li>
                <li>${item.Salary}</li>
                <button>+</button>
              </ul>
        </a>
        `;
    });

    jobsContainer.innerHTML = showInHtml.join("");

    console.log(data); // Now you can log the actual data fetched
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

getData();
