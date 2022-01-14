function goWrite() {
    window.location.href = "/writepost"
}

function goMypage() {
    window.location.href = "/mypage"
}

function reRoad() {
    window.location.reload()
}

// 댓글 html 요소 생성
function getCommentElement(nickname, comment, commentId) {
    let commentEl = "<div class='comment-body' data-nick='"+nickname+"'><div class='body-wrapper'><span class='comment-left'>" + nickname + "</span>";
    commentEl += "<span class='comment-right'>" + comment + "</span></div>";
    commentEl += "<div class='delete-wrapper'><span class='comment-delete hide' data-ci='"+commentId+"'><img src='../static/images/close.png'/></span></div></div>";
    return commentEl;
}

// 작성한 댓글 html 요소 생성
function getNewCommentElement(nickname, comment) {
    let commentEl = "<div class='comment-body' data-nick='"+nickname+"'><div class='body-wrapper'><span class='comment-left'>" + nickname + "</span>";
    commentEl += "<span class='comment-right'>" + comment + "</span></div>";
    commentEl += "<div class='delete-wrapper'><span class='comment-delete hide'><img src='../static/images/close.png'/></span></div></div>";
    return commentEl;
}

// 댓글 삭제 버튼 show/hide
function removeButtonSwitch(selectEl, myNick) {
    const commentNick = selectEl.data('nick');
    if (myNick == commentNick) {
        selectEl.find('.comment-delete').toggleClass('hide'); // 삭제 버튼 hide클래스 추가/삭제
    }
}

// 각 포스트 하위 태그들의 html 가져온다. (클래스로만 접근가능)
function getMyHtml(postId, myClass) {
    return $('#' + postId).find('.'+myClass).clone().wrapAll("<div/>").parent().html();
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
                    // 각 댓글 생성 및 추가
                    const myNick = response['nickname'];
                    const commentList = response['comments'];
                    for (let i = 0; i < commentList.length; i++) {
                        const nickname = commentList[i].nickname;
                        const comment = commentList[i].comment;
                        const commentId = commentList[i]._id;
                        $('#comment-wrapper').append(getCommentElement(nickname, comment, commentId));
                    }
                    $('#comment-modal').data('post', postId);

                    // 해당 포스트의 글쓴이 정보 및 포스트 내용 태그 생성 및 추가
                    const writerImg = getMyHtml(postId, "profile-img");
                    const writerNick = getMyHtml(postId, "profile-txt");
                    const writerContent = getMyHtml(postId, "post-content");
                    $('#cmb-post').append("<div class='post-header'><div class='left-wrapper'>"+writerImg+"</div></div>");
                    $('#cmb-post .post-header .left-wrapper').append(writerNick);
                    $('#cmb-post').append(writerContent);

                    // 각 댓글을 마우스오버/마우스아웃 한다면..
                    $('.comment-body')
                        .mouseover(function() {
                            removeButtonSwitch($(this), myNick)
                        })
                        .mouseout(function(){
                            removeButtonSwitch($(this), myNick)
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
                $('#comment-wrapper').append(getNewCommentElement(nickname, commentWrite))
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