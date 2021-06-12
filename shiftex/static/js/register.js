/*jshint esversion: 8 */
/*globals $*/

$("document").ready( () => {

    const passwordField = $("#password");

    /**
     * Password validator before submit to give a hint on security prerequisites
     */
    function passwordValidation() {
        const checkRegex = new RegExp("^(?=.*?[A-Za-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$");

        if (checkRegex.test(passwordField.val())) {
            $(".password-hint").remove();

        } else {
            if (!$(".password-hint")[0]) {
                $(`<span class="password-hint">
                    Minimum six characters, at least one letter, one number and one special character.
                   </span>`
                ).insertAfter(passwordField);
            }
        }
    }
    passwordField.change(() => {
        passwordValidation();
    });
});
