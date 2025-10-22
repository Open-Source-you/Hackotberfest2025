let compdes = ["rock","paper","scissor"];

function game(){
    if (input==cplay)
    {
        you.innerHTML =`<h1>you choosed ${input}!</h1>`;
        computer.innerHTML = `<h1>computer choosed ${cplay}!</h1>`
        winner.innerHTML = '<h1>Draw!!!</h1>';
    }
    else if(input!=cplay)
    {
        if(input=='paper'&& cplay=='scissor')
        {
            you.innerHTML =`<h1>you choosed ${input}!</h1>`;
            computer.innerHTML = `<h1>computer choosed ${cplay}!</h1>`
            winner.innerHTML = '<h1>computer win!!!</h1>';
            score.lastElementChild.innerHTML =`<h1>${++Compscore}</h1>`;
        }
        else if(input=='paper'&& cplay=='rock')
        {
            you.innerHTML =`<h1>you choosed ${input}!</h1>`;
        computer.innerHTML = `<h1>computer choosed ${cplay}!</h1>`
        winner.innerHTML = '<h1>you win!!!</h1>';
        score.firstElementChild.innerHTML =`<h1>${++Youscore}</h1>`;
        }
        else if(input=='scissor' && cplay=='rock')
        {
            you.innerHTML =`<h1>you choosed ${input}!</h1>`;
            computer.innerHTML = `<h1>computer choosed ${cplay}!</h1>`
            winner.innerHTML = '<h1>computer win!!!</h1>';
            score.lastElementChild.innerHTML =`<h1>${++Compscore}</h1>`;
        }
        else if(input=='scissor'&& cplay=='paper')
        {
            you.innerHTML =`<h1>you choosed ${input}!</h1>`;
            computer.innerHTML = `<h1>computer choosed ${cplay}!</h1>`
            winner.innerHTML = '<h1>You win!!!</h1>';
            score.firstElementChild.innerHTML =`<h1>${++Youscore}</h1>`;
        }
        else if(cplay=='paper'&& input=='rock')
        {
            you.innerHTML =`<h1>you choosed ${input}!</h1>`;
            computer.innerHTML = `<h1>computer choosed ${cplay}!</h1>`
            winner.innerHTML = '<h1>computer wons!!!</h1>';
            score.lastElementChild.innerHTML =`<h1>${++Compscore}</h1>`;
        }
        else if(cplay=='scissor' && input=='rock')
        {
            you.innerHTML =`<h1>you choosed ${input}!</h1>`;
            computer.innerHTML = `<h1>computer choosed ${cplay}!</h1>`
            winner.innerHTML = '<h1>you wons!!!</h1>';
            score.firstElementChild.innerHTML =`<h1>${++Youscore}</h1>`;
        }
    }
}
paper.addEventListener('click',function(e){
    input = 'paper';
    cplay = compdes[Math.floor(Math.random()*3)];
    game();
});
scissor.addEventListener('click', function(e){
    input = 'scissor'
    cplay = compdes[Math.floor(Math.random()*3)];
    game();
});
rock.addEventListener('click',function(e){
    cplay = compdes[Math.floor(Math.random()*3)];
    input = 'rock';
    game();

});
