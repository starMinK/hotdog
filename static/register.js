function register() {
    const regExp = /[ㄱ-ㅎㅏ-ㅣ가-힣]/g;

    if (!$('.id').val()) {
        alert('아이디를 입력해주세요.')
    } else if (regExp.test($('.id').val())){
        alert('아이디는 영어, 숫자, 특수문자로만 이루어질 수 있습니다.')
    } else if (!$('.password').val()) {
        alert('비밀번호를 입력해주세요.')
    } else if(regExp.test($('.password').val())) {
        alert('비밀번호는 영어, 숫자, 특수문자로만 이루어질 수 있습니다.')
    }else if (!$('.passwordCheck').val()) {
        alert('비밀번호 확인란을 입력해주세요.')
    } else if (!$('.nickname').val()) {
        alert('닉네임을 입력해주세요.')
    } else if ($('.password').val() != $('.passwordCheck').val()) {
        alert('비밀번호와 비밀번호 확인 값이 다릅니다.')
    }else {
        let id = $('.id').val();
        let password = $('.password').val();
        let nickname = $('.nickname').val();

        $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: id,
            pw_give: password,
            nickname_give: nickname
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.history.back();
            } else if(response['result'] == 'id_default'){
                alert('중복된 아이디가 있습니다.')
            } else if(response['result'] == 'nickname_default'){
                alert('중복된 닉네임이 있습니다.')
            } else {
                alert(response['msg'])
            }
        }
    });
    }
}

function passwordShow() {
    if ($('.password').attr('type') == 'password') {
        $('.passwordBox > i').attr('class', "fa-sharp fa-solid fa-eye-slash");
        $('.password').attr('type', "text");
    } else {
        $('.passwordBox > i').attr('class', "fa-sharp fa-solid fa-eye");
        $('.password').attr('type', "password");
    }
}