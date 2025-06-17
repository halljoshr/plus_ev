from collections import defaultdict
import datetime as dt
from enum import Enum
import json
import random
import uuid
from xml.etree.ElementTree import PI

import aiohttp
import asyncio
from django.db import transaction
from django.db.models import Q, F
import pytz
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# If you see a linter error for 'dotenv', install it with: pip install python-dotenv


from .config import BANKROLL, KELLY_FRACTION
from .models import PlusEV, PlacedBet

from data_dawgs_web.utils import datetime_helpers as dt_help


########################################################################
# Classes
########################################################################
class Sports(Enum):
    BASKETBALL_NBA = "basketball_nba"
    SOCCER_EPL = "soccer_epl"
    BASEBALL_MLB = "baseball_mlb"
    HOCKEY_NHL = "icehockey_nhl"


class BaseballPlayerMarkets(Enum):
    BATTER_TOTAL_BASES = "batter_total_bases"
    BATTER_HITS = "batter_hits"
    BATTER_HOME_RUNS = "batter_home_runs"
    BATTER_RUNS_SCORED = "batter_runs_scored"
    BATTER_HITS_RUNS_RBIS = "batter_hits_runs_rbis"
    BATTER_RBIS = "batter_rbis"
    PITCHER_OUTS = "pitcher_outs"
    PITCHER_STRIKEOUTS = "pitcher_strikeouts"
    PITCHER_EARNED_RUNS = "pitcher_earned_runs"
    # PITCHER_RECORD_A_WIN = "pitcher_record_a_win"
    PITCHER_HITS_ALLOWED = "pitcher_hits_allowed"
    PITCHER_STRIKEOUTS_ALT = "pitcher_strikeouts_alternate"


class BaseMarkets(Enum):
    H2H = "h2h"
    SPREADS = "spreads"
    TOTALS = "totals"
    # OUTRIGHTS = "outrights"
    ALT_SPREADS = "alternate_spreads"
    ALT_TOTALS = "alternate_totals"
    # TEAM_TOTALS = "team_totals"
    # ALT_TEAM_TOTALS = "alternate_team_totals"


class BaseballPeriodMarkets(Enum):
    H2H_FIRST_1_INNINGS = "h2h_1st_1_innings"
    H2H_FIRST_3_INNINGS = "h2h_1st_3_innings"
    H2H_FIRST_5_INNINGS = "h2h_1st_5_innings"
    H2H_FIRST_7_INNINGS = "h2h_1st_7_innings"
    # H2H_3WAY_FIRST_1_INNINGS = "h2h_3_way_1st_1_innings"
    # H2H_3WAY_FIRST_3_INNINGS = "h2h_3_way_1st_3_innings"
    # H2H_3WAY_FIRST_5_INNINGS = "h2h_3_way_1st_5_innings"
    # H2H_3WAY_FIRST_7_INNINGS = "h2h_3_way_1st_7_innings"
    SPREADS_FIRST_1_INNINGS = "spreads_1st_1_innings"
    SPREADS_FIRST_3_INNINGS = "spreads_1st_3_innings"
    SPREADS_FIRST_5_INNINGS = "spreads_1st_5_innings"
    SPREADS_FIRST_7_INNINGS = "spreads_1st_7_innings"
    TOTALS_FIRST_1_INNINGS = "totals_1st_1_innings"
    TOTALS_FIRST_3_INNINGS = "totals_1st_3_innings"
    TOTALS_FIRST_5_INNINGS = "totals_1st_5_innings"
    TOTALS_FIRST_7_INNINGS = "totals_1st_7_innings"


class BasketballPlayerMarkets(Enum):
    PLAYER_POINTS = "player_points"
    PLAYER_ASSISTS = "player_assists"
    PLAYER_REBOUNDS = "player_rebounds"
    PLAYER_THREES = "player_threes"
    PLAYER_BLOCKS = "player_blocks"
    PLAYER_STEALS = "player_steals"
    PLAYER_POINTS_REBOUNDS_ASSISTS = "player_points_rebounds_assists"
    PLAYER_POINTS_ASSISTS = "player_points_assists"
    PLAYER_POINTS_REBOUNDS = "player_points_rebounds"


# class SoccerPlayerMarkets(Enum):
#     PLAYER_GOALS = "player_goals"
#     PLAYER_ASSISTS = "player_assists"


class HockeyPlayerMarkets(Enum):
    PLAYER_POINTS = "player_points"
    PLAYER_GOALS = "player_goals"
    PLAYER_ASSISTS = "player_assists"
    PLAYER_TOTAL_SAVES = "player_total_saves"


class Bookmakers(Enum):
    BETMGM = "betmgm"
    BETRIVERS = "betrivers"
    DRAFTKINGS = "draftkings"
    FANDUEL = "fanduel"
    CAESARS = "williamhill_us"
    ESPNBET = "espnbet"
    TIPICO = "tipico_us"
    BETFRED = "windcreek"
    SUPERBOOK = "superbook"
    HARDROCKBET = "hardrockbet"
    BETPARX = "betparx"
    BOVADA = "bovada"
    PINNACLE = "pinnacle"


########################################################################
# API HELPERS
########################################################################
def create_events_string(sport) -> str:

    time_format = "%Y-%m-%dT%H:%M:%SZ"
    paid_api_key = os.environ["PAID_API_KEY"]
    # sport = "basketball_nba"
    base_url = "https://api.the-odds-api.com/"

    today = dt.datetime.today().date()

    # Create a datetime object for today at 12:00 PM
    noon_today = dt.datetime.combine(today, dt.datetime.min.time()) + dt.timedelta(
        hours=12
    )

    # start_time_str = dt_help.convert_est_to_gmt_str(
    #     dt.datetime.now().strftime(time_format)
    # )
    start_time_str = dt.datetime.now().strftime(time_format)
    # get end time str
    end_time_str = dt_help.convert_est_to_gmt_str(
        (noon_today + dt.timedelta(days=1)).strftime(time_format)
    )

    return (
        base_url
        + f"v4/sports/{sport}/events?apiKey={paid_api_key}&commenceTimeFrom={start_time_str}&commenceTimeTo={end_time_str}"
    )


def create_event_details_string(event) -> str:

    event_id = event["id"]
    sport = event["sport_key"]
    paid_api_key = os.environ["PAID_API_KEY"]
    # sport = "basketball_nba"
    # book_makers = "betmgm,betrivers,bovada,draftkings,fanduel,pinnacle"
    book_makers = "betmgm,betrivers,williamhill_us,draftkings,fanduel,espnbet,tipico_us,windcreek,superbook,hardrockbet,betparx,bovada,pinnacle"
    base_url = "https://api.the-odds-api.com/"

    if sport == "basketball_nba":
        # markets = "player_points,player_assists"
        markets = ",".join([market.value for market in BasketballPlayerMarkets])
    elif sport == "baseball_mlb":
        # markets = "batter_total_bases,pitcher_strikeouts"
        market_list = [market.value for market in BaseballPlayerMarkets] + [
            market.value for market in BaseballPeriodMarkets
        ]
        markets = ",".join([market for market in market_list])
        # markets = ",".join([market.value for market in BaseballPeriodMarkets])
    elif sport == "icehockey_nhl":
        markets = ",".join([market.value for market in HockeyPlayerMarkets])

    base_markets = ",".join([market.value for market in BaseMarkets])

    markets = markets + "," + base_markets

    return (
        base_url
        + f"v4/sports/{sport}/events/{event_id}/odds?apiKey={paid_api_key}&bookmakers={book_makers}&markets={markets}"
    )


########################################################################
# +EV HELPERS
########################################################################


def remove_vig_and_calculate_probabilities(decimal_odds):

    if 0 in decimal_odds:
        return None, None
    # Convert decimal odds to implied probabilities
    probabilities = [1 / odds for odds in decimal_odds]

    # Calculate the overround
    overround = sum(probabilities)

    # Remove the vig by scaling down the probabilities
    no_vig_probabilities = [prob / overround for prob in probabilities]

    # Convert back to no-vig decimal odds
    no_vig_odds = [1 / prob for prob in no_vig_probabilities]

    return no_vig_odds, no_vig_probabilities


# def handle_straight_bets(straights_df):
#     straights_df["abs_point"] = straights_df["point"].abs()
#     straights_df["match_key"] = straights_df["abs_point"].astype(str)
#     matched_df = straights_df.merge(straights_df, on=["match_key", "bookmaker"])

#     matched_df = matched_df[
#         (matched_df["point_x"] == -matched_df["point_y"])
#         & (matched_df["description_x"] != matched_df["description_y"])
#     ]
#     our_table = matched_df.pivot_table(
#         index=["description_x", "point_x"], columns="bookmaker", values="price_x"
#     )
#     our_table.dropna(thresh=3, inplace=True)
#     our_table["average"] = our_table.mean(axis=1).round(2)

#     return our_table


def handle_straight_bets(straights_df):
    straights_df["abs_point"] = straights_df["point"].abs()
    straights_df["match_key"] = straights_df["abs_point"].astype(str)
    matched_df = straights_df.merge(straights_df, on=["match_key", "bookmaker"])

    matched_df = matched_df[
        (matched_df["point_x"] == -matched_df["point_y"])
        & (matched_df["description_x"] != matched_df["description_y"])
    ]

    # print(matched_df, "MATCHED DF")

    our_table = matched_df.pivot_table(
        index=["description_x", "point_x", "market_x"],
        columns="bookmaker",
        values="price_x",
    )
    our_table.dropna(thresh=3, inplace=True)
    our_table["average"] = our_table.mean(axis=1).round(2)

    return our_table


def kelly_bet(bankroll, odds, probability_win, kelly_fraction=1.0):
    """
    Calculate the bet size using the Kelly Criterion.

    Parameters:
    - bankroll (float): The total amount of money available for betting.
    - odds (float): The total payout on the bet per unit staked (including the stake).
    - probability_win (float): The probability of winning the bet.
    - kelly_fraction (float): The fraction of the Kelly bet to actually bet (defaults to 1.0 for full Kelly).

    Returns:
    - float: The amount of money to bet according to the adjusted Kelly Criterion.
    """
    # The multiplier (b) is the net odds received on the wager, which is odds - 1 (since odds include the stake)
    b = odds - 1

    if b <= 0:
        print("Invalid odds value. Please provide a positive value.")
        return 0
    # Probability of losing
    q = 1 - probability_win
    # Calculate the full Kelly fraction
    full_kelly = (b * probability_win - q) / b
    # Adjust the Kelly fraction if needed
    bet_size = bankroll * full_kelly * kelly_fraction
    return max(round(bet_size, 0), 0)  # Ensure the bet size is not negative


def find_other_option(row):
    if row["description"] == "Over":
        return "Under"
    elif row["description"] == "Under":
        return "Over"
    elif row["description"] == row["team_1"]:
        return row["team_2"]
    elif row["description"] == row["team_2"]:
        return row["team_1"]


def find_favorite(row):
    if "spreads" in row["market"]:
        if row["point"] < 0:
            return row["description"]
        else:
            return row.other_team
    else:
        return "Under"


def create_event_dataframe(event_data):
    event_df = pd.DataFrame()
    straights_df = pd.DataFrame()
    props_df = pd.DataFrame()
    for bookmaker in event_data["bookmakers"]:
        for market in bookmaker["markets"]:
            prop_df = pd.DataFrame()
            straight_df = pd.DataFrame()
            for outcome in market["outcomes"]:
                # print(market, outcome)

                event_str = (
                    str(event_data["away_team"])
                    + " vs "
                    + str(event_data["home_team"]),
                )
                # TODO Need to add all of the possible period markets

                if market["key"] in [market.value for market in BaseMarkets] + [
                    market.value for market in BaseballPeriodMarkets
                ]:
                    straight_df = pd.concat(
                        [
                            straight_df,
                            pd.DataFrame(
                                {
                                    "sport_title": event_data["sport_title"],
                                    "event": event_str,
                                    "date": dt_help.convert_gmt_to_est(
                                        event_data["commence_time"]
                                    ),
                                    "bookmaker": bookmaker["key"],
                                    "market": market["key"],
                                    "outcome": outcome["name"],
                                    "description": outcome["name"],
                                    "price": outcome["price"],
                                    "point": outcome.get("point", 0),
                                },
                                index=[0],
                            ),
                        ],
                        axis=0,
                    )
                else:

                    prop_df = pd.concat(
                        [
                            prop_df,
                            pd.DataFrame(
                                {
                                    "sport_title": event_data["sport_title"],
                                    "event": event_str,
                                    # "date": dt_help.convert_gmt_to_est(
                                    #     event_data["commence_time"]
                                    # ),
                                    "date": dt_help.convert_gmt_to_est(
                                        event_data["commence_time"]
                                    ),
                                    "bookmaker": bookmaker["key"],
                                    "market": market["key"],
                                    "outcome": outcome["name"],
                                    "description": outcome.get(
                                        "description", event_str
                                    ),
                                    # "description": outcome["description"],
                                    "price": outcome["price"],
                                    "point": outcome.get("point", 0),
                                    # "point": outcome["point"],
                                },
                                index=[0],
                            ),
                        ],
                        axis=0,
                    )

            props_df = pd.concat([props_df, prop_df], axis=0)
            straights_df = pd.concat([straights_df, straight_df], axis=0)

    return props_df, straights_df


def find_positive_ev_opportunities(pivot_df, tmp):
    # Loop over the pivot_df and calculate the average column for each description
    # point outcome paired on point
    final_df = pd.DataFrame()
    averages = {}
    for _, row in tmp.iterrows():
        description = row["description"]
        point = row["point"]
        outcome = row["outcome"]
        average = row["average"]
        market = row["market"]

        key = (description, point, market)
        if key not in averages:
            averages[key] = {}

        averages[key][outcome] = average

    for key, value in averages.items():
        description, point, market = key
        dec_odds = [0, 0]
        for outcome, average in value.items():
            if outcome == "Over":
                dec_odds[0] = average
                side1 = "Over"
            elif outcome == "Under":
                dec_odds[1] = average
                side2 = "Under"
            elif len(value) == 2:
                if sorted(value.keys())[0] == outcome:
                    dec_odds[0] = average
                    side1 = sorted(value.keys())[0]
                elif sorted(value.keys())[1] == outcome:
                    dec_odds[1] = average
                    side2 = sorted(value.keys())[1]
                # print(outcome, average)

        _, no_vig_probabilities = remove_vig_and_calculate_probabilities(dec_odds)

        if no_vig_probabilities is None:
            continue

        over_evs = no_vig_probabilities[0] * (
            pivot_df.loc[(description, side1, point, market)] - 1
        ) - (1 - no_vig_probabilities[0])

        under_evs = no_vig_probabilities[1] * (
            pivot_df.loc[(description, side2, point, market)] - 1
        ) - (1 - no_vig_probabilities[1])

        over_ev_df = pd.Series(over_evs).to_frame().T
        under_ev_df = pd.Series(under_evs).to_frame().T

        over_ev_df["win_prob"] = no_vig_probabilities[0]
        under_ev_df["win_prob"] = no_vig_probabilities[1]

        final_df = pd.concat([final_df, over_ev_df, under_ev_df], axis=0)

    return final_df, pivot_df


def find_positive_ev_opportunities_straights(our_table, tmp):
    final_df = pd.DataFrame()
    for _, row in tmp.iterrows():
        point = row["point_x"]
        name = row["description_x"]
        market = row["market_x"]
        other_row = tmp.loc[
            (tmp.point_x == -point)
            & (tmp.description_x != name)
            & (tmp.market_x == market)
        ]
        # print(other_row)
        if other_row.empty:
            continue
        avg = row["average"]
        other_avg = other_row["average"].values[0]
        other_name = other_row["description_x"].values[0]
        other_point = other_row["point_x"].values[0]
        _, no_vig_probabilities = remove_vig_and_calculate_probabilities(
            [avg, other_avg]
        )

        if no_vig_probabilities is None:
            # print(f"Skipping {description} {point} {market}")
            # print(dec_odds)
            # print(key, value)
            continue

        over_evs = no_vig_probabilities[0] * (
            our_table.loc[(name, point, market)] - 1
        ) - (1 - no_vig_probabilities[0])

        under_evs = no_vig_probabilities[1] * (
            our_table.loc[(other_name, other_point, market)] - 1
        ) - (1 - no_vig_probabilities[1])

        over_ev_df = pd.Series(over_evs).to_frame().T
        under_ev_df = pd.Series(under_evs).to_frame().T

        over_ev_df["win_prob"] = no_vig_probabilities[0]
        under_ev_df["win_prob"] = no_vig_probabilities[1]

        final_df = pd.concat([final_df, over_ev_df, under_ev_df], axis=0)

    final_df.drop_duplicates(inplace=True)

    return final_df, our_table


def process_event_details(event_details):
    props_df, straights_df = create_event_dataframe(event_details)

    if props_df.empty and straights_df.empty:
        return (None, None, None), (None, None, None)

    # print(props_df)

    # print(props_df.columns)

    try:
        props_holder_df = props_df[
            [
                "description",
                "outcome",
                "point",
                "market",
                "sport_title",
                "date",
                "event",
            ]
        ]

        props_pivot_df = props_df.pivot_table(
            index=["description", "outcome", "point", "market"],
            columns="bookmaker",
            values="price",
        )

        props_pivot_df["average"] = props_pivot_df.mean(axis=1).round(2)

        tmp = props_pivot_df.reset_index()

        tmp.dropna(thresh=3, inplace=True)

        final_props_df, props_pivot_df = find_positive_ev_opportunities(
            props_pivot_df, tmp
        )
    except Exception as e:
        print(e)
        props_holder_df = pd.DataFrame()
        final_props_df, props_pivot_df = pd.DataFrame(), pd.DataFrame()

    straights_holder_df = straights_df[
        ["description", "outcome", "point", "market", "sport_title", "date", "event"]
    ]

    # This is where we handle the straight bets
    if not straights_df.empty:
        our_table = handle_straight_bets(straights_df)
        # print(our_table)
        final_straight_df, straights_pivot_df = (
            find_positive_ev_opportunities_straights(our_table, our_table.reset_index())
        )

    return (
        (final_props_df, props_pivot_df, props_holder_df),
        (final_straight_df, straights_pivot_df, straights_holder_df),
    )


def create_final_ev_response(event_details, **kwargs):
    final_df = pd.DataFrame()
    final_odds_df = pd.DataFrame()
    final_holder_df = pd.DataFrame()

    final_df_s = pd.DataFrame()
    final_odds_df_s = pd.DataFrame()
    final_holder_df_s = pd.DataFrame()

    # This might change because it might already be a list of tuples!
    for (df, odds_df, holder_df), (df_s, odds_df_s, holder_df_s) in event_details:
        if holder_df is None:
            continue
        final_df = pd.concat([final_df, df], axis=0)
        final_odds_df = pd.concat([final_odds_df, odds_df], axis=0)
        final_holder_df = pd.concat([final_holder_df, holder_df], axis=0)

        final_df_s = pd.concat([final_df_s, df_s], axis=0)
        final_odds_df_s = pd.concat([final_odds_df_s, odds_df_s], axis=0)
        final_holder_df_s = pd.concat([final_holder_df_s, holder_df_s], axis=0)

    # Props section!
    final_df.dropna(thresh=3, inplace=True)
    final_df.index.set_names(final_odds_df.index.names, inplace=True)

    ev_odds_df = pd.merge(
        final_df,
        final_odds_df,
        left_index=True,
        right_index=True,
        suffixes=("_ev", "_odds"),
    )

    ev_odds_df.reset_index(inplace=True)

    output_df = pd.merge(
        ev_odds_df,
        final_holder_df,
        on=["description", "outcome", "point", "market"],
        how="left",
    )

    output_df.drop_duplicates(
        subset=["description", "outcome", "point", "market"], inplace=True, keep="first"
    )

    grouped = output_df.groupby(["description", "market", "point"])

    group_indices_to_uuids = {
        idx: str(uuid.uuid4()) for idx in grouped.ngroup().unique()
    }

    # Assign pair IDs using the mapping
    output_df["pair_id"] = grouped.ngroup().map(group_indices_to_uuids)

    output_df.columns = output_df.columns.str.lower()

    # spreads and straights section!
    final_df_s.dropna(thresh=3, inplace=True)
    final_df_s.index.set_names(final_odds_df_s.index.names, inplace=True)

    ev_odds_df_s = pd.merge(
        final_df_s,
        final_odds_df_s,
        left_index=True,
        right_index=True,
        suffixes=("_ev", "_odds"),
    )

    ev_odds_df_s.reset_index(inplace=True)

    output_df_s = pd.merge(
        ev_odds_df_s,
        final_holder_df_s,
        left_on=["description_x", "description_x", "point_x", "market_x"],
        right_on=["description", "outcome", "point", "market"],
        how="left",
    )

    output_df_s.drop_duplicates(
        subset=["description_x", "point", "market"], inplace=True, keep="first"
    )

    output_df_s[["team_1", "team_2"]] = output_df_s["event"].str.split(
        " vs ", expand=True
    )

    # Find the other team that is not listed in the description column
    output_df_s["other_team"] = output_df_s.apply(
        lambda row: (
            # row["team_1"] if row["team_1"] != row["description"] else row["team_2"]
            find_other_option(row)
        ),
        axis=1,
    )

    # output_df_s["favorite"] = output_df_s.apply(
    #     lambda x: x.description if x.point < 0 else x.other_team, axis=1
    # )

    output_df_s["favorite"] = output_df_s.apply(lambda x: find_favorite(x), axis=1)

    output_df_s["norm_point"] = output_df_s["point"].abs()

    output_df_s["pair_key"] = (
        output_df_s["event"]
        + "|"
        + output_df_s["favorite"]
        + "|"
        + output_df_s["norm_point"].astype(str)
        + "|"
        + output_df_s["market"]
    )

    unique_keys = output_df_s["pair_key"].unique()
    pair_id_map = {key: str(uuid.uuid4()) for key in unique_keys}
    output_df_s["pair_id"] = output_df_s["pair_key"].map(pair_id_map)

    output_df_s.columns = output_df_s.columns.str.lower()

    # return output_df_s

    # return pd.concat([output_df, output_df_s[output_df.columns]], axis=0)

    final_output_df = pd.concat([output_df, output_df_s[output_df.columns]], axis=0)

    p_keys = create_n_save_plus_ev_objects(
        final_output_df.round(4).to_dict(orient="records")
    )

    final_output_df["p_key"] = p_keys

    final_output_df = filter_placed_bets(final_output_df)

    return prep_data_for_display(final_output_df, **kwargs)


def create_final_ev_response(event_details, **kwargs):
    final_df = pd.DataFrame()
    final_odds_df = pd.DataFrame()
    final_holder_df = pd.DataFrame()

    final_df_s = pd.DataFrame()
    final_odds_df_s = pd.DataFrame()
    final_holder_df_s = pd.DataFrame()

    # This might change because it might already be a list of tuples!
    for (df, odds_df, holder_df), (df_s, odds_df_s, holder_df_s) in event_details:
        if holder_df is None:
            continue
        final_df = pd.concat([final_df, df], axis=0)
        final_odds_df = pd.concat([final_odds_df, odds_df], axis=0)
        final_holder_df = pd.concat([final_holder_df, holder_df], axis=0)

        final_df_s = pd.concat([final_df_s, df_s], axis=0)
        final_odds_df_s = pd.concat([final_odds_df_s, odds_df_s], axis=0)
        final_holder_df_s = pd.concat([final_holder_df_s, holder_df_s], axis=0)

    # Props section!
    final_df.dropna(thresh=3, inplace=True)
    final_df.index.set_names(final_odds_df.index.names, inplace=True)

    ev_odds_df = pd.merge(
        final_df,
        final_odds_df,
        left_index=True,
        right_index=True,
        suffixes=("_ev", "_odds"),
    )

    ev_odds_df.reset_index(inplace=True)

    output_df = pd.merge(
        ev_odds_df,
        final_holder_df,
        on=["description", "outcome", "point", "market"],
        how="left",
    )

    output_df.drop_duplicates(
        subset=["description", "outcome", "point", "market"], inplace=True, keep="first"
    )

    grouped = output_df.groupby(["description", "market", "point"])

    group_indices_to_uuids = {
        idx: str(uuid.uuid4()) for idx in grouped.ngroup().unique()
    }

    # Assign pair IDs using the mapping
    output_df["pair_id"] = grouped.ngroup().map(group_indices_to_uuids)

    output_df.columns = output_df.columns.str.lower()

    # spreads and straights section!
    final_df_s.dropna(thresh=3, inplace=True)
    final_df_s.index.set_names(final_odds_df_s.index.names, inplace=True)

    ev_odds_df_s = pd.merge(
        final_df_s,
        final_odds_df_s,
        left_index=True,
        right_index=True,
        suffixes=("_ev", "_odds"),
    )

    ev_odds_df_s.reset_index(inplace=True)

    # print(ev_odds_df_s, "EV_ODDS")
    # print(final_holder_df_s, "HOLDER")

    output_df_s = pd.merge(
        ev_odds_df_s,
        final_holder_df_s,
        left_on=["description_x", "description_x", "point_x", "market_x"],
        right_on=["description", "outcome", "point", "market"],
        how="left",
    )

    output_df_s.drop_duplicates(
        subset=["description_x", "point", "market"], inplace=True, keep="first"
    )

    output_df_s[["team_1", "team_2"]] = output_df_s["event"].str.split(
        " vs ", expand=True
    )

    # Find the other team that is not listed in the description column
    output_df_s["other_team"] = output_df_s.apply(
        lambda row: (
            # row["team_1"] if row["team_1"] != row["description"] else row["team_2"]
            find_other_option(row)
        ),
        axis=1,
    )

    # output_df_s["favorite"] = output_df_s.apply(
    #     lambda x: x.description if x.point < 0 else x.other_team, axis=1
    # )

    output_df_s["favorite"] = output_df_s.apply(lambda x: find_favorite(x), axis=1)

    output_df_s["norm_point"] = output_df_s["point"].abs()

    output_df_s["pair_key"] = (
        output_df_s["event"]
        + "|"
        + output_df_s["favorite"]
        + "|"
        + output_df_s["norm_point"].astype(str)
        + "|"
        + output_df_s["market"]
    )

    unique_keys = output_df_s["pair_key"].unique()
    pair_id_map = {key: str(uuid.uuid4()) for key in unique_keys}
    output_df_s["pair_id"] = output_df_s["pair_key"].map(pair_id_map)

    output_df_s.columns = output_df_s.columns.str.lower()

    # return output_df_s

    # return pd.concat([output_df, output_df_s[output_df.columns]], axis=0)

    final_output_df = pd.concat([output_df, output_df_s[output_df.columns]], axis=0)

    p_keys = create_n_save_plus_ev_objects(
        final_output_df.round(4).to_dict(orient="records")
    )

    final_output_df["p_key"] = p_keys

    final_output_df = filter_placed_bets(final_output_df)

    return prep_data_for_display(final_output_df, **kwargs)


def filter_placed_bets(output_df):
    utc = pytz.UTC
    # Ensure the date in the DataFrame is in UTC
    output_df["date"] = pd.to_datetime(output_df["date"]).dt.tz_convert(utc)

    # Create unique bets tuple from DataFrame
    unique_bets = output_df[
        ["market", "description", "point", "date"]
    ].drop_duplicates()

    # Create a compound query for all unique bets
    query = Q()
    for _, bet in unique_bets.iterrows():
        query |= Q(
            plus_ev__market=bet["market"],
            plus_ev__description=bet["description"],
            plus_ev__point=bet["point"],
            plus_ev__date=bet["date"],
        )

    # Query the database
    matched_bets = (
        PlacedBet.objects.filter(query)
        .annotate(
            market=F("plus_ev__market"),
            description=F("plus_ev__description"),
            point=F("plus_ev__point"),
            date=F("plus_ev__date"),
        )
        .values_list("market", "description", "point", "date")
    )

    matched_bets_set = set(matched_bets)

    # Filtering DataFrame
    def bet_in_placed_bets(row):
        return (
            row["market"],
            row["description"],
            float(row["point"]),
            row["date"],
        ) in matched_bets_set

    return output_df[~output_df.apply(bet_in_placed_bets, axis=1)]


def prep_data_for_display(posts_df=None, filtered=True, **kwargs):

    print(kwargs)
    paired_bets = defaultdict(list)
    if posts_df is None:
        # This part is for testing purposes!
        posts = PlusEV.objects.all().values()
        for post in posts:
            if "pair_id" in post and isinstance(post["pair_id"], uuid.UUID):
                post["pair_id"] = str(post["pair_id"])

            paired_bets[post["pair_id"]].append(post)
        posts_df = pd.DataFrame(posts)

    posts_df = set_best_ev_opportunity(posts_df)

    # if filtered:
    #     # TODO in theory this is where we would add the filter logic!
    #     columns_subset = [x for x in posts_df.columns if x.endswith("_ev")]
    #     filter_condition = posts_df[columns_subset].gt(0).any(axis=1)
    #     posts_df = posts_df.groupby("pair_id").filter(
    #         lambda group: filter_condition[group.index].any()
    #     )

    if filtered:
        # Existing filter for positive expected value
        columns_subset = [x for x in posts_df.columns if x.endswith("_ev")]
        ev_condition = posts_df[columns_subset].gt(0).any(axis=1)

        # Create a boolean DataFrame where True indicates non-NaN values
        non_nan_condition = posts_df[columns_subset].notna()

        # Sum these True values row-wise and check if at least three are non-NaN
        at_least_x_non_nan = non_nan_condition.sum(axis=1) >= 2

        max_odds = kwargs.get("max_odds", None)
        bookmakers = kwargs.get("bookmakers", None)

        print("MAX ODDS: ", max_odds)

        # New filter for maximum odds
        if max_odds is not None:
            max_odds = float(max_odds)
            odds_condition = posts_df["average_odds"] < max_odds
        else:
            odds_condition = pd.Series(
                [True] * len(posts_df), index=posts_df.index
            )  # No odds filter if max_odds is not specified

        # New filter for bookmaker selection
        if bookmakers is not None:
            bookmakers = [x + "_ev" for x, y in bookmakers.items() if y]
            # Ensure that bookmakers is a list, in case a single bookmaker is accidentally passed as a string
            if isinstance(bookmakers, str):
                bookmakers = [bookmakers]

            # Filter for rows where the best bookmaker is in the provided list of bookmakers
            bookmaker_condition = posts_df["best_ev_bookmaker"].isin(bookmakers)
        else:
            bookmaker_condition = pd.Series(
                [True] * len(posts_df), index=posts_df.index
            )  # No bookmaker filter if none are specified

        # Combine conditions with logical AND
        combined_condition = (
            ev_condition & odds_condition & bookmaker_condition & at_least_x_non_nan
        )

        # Combine conditions with logical AND
        # combined_condition = ev_condition & odds_condition

        # Filter the DataFrame based on combined conditions
        # posts_df = posts_df[combined_condition]

        posts_df = posts_df.groupby("pair_id").filter(
            lambda group: combined_condition[group.index].any()
        )

    # print(kwargs["bankroll"], kwargs["kelly_fraction"])
    bankroll = kwargs.get("bankroll", BANKROLL)
    kelly_fraction = kwargs.get("kelly_fraction", KELLY_FRACTION)

    posts_df["bet_amount"] = posts_df.apply(
        lambda row: kelly_bet(
            float(bankroll), row["best_ev_odds"], row["win_prob"], float(kelly_fraction)
        ),
        axis=1,
    )

    posts_df.fillna(value="null", inplace=True)
    # posts_df.fillna(value="null", inplace=True)

    if "date" in posts_df.columns:
        posts_df["date"] = posts_df["date"].astype(str)

    # if "date" in posts_df.columns:
    #     posts_df["date"] = posts_df["date"].astype(str)

    grouped_bets = posts_df.round(4).groupby("pair_id")
    # grouped_bets = posts_df.round(4).groupby("pair_id")

    paired_bets_list = [
        {"pair_id": str(pair_id), "bets": group.to_dict(orient="records")}
        for pair_id, group in grouped_bets
    ]

    return json.dumps(paired_bets_list)


def set_best_ev_opportunity(df):
    # Define the columns to use for computing best EV
    ev_columns = [
        "betmgm_ev",
        "betrivers_ev",
        "bovada_ev",
        "draftkings_ev",
        "espnbet_ev",
        "fanduel_ev",
        "williamhill_us_ev",
        "windcreek_ev",
        "superbook_ev",
        "hardrockbet_ev",
        "betparx_ev",
        "pinnacle_ev",
        "tipico_us_ev",
    ]

    # Filter out the columns that actually exist in the DataFrame
    existing_ev_columns = [col for col in ev_columns if col in df.columns]

    # Check if there are any valid EV columns available
    if existing_ev_columns:
        df["best_ev"] = df[existing_ev_columns].max(axis=1)
        df["best_ev_bookmaker"] = df[existing_ev_columns].idxmax(axis=1)
    else:
        df["best_ev"] = None
        df["best_ev_bookmaker"] = None

    # Map the bookmaker EV column names to their corresponding odds column names
    odds_column_map = {
        "betmgm_ev": "betmgm_odds",
        "draftkings_ev": "draftkings_odds",
        "fanduel_ev": "fanduel_odds",
        "betrivers_ev": "betrivers_odds",
        "bovada_ev": "bovada_odds",
        "pinnacle_ev": "pinnacle_odds",
        "espnbet_ev": "espnbet_odds",
        "hardrockbet_ev": "hardrockbet_odds",
        "williamhill_us_ev": "williamhill_us_odds",
        "windcreek_ev": "windcreek_odds",
        "superbook_ev": "superbook_odds",
        "betparx_ev": "betparx_odds",
        "tipico_us_ev": "tipico_us_odds",
    }

    # Ensure best_ev_bookmaker is not None before mapping to odds
    df["best_ev_odds"] = df.apply(
        lambda row: (
            row[odds_column_map[row["best_ev_bookmaker"]]]
            if row["best_ev_bookmaker"] in odds_column_map
            else None
        ),
        axis=1,
    )

    return df


########################################################################
# DATABASE HELPERS
########################################################################
def create_n_save_plus_ev_objects(final_ev_response):
    plus_ev_objects = []

    for event in final_ev_response:
        plus_ev_objects.append(
            PlusEV(
                pair_id=event.get("pair_id"),
                sport=event.get("sport_title"),
                market=event.get("market"),
                date=(
                    dt.datetime.strptime(event["date"], "%Y-%m-%dT%H:%M:%SZ")
                    if "date" in event
                    else None
                ),
                event=event.get("event"),
                description=event.get("description"),
                outcome=event.get("outcome"),
                point=event.get("point"),
                betmgm_ev=event.get(
                    "betmgm_ev", np.nan
                ),  # Using np.nan as an example default
                draftkings_ev=event.get("draftkings_ev", np.nan),
                fanduel_ev=event.get("fanduel_ev", np.nan),
                betrivers_ev=event.get("betrivers_ev", np.nan),
                bovada_ev=event.get("bovada_ev", np.nan),
                pinnacle_ev=event.get("pinnacle_ev", np.nan),
                average_ev=event.get("average_ev", np.nan),
                betmgm_odds=event.get("betmgm_odds", np.nan),
                draftkings_odds=event.get("draftkings_odds", np.nan),
                fanduel_odds=event.get("fanduel_odds", np.nan),
                betrivers_odds=event.get("betrivers_odds", np.nan),
                bovada_odds=event.get("bovada_odds", np.nan),
                pinnacle_odds=event.get("pinnacle_odds", np.nan),
                average_odds=event.get("average_odds", np.nan),
                win_prob=event.get("win_prob", np.nan),
                williamhill_us_ev=event.get("williamhill_us_ev", np.nan),
                windcreek_ev=event.get("windcreek_ev", np.nan),
                superbook_ev=event.get("superbook_ev", np.nan),
                hardrockbet_ev=event.get("hardrockbet_ev", np.nan),
                betparx_ev=event.get("betparx_ev", np.nan),
                tipico_us_ev=event.get("tipico_us_ev", np.nan),
                espnbet_ev=event.get("espnbet_ev", np.nan),
                williamhill_us_odds=event.get("williamhill_us_odds", np.nan),
                windcreek_odds=event.get("windcreek_odds", np.nan),
                superbook_odds=event.get("superbook_odds", np.nan),
                hardrockbet_odds=event.get("hardrockbet_odds", np.nan),
                betparx_odds=event.get("betparx_odds", np.nan),
                tipico_us_odds=event.get("tipico_us_odds", np.nan),
                espnbet_odds=event.get("espnbet_odds", np.nan),
            )
        )

    with transaction.atomic():  # Ensuring all or nothing is saved
        created_objects = PlusEV.objects.bulk_create(plus_ev_objects)

    # Extracting the primary keys of the newly added objects
    primary_keys = [obj.pk for obj in created_objects]
    print("Primary keys of the newly added objects:", primary_keys)

    return primary_keys  # Return the list of primary keys or the objects themselves if needed

    # PlusEV.objects.bulk_create(plus_ev_objects)

    # return plus_ev_objects


def save_placed_bet(data):

    plus_ev_instance = PlusEV.objects.get(id=data.get("p_key"))
    bet_amount = data["pair"]["bestPositiveEvBet"].get("bet_amount")

    print()
    print("Instance: ")
    print(plus_ev_instance)
    print()
    print(f"Bet Amount: {bet_amount}")

    try:
        new_bet = PlacedBet.objects.create(
            plus_ev=plus_ev_instance, bet_amount=bet_amount
        )

        return new_bet
    except PlusEV.DoesNotExist:
        print("PlusEV instance not found.")
        return None
    except Exception as e:
        print(e)
        return None


########################################################################
# ASYNC HELPERS
########################################################################
async def fetch_events():
    # async with aiohttp.ClientSession() as session:
    #     # Replace 'events_api_url' with the actual URL for the events API
    #     async with session.get(create_events_string()) as response:
    #         events = await response.json()
    #         # Just to test with getting 3 events.
    #         return events[:5]
    #         # return events
    pass


async def fetch_event_details(event):
    async with aiohttp.ClientSession() as session:
        # Replace 'event_details_url' with the actual URL, including the event_id
        async with session.get(create_event_details_string(event)) as response:
            event_details = await response.json()

            return process_event_details(event_details)


async def fetch_events_for_sport(session, sport):
    async with session.get(create_events_string(sport)) as response:
        return await response.json()


async def fetch_all_sports_events(sports):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_events_for_sport(session, sport) for sport in sports]
        results = await asyncio.gather(*tasks)
        # Flatten the list if necessary and slice events as needed
        flat_results = [
            item for sublist in results for item in sublist
        ]  # Adjust as necessary
        return flat_results
