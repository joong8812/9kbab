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
    $('#help_id').text('아이디는 영문, 숫자, 특수문자(._-) 사용가능. 2-10자로 입력하세요.')
    $('#check_id').val('중복체크').css({'color':'gray'})
    $('#userid').focus()
    return true;
  }

  if (!is_id(userid)) {
    $('#help_id').text('아이디는 영문, 숫자, 특수문자(._-) 사용가능. 2-10자로 입력하세요.')
    $('#check_id').val('중복체크').css({'color':'gray'})
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
        $('#check_id').val('중복체크').css({'color':'gray'})
        $('#userid').focus()
        return true;
      }
      else {
        $('#help_id').text('　')
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
    $('#help_nick').text('닉네임을 입력하세요.')
    $('#check_name').val('중복체크').css({'color':'gray'})
    $('#nickname').focus()
    return true;
  }
  if (!is_nick(nickname)){
    $('#help_nick').text('닉네임은 한글/영문/숫자/특수문자(._-)가능. 2-10자로 입력하세요.')
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
        $('#help_nick').text('이미 존재하는 닉네임입니다.')
        $('#check_name').val('중복체크').css({'color':'gray'})
        $('#nickname').focus()
        return true;
      }
      else {
        $('#help_nick').text('　')
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
    $('#help_pw1').text('비밀번호는 영문/숫자를 혼합하여 4-20자로 입력하세요.')
    $('#pw').focus()
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