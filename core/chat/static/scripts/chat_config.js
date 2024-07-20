const roomName = JSON.parse(document.getElementById('room-name').textContent)
const user_username = JSON.parse(document.getElementById('user_username').textContent);
console.log(roomName);
console.log(screen.width);
const send_button=$('#send_message');

const message_box=$('#message_box_chatarea');
/* memeber_action is just li items storing member name */
let member_action=document.querySelectorAll('.member_action');
let current_state={
    'main':document.querySelector('.contact_list'),
    'hidden':document.querySelector('.chatarea')
}
let proto=''
if (window.location.protocol=='http:'){proto='ws'}
else{proto='wss'};
const chatsocket=new WebSocket(
    `${proto}://`+
    window.location.host+
    '/ws/chat/'+
    roomName+
    '/'
);

chatsocket.onmessage = function(e){
    const data = JSON.parse(e.data);
    console.log(data)
    add_msg_to_box(data.username,data.message);
    console.log(data.username)
}
chatsocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
function add_msg_to_box(username,message){
    $(message_box).append(`<p class="type1">(${username}):${message}</p>`)
};
function display_mobile() {
    current_state['main'].style.display='flex';
    current_state['hidden'].style.display='none';
    let items=[document.querySelector('.contact_list'),document.querySelector('.chatarea')]
    document.querySelector('#show_contact').addEventListener('click',()=>{
        items[1].style.display='none';
        items[0].style.display='flex';
        current_state.main=items[0];
        current_state.hidden=items[1];
    })
    document.querySelector('#show_chats_area').addEventListener("click",()=>{
        items[0].style.display='none';
        items[1].style.display='flex';
        current_state.main=items[1];
        current_state.hidden=items[0];
    }

    )
}
function popover_maker(id_n){
    popover=document.createElement('div');
    popover.popover='auto';
    popover.classList.add('modal_popover')
    popover.id=`${id_n}_popover`;
    document.body.appendChild(popover);
    return popover;
};
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
function popover_closer(id){
    p=document.querySelector(`#${id}`)
    p.hidePopover()
    document.body.removeChild(p)
};
function make_ban_user_req(username,room_name){
    $.ajax({
        type:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        url:`${window.location.protocol}//${window.location.host}/ban_user/`,
        data:`room_name=${room_name}&username=${username}`,
        dataType:'json',
        success: function (data) {
            data.responseText
            makeToast(data.responseText,'success',0);
            $(`#${username}`).hide()
            $(`#${username}`).remove()
            $(`#${username}_popover`).remove()
        
            
        },
        error: function(data) {
            console.log(data.responseText);
            makeToast(data.responseText,'error',0);
        }
    })
};
function open_action_popup(el){
    p=popover_maker(el.target.id);
    data=document.createElement('div');
    data.style.backgroundColor='black';
    data.innerHTML=`<button onclick="popover_closer('${el.target.id}_popover')">❌</button><br><h3>Action</h3><br> 
    <button onclick="make_ban_user_req('${el.target.id}','${roomName}')"> BAN user :${el.target.id}</button><br><p>⚠ user will be banned forever</p>`;
    data.style.color='red';
    p.appendChild(data);
    p.showPopover();
};
$(send_button).click(()=>{
    msg=$('#final_msg_entry')
    if(msg.val()){
        chatsocket.send(JSON.stringify({
            'message': msg.val(),
            'username':user_username
        }));
        msg.val('');
    }
});
member_action.forEach((el)=>{
    if (authorized_to_act){
    el.addEventListener('click',(el)=>{open_action_popup(el)})}
});

if (window.innerWidth<800){display_mobile()}
onresize=()=>{
    if(window.innerWidth<800){
        display_mobile();
    }
    else{
        document.querySelector('.contact_list').style.display='flex';
        document.querySelector('.chatarea').style.display='flex';
    };
}











