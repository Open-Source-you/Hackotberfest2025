const RandomOne= Math.floor(Math.random()*6 + 1);

const ImageOne = './img/dice' + RandomOne + '.png';

document.querySelectorAll('img')[0].setAttribute('src', ImageOne);

const RandomTwo= Math.floor(Math.random()*6 + 1);

const ImageTwo = './img/dice' + RandomTwo + '.png';

document.querySelectorAll('img')[1].setAttribute('src', ImageTwo);

if(RandomOne > RandomTwo){
    document.querySelector('h1').innerHTML = 'Player 1 Wins !! Congratulations!';
}
else if(RandomOne < RandomTwo){
    document.querySelector('h1').innerHTML = 'Player 2 Wins !! Congratulations!';
}
else{
    document.querySelector('h1').innerHTML = 'Game Draw !';
}
