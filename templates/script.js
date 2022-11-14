function register() {
            if (!$('.id').val()) {
                alert('아이디를 입력해주세요.')
            }else if (!$('.password').val()){
                alert('비밀번호를 입력해주세요.')
            }else if (!$('.passwordCheck').val()){
                alert('비밀번호 확인란을 입력해주세요.')
            }else if (!$('.nickname').val()) {
                alert('닉네임을 입력해주세요.')
            }

            if ($('.password').val() != $('.passwordCheck').val()) {
                alert('비밀번호와 비밀번호 확인 값이 다릅니다.')
            }
        }

function passwordShow() {
    if($('.password').attr('type') == 'password'){
            $('.passwordBox > i').attr('class',"fa-sharp fa-solid fa-eye-slash");
            $('.password').attr('type',"text");
        }else{
            $('.passwordBox > i').attr('class',"fa-sharp fa-solid fa-eye");
            $('.password').attr('type',"password");
        }
}

function passwordCheckShow() {
    if($('.passwordCheck').attr('type') == 'password'){
            $('.passwordCheckBox > i').attr('class',"fa-sharp fa-solid fa-eye-slash");
            $('.passwordCheck').attr('type',"text");
        }else{
            $('.passwordCheckBox > i').attr('class',"fa-sharp fa-solid fa-eye");
            $('.passwordCheck').attr('type',"password");
        }
}