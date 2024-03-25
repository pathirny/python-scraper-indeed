let jobs = document.getElementById("indiviudal-job")
console.log(jobs)

async function getData(){
    try {
        let response = await fetch("http://127.0.0.1:5000");
        
        // Check if the request was successful (status code 200)
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        
        let data = await response.json(); // Parse the response body as JSON
        
        console.log(data); // Now you can log the actual data fetched
    } catch (error) {
        console.error('Error fetching data:', error);
    }

    for(let i = 0; i < data[0].length; i++){
        // need append data to the front end with correct format
    }
}

getData();