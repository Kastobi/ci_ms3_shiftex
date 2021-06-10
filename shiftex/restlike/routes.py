"""
shiftex restlike package - routes module
=====================================

Provides restlike endpoints for shiftex.
"restlike" because most routes need a login,
so no pure REST.

routes:
    SwapsQueriesAPI, login required
    GET -> /api/swaps/<rotation_id> -> list of swap documents by rotation_id

    SwapQueryAPI, login required
    /api/swap/<shift_id> -> GET -> swap document for shift_id
    /api/swap/<shift_id> -> PUT -> create swap document for shift_id, therefore place a swap request
    /api/swap/<shift_id> -> DELETE -> delete swap document for shift_id, therefore revoke the swap request

    SwapHandlingAPI, login required
    /api/swap/<request_id>/<mode>/<offer_id>
        -> PATCH
            -> offer -> offer the offer_id shift in exchange for request_id shift
            -> reject -> reject offered shift
            -> accept -> accept offered shift
            -> confirm -> confirm swap offer_id shift for request_id shift

    ShiftsQueriesAPI, login required
    /api/shifts/ -> POST ->
        request-data: {"_ids": list of shift ids}
        response: list of dicts, containing base data to requested shifts (shiftId, drugstoreId, from, to)

"""

from bson import ObjectId
from flask import request
from flask_login import login_required
from flask_restful import Resource

from shiftex.main import mongo
from shiftex.restlike import api


class SwapsQueriesAPI(Resource):
    @login_required
    def get(self, rotation_id):
        """
        Query swap collection and find swap_requests in the specified rotation

        :param rotation_id: int, rotation identifier in dataset "planId"
        :return:
            error 404: when rotation_id not in swaps collection
            success 200: list of swap documents for rotation_id
        """
        swaps_plan_cursor = list(mongo.db.swaps.find({"planId": int(rotation_id)}))
        if len(swaps_plan_cursor) == 0:
            return {"error": "Not Found"}, 404

        else:
            swaps_plan = []
            for document in swaps_plan_cursor:
                document.pop("_id")
                swaps_plan.append(document)
            return swaps_plan, 200


api.add_resource(SwapsQueriesAPI, "/api/swaps/<rotation_id>", endpoint="swaps_queries")


class SwapQueryAPI(Resource):
    @login_required
    def get(self, shift_id):
        """
        Query swap collection for the swap document of specified shift_id

        :param shift_id: str, shift identifier
        :return:
            error 404: when there is no matching swap request for shiftId
            success 200: swap document for shiftId
        """
        check_swap = mongo.db.swaps.find_one({"shiftId": shift_id})
        if check_swap is None:
            return {"error": "Not Found"}, 404

        else:
            check_swap.pop("_id")
            return check_swap, 200

    @login_required
    def put(self, shift_id):
        """
        Query swap collection and place a swap document for specified shift_id

        :param shift_id: str, shift identifier
        :return:
            error 409: when there is a matching swap request already
            success 201: created swap document for shiftId
        """
        check_swap = mongo.db.swaps.find_one({"shiftId": shift_id})
        if check_swap is not None:
            return {"error": "Already there"}, 409

        else:
            find_shift_cursor = mongo.db.shifts.find_one({"_id": ObjectId(shift_id)})
            query_document = {
                "shiftId": shift_id,
                "drugstoreId": find_shift_cursor["drugstoreId"],
                "planId": find_shift_cursor["planId"],
                "digitsId": find_shift_cursor["digitsId"],
                "offer": [],
                "reject": [],
                "accept": []
            }
            mongo.db.swaps.insert_one(query_document)
            return {"success": "Swap query posted"}, 201

    @login_required
    def delete(self, shift_id):
        """
        Query swap collection and delete the swap document for specified shift_id

        :param shift_id: str, shift identifier
        :return:
            error 404: when there is no matching swap document
            success 204: deleted swap document for shiftId
        """
        check_swap = mongo.db.swaps.find_one({"shiftId": shift_id})
        if check_swap is None:
            return {"error": "Not Found"}, 404

        else:
            mongo.db.swaps.delete_one({"shiftId": shift_id})
            return "", 204


api.add_resource(SwapQueryAPI, "/api/swap/<shift_id>", endpoint="swap_query")


class SwapHandlingAPI(Resource):
    @login_required
    def patch(self, request_id, mode, offer_id):
        """

        :param request_id: str, swap-request-document identifier, matching its shiftId
        :param mode: str, one of [offer, reject, accept, confirm]
        :param offer_id: str, shift identifier for the shift offered/rejected/accepted/confirm
        :return:
            error 409: matching result already found
            success 201: database operation done
        """
        original_swap_document = mongo.db.swaps.find_one({"shiftId": request_id})
        original_shift_document = mongo.db.shifts.find_one({"_id": ObjectId(request_id)})
        offer_shift_document = mongo.db.shifts.find_one({"_id": ObjectId(offer_id)})

        if original_swap_document is None:
            return {"error": "Original shift not found"}, 404
        elif mode not in ["offer", "reject", "accept", "confirm"]:
            return {"error": "Mode not supported"}, 400
        elif offer_shift_document is None:
            return {"error": "Offered shift not found"}, 404

        elif mode == "offer":
            if offer_id in original_swap_document["offer"] or \
                            original_swap_document["reject"] or \
                            original_swap_document["accept"]:
                return {"error": "Offered already"}, 409
            else:
                mongo.db.swaps.find_one_and_update(
                    {"shiftId": request_id},
                    {"$addToSet":
                        {"offer": offer_id}
                     }
                )
                return {"success": "Offer posted"}, 201

        elif mode == "reject":
            if offer_id in original_swap_document[mode]:
                return {"error": "Rejected already"}, 409
            else:
                mongo.db.swaps.find_one_and_update(
                    {"shiftId": request_id},
                    {"$addToSet":
                        {mode: offer_id},
                     "$pull":
                        {"offer": offer_id,
                         "accept": offer_id
                         }
                     }
                )
                return {"success": "Offer rejected"}, 201

        elif mode == "accept":
            if offer_id in original_swap_document[mode]:
                return {"error": "Accepted already"}, 409
            else:
                mongo.db.swaps.find_one_and_update(
                    {"shiftId": request_id},
                    {"$addToSet":
                        {mode: offer_id},
                     "$pull":
                        {"offer": offer_id,
                         "reject": offer_id
                         }
                     }
                )
                return {"success": "Offer accepted"}, 201

        elif mode == "confirm":
            """
            1. swaps drugstore identifiers and data in shift documents
            2. removes shift identifier from updated documents
            3. replaces matching shift documents with new identifiers in shifts collection
            4. removes remaining dead_link identifiers from swaps collection
            """
            original_shift_document["drugstore"], offer_shift_document["drugstore"] =\
                offer_shift_document["drugstore"], original_shift_document["drugstore"]

            original_shift_document["drugstoreId"], offer_shift_document["drugstoreId"] =\
                offer_shift_document["drugstoreId"], original_shift_document["drugstoreId"]

            original_shift_document.pop("_id")
            offer_shift_document.pop("_id")

            object_id_list = [ObjectId(request_id), ObjectId(offer_id)]
            id_list = [request_id, offer_id]

            mongo.db.shifts.delete_many({"_id": {"$in": object_id_list}})
            mongo.db.shifts.insert_many([original_shift_document, offer_shift_document])

            mongo.db.swaps.delete_many({"shiftId": {"$in": id_list}})
            mongo.db.swaps.update_many({}, {"$pull": {
                                                "offer": {"$in": id_list},
                                                "reject": {"$in": id_list},
                                                "accept": {"$in": id_list}
            }})
            return {"success": "Swap confirmed"}, 201

        else:
            return {"error": "Bad request"}, 400


api.add_resource(SwapHandlingAPI, "/api/swap/<request_id>/<mode>/<offer_id>", endpoint="swap_handling")


class ShiftsQueriesAPI(Resource):
    @login_required
    def post(self):
        """
        Returns shift data (shiftId, drugstoreId, from, to) for requested ids

        :return:
            success 200: list of dicts for provided shift_ids
        """
        shift_id_dict = eval(request.data.decode("UTF-8"))
        shift_object_id_list = []
        for object_id_string in shift_id_dict["ids"]:
            shift_object_id_list.append(ObjectId(object_id_string))

        shifts_list = list(mongo.db.shifts.aggregate([
            {"$match": {"_id": {"$in": shift_object_id_list}}},
            {"$project": {
                "_id": 0,
                "shiftId": {
                    "$toString": "$_id"
                },
                "drugstoreId": 1,
                "from": 1,
                "to": 1
            }}
        ]))
        return shifts_list, 200


api.add_resource(ShiftsQueriesAPI, "/api/shifts/", endpoint="shifts_queries")
