const dialog=document.querySelector('dialog');
const input_box=document.querySelector('#input');
const close_b=document.querySelector('#close');
var global_var={'menu_popup':'',};
let urls=[];


/* functions */
function show_dialog(){
    dialog.showModal();
};
function open_menu(){
    let b=document.querySelector('#menu-icon');
    if (b.value==="open"){
        global_var['menu_popup'].showPopover();
}
    else{
        global_var['menu_popup'].hidePopover();
    };

};
function show_navigation(){
    let a=document.querySelector('nav.top_nav.large');
    let more=document.createElement('div');
    more.innerHTML = document.querySelector('.side_section').innerHTML;
    more.style.display='block';
    b=document.createElement('div');
    b.classList.add('menu-box');
    c=document.createElement('div');
    c.innerHTML=a.innerHTML;
    c.removeChild(c.firstChild.nextSibling);
    b.popover='auto';
    c.classList.add('menu');
    b.style.margin='0px auto 0px 0px';
    let button=document.createElement('button');
    button.innerHTML='<i class="fa-solid fa-x"></i>';
    button.addEventListener('click',()=>{b.hidePopover();
    });
    b.appendChild(button);
    b.appendChild(c);
    b.appendChild(more);
    b.id='menu_box';
    document.body.appendChild(b);
    b.addEventListener('toggle',(event)=>{
        button=document.querySelector('#menu-icon');
        if (event.newState === "open") {
            button.value='close';}
        else{
            button.value='open';
        };
    })
    return b
};
/* id is the id of container to append url */
function append_room_link(data,id,my_action){
    let url=`<p id="url_p${data['roomname']}"><a style="white-space:nowrap;" href="${window.location.href}chat/${data['roomname']}">${data['roomname']}</a>---admin(${data['admin']})
    <button value=${data['roomname']} style="background-color:red;" onclick="${my_action}(this.value)">${my_action}</button></P>`;
    $(`#${id}`).append(url);
};
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
function delete_room(e){
    roomname=e
    $.ajax({
        type:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        url:`${window.location.href}delete/`,
        data:`roomname=${roomname}`,
        dataType:'json',
        success: function (data) {
            console.log(data.data);
            makeToast(data.data,'success',0);
            $(`#url_p${roomname}`).hide()
            $(`#url_p${roomname}`).remove()
            
        },
        error: function(data) {
            console.log(data.data)
            makeToast(data.data,'error',0);
        }
    })
}
function move_out(e){
    roomname=e
    console.log(roomname);
    $.ajax({
        type:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        url:`${window.location.href}leave/`,
        data:`roomname=${roomname}`,
        dataType:'json',
        success: function (data) {
            console.log(data.data);
            makeToast(data.data,'success',0);
            $(`#url_p${roomname}`).hide()
            $(`#url_p${roomname}`).remove()
        },
        error: function(data) {
            console.log(data);
            makeToast(data.data,'error',0);
        }
    })
}



/* ajax call to save form */
var frm = $('#room_creation');
frm.submit(function () {
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            dialog.close();
            makeToast('room created sucessfully','success',0);
            append_room_link(data,'admin_of','delete_room');

        },
        error: function(data) {
            console.log(data);
            makeToast(data.responseText,'error',0);
        }
    });
    return false;
});




/* event listeners */
close_b.addEventListener("click",(e)=>{
    dialog.close();
    console.log('clicked');
});

if (window.innerWidth<800){
    global_var['menu_popup']=show_navigation();
}
onresize=()=>{
    if (window.innerWidth<800){
        global_var['menu_popup']=show_navigation();
    }
}
$('#visit_room').click(()=>{
    let link=$('#visit_room_val').val();
    window.location.href = `${window.location.href}chat/${link}`;
    return false
})


/* initialisation for small screens */
/* using var puts the variable at the top */









