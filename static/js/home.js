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
    // 각 포스트의 댓글 버튼을 누른다면...
    $('.post-icon-2').click(function () {
        const commentIcon = $(this);
        const postId = commentIcon.data('post');

        $.ajax({
            type: 'POST',
            url: '/comment',
            data: {'post_id_give': postId},
            success: function (response) {
                if (response['result'] == 'success') {
                    // 댓글 div 생성 및 추가
                    const myNick = response['nickname'];
                    const commentList = response['comments'];
                    for (let i = 0; i < commentList.length; i++) {
                        const nickname = commentList[i].nickname;
                        const comment = commentList[i].comment;
                        const commentId = commentList[i]._id;

                        // 각 코멘트 생성 및 추가
                        let addSoon = "<div class='comment-body' data-nick='"+nickname+"'><div class='body-wrapper'><span class='comment-left'>" + nickname + "</span>";
                        addSoon += "<span class='comment-right'>" + comment + "</span></div>";
                        addSoon += "<div class='delete-wrapper'><span class='comment-delete hide' data-ci='"+commentId+"'><img src='../static/images/close.png'/></span></div></div>";
                        $('#comment-wrapper').append(addSoon)
                    }
                    $('#comment-modal').data('post', postId);

                    // 해당 포스트의 글쓴이 정보 및 포스트 내용 태그 생성 및 추가
                    const writerImg = $('#' + postId).find('.profile-img').clone().wrapAll("<div/>").parent().html();
                    const writerNick = $('#' + postId).find('.profile-txt').clone().wrapAll("<div/>").parent().html();
                    const writerContent = $('#' + postId).find('.post-content').clone().wrapAll("<div/>").parent().html();
                    $('#cmb-post').append("<div class='post-header'><div class='left-wrapper'>"+writerImg+"</div></div>");
                    $('#cmb-post .post-header .left-wrapper').append(writerNick);
                    $('#cmb-post').append(writerContent);

                    // 각 댓글을 마우스오버/마우스아웃 한다면..
                    $('.comment-body')
                        .mouseover(function() {
                            const commentNick = $(this).data('nick');
                            if (myNick == commentNick) {
                                $(this).find('.comment-delete').toggleClass('hide'); // 삭제 버튼 보임
                            }
                        })
                        .mouseout(function(){
                            const commentNick = $(this).data('nick');
                            if (myNick == commentNick) {
                                $(this).find('.comment-delete').toggleClass('hide'); // 삭제 버튼 사라짐
                            }
                        });

                    // 각 댓글 삭제 버튼을 누른다면...
                    $('.comment-delete').click(function (){
                        const commentId = $(this).data('ci');
                        const commentDiv = $(this).parent().parent();
                        const is_delete = confirm("정말 이 댓글을 삭제하시겠습니까?");
                        if (is_delete) {
                            $.ajax({
                                type: 'POST',
                                url: '/api/comment/delete',
                                data: {comment_id_give: commentId},
                                success: function (response) {
                                    if (response['result'] == 'success') {
                                        commentDiv.remove(); // 댓글 삭제
                                    } else {
                                        alert(response['msg'])
                                    }
                                },
                                error: function (err) {
                                    console.log('error:' + err)
                                }
                            })
                        }
                    })

                    //팝업창을 가운데로 띄우기 위해 현재 화면의 가운데 값과 스크롤 값을 계산하여 팝업창 CSS 설정
                    $("#comment-modal").css({
                        "top": (($(window).height() - $("#comment-modal").outerHeight()) / 2 + $(window).scrollTop()) + "px",
                        "left": (($(window).width() - $("#comment-modal").outerWidth()) / 2 + $(window).scrollLeft()) + "px",
                    });
                    $("body").css("overflow", "hidden");//body 스크롤바 없애기
                    $("#comment-modal").fadeIn();   // modal 보여주기
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

// 댓글 닫기 버튼을 누르면 ...
function closeModal() {
    window.location.href = '/home'
}

// 댓글 남기기 버튼을 누르면 ...
function leaveComment() {
    const commentWrite = $('#comment-writing').val();
    const postId = $('#comment-modal').data('post');

    // 작성한 댓글 없는 경우 종료
    if (commentWrite == '') return;

    $.ajax({
        type: 'POST',
        url: '/api/comment',
        data: {'post_id_give': postId, 'comment_give': commentWrite},
        success: function (response) {
            if (response['result'] == 'success') {
                const nickname = response['nickname']

                // 작성한 댓글을 태그 생성 후 추가
                let addSoon = "<div class='comment-body'><div class='body-wrapper'><span class='comment-left'>" + nickname + "</span>";
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