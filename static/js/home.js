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
    let commentEl = "<div class='comment-body' data-nick='" + nickname + "'><div class='body-wrapper'><span class='comment-left'>" + nickname + "</span>";
    commentEl += "<span class='comment-right'>" + comment + "</span></div>";
    commentEl += "<div class='delete-wrapper'><span class='comment-delete hide' data-ci='" + commentId + "'><img src='../static/images/close.png'/></span></div></div>";
    return commentEl;
}

// 작성한 댓글 html 요소 생성
function getNewCommentElement(nickname, comment) {
    let commentEl = "<div class='comment-body' data-nick='" + nickname + "'><div class='body-wrapper'><span class='comment-left'>" + nickname + "</span>";
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
    return $('#' + postId).find('.' + myClass).clone().wrapAll("<div/>").parent().html();
}

function setDeletebutton(myNick) {
    // 각 댓글을 마우스오버/마우스아웃 한다면..
    $('.comment-body')
        .mouseover(function () {
            removeButtonSwitch($(this), myNick)
        })
        .mouseout(function () {
            removeButtonSwitch($(this), myNick)
        });

    // 각 댓글 삭제 버튼을 누른다면...
    $('.comment-delete').click(function () {
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
                    $('#cmb-post').append("<div class='post-header'><div class='left-wrapper'>" + writerImg + "</div></div>");
                    $('#cmb-post .post-header .left-wrapper').append(writerNick);
                    $('#cmb-post').append(writerContent);

                    // 각 댓글 삭제 버튼 세팅
                    setDeletebutton(myNick);
                    // // 각 댓글을 마우스오버/마우스아웃 한다면..
                    // $('.comment-body')
                    //     .mouseover(function() {
                    //         removeButtonSwitch($(this), myNick)
                    //     })
                    //     .mouseout(function(){
                    //         removeButtonSwitch($(this), myNick)
                    //     });
                    //
                    // // 각 댓글 삭제 버튼을 누른다면...
                    // $('.comment-delete').click(function (){
                    //     const commentId = $(this).data('ci');
                    //     const commentDiv = $(this).parent().parent();
                    //     const is_delete = confirm("정말 이 댓글을 삭제하시겠습니까?");
                    //     if (is_delete) {
                    //         $.ajax({
                    //             type: 'POST',
                    //             url: '/api/comment/delete',
                    //             data: {comment_id_give: commentId},
                    //             success: function (response) {
                    //                 if (response['result'] == 'success') {
                    //                     commentDiv.remove(); // 댓글 삭제
                    //                 } else {
                    //                     alert(response['msg'])
                    //                 }
                    //             },
                    //             error: function (err) {
                    //                 console.log('error:' + err)
                    //             }
                    //         })
                    //     }
                    // })

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

    // 좋아요 버튼을 누른다면 ...
    $('.post-icon').click(function () {
        const heartIcon = $(this); // 선택한 포스트의 좋아요 element
        const postId = heartIcon.data('id'); // 선택한 포스트의 id를 담음
        const likeId = "#" + postId + "-like-cnt"; // [좋아요 카운트] element
        const reqHeartStatus = heartIcon.data('heart') == '0' ? 1 : 0; // 기존 [좋아요 상태]를 보고 요청 할 [좋아요 상태] 설정

        $.ajax({
            type: 'POST',
            url: '/api/like',
            data: {'like_give': reqHeartStatus, 'post_id_give': postId},
            success: function (response) {
                if (response['result'] == 'success') {
                    if (reqHeartStatus) { // 요청한 [좋아요 상태]가 1(좋아요!) 이면 ...
                        heartIcon.data('heart', '1'); // [좋아요 상태] 1로 설정
                        heartIcon.attr('src', '../static/images/heart_full.png'); // 빨간 하트로 이미지 설정

                        if ($(likeId).text().trim() == '') { // [좋아요 카운트]가 없다면
                            $(likeId).text('1'); // [좋아요 카운트] 1로
                            $(likeId).next().text('명이 좋아합니다😍'); // 그 뒤에 문구
                        } else {
                            const changeHeartCnt = parseInt($(likeId).text()) + 1; // [좋아요 카운트] 1 더함
                            $(likeId).text(changeHeartCnt); // [좋아요 카운트] element에 수정한 값 표시
                        }

                    } else { // 요청한 [좋아요 상태]가 0(좋아요 해제!) 이면 ...
                        heartIcon.data('heart', '0'); // [좋아요 상태] 0으로 설정
                        heartIcon.attr('src', '../static/images/heart_empty.png'); // 빈 하트로 이미지 설정
                        const changeHeartCnt = parseInt($(likeId).text()) - 1; // [좋아요 카운트] 1 뺌

                        if (!changeHeartCnt) { // [좋아요 카운트]가 0 이라면 ..
                            $(likeId).text(''); // [좋아요 카운트] 없애고
                            $(likeId).next().text('No one likes me😭️'); // 그 뒤에 새로운 문구
                        } else {
                            $(likeId).text(changeHeartCnt) // [좋아요 카운트] element에 수정한 값 표시
                        }
                    }
                } else {
                    console.log(response['msg'])
                }
            },
            error: function (err) {
                console.log('error:' + err)
            }
        })
    })

    // 스크랩 버튼을 누른다면 ...
     $('.post-icon-3').click(function(){
        const scrapIcon = $(this); // 선택한 포스트의 scrap element
        const postId = scrapIcon.data('id'); // 선택한 포스트의 id를 담음
         console.log(scrapIcon)
        /*const scrapId = "#" + postId + "-like-cnt"; // [스크랩 카운트] element*/
        const reqscrapStatus = scrapIcon.data('scrap') == '0' ? 1 : 0; // 기존 [좋아요 상태]를 보고 요청 할 [좋아요 상태] 설정

        $.ajax({
            type: 'POST',
            url: '/home/scrap',
            data: {'scrap_give': reqscrapStatus, 'post_id_give': postId},
            success: function (response) {
                if (response['result'] == 'success') {
                    if (reqscrapStatus) { // 요청한 [스크랩 상태]가 1(스크랩) 이면 ...
                        scrapIcon.data('scrap', '1'); // [스크랩 상태] 1로 설정
                        scrapIcon.attr('src', '../static/images/scrap_full.png'); // scrap컬러로 이미지 설정
                    } else { // 요청한 [스크랩 상태]가 0(스크랩 해제) 이면 ...
                        scrapIcon.data('scrap', '0'); // [좋아요 상태] 0으로 설정
                        scrapIcon.attr('src', '../static/images/scrap_empty.png'); // 빈 스크랩으로 이미지 설정
                    }
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
                const myNick = response['info']['nickname'];
                const commentId = response['info']['comment_id']

                // 작성한 댓글을 태그 생성 후 추가
                $('#comment-wrapper').append(getCommentElement(myNick, commentWrite, commentId));
                // 댓글 삭제 버튼 세팅
                setDeletebutton(myNick);
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