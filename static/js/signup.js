function checkSelectAll()  {
  const checkboxes
      =document.querySelectorAll('input[name="agree"]');
  const checked
      =document.querySelectorAll('input[name="agree"]:checked');
  const selectAll
      =document.querySelector('input[name="selectall"]');

  if(checkboxes.length === checked.length)  {
    selectAll.checked = true;
  }
  else {
    selectAll.checked = false;
  }
}

function selectAll(selectAll)  {
  const checkboxes
      = document.getElementsByName('agree');

  checkboxes.forEach((checkbox) => {
    checkbox.checked = selectAll.checked
  })
}

//----------아이디/비밀번호/이메일 정규표현식

function is_id(asValue) {
  var regid = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
  return regid.test(asValue);}

function is_pw(asValue) {
  var regpw = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{4,20}$/;
  return regpw.test(asValue);}

function is_email(asValue) {
  var regemail = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
  return regemail.test(asValue);}

function is_nick(asValue) {
  var regnick = /^(?=.*[a-zA-Z가-힣])[-a-zA-Z0-9가-힣_.]{2,10}$/;
  return regnick.test(asValue);}

//----------중복확인: 아이디
function checkid() {
  let userid = $('#userid').val()

  if (userid == "") {
    $('#help_id').text('영문/숫자/특수문자(._-)가능. 2-10자 입력')
    $('#check_id').val('중복체크').css({'color':'#67BAB2','background-color':'white'})
    $('#userid').focus()
    return true;
  }

  if (!is_id(userid)) {
    $('#help_id').text('영문/숫자/특수문자(._-)가능. 2-10자 입력')
    $('#check_id').val('중복체크').css({'color':'#67BAB2','background-color':'white'})
    $('#userid').focus()
    return true;
  }

  $.ajax({
    type: "POST",
    url: "/signup/id_check",
    data:{id_give: userid},
    success: function(response){
      if (response['exists']){
        $('#help_id').text('이미 존재하는 아이디입니다.')
        $('#check_id').val('중복체크').css({'color':'#67BAB2','background-color':'white'})
        $('#userid').focus()
        $('#userid').val(null)
        return true;
      }
      else {
        $('#help_id').text('　')
        $('#check_id').val('사용가능').css({'color':'white','background-color':'#67BAB2'})
        return false;
      }
    }
  })
}

//----------중복확인: 닉네임
function checknick() {
  let nickname = $('#nickname').val()
  console.log(nickname)

  if (nickname == ""){
    $('#help_nick').text('닉네임을 입력하세요.')
    $('#check_name').val('중복체크').css({'color':'#67BAB2','background-color':'white'})
    $('#nickname').focus()
    return true;
  }
  if (!is_nick(nickname)){
    $('#help_nick').text('잘못된 형식입니다. 한글/영문/숫자/특수문자(._-)가능. 2-10자내')
    $('#check_name').val('중복체크').css({'color':'#67BAB2','background-color':'white'})
    $('#nickname').focus()
    $('#nickname').val(null)
    return true;
  }

    $.ajax({
    type: "POST",
    url: "/signup/nick_check",
    data:{nick_give: nickname},
    success: function(response){
      if (response["exists"]){
        $('#help_nick').text('이미 존재하는 닉네임입니다.')
        $('#check_name').val('중복체크').css({'color':'#67BAB2','background-color':'white'})
        $('#nickname').focus()
        $('#nickname').val(null)
        return true;
      }
      else {
        $('#help_nick').text('　')
        $('#check_name').val('사용가능').css({'color':'white','background-color':'#67BAB2'})
        return false;
      }
    }
  })
}

//----------회원가입 버튼 눌렀을때
function signup(){
  let userid = $('#userid').val()
  let nickname = $('#nickname').val()
  let email = $('#useremail').val()
  let pw1 = $('#pw').val()
  let pw2 = $('#pw-check').val()
  const isHuman = $('#check_digit').val();
  console.log(userid, email, nickname, pw1)


  if ($('#check_id').val() == "중복체크"){
    $('#help_id').text('중복확인해주세요')
    $('#userid').focus()
    return;
  }

  if ($('#check_name').val() == '중복체크'){
    $('#help_nick').text('중복확인해주세요')
    $('#nickname').focus()
    return;
  }

  if (!is_email(email)){
    $('#help_email').text('이메일 형식을 입력하세요')
    $('#useremail').focus()
    $('#useremail').val(null)
    return;
  }
  else{
    $('#help_email').text('　')
  }

  if (pw1 == "") {
    $('#help_pw1').text('비밀번호를 입력하세요.')
    $('#pw').focus()
    return;
  }
  else if (!is_pw(pw1)) {
    $('#help_pw1').text('잘못된 형식입니다. 영문/숫자 혼합, 4-20자로 입력')
    $('#pw').focus()
    $('#pw').val(null)
    return;
  }
  else{
    $('#help_pw1').text('　')
  }

  if (pw2 == "") {
    $('#help_pw2').text('재확인 비밀번호를 입력하세요.')
    $('#pw-check').focus()
    return;
  }
  else if (pw2 != pw1) {
    $('#help_pw2').text('비밀번호가 일치하지 않습니다.')
    $('#pw-check').focus()
    $('#pw-check').val(null)
    return;
  }
  else{
    $('#help_pw2').text('　')
  }

  if ($('#check_all').is(':checked') == false){
    alert('약관에 동의해주세요.')
    $('#check_all').focus()
    return false;
  }

  if (isHuman.indexOf('사람') == -1) {
    $('#captcha-area').css(
        'border', 'solid 2px #F9C428'
    );
    return;
  }

  $.ajax({
    type: "POST",
    url: "/api/signup",
    data:{
      id_give: userid,
      em_give: email,
      nick_give: nickname,
      pw_give: pw1
    },
    success: function(response){
      if (response['result']=='success'){
        alert(response['msg'])
        window.location.replace("/login")
      }
      else if (response['result']=='fail'){
        alert('입력 정보를 확인해주세요')
      }
    }
  })
}

// 전역 캔버스 object 생성(캔버스 설정 세팅)
const canvas = function (p) {
    p.setup = function () {
        p.createCanvas(100, 100); // 100x100 캔버스
        p.background(0); // 배경은 검은색
    }
    p.draw = function () {
    }

    p.mouseDragged = function () {
        p.fill(253, 253, 253); // 하얀색
        p.noStroke(); // 테두리 없앤다
        if (p.mouseButton == p.LEFT) { // 왼쪽 버튼을 누른다면
            p.circle(p.mouseX, p.mouseY, 9); // 9 크기의 원을 그린
        }
    }
};

$(document).ready(function () {
    new p5(canvas, 'canvas-wrapper'); // div에 캔버스 생성
})


function canvasToBase64() {
    const c = $('#canvas-wrapper').find('canvas'); // 캔버스 element
    const imageData = c[0].toDataURL('image/jpg'); // 캔버스를 base64 image string 으로
    const answer = $('#digit-img').data('answer'); // 제시 한 이미지의 정답

    $.ajax({
        type: 'POST',
        url: '/api/digit',
        data: {'user_digit_give': imageData, 'answer_digit_give': answer},
        success: function (response) {
            if (response['result'] == 'success') {  // 제시 그림과 사용자 그림 일치
                $('#box-wrapper').children().children().text('');
                $('#check_digit').val('당신은 사람이군요!').css({
                    'color': 'white',
                    'border': 'solid 1px #67BAB2',
                    'background-color': '#67BAB2'});
                $('#captcha-area').css('border', 'solid 2px #67BAB2');
                $('#captcha-area').addClass('disabled-captcha');
            } else { // 그림 불일치
                let errCnt = parseInt($('#check_digit').data('count'));
                errCnt += 1;

                if (errCnt == 3) { // 3번 불일치 시
                    alert('3번 불일치하여 회원가입을 진행할 수 없습니다')
                    window.location.href = '/';
                } else {
                    $('#check_digit').data('count', errCnt);
                    if (errCnt == 1) { // 1번 불일치 시
                        $('#check_digit').val('이쁘게 다시 한번!')
                        $('#captcha-area').css(
                            'border', 'solid 2px #67BAB2'
                        );
                    } else { // 2번 불일치 시
                        $('#check_digit').val('혹시 로..봇.. 아니죠?').css({
                            'color': '#FF2800',
                            'border': 'solid 1px #FF2800'
                        });
                        $('.check_btn.active').css({
                            'background-color': '#FF2800',
                            'color': 'white'
                        })
                        $('#captcha-area').css(
                            'border', 'solid 2px #FF2800'
                        );
                    }
                    $('#canvas-wrapper').empty(); // 기존 캔버스 지우기
                    new p5(canvas, 'canvas-wrapper'); // 새로운 캔버스 생성
                    window.location.hash = '#box-wrapper';
                }
            }
        },
        error: function (err) {
            console.log('error:' + err)
        }
    })
}