function doPost() {
    const form = $('#file_form')[0];
    let formData = new FormData(form);
    const post_photo = $('#post-photo')[0].files[0];
    const post_writing = $('#post-writing').val();
    const post_tag = $('#post-tag').val();
    const post_location = $('#post-location').val();

    if (post_photo == null) {
        alert("사진이 꼭 필요해요 !!");
        $('#post-photo').focus();
        return;
    }
    if (post_writing.trim() == "") {
        alert("글 작성 부탁드립니다 :)");
        $('#post-writing').val("");
        $('#post-writing').focus();
        return;
    }
    formData.append('photo_give', post_photo);
    formData.append('writing_give', post_writing)
    formData.append('tag_give', post_tag)
    formData.append('location_give', post_location)

    $.ajax({
        type: 'POST',
        url: '/api/writepost',
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            if (response['result'] == 'success') {
                alert(response['msg'])
                window.location.href = '/'
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
    window.history.back();
}

function setThumbnail(event) {
    let reader = new FileReader();

    const form = $('#file_form')[0];
    let formData = new FormData(form);
    const post_photo = $('#post-photo')[0].files[0];
    console.log(post_photo)
    if ($('#post-photo')[0].files.length != 0) {
        $('#none').toggleClass('lololo')
        formData.append('file_give', post_photo);

        $.ajax({
            type: 'POST',
            url: '/api/autotag',
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                if (response['result'] == 'success') {
                    $('#post-tag').val('#' + response['tag'])
                    console.log('성공')
                } else {
                    console.log('실패')
                }
                $('#none').toggleClass('lololo')
                reader.onload = function (event) {
                    let img = document.createElement("img");
                    img.setAttribute("src", event.target.result);
                    img.setAttribute("class", "preview");


                    if (document.querySelector("div#photo-preview img") != null) {
                        $(".preview").remove();
                    }
                    document.querySelector("div#photo-preview").appendChild(img)
                    console.log('test1'); //이부분에 태그를 출력?

                };
                reader.readAsDataURL(event.target.files[0]);
            }
        });

    }
}