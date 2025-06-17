from collections import defaultdict
import json
import logging
import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


import aiohttp
import asyncio
from asgiref.sync import sync_to_async
import pandas as pd
import numpy as np

from .models import PlusEV
from .utils import (
    create_final_ev_response,
    fetch_events,
    fetch_event_details,
    prep_data_for_display,
    set_best_ev_opportunity,
    fetch_all_sports_events,
    save_placed_bet,
)


logger = logging.getLogger("pev_app")


async def fetch_data(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        data = json.loads(body_unicode)

        print(data)

        sports = ["basketball_nba", "baseball_mlb", "icehockey_nhl"]

        # Fetch the list of events
        # events = await fetch_events()

        events = await fetch_all_sports_events(sports)

        # Create a list of tasks to fetch details for each event
        tasks = [fetch_event_details(event) for event in events]

        # Gather and execute all tasks concurrently
        event_details = await asyncio.gather(*tasks)

        final_response = await sync_to_async(create_final_ev_response)(
            event_details, **data
        )

        return JsonResponse(final_response, safe=False)
        # return JsonResponse({"tmp": 123}, safe=False)


def save_bet(request):
    """
    Steps here

    1. Save the position of the actual bet to info sent to frontend XXX
    2. Create a checkbox that triggers post request XXX
    3. Create a database table to store the bets
    4. Save the bets to the database
    5. Check this db table for bets before sending data to frontend
    6. Build a view where we can look at our bets.

    """
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        data = json.loads(body_unicode)

        print(data)

        new_bet = save_placed_bet(data)

        if new_bet is None:
            return JsonResponse({"status": "failed"}, safe=False)

        return JsonResponse({"status": "success"}, safe=False)


@api_view(["POST"])
def get_posts(request):
    print(request.data)

    paired_bets_json = prep_data_for_display(**request.data)
    # logger.debug(f"Sending data to frontend: {paired_bets_json}")

    return JsonResponse(paired_bets_json, safe=False)

    # return JsonResponse(posts_json, safe=False)
