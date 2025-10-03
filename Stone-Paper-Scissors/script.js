const moves=["rock","paper","scissors"];

let humans=0;
let bots=0;

let sc=document.querySelectorAll(".counter div");
let res=document.getElementById("result");

document.getElementById("rock").addEventListener("click", ()=>gameplay("rock"));
document.getElementById("paper").addEventListener("click", ()=>gameplay("paper"));
document.getElementById("scissors").addEventListener("click", ()=>gameplay("scissors"));

function compchoice(){
    let choice=Math.floor(Math.random()*moves.length);
    return moves[choice];
}

function gameplay(playerchoice) {
let computer=compchoice();
let result="";
if(computer==playerchoice){
    result=`It's a draw! Both chose ${playerchoice}`;
}
else if(
      (playerchoice=='paper')&&(computer=='rock') ||
      (playerchoice=='rock')&&(computer=='scissors') ||
      (playerchoice=='scissors')&&(computer=='paper')
){
    result=`You Win this round! ${playerchoice} beats ${computer}`;
    humans++;
}
else{
    result=`You Lose this round! ${computer} beats ${playerchoice}`;
    bots++;
}
end();
updateresult(result);
updatescore();
}

function updatescore(){
sc[0].innerHTML=`<br>A SCORE:<br><br><br>${humans}`;
sc[2].innerHTML=`B SCORE:<br><br><br>${bots}`;
}

function updateresult(result){
    sc[1].innerHTML=`<br>This Round:<br><br>${result}`;
    
}

function end(){
    if(humans==3||bots==3){
        let finalmsg= (humans==3)?"Yay you won the game!":"Damn lost to a bot" ;
        popup(finalmsg);
    }
}

function popup(finalmsg){
    let a= document.getElementById("popup");
    a.innerHTML=`<b>${finalmsg}</b><br></br><small>click here to close</small>`;
    a.style.display="flex";
    a.onclick=()=>{
        a.style.display="none";
        reset();
    };
}

function reset(){
    humans=0;
    bots=0;
    updatescore();
}
