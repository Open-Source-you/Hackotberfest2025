const phonePassword = document.getElementById('phonePassword');
const phoneContainer = document.querySelector('.phoneContainer');
const loginPageContainer = document.querySelector('.loginPageContainer');
const userLogin = document.querySelector('.userLogin');
const batteryIcon = document.getElementById('batteryIcon');
const password = 'password';
const incorrect = `Password not correct`;
const clock = document.querySelector('.clock');
const homeBtn = document.querySelector('.homeBtn');

function dial() {
    const dialNumbers = document.querySelectorAll('.numberBg');
    dialNumbers.forEach(number => {
        number.addEventListener('click', () => {
            number.style.background = '#c0c0cf';
            setTimeout(() => {
                number.style.background = 'transparent';
            }, 300);
        });
    });
}



```javascript
function getWeather() {
  fetch(url)
    .then(response => response.json())
    .then(data => {
      data.data.forEach(item => {
        const iconUrl = `https://www.weatherbit.io/static/img/icons/${item.weather.icon}.png`;
        document.querySelector('.weatherIcon').innerHTML = `<img src="${iconUrl}"></img>`;
        document.querySelector('.weatherCity').innerHTML = item.city_name;
        document.querySelector('.weatherTemp').innerHTML = item.temp + ' &deg; C';
      });
    })
    .catch(err => console.log(err));
}
```

function homePage() {
    loginPageContainer.innerHTML = `
    <div class="homePageContainer container">
    <div class="homePageHeading">
        <div class="homePageClock">
            <p></p>
        </div>
        <div class="homePageWeather">
            <div class="weatherIcon"></div>
            <div class="weatherWrap">
                <p class="weatherCity"></p>
                <p class="weatherTemp"></p>
            </div>
        </div>
    </div>
    <div class="homePageMenu">
        <img src="./img/call.png" class="menuIcon callIcon">
        <img src="./img/message.png" class="menuIcon messageIcon">
        <img src="./img/email.png" class="menuIcon emailIcon">
        <img src="./img/contact.png" class="menuIcon contactIcon">
        <img src="./img/alarm.png" class="menuIcon alarmIcon">
        <img src="./img/gallery.png" class="menuIcon galleryIcon">
        <img src="./img/notes.png" class="menuIcon notesIcon">
        <img src="./img/settings.png" class="menuIcon settingsIcon">
    </div>
    <img src="./img/homebutton.png" class="homeBtn">
</div>
    `;
}

function settingsPage() {
    const settingsContainer = document.querySelector('.settingsContainer');
    loginPageContainer.innerHTML = `
        <div class="settingsContainer container">
        <h2>Settings</h2>
        <div class="settingsWrap">
            <div class="row">
                <div class="rowContent">
                    <img src="./img/settings.png">
                    <p>General</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
            <div class="row">
                <div class="rowContent">
                    <img src="./img/email.png">
                    <p>Email</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
            <div class="row">
                <div class="rowContent">
                    <img src="./img/music.png">
                    <p>Music</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
            <div class="row">
                <div class="rowContent">
                    <img src="./img/notes.png">
                    <p>Notes</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
            <div class="row">
                <div class="rowContent">
                    <img src="./img/calendar.png">
                    <p>Calendar</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
            <div class="row compass removeBorder">
                <div class="rowContent">
                    <img src="./img/compass.png">
                    <p>Compass</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
            <div class="row">
                <div class="rowContent">
                    <img src="./img/alarm.png">
                    <p>Alarm</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
            <div class="row removeBorder">
                <div class="rowContent">
                    <img src="./img/maps.png">
                    <p>Maps</p>
                </div>
                <i class="fas fa-angle-right"></i>
            </div>
        </div>
        <img src="./img/homebutton.png" class="homeBtn">
    </div>
        `;
}

function emailPage() {
    loginPageContainer.innerHTML = `
    <div class="emailPageContainer container">
    <div class="edit">
        <p>Edit</p>
    </div>
    <div class="heading">
        <h2>Mailboxes</h2>
    </div>
    <div class="emailWrap">
        <div class="row first">
            <div class="rowInfo">
                <i class="fas fa-inbox fa-lg"></i>
                <p>Inbox</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
        <div class="row">
            <div class="rowInfo">
                <i class="fas fa-star fa-lg"></i>
                <p>VIP</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
        <div class="row outbox">
            <div class="rowInfo">
                <i class="fas fa-inbox fa-lg"></i>
                <p>Outbox</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
        <div class="row bd-bottom">
            <div class="rowInfo">
                <i class="far fa-copy fa-lg"></i>
                <p>Drafts</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
        <div class="row bd-bottom">
            <div class="rowInfo">
                <i class="far fa-paper-plane fa-lg"></i>
                <p>Sent</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
        <div class="row">
            <div class="rowInfo">
                <i class="far fa-trash-alt fa-lg"></i>
                <p>Trash</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
    </div>
    <img src="./img/homebutton.png" class="homeBtn">
</div>
    `;
}

function galleryPage() {
    loginPageContainer.innerHTML = `
    <div class="galleryPageContainer container">
    <div class="heading">
        <p>Albums</p>
        <p>All Photos</p>
        <p>Select</p>
    </div>
    <div class="imgWrap"></div>
    <img src="./img/homebutton.png" class="homeBtn">
    </div>
    `;
}

function alarmPage() {
    loginPageContainer.innerHTML = `
    <div class="alarmPageContainer container">
    <div class="heading">
        <p>Edit</p>
        <p>Alarm</p>
        <i class="fas fa-plus fa-sm"></i>
    </div>
    <div class="row">
        <div class="rowInfo">
            <h2>1:34 AM</h2>
            <p>Alarm, Every day</p>
        </div>
        <i class="fas fa-toggle-on"></i>
    </div>
    <div class="row">
        <div class="rowInfo">
            <h2>1:41 AM</h2>
            <p>Alarm, Every day</p>
        </div>
        <i class="fas fa-toggle-on"></i>
    </div>
    <div class="row">
        <div class="rowInfo">
            <h2>5:30 AM</h2>
            <p>Alarm, Every day</p>
        </div>
        <i class="fas fa-toggle-on"></i>
    </div>
    <div class="row">
        <div class="rowInfo">
            <h2>6:45 PM</h2>
            <p>Alarm, Every day</p>
        </div>
        <i class="fas fa-toggle-on"></i>
    </div>
    <div class="row">
        <div class="rowInfo">
            <h2>7:15 AM</h2>
            <p>Alarm, Every day</p>
        </div>
        <i class="fas fa-toggle-on"></i>
    </div>
    <img src="./img/homebutton.png" class="homeBtn">
</div>
    `;
}

function notesPage() {
    loginPageContainer.innerHTML = `
    <div class="notesPageContainer container">
    <div class="heading">
        <div class="menu">
            <i class="fas fa-bars"></i>
            <h3>All notes</h3>
        </div>
        <i class="fas fa-ellipsis-v"></i>
    </div>
    <div class="searchBar">
        <input type="search" name="Search" placeholder="Search notes">
    </div>
    <div class="noteWrap">
        <div class="note">
            <p>Walk the dog</p>
            <span>Just now</span>
        </div>
        <div class="note">
            <p>Learn JS</p>
            <span>3 Months ago</span>
        </div>
        <div class="note">
            <p>Do homework</p>
            <span>2 hours ago</span>
        </div>
        <div class="note">
            <p>Cook dinner</p>
            <span>20 minutes ago</span>
        </div>
    </div>
    <img src="./img/homebutton.png" class="homeBtn">
    </div>
    `;
}

function contactPage() {
    loginPageContainer.innerHTML = `
    <div class="contactPageContainer container">
    <div class="menu">
        <i class="fas fa-ellipsis-v fa-sm"></i>
    </div>
    <div class="heading">
        <h2>Contacts</h2>
        <span>416 Contacts</span>
    </div>
    <div class="searchBar">
        <input type="search" name="Search" placeholder="Search">
    </div>
    <div class="rowWrap">
        <div class="row">
            <div class="rowInfo">
                <div class="circle">
                    <i class="fas fa-user-friends"></i>
                </div>
                <p>Groups</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
        <div class="row">
            <div class="rowInfo">
                <div class="circle">
                    <i class="fas fa-address-card"></i>
                </div>
                <p>Business cards</p>
            </div>
            <i class="fas fa-angle-right"></i>
        </div>
        <div class="row">
            <div class="rowInfo">
                <div class="circle profile"></div>
                <div class="user">
                    <p>Abby</p>
                    <span>My card</span>
                </div>
            </div>
        </div>
        <h4 class="title">A</h4>
        <div class="row">
            <div class="rowInfo">
                <div class="circle profile second"></div>
                <div class="user">
                    <p>Amanda</p>
                    <span>GUI Designer</span>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="rowInfo">
                <div class="circle profile third"></div>
                <div class="user">
                    <p>Ashley</p>
                    <span>English teacher</span>
                </div>
            </div>
        </div>
    </div>
    <img src="./img/homebutton.png" class="homeBtn">
    </div>
    `;
}

function callPage() {
    loginPageContainer.innerHTML = `
    <div class="callPageContainer container">
    <div class="heading">
        <p>Phone</p>
        <i class="fas fa-ellipsis-v"></i>
    </div>
    <div class="callerInfo">
        <div class="row">
            <i class="fas fa-phone-slash fa-xs"></i>
            <p>Abby</p>
        </div>
        <span>1/10</span>
    </div>
    <div class="callerInfo">
        <div class="row">
            <i class="fas fa-phone-slash fa-xs"></i>
            <p class="missedCall">Amanda</p>
        </div>
        <span>15/09</span>
    </div>
    <div class="callerInfo">
        <div class="row">
            <i class="fas fa-phone-slash fa-xs"></i>
            <p>Ashley</p>
        </div>
        <span>14/09</span>
    </div>
    <div class="callerInfo last">
        <div class="row">
            <i class="fas fa-phone-slash fa-xs"></i>
            <p>Charlotte</p>
        </div>
        <span>14/09</span>
    </div>
    <div class="dialContainer">
        <div class="dialRow">
            <div class="number numberBg">1</div>
            <div class="number numberBg">2</div>
            <div class="number numberBg">3</div>
        </div>
        <div class="dialRow">
            <div class="number numberBg">4</div>
            <div class="number numberBg">5</div>
            <div class="number numberBg">6</div>
        </div>
        <div class="dialRow">
            <div class="number numberBg">7</div>
            <div class="number numberBg">8</div>
            <div class="number numberBg">9</div>
        </div>
        <div class="dialRow">
            <div class="number numberBg">*</div>
            <div class="number numberBg">0</div>
            <div class="number numberBg">#</div>
        </div>
        <div class="dialRow">
            <div class="number"><i class="fas fa-th"></i></div>
            <div class="number phone"><i class="fas fa-phone"></i></div>
            <div class="number"><i class="fas fa-backspace"></i></div>
        </div>
    </div>
    <img src="./img/homebutton.png" class="homeBtn">
    </div>
    `;
}

function messagePage() {
    loginPageContainer.innerHTML = `
    <div class="messagePageContainer container">
    <div class="heading">
        <i class="fas fa-angle-left"></i>
        <i class="fas fa-phone"></i>
    </div>
    <h2 class="user">Abby</h2>
    <div class="chatContainer">
        <div class="chat">
            <img src="./img/profile1.jpg" alt="profile1">
            <div class="chatMessage">
                <span>14:28</span>
                <div class="row first">
                    <p>Why didn't you join us today? It was a pretty awesome day. We all wished you were
                        there with us</p>
                </div>
            </div>
        </div>
        <div class="chat reversed">
            <img src="./img/profile2.jpg" alt="profile1">
            <div class="chatMessage">
                <span>14:28</span>
                <div class="row second">
                    <p>Let me check my schedule first. Then I wil let you know asap.</p>
                </div>
            </div>
        </div>
        <div class="sendMessage">
           <div class="typeMessage">
            <i class="fas fa-camera"></i>
            <p>Type here...</p>
           </div>
           <i class="far fa-paper-plane"></i>
        </div>
    </div>
    <img src="./img/homebutton.png" class="homeBtn">
    </div>
    `;
}

document.body.addEventListener('click', e => {
    if (e.target.classList.contains('settingsIcon')) {
        settingsPage();
    }
    if (e.target.classList.contains('homeBtn')) {
        homePage();
        getWeather();
    }
    if (e.target.classList.contains('emailIcon')) {
        emailPage();
    }
    if (e.target.classList.contains('galleryIcon')) {
        galleryPage();
        allImages();
    }
    if (e.target.classList.contains('alarmIcon')) {
        alarmPage();
        checkbox();
    }
    if (e.target.classList.contains('notesIcon')) {
        notesPage();
    }
    if (e.target.classList.contains('contactIcon')) {
        contactPage();
    }
    if (e.target.classList.contains('callIcon')) {
        callPage();
        dial();
    }
    if (e.target.classList.contains('messageIcon')) {
        messagePage();
    }
});

if (phonePassword !== null) {
    phonePassword.addEventListener('keyup', e => {
        if (e.keyCode === 13 && phonePassword.value === password) {
            homePage();
            getWeather();
        } else if (e.keyCode === 13 && phonePassword.value !== password) {
            const incorrectPassword = document.createElement('p');
            incorrectPassword.append(incorrect);
            userLogin.append(incorrectPassword);
            setTimeout(() => {
                incorrectPassword.innerHTML = '';
            }, 2000);
        }
    });
}

function runClock() {
    let date = new Date();
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let seconds = date.getSeconds();
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }
    if (seconds < 10) {
        seconds = '0' + seconds;
    }
    clock.firstElementChild.innerText = hours + ":" + minutes + ":" + seconds;
    const homePageClock = document.querySelector('.homePageClock p');
    if (homePageClock) {
        homePageClock.innerText = hours + ":" + minutes + ":" + seconds;
    }
}

setInterval(() => {
    runClock();
}, 1000);

function checkbox() {
    const checkboxes = document.querySelectorAll('.fa-toggle-on');
    checkboxes.forEach(checkboxIcon => {
        checkboxIcon.addEventListener('click', () => {
            if (checkboxIcon.classList.contains('fa-toggle-on')) {
                checkboxIcon.classList.remove('fa-toggle-on');
                checkboxIcon.classList.add('fa-toggle-off');
            } else {
                checkboxIcon.classList.remove('fa-toggle-off');
                checkboxIcon.classList.add('fa-toggle-on');
            }
        });
    });
}

function battery() {
    batteryIcon.innerHTML = '&#xf243';
    setTimeout(() => {
        batteryIcon.innerHTML = '&#xf242';
    }, 1000);
    setTimeout(() => {
        batteryIcon.innerHTML = '&#xf241';
    }, 2000);
    setTimeout(() => {
        batteryIcon.innerHTML = '&#xf240';
    }, 3000);
}

battery();

setInterval(battery, 4000);
