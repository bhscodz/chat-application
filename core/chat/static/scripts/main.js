const dialog=document.querySelector('dialog');
const input_box=document.querySelector('#input');
const submit=document.querySelector('#confirm');
const close_b=document.querySelector('#close');
document.querySelector('.main_section').style.height=`${window.innerHeight-157}px`
document.querySelector('.side_section').style.height=`${window.innerHeight-157}px`
let urls=[]
console.log(screen.width)
function show(e){
    dialog.showModal();  
};
close_b.addEventListener("click",(e)=>{
    dialog.close();
    console.log('clicked');
});
submit.addEventListener('click',(event)=>{
    const data=input_box.value
    if(data != ''){
        if(!urls.includes(data)){;
        const new_data=document.createElement('li');
        const new_data_link=document.createElement('a');

        new_data.style.width='100%';
        new_data_link.style.whiteSpace='nowrap';
        new_data_link.setAttribute('target','_blank');
        const url=window.location.href+'chat/'+(data.replace(/\s/g, ""))
        new_data_link.setAttribute('href',url);

        new_data_link.textContent='👉'+url;
        new_data.appendChild(new_data_link);
        document.querySelector('main section ul').appendChild(new_data);
        urls.push(data)

        
    }
    else{
        alert('room already exists')
    };
};
    
});

