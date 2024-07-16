const show_contact=document.querySelector('#show_contact');
const chatarea=document.querySelector('.chatarea');
const contact=document.querySelector('.contact_list');
const roomName = JSON.parse(document.getElementById('room-name').textContent)
console.log(roomName)
console.log(screen.width)

function connect(){
const chatsocket=new WebSocket(
    'ws://'+
    '127.0.0.1:8000'+
    '/ws/chat/'+
    roomName+
    '/'
);

chatsocket.onmessage = function(e){
    data =e.data
    console.log(data)
    let para=document.createElement('div')
    para.textContent=data
    document.querySelector('section.chatarea').appendChild(para)
}
chatsocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
};

show_contact.addEventListener('click',(e)=>{
    chatarea.classList.add('move_away');
    contact.classList.remove('no_display');
    contact.classList.add('move_in');
});
contact.querySelectorAll('ul li').forEach((el)=>{
    el.addEventListener('click',(e)=>{
        const person_name=e.target.textContent;
        chatarea.querySelector('header span').textContent=person_name;
        
        if (window.innerWidth<800){
            display_small(person_name)
        };
        
    })
});
/* for small screens */
function display_small(person_name){
    chatarea.style.display='flex';
    contact.classList.add('no_display');
    contact.classList.remove('move_in');
    chatarea.classList.remove('move_away');
};
