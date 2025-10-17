const apikey="97c7f36935f34d5ae0291a16a6a9d2e1";
const apiurl="https://api.openweathermap.org/data/2.5/weather?units=metric&q=";

const searchbox = document.querySelector(".search input");
const searchbtn = document.querySelector(".search button") 
const weatherIcon = document.querySelector(".weather-icon")
async function checkweather(city){
    const response = await fetch(apiurl + city + `&appid=${apikey}`);
    var data = await response.json();
    console.log(data);

    document.querySelector(".city").innerHTML = data.name;
    document.querySelector(".temp").innerHTML = Math.round(data.main.temp) + "°c";
    document.querySelector(".humidity").innerHTML = data.main.humidity +"%";
    document.querySelector(".wind").innerHTML = data.wind.speed +"Km/Hr";

    if(data.weather[0].main == "Clouds"){
        weatherIcon.src="images/clouds.png";
    }
    else if(data.weather[0].main == "Clear"){
        weatherIcon.src="images/clear.png";
    }
    else if(data.weather[0].main == "Drizzle"){
        weatherIcon.src="images/drizzle.png";
    }
    else if(data.weather[0].main == "Mist"){
        weatherIcon.src="images/mist.png";
    }
    else if(data.weather[0].main == "Rain"){
        weatherIcon.src="images/rain.png";
    }
    else if(data.weather[0].main == "Snow"){
        weatherIcon.src="images/snow.png";
    }
}
searchbtn.addEventListener("click",()=>{
    checkweather(searchbox.value);
})
searchbox.addEventListener("keypress",(e)=>{
    if(e.key=="Enter"){
        checkweather(searchbox.value);
    }
})