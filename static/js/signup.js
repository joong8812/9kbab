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

//----------중복확인: 아이디
function checkid() {
  let userid = $('#userid').val()
  console.log(userid)
  if (userid == "") {
    alert('아이디를 입력하세요.')
    $('#check_id').val('중복체크').css({'color':'gray'})
    $('#userid').focus()
    return true;
  }
  if (!is_id(userid)) {
    alert('아이디 형식을 확인하세요.')
    $('#check_id').val('중복체크').css({'color':'gray'})
    $('#userid').focus()
    return true;
  }
  $.ajax({
    type: "POST",
    url: "/signup/id_check",
    data:{id_give: userid},
    success: function(response){
      if (response["exists"]){
        alert('이미 존재하는 아이디입니다.')
        $('#check_id').val('중복체크').css({'color':'gray'})
        $('#userid').focus()
        return true;
      }
      else {
        $('#check_id').val('사용가능').css({'color':'green'})
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
    alert('닉네임을 입력하세요.')
    $('#check_name').val('중복체크').css({'color':'gray'})
    $('#nickname').focus()
    return true;
  }

  $.ajax({
    type: "POST",
    url: "/signup/nick_check",
    data:{nick_give: nickname},
    success: function(response){
      if (response["exists"]){
        alert('이미 존재하는 닉네임입니다.')
        $('#check_name').val('중복체크').css({'color':'gray'})
        $('#nickname').focus()
        return true;
      }
      else {
        $('#check_name').val('사용가능').css({'color':'green'})
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
  console.log(userid, nickname, email, pw1, pw2)

  //아이디입력조건 함수
  checkid()

  //닉네임입력조건 함수
  checknick()

  if (!is_email(email)){
    alert('이메일 형식을 입력하세요')
    $('#useremail').focus()
    return;
  }

  if (pw1 == "") {
    alert('비밀번호를 입력하세요.')
    $('#pw').focus()
    return;
  }
  else if (!is_pw(pw1)) {
    alert('비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 4-20자')
    $('#pw').focus()
    return;
  }
  if (pw2 == "") {
    alert('재확인 비밀번호를 입력하세요.')
    $('#pw-check').focus()
    return;
  }
  else if (pw2 != pw1) {
    alert('비밀번호가 일치하지 않습니다.')
    $('#pw-check').focus()
    return;
  }

  if ($('#check_all').is(':checked') == false){
    alert('약관에 동의해주세요.')
    $('#check_all').focus()
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
      alert('회원가입을 축하합니다!!')
      window.location.replace("/login")
    }
  })
}