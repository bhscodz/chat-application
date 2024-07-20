const counter={
    't_number':0,
    'message':{},
}

function updateCounter(msg){
    counter.t_number++;
    let num=counter.t_number;
    counter.message[String(num)]=msg;
    
    sessionStorage.setItem('mysessionstore',JSON.stringify(counter));
};
function makeToast(msg,cls,time) {
    let gap_length=50
    if (msg.length>70){gap_length=100};
    const popover = document.createElement("article");
    popover.popover = "manual";
    popover.classList.add("toast");
    popover.classList.add(cls);
    
    popover.textContent = msg;
    document.body.appendChild(popover);
    
    setTimeout(() => {
        popover.classList.add("newest");
        popover.showPopover();
      }, 1000+(counter.t_number*1000*time));
    
      popover.addEventListener('toggle',(event)=>{
        if (event.newState === "open") {
            moveToastsUp(gap_length);}
    })
    
    updateCounter(msg);
  
    setTimeout(() => {
      popover.hidePopover();
      popover.remove();
    }, 10000+(counter.t_number*1000));

}

function moveToastsUp(gap_length) {
    
    const toasts = document.querySelectorAll(".toast");
    toasts.forEach((toast) => {
        if (toast.classList.contains("newest")) {
        toast.style.top = `5px`;
        toast.classList.remove("newest");
        } 
        else {
        const prevValue = toast.style.top.replace("px", "");
        const newValue = parseInt(prevValue) + gap_length;
        toast.style.top = `${newValue}px`;
        }
    });
}

function load_messages_to_toast(){
const loaded_msg=document.querySelectorAll('ul.loadmsg li');
let val=loaded_msg.length;

let i=0;
while(i<val){
    makeToast(loaded_msg[i].textContent,loaded_msg[i].classList[0],1);
    i++;
}
document.querySelectorAll("ul.loadmsg").innerHTML=''
load_all_noti()
};

function load_all_noti(){
    const board=document.createElement('div');
    board.classList.add('noti_board');
    const mysessiondata=JSON.parse(sessionStorage.getItem("mysessionstore"));
    for (i in  mysessiondata.message) {
        let p=document.createElement('p');
        p.textContent=mysessiondata.message[i]
        board.appendChild(p);
    };
    board.id='noti_board';
    board.popover='manual';
    document.body.appendChild(board);

};

/* const mysessiondata=JSON.parse(sessionStorage.getItem("mysessionstore"));
    console.log(mysessiondata); */

load_messages_to_toast();


