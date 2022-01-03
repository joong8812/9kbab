function doEdit(post_id) {
    const edit_writing = $('#edit-writing').val();
    const edit_tag = $('#edit-tag').val();
    const edit_location = $('#edit-location').val();

    $.ajax({
        type: 'POST',
        url: '/api/mypostedit',
        data: {writing_give:edit_writing, tag_give:edit_tag, location_give:edit_location, post_id_give: post_id},
        success: function (response) {
            if (response['result'] == 'success') {
                alert(response['msg'])
                window.location.href = '/myfeed'
            } else {
                alert(response['msg'])
                window.location.reload()
            }
        },
        error: function (err) {
            console.log('error:' + err)
        }
    })
}

function doCancel() {
    window.location.href = '/myfeed'
}

function setThumbnail(event) {
    let reader = new FileReader();
    reader.onload = function (event) {
        let img = document.createElement("img");
        img.setAttribute("src", event.target.result);
        img.setAttribute("class", "preview");

        if (document.querySelector("div#photo-preview img") != null) {
            $(".preview").remove();
        }
        document.querySelector("div#photo-preview").appendChild(img);
    };
    reader.readAsDataURL(event.target.files[0]);
}