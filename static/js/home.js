function goWrite() {
    window.location.href = "/writepost"
}

function goMypage() {
    window.location.href = "/mypage"
}

function reRoad() {
    window.location.reload()
}

$(function () {
    $('.post-icon-2').click(function () {
        const commentIcon = $(this);
        postId = commentIcon.data('post');

        $.ajax({
            type: 'POST',
            url: '/comment',
            data: {'post_id_give': postId},
            success: function (response) {
                if (response['result'] == 'success') {
                    commentList = response['comments'];
                    for (let i = 0; i < commentList.length; i++) {
                        const nickname = commentList[i].nickname;
                        const comment = commentList[i].comment;
                        let addSoon = "<div class='comment-body'><span class='comment-left'>" + nickname + "</span>";
                        addSoon += "<span class='comment-right'>" + comment + "</span></div>";
                        $('#comment-wrapper').append(addSoon)
                    }
                    $('#comment-modal').data('post', postId);
                    $("#comment-modal").css({
                        "top": (($(window).height() - $("#comment-modal").outerHeight()) / 2 + $(window).scrollTop()) + "px",
                        "left": (($(window).width() - $("#comment-modal").outerWidth()) / 2 + $(window).scrollLeft()) + "px",
                        //팝업창을 가운데로 띄우기 위해 현재 화면의 가운데 값과 스크롤 값을 계산하여 팝업창 CSS 설정
                    });
                    $("body").css("overflow", "hidden");//body 스크롤바 없애기
                    $("#comment-modal").fadeIn();
                } else {
                    alert(response['msg'])
                }
            },
            error: function (err) {
                console.log('error:' + err)
            }
        })
    })
})

function closeModal() {
    window.location.href = '/home'
}

function leaveComment() {
    const commentWrite = $('#comment-writing').val();
    const postId = $('#comment-modal').data('post');

    if (commentWrite == '') return;

    $.ajax({
        type: 'POST',
        url: '/api/comment',
        data: {'post_id_give': postId, 'comment_give': commentWrite},
        success: function (response) {
            if (response['result'] == 'success') {
                const userId = response['user_id']
                let addSoon = "<div class='comment-body'><span class='comment-left'>" + userId + "</span>";
                addSoon += "<span class='comment-right'>" + commentWrite + "</span></div>";
                $('#comment-wrapper').append(addSoon)
                $('#comment-writing').val("");
            } else {
                alert(response['msg'])
            }
        },
        error: function (err) {
            console.log('error:' + err)
        }
    })
}