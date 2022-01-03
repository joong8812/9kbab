function Thumbnail(event){
    var reader = new FileReader();

    reader.onload = function(event){
        var img = document.createElement("img");
        img.setAttribute("src", event.target.result);
        img.setAttribute("id","default_img")

        if (document.querySelector("div#preview img") != null){
            $('#default_img').remove();
        }

        document.querySelector("div#preview").appendChild(img);
    };
    reader.readAsDataURL(event.target.files[0]);
}

function profile_edit(save) {
    const form = $('profile_form')[0];
    let formData = new FormData(form);
    let pf_image = $('#upload')[0].files[0];

    const introduce = $('#myintro').val();
    let change_photo = 'y';

    if (pf_image == null){
        pf_image = save
        change_photo = 'n'
    }

    formData.append('profile_give', change_photo);
    formData.append('pfile_give',pf_image);
    formData.append('introduce_give',introduce);

    $.ajax({
        type: 'POST',
        url: '/profile/edit',
        processData: false,
        contentType: false,
        data: formData,
        success: function(response){
            if (response['result'] == 'success'){
                alert(response['msg'])
                window.location.href='/mypage'
            }
            else {
                alert(response['msg'])
                window.location.reload();
            }
        }
    })
}