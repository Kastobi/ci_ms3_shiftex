/*jshint esversion: 8 */
/*globals globals, $*/

$("document").ready( () => {

    function localeString(timestamp) {
        return new Date(parseInt(timestamp)).toLocaleString();
    }

    function ajaxFailure(jqXHR, textStatus, errorThrown) {
        // todo: flask flash modify for proper HTML display
        console.log("Error!");
        console.log(textStatus);
        console.log(errorThrown);
    }

    function sortList() {
        /**
         * Sorts swap requests into shifts list for comfort comprehension
         *
         * https://stackoverflow.com/questions/22906760/jquery-sort-table-data
         * todo: maybe move to jinja template?
         * @type {*|Window.jQuery|HTMLElement}
         */
        const tbody = $("tbody");
        tbody.find("tr").sort(function(a, b) {
            return $("td:first", a).text().localeCompare(($("td:first", b).text()));
        }).appendTo(tbody);
    }
    sortList();

    function listControl() {
        /**
         * Adds controls to the shifts table
         *  toggle: show all or just upcoming (upcoming default)
         *  select: show shifts, swap requests or both (default: shifts)
         *
         * @type {*|Window.jQuery|HTMLElement}
         */
        const shiftRows = $(".shift-row");
        const requestRows = $(".request-row");
        const shiftRowsUpcoming = $(".shift-row.upcoming");
        const requestRowsUpcoming = $(".request-row.upcoming");

        const bothToggle = $("#both")[0].checked;
        const shiftsToggle = $("#shifts")[0].checked;
        const requestToggle = $("#requests")[0].checked;
        const upcomingToggle = $("#show-future-only")[0].checked;

        if (bothToggle && !upcomingToggle) {
            shiftRows.show();
            requestRows.show();
        } else if (bothToggle && upcomingToggle) {
            shiftRows.hide();
            requestRows.hide();
            shiftRowsUpcoming.show();
            requestRowsUpcoming.show();
        } else if (shiftsToggle && !upcomingToggle) {
            shiftRows.show();
            requestRows.hide();
        } else if (shiftsToggle && upcomingToggle) {
            shiftRows.hide();
            requestRows.hide();
            shiftRowsUpcoming.show();
        } else if (requestToggle && !upcomingToggle) {
            shiftRows.hide();
            requestRows.show();
        } else if (requestToggle && upcomingToggle) {
            shiftRows.hide();
            requestRows.hide();
            requestRowsUpcoming.show();
        }
    }

    $(`input[name="list"]`).click(function () {
        listControl();
    });


    function toggleSwap(element) {
        /**
         * Button for toggling shift requests by the user
         *
         * css class highlights status of shift("swap-open" = There is an open swap request already present),
         * ajax http method based on presence of this class ("DELETE" to revoke, "PUT" to request swap),
         * ajax url based on data-id html attribute of button,
         *
         * @param element button of shift table;
         *      attribute "data-id" maps to shift,
         *      css-class "swap-open" flags status
         */
        const httpMethod = element.classList.contains("swap-open") ? "DELETE" : "PUT";

        const toggleSwap = $.ajax({
            url: `${$SCRIPT_ROOT}/api/swap/${element.dataset.id}`,
            method: httpMethod,
            success: function (data, textStatus, jqXHR) {
                toggleSuccess();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                ajaxFailure(jqXHR, textStatus, errorThrown);
            }
        });

        function toggleSuccess() {
            if (element.classList.contains("swap-open")) {
                element.classList.remove("swap-open", "btn-outline-danger");
                element.classList.add("btn-outline-secondary");
                element.innerText = "Request Swap";
                $(`button[data-id="${element.dataset.id}"].swap-handle`).remove();
            } else {
                element.classList.add("swap-open", "btn-outline-danger");
                element.innerText = "Revoke Request";
                $(`<button class="btn btn-block btn-outline-success swap-handle" data-id="${element.dataset.id}" 
                    data-target="#handle-modal" data-toggle="modal">Handle Offers</button>`)
                    .insertBefore(`button[data-id="${element.dataset.id}"].swap-open`);
            }
        }
    }

    $(".swap-toggle").click(function () {
        // todo: add security question to revoke request
        toggleSwap(this);
    });

    /**
     * Dynamic generated Modal for handling offers on a shift request
     * shiftId acquired from button data-id attribute
     * first ajax call to get swap with offers
     * second ajax call to get data on the offers
     */

    $("#handle-modal").on("show.bs.modal", function (event) {
        const modal = $(this);
        const button = $(event.relatedTarget);
        const shiftRow = button.closest(".shift-row");
        const dateDay = new Date(parseInt(shiftRow.children(".shift-from")[0].dataset.time)).toDateString();
        const shiftId = button.data("id");

        const getSwapDocument = $.ajax({
            /**
             * First call, gets the swap document
             */
            url: `${$SCRIPT_ROOT}/api/swap/${shiftId}`,
            method: "GET",
            dataType: "json",
            success: function(data, textStatus, jqXHR) {
                generateHandleModal(data, textStatus, jqXHR);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                ajaxFailure(jqXHR, textStatus, errorThrown);
            }
        });

        function generateHandleModal(data, textStatus, jqXHR) {
            modal.find(".modal-title").text("Offers for your shift on " + dateDay);
            modal.find(".modal-body").html(`
                <table class="table table-sm">
                    <thead class="thead-light">
                        <tr>
                            <th>From</th>
                            <th>To</th>
                            <th>Duration</th>
                            <th>Handling</th>
                        </tr>
                    </thead>
                    <tbody class="modal-tbody">
                    </tbody>
                </table>`);

            /**
             * Build a list of shiftIds to query for, from shiftIds in swap document
             */
            const offerList = data.offer;
            const acceptList = data.accept;
            const rejectList = data.reject;
            const requestShiftsList = {"ids": data.offer.concat(data.accept).concat(data.reject)};

            const requestShifts = $.ajax({
                /**
                 * Query for information on offered shifts
                 */
                url: `${$SCRIPT_ROOT}/api/shifts/`,
                method: "POST",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(requestShiftsList),
                success: function (data, textStatus, jqXHR) {
                    populateHandleModalTable(data);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown);
                }
            });

            function populateHandleModalTable(data) {
                /**
                 * Populate table with offered shifts information
                 *
                 * @param array of objects from requestShifts ajax call
                 */
                for (let offer of data) {
                    $(".modal-tbody").append(`
                    <tr>
                        <td>${localeString(offer.from)}</td>
                        <td>${localeString(offer.to)}</td>
                        <td>${Math.abs(offer.to - offer.from) / 3.6e6} hours</td>
                        <td>
                            <button class="btn btn-block btn-outline-success offer-accept offer-handle" data-id="${offer.shiftId}">
                                    Accept
                            </button>
                            <button class="btn btn-block btn-outline-danger offer-reject offer-handle" data-id="${offer.shiftId}">
                                    Reject
                            </button>
                        </td>
                    </tr>
                    `);
                }

                for (let shift of acceptList) {
                    $(`button.offer-accept[data-id=${shift}]`)
                        .removeClass("btn-outline-success")
                        .addClass("btn-success")
                        .text("Accepted")
                        .prop("disabled", true);
                }
                for (let shift of rejectList) {
                    $(`button.offer-reject[data-id=${shift}]`)
                        .removeClass("btn-outline-danger")
                        .addClass("btn-danger")
                        .text("Rejected")
                        .prop("disabled", true);
                }


                function handleOffer(element) {
                    /**
                     * Add Functionality to accept or reject an offered shift
                     *
                     @param element button of handle modal offered shifts table;
                     *      attribute "data-id" maps to shift,
                     *      css-class "accepted", "rejected" flags status
                     */
                    const mode = element.classList.contains("offer-accept") ? "accept" : "reject";

                    const offerId = element.dataset.id;
                    const acceptRejectOffer = $.ajax({
                        /**
                         * Accept / Reject the offered shift
                         */
                        url: `${$SCRIPT_ROOT}/api/swap/${shiftId}/${mode}/${offerId}`,
                        method: "PATCH",
                        success: function (data, textStatus, jqXHR) {
                            handleOfferSuccess(element, mode);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                           ajaxFailure(jqXHR, textStatus, errorThrown);
                        }
                    });

                    function handleOfferSuccess(element, mode) {
                        if (mode === "accept") {
                            $(`button.offer-reject[data-id=${element.dataset.id}]`)
                                .removeClass("btn-danger")
                                .addClass("btn-outline-danger")
                                .text("Reject")
                                .prop("disabled", false);
                            $(`button.offer-accept[data-id=${element.dataset.id}]`)
                                .removeClass("btn-outline-success")
                                .addClass("btn-success")
                                .text("Accepted")
                                .prop("disabled", true);

                        } else if (mode === "reject") {
                            $(`button.offer-accept[data-id=${element.dataset.id}]`)
                                .removeClass("btn-success")
                                .addClass("btn-outline-success")
                                .text("Accept")
                                .prop("disabled", false);
                            $(`button.offer-reject[data-id=${element.dataset.id}]`)
                                .removeClass("btn-outline-danger")
                                .addClass("btn-danger")
                                .text("Rejected")
                                .prop("disabled", true);
                        }
                    }
                }

                $(".offer-handle").click(function () {
                    handleOffer(this);
                });
            }
        }
    });

    /**
     * Modal for offering shifts on a swap request
     * shiftId acquired from button data-id attribute
     */

    $("#offer-modal").on("show.bs.modal", function (event) {
        const modal = $(this);
        const button = $(event.relatedTarget);
        const requestRow = button.closest(".request-row");
        const dateDay = new Date(parseInt(requestRow.children(".request-from")[0].dataset.time)).toDateString();
        const shiftId = button.data("id");

        const userShiftList = {"ids": []};
        $(".upcoming .swap-toggle").each(function() {
            userShiftList["ids"].push(this.dataset.id);
        });

        const requestShifts = $.ajax({
            /**
             * Request information on shifts of user, to select shifts to offer
             */
                url: `${$SCRIPT_ROOT}/api/shifts/`,
                method: "post",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(userShiftList),
                success: function (data, textStatus, jqXHR) {
                    populateOfferShiftsTable(data);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown);
                }
            });

        function populateOfferShiftsTable(data) {
            modal.find(".modal-title").text("Shifts you can offer in exchange, for shift on " + dateDay);
            modal.find(".modal-body").html(`
                <table class="table table-sm">
                    <thead class="thead-light">
                        <tr>
                            <th>From</th>
                            <th>To</th>
                            <th>Duration</th>
                            <th>Offer shift</th>
                        </tr>
                    </thead>
                    <tbody class="modal-tbody">
                    </tbody>
                </table>`);

            for (let shift of data) {
                $(".modal-tbody").append(`
                    <tr>
                        <td>${localeString(shift.from)}</td>
                        <td>${localeString(shift.to)}</td>
                        <td>${Math.abs(shift.to - shift.from) / 3.6e6} hours</td>
                        <td>
                            <button class="btn btn-block btn-outline-secondary offer-shift" 
                                data-id="${shift.shiftId}">
                                    Offer shift
                            </button>
                        </td>
                    </tr>`);
            }

            const getSwapDocument = $.ajax({
                /**
                 *  Request already offered / rejected / accepted offers
                 */
                url: `${$SCRIPT_ROOT}/api/swap/${shiftId}`,
                method: "GET",
                dataType: "json",
                success: function(data, textStatus, jqXHR) {
                    selectOfferedShifts(data, textStatus, jqXHR);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown);
                }
            });

            function selectOfferedShifts(data) {
                $("button.offer-shift").each(function(i) {
                    if (data.accept.includes(this.dataset.id)) {
                        this.classList.add("offer-accepted", "btn-success");
                        this.classList.remove("btn-outline-secondary", "offer-shift");
                        this.innerText = "Accepted";
                        this.disabled=true;
                    } else if (data.reject.includes(this.dataset.id)) {
                        this.classList.remove("btn-outline-secondary", "offer-shift");
                        this.classList.add("offer-rejected", "btn-danger");
                        this.innerText = "Rejected";
                        this.disabled=true;
                    } else if (data.offer.includes(this.dataset.id)) {
                        this.classList.remove("btn-outline-secondary", "offer-shift");
                        this.classList.add("offer-revoke", "btn-outline-danger");
                        this.innerText = "Revoke Offer";
                    }
                });
            }

            function offerShift(element) {
                const offerId = element.dataset.id;

                const placeOffer = $.ajax({
                    url: `${$SCRIPT_ROOT}/api/swap/${shiftId}/offer/${offerId}`,
                    method: "patch",
                    success: function (data, textStatus, jqXHR) {
                        offerPlacementSuccess();
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        ajaxFailure(jqXHR, textStatus, errorThrown);
                    }
                });

                function offerPlacementSuccess() {
                    if (element.classList.contains("offer-shift")) {
                        element.classList.remove("offer-shift", "btn-outline-secondary");
                        element.classList.add("offer-revoke", "btn-outline-danger");
                        element.innerText = "Revoke Offer";
                    } else {
                        element.classList.remove("offer-revoke", "btn-outline-danger");
                        element.classList.add("offer-shift", "btn-outline-secondary");
                        element.innerText = "Offer shift";
                    }
                }
            }

            $(".offer-shift").click(function () {
                    offerShift(this);
                });
        }
    });

    /**
     * Modal to confirm an accepted offer and therefore execute the request
     */

    $("#confirm-modal").on("show.bs.modal", function (event) {
        const modal = $(this);
        const button = $(event.relatedTarget);
        const requestRow = button.closest(".request-row");
        const dateDay = new Date(parseInt(requestRow.children(".request-from")[0].dataset.time)).toDateString();
        const shiftId = button.data("id");
        const confirmIds = button.data("confirm").replace(/[\[\]']/g, "").split(",");
        const confirmIdList = confirmIds.map(id => id.trim());

        modal.find(".modal-body").html(`
                <table class="table table-sm">
                    <thead class="thead-light">
                        <tr>
                            <th>Transaction</th>
                            <th>From</th>
                            <th>To</th>
                            <th>Duration</th>
                        </tr>
                    </thead>
                    <tbody class="confirm-modal-tbody">
                    </tbody>
                </table>`);

        const shiftList = {"ids": confirmIdList.concat(shiftId)};
        const requestShifts = $.ajax({
                /**
                 * Request information on requested shift and accepted shift, to confirm
                 * offer
                 */
                url: `${$SCRIPT_ROOT}/api/shifts/`,
                method: "post",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(shiftList),
                success: function (data, textStatus, jqXHR) {
                    generateConfirmTable(data);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    ajaxFailure(jqXHR, textStatus, errorThrown);
                }
            });

        function generateConfirmTable(data) {
            /**
             * Generate an "Shift from swap request" vs "accepted shift for swap"
             * table for every accepted swap, to clarify swap before execution
             */
            const requestDocument = data.filter(shift => shift["shiftId"] === shiftId)[0];
            for (let offer_id of confirmIdList) {
                let confirmDocument = data.filter(shift => shift["shiftId"] === offer_id)[0];
                $(".confirm-modal-tbody").append(`
                    <tr>
                        <td>You get</td>
                        <td>${localeString(requestDocument.from)}</td>
                        <td>${localeString(requestDocument.to)}</td>
                        <td>${Math.abs(requestDocument.to - requestDocument.from) / 3.6e6} hours</td>
                    </tr>
                    <tr>
                        <td>You trade in</td>
                        <td>${localeString(confirmDocument.from)}</td>
                        <td>${localeString(confirmDocument.to)}</td>
                        <td>${Math.abs(confirmDocument.to - confirmDocument.from) / 3.6e6} hours</td>
                    </tr>
                    <tr>
                        <td colspan="4">
             
                    <button class="btn btn-block btn-light confirm-offer"
                                data-id="${shiftId}" data-target="${offer_id}">
                                    Confirm swap
                    </button>
                    </td>
                    </tr>`);

                function confirmOffer(element) {
                    const shiftId = element.dataset.id;
                    const confirmId = element.dataset.target;

                    const sendConfirmation = $.ajax({
                        /**
                         * confirm and therefore execute the offer
                         */
                        url: `${$SCRIPT_ROOT}/api/swap/${shiftId}/confirm/${confirmId}`,
                        method: "patch",
                        success: function (data, textStatus, jqXHR) {
                            confirmSuccess();
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            ajaxFailure(jqXHR, textStatus, errorThrown);
                        }
                    });
                }

                function confirmSuccess() {
                    window.location.reload(true);
                }
            }

            $("button.confirm-offer").click(function () {
                    confirmOffer(this);
            });
        }
    });

    $(".modal").on("shown.bs.modal", function () {
        $(".modal").trigger("focus");
    });
});
