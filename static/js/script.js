$("document").ready( () => {

    function toggleSwap(element) {

        const httpMethod = element.classList.contains("swap-open") ? "DELETE" : "PUT"

        function toggleSuccess() {
            if (element.classList.contains("swap-open")) {
                element.classList.remove("swap-open")
                element.innerText = "Open Request"
            } else {
                element.classList.add("swap-open")
                element.innerText = "Revoke Request"
            }
        }

        function toggleFailure(jqXHR, textStatus, errorThrown) {
            // todo: flask flash modify for proper HTML display
            console.log("Error!")
            console.log(textStatus)
            console.log(errorThrown)
        }

        const request = $.ajax({
            url: `${$SCRIPT_ROOT}/api/swaps/${element.id}`,
            method: httpMethod,
            success: function () {
                toggleSuccess()
            },
            error: function (jqXHR, textStatus, errorThrown) {
                toggleFailure(jqXHR, textStatus, errorThrown)
            }
        })
    }

    $(".swap-toggle").click(function () {
        // todo: add security question to revoke request
        toggleSwap(this)
    })

})
