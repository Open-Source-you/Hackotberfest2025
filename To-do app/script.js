let input=document.getElementById("input");
let c=document.getElementById("box");
let d=document.getElementById("form");



d.addEventListener("submit",(e)=>{

    e.preventDefault();

    let b=document.getElementById("input").value;
   if(b===""){
    alert("Enter text");
    return;
   }

    let div=document.createElement("div");
    div.style.margin="0px";
    div.style.height="115px";
    div.style.width="115px";
    div.style.boxShadow=" 4px 4px 10px black";
    div.style.backgroundColor="pink";
    div.style.border="2px solid white";
    div.style.borderRadius="11px";
    div.style.textAlign="center";
    div.style.display="flex";
    div.style.alignItems="center";
    div.style.justifyContent="center";
    div.style.overflow="auto";
    div.style.wordBreak="break-word";
    div.classList.add("task");
    div.style.setProperty('scrollbar-width', 'none');


    let span = document.createElement("span");
    span.textContent = b;
    span.style.padding = "4px";




    let but=document.createElement("input");
    but.type="checkbox";
    but.style.marginTop="4px";
    but.addEventListener("change",(e)=>{
        if(but.checked){
            span.style.textDecoration="line-through";
            span.style.textDecorationThickness="2px";
            div.style.boxShadow="none";
        }
        else{
            span.style.textDecoration="none";
            div.style.boxShadow=" 4px 4px 10px black";
        }
    })


    let wrapper=document.createElement("div");
    wrapper.id="wrapper";
    wrapper.style.display="flex";
    wrapper.style.margin="15px";



    div.appendChild(span);
    wrapper.appendChild(but);
    wrapper.appendChild(div);
    c.appendChild(wrapper);


    input.value="";

});
