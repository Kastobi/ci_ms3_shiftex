$("document").ready( () => {

    function localeString(timestamp) {
        return new Date(parseInt(timestamp)).toLocaleString()
    }

    function ajaxFailure(jqXHR, textStatus, errorThrown) {
        // todo: flask flash modify for proper HTML display
        console.log("Error!")
        console.log(textStatus)
        console.log(errorThrown)
    }

    function sortList() {
        // https://stackoverflow.com/questions/22906760/jquery-sort-table-data
        //todo: maybe move to jinja template?
        const tbody = $("tbody")
        tbody.find("tr").sort(function(a, b) {
            return $("td:first", a).text().localeCompare(($("td:first", b).text()))
        }).appendTo(tbody)
    }
    sortList()

    function listControl() {
        const shiftRows = $(".shift-row")
        const requestRows = $(".request-row")
        const shiftRowsUpcoming = $(".shift-row.upcoming")
        const requestRowsUpcoming = $(".request-row.upcoming")

        const bothToggle = $("#both")[0].checked
        const shiftsToggle = $("#shifts")[0].checked
        const requestToggle = $("#requests")[0].checked
        const upcomingToggle = $("#show-future-only")[0].checked

        if (bothToggle && !upcomingToggle) {
            shiftRows.show()
            requestRows.show()
        } else if (bothToggle && upcomingToggle) {
            shiftRows.hide()
            requestRows.hide()
            shiftRowsUpcoming.show()
            requestRowsUpcoming.show()
        } else if (shiftsToggle && !upcomingToggle) {
            shiftRows.show()
            requestRows.hide()
        } else if (shiftsToggle && upcomingToggle) {
            shiftRows.hide()
            requestRows.hide()
            shiftRowsUpcoming.show()
        } else if (requestToggle && !upcomingToggle) {
            shiftRows.hide()
            requestRows.show()
        } else if (requestToggle && upcomingToggle) {
            shiftRows.hide()
            requestRows.hide()
            requestRowsUpcoming.show()
        }
    }

    $(`input[name="list"]`).click(function () {
        listControl()
    })


    /**
     * Button for toggling shift requests by the user
     *
     * css class highlights status of shift("swap-open" = There is an open swap request already present),
     * ajax http method based on presence of this class ("DELETE" to revoke, "PUT" to open request),
     * ajax url based on data-id html attribute of button,
     *
     * @param element button of shift table; attribute "data-id" maps to shift, css-class "swap-open" flags status
     */
    function toggleSwap(element) {
        const httpMethod = element.classList.contains("swap-open") ? "DELETE" : "PUT"

        function toggleSuccess() {
            if (element.classList.contains("swap-open")) {
                element.classList.remove("swap-open")
                element.innerText = "Open Request"
                $(`button[data-id="${element.dataset.id}"].swap-handle`).remove()
            } else {
                element.classList.add("swap-open")
                element.innerText = "Revoke Request"
                $(`<button class="btn btn-light swap-handle" data-id="${element.dataset.id}" 
                    data-target="#handle-modal" data-toggle="modal">Handle Offers</button>`)
                    .insertBefore(`button[data-id="${element.dataset.id}"].swap-open`)
            }
        }

        const request = $.ajax({
            url: `${$SCRIPT_ROOT}/api/swap/${element.dataset.id}`,
            method: httpMethod,
            success: function (data, textStatus, jqXHR) {
                toggleSuccess()
            },
            error: function (jqXHR, textStatus, errorThrown) {
                ajaxFailure(jqXHR, textStatus, errorThrown)
            }
        })
    }

    $(".swap-toggle").click(function () {
        // todo: add security question to revoke request
        toggleSwap(this)
    })

    /**
     * Modal for handling of offers on a shift request
     * shiftId acquired from button data-id attribute
     * first ajax call to get swap with offers
     * second ajax call to get data on the offers
     */

    $("#handle-modal").on("show.bs.modal", function (event) {
        const modal = $(this)
        const button = $(event.relatedTarget)
        const shiftRow = button.closest(".shift-row")
        const dateDay = new Date(parseInt(shiftRow.children(".shift-from")[0].dataset.time)).toDateString()
        const shiftId = button.data("id")

        const requestSwap = $.ajax({
                url: `${$SCRIPT_ROOT}/api/swap/${shiftId}`,
                method: "GET",
                dataType: "json",
                success: function(data, textStatus, jqXHR) {
                    handleSuccess(data, textStatus, jqXHR)
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown)
                }
            }
        )

        function handleSuccess(data, textStatus, jqXHR) {
            modal.find(".modal-title").text("Offers for shift on " + dateDay)
            modal.find(".modal-body").html(`
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>From</th>
                            <th>To</th>
                            <th>Duration</th>
                            <th>Handling</th>
                        </tr>
                    </thead>
                    <tbody class="modal-tbody">
                    </tbody>
                </table>`)

            const offerList = data.offer
            const acceptList = data.accept
            const rejectList = data.reject
            const requestShiftsList = {"ids": data.offer.concat(data.accept).concat(data.reject)}

            const requestShifts = $.ajax({
                url: `${$SCRIPT_ROOT}/api/shifts/`,
                method: "post",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(requestShiftsList),
                success: function (data, textStatus, jqXHR) {
                    modalShiftsSuccess(data)
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown)
                }
            })

            function modalShiftsSuccess(data) {
                for (let offer of data) {
                    $(".modal-tbody").append(`
                    <tr>
                        <td>${localeString(offer.from)}</td>
                        <td>${localeString(offer.to)}</td>
                        <td>${Math.abs(offer.to - offer.from) / 3.6e6} hours</td>
                        <td>
                            <button class="btn btn-light offer-accept offer-handle" data-id="${offer.shiftId}">
                                    Accept
                            </button>
                            <button class="btn btn-light offer-reject offer-handle" data-id="${offer.shiftId}">
                                    Reject
                            </button>
                        </td>
                    </tr>
                    `)
                }

                for (let shift of acceptList) {
                    $(`button.offer-accept[data-id=${shift}]`).addClass("accepted")
                }
                for (let shift of rejectList) {
                    $(`button.offer-reject[data-id=${shift}]`).addClass("rejected")
                }

                function handleOffer(element) {
                    const mode = element.classList.contains("offer-accept") ? "accept" : "reject"

                    if (element.classList.contains(`${mode}ed`)) {
                        return
                    }

                    const offerId = element.dataset.id
                    const request = $.ajax({
                        url: `${$SCRIPT_ROOT}/api/swap/${shiftId}/${mode}/${offerId}`,
                        method: "PATCH",
                        success: function (data, textStatus, jqXHR) {
                            handleOfferSuccess(element, mode)
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                           ajaxFailure(jqXHR, textStatus, errorThrown)
                        }
                    })

                    function handleOfferSuccess(element, mode) {
                        if (mode === "accept") {
                            $(`button.offer-reject[data-id=${element.dataset.id}]`).removeClass("rejected")
                            element.classList.add("accepted")
                        } else if (mode === "reject") {
                            $(`button.offer-accept[data-id=${element.dataset.id}]`).removeClass("accepted")
                            element.classList.add("rejected")
                        }
                    }
                }

                $(".offer-handle").click(function () {
                    handleOffer(this)
                })
            }
        }
    })

    /**
     * Modal for offering shifts on a swap request
     * shiftId acquired from button data-id attribute
     */

    $("#offer-modal").on("show.bs.modal", function (event) {
        const modal = $(this)
        const button = $(event.relatedTarget)
        const requestRow = button.closest(".request-row")
        const dateDay = new Date(parseInt(requestRow.children(".request-from")[0].dataset.time)).toDateString()
        const shiftId = button.data("id")

        const userShiftList = {"ids": []}
        $(".upcoming .swap-toggle").each(function() {
            userShiftList["ids"].push(this.dataset.id)
        })

        const requestShifts = $.ajax({
                url: `${$SCRIPT_ROOT}/api/shifts/`,
                method: "post",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(userShiftList),
                success: function (data, textStatus, jqXHR) {
                    offerShiftsSuccess(data)
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown)
                }
            })

        function offerShiftsSuccess(data) {
            modal.find(".modal-title").text("Possible swaps for shift on " + dateDay)
            modal.find(".modal-body").html(`
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>From</th>
                            <th>To</th>
                            <th>Duration</th>
                            <th>Offer shift</th>
                        </tr>
                    </thead>
                    <tbody class="modal-tbody">
                    </tbody>
                </table>`)

            for (let shift of data) {
                $(".modal-tbody").append(`
                    <tr>
                        <td>${localeString(shift.from)}</td>
                        <td>${localeString(shift.to)}</td>
                        <td>${Math.abs(shift.to - shift.from) / 3.6e6} hours</td>
                        <td>
                            <button class="btn btn-light offer-accept offer-shift" data-id="${shift.shiftId}">
                                    Offer shift
                            </button>
                        </td>
                    </tr>`)
            }

            function offerShift(element) {
                const offerId = element.dataset.id

                const placeOffer = $.ajax({
                    url: `${$SCRIPT_ROOT}/api/swap/${shiftId}/offer/${offerId}`,
                    method: "patch",
                    success: function (data, textStatus, jqXHR) {
                        offerPlacementSuccess()
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        ajaxFailure(jqXHR, textStatus, errorThrown)
                    }
                })

                function offerPlacementSuccess() {
                    element.classList.add("offered")
                }

            }

            $(".offer-shift").click(function () {
                    offerShift(this)
                })
        }
    })

    $("#confirm-modal").on("show.bs.modal", function (event) {
        const modal = $(this)
        const button = $(event.relatedTarget)
        const requestRow = button.closest(".request-row")
        const dateDay = new Date(parseInt(requestRow.children(".request-from")[0].dataset.time)).toDateString()
        const shiftId = button.data("id")
        const confirmId = button.data("confirm")

        modal.find(".modal-body").html(`
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Transaction</th>
                            <th>From</th>
                            <th>To</th>
                            <th>Duration</th>
                        </tr>
                    </thead>
                    <tbody class="confirm-modal-tbody">
                    </tbody>
                </table>`)

        const shiftList = {"ids": [shiftId, confirmId]}
        const requestShifts = $.ajax({
                url: `${$SCRIPT_ROOT}/api/shifts/`,
                method: "post",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(shiftList),
                success: function (data, textStatus, jqXHR) {
                    requestShiftsSuccess(data)
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown)
                }
            })

        function requestShiftsSuccess(data) {
            const confirmButton = $(".confirm-offer")
            $(".confirm-modal-tbody").append(`
                    <tr>
                        <td>You get</td>
                        <td>${localeString(data[0].from)}</td>
                        <td>${localeString(data[0].to)}</td>
                        <td>${Math.abs(data[0].to - data[0].from) / 3.6e6} hours</td>
                    </tr>
                    <tr>
                        <td>You trade in</td>
                        <td>${localeString(data[1].from)}</td>
                        <td>${localeString(data[1].to)}</td>
                        <td>${Math.abs(data[1].to - data[1].from) / 3.6e6} hours</td>
                    </tr>`)

            confirmButton.attr("data-id", shiftId).attr("data-target", confirmId)

            function confirmOffer(element) {
                const shiftId = element.dataset.id
                const confirmId = element.dataset.target

                const sendRequest = $.ajax({
                    url: `${$SCRIPT_ROOT}/api/swap/${shiftId}/confirm/${confirmId}`,
                    method: "patch",
                    success: function (data, textStatus, jqXHR) {
                        confirmSuccess()
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        ajaxFailure(jqXHR, textStatus, errorThrown)
                    }
                })

                function confirmSuccess() {
                    // todo: dismiss modal
                    // todo: reload user.html
                    console.log("Confirmed!")
                }
            }

            confirmButton.click(function () {
                    confirmOffer(this)
                })

        }

    })

    $(".modal").on("shown.bs.modal", function () {
        $(".modal").trigger("focus")
    })
})
