import os
from json import load
from urllib import response

from click import UsageError
from app.errors.errors import DatabaseError, InvalidUsageError, NotInDatabaseError
from flask import jsonify, current_app

from app.models import (
    AlignmentScores,
    EffectChoice,
    SolutionChoice,
    UserBJourney,
    Conversations,
    Users,
    AlignmentFeed,
)
from app.network_x_tools.network_x_utils import network_x_utils
from app import db


def build_alignment_scores_response(alignment_scores_uuid):
    """
    Deal with database interactions to provide response for GET alignment scores request.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - overall similarity score
    - alignment scores for all values, along with their properties
    - top value and score from the alignment scores
    - user a's first name
    - user b's name
    """

    (alignment, userB_name, userA_name) = (
        db.session.query(AlignmentScores, Conversations.receiver_name, Users.first_name)
        .join(
            UserBJourney,
            UserBJourney.alignment_scores_uuid == AlignmentScores.alignment_scores_uuid,
        )
        .join(
            Conversations,
            Conversations.conversation_uuid == UserBJourney.conversation_uuid,
        )
        .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )

    raw_values_map = get_values_map()
    values_map = {
        raw_value_map["id"]: raw_value_map for raw_value_map in raw_values_map.values()
    }
    alignment_scores = [
        {
            "description": value_map["description"],
            "id": value_id,
            "name": value_map["name"],
            "shortDescription": value_map["shortDescription"],
            "score": get_alignment_value(alignment, value_id),
        }
        for (value_id, value_map) in values_map.items()
    ]
    alignment_scores.sort(key=lambda x: -x["score"])

    response = {
        "overallSimilarityScore": as_percent(alignment.overall_similarity_score),
        "topMatchPercent": alignment.top_match_percent,
        "topMatchValue": alignment.top_match_value,
        "valueAlignment": alignment_scores,
        "userAName": userA_name,
        "userBName": userB_name,
    }

    return response


def get_alignment_value(alignment, value_name):
    """Get the alignment score for the value, as a percentage."""
    return as_percent(getattr(alignment, value_name + "_alignment"))


def as_percent(number):
    """Turn number between 0 and 1 to a percentage."""
    return int(100.0 * number)


def get_values_map():
    """Get a name->description dict for all values."""
    try:
        file = os.path.join(
            os.getcwd(), "app/personal_values/static", "value_descriptions.json"
        )
        with open(file) as f:
            data = load(f)
    except FileNotFoundError:
        return jsonify({"error": "Value descriptions file not found"}), 404
    return data


def build_shared_impacts_response(alignment_scores_uuid):
    """
    Deal with database interactions to provide response for GET shared impacts request.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - the id, shared score, short description, title, image url (if available), and associated
    personal value(s) for each shared impact
    - user a's first name
    - user b's name
    """

    G = current_app.config["G"].copy()
    nx = network_x_utils()

    (alignment_scores, alignment_feed, userB_name, userA_name) = (
        db.session.query(
            AlignmentScores,
            AlignmentFeed,
            Conversations.receiver_name,
            Users.first_name,
        )
        .join(
            UserBJourney,
            UserBJourney.alignment_scores_uuid == AlignmentScores.alignment_scores_uuid,
        )
        .join(
            AlignmentFeed,
            AlignmentFeed.alignment_feed_uuid == UserBJourney.alignment_feed_uuid,
        )
        .join(
            Conversations,
            Conversations.conversation_uuid == UserBJourney.conversation_uuid,
        )
        .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )

    climate_effects_iris = [
        alignment_feed.aligned_effect_1_iri,
        alignment_feed.aligned_effect_2_iri,
        alignment_feed.aligned_effect_3_iri,
    ]

    climate_effects_iris = [
        "webprotege.stanford.edu." + iri for iri in climate_effects_iris
    ]

    climate_effects = effect_details(G, climate_effects_iris, nx)

    response = {
        "climateEffects": climate_effects,
        "userAName": userA_name,
        "userBName": userB_name,
    }

    return response


def effect_details(G, climate_effects_iris, nx):
    """
    Get the full details for each shared climate impact, including id, shared score, description, title, image (if available), and
    associated personal values.

    Note - shared scores are currently hard-coded as a placeholder until implementation is decided.
    """

    climate_effects = []

    # TODO: implement shared scores
    for iri in climate_effects_iris:
        for node in G.nodes:
            if G.nodes[node]["iri"] == iri:
                nx.set_current_node(G.nodes[node])
                effect = {
                    "effectId": nx.get_node_id(),
                    "sharedScore": 42.00,
                    "effectShortDescription": nx.get_short_description(),
                    "effectTitle": G.nodes[node]["label"],
                    "imageUrl": nx.get_image_url_or_none(),
                    "relatedPersonalValues": map_associated_personal_values(
                        G.nodes[node]["personal_values_10"]
                    ),
                }

                climate_effects.append(effect)

    return climate_effects


def get_personal_values_map():
    """Load the data from the schwartz questions JSON file."""

    try:
        file = os.path.join(
            os.getcwd(), "app/questions/static", "schwartz_questions.json"
        )
        with open(file) as json_file:
            data = load(json_file)
    except FileNotFoundError:
        return jsonify({"error": "Schwartz questions not found"}), 404
    return data


def map_associated_personal_values(personal_values_boolean_list):
    """
    Take the associated personal values for a shared impact and map them to the value names from the schwartz questions JSON file.

    Parameters
    ==========
    - a list of 10 boolean values (0 or 1) taken from the impact's NetworkX node information that indicate whether a climate impact is associated
    with that personal value

    Returns
    ==========
    - a list of personal values associated with a climate impact

    """

    personal_values_map = get_personal_values_map()

    # IDs are hard-coded as temporary solution until known whether we will implement 19 values list and/or change value names displayed to the user.
    json_value_ids = [8, 3, 1, 7, 9, 10, 5, 6, 2, 4]

    value_dict = dict(zip(json_value_ids, personal_values_boolean_list))

    personal_values = []

    for key, val in value_dict.items():
        if val:
            for value in personal_values_map["SetOne"]:
                if key == value["id"]:
                    personal_values.append(value["value"])

    return personal_values


def build_shared_solutions_response(alignment_scores_uuid):
    """
    Deal with database interactions to provide response for GET shared solutions request.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - the id, shared score, short description, title, and image url (if available) for each shared solution
    - user a's first name
    - user b's name
    """

    G = current_app.config["G"].copy()
    nx = network_x_utils()

    (alignment_scores, alignment_feed, userB_name, userA_name) = (
        db.session.query(
            AlignmentScores,
            AlignmentFeed,
            Conversations.receiver_name,
            Users.first_name,
        )
        .join(
            UserBJourney,
            UserBJourney.alignment_scores_uuid == AlignmentScores.alignment_scores_uuid,
        )
        .join(
            AlignmentFeed,
            AlignmentFeed.alignment_feed_uuid == UserBJourney.alignment_feed_uuid,
        )
        .join(
            Conversations,
            Conversations.conversation_uuid == UserBJourney.conversation_uuid,
        )
        .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )

    climate_solutions_iris = [
        alignment_feed.aligned_solution_1_iri,
        alignment_feed.aligned_solution_2_iri,
        alignment_feed.aligned_solution_3_iri,
        alignment_feed.aligned_solution_4_iri,
        alignment_feed.aligned_solution_5_iri,
        alignment_feed.aligned_solution_6_iri,
        alignment_feed.aligned_solution_7_iri,
    ]

    climate_solutions = solution_details(G, climate_solutions_iris, nx)

    response = {
        "climateSolutions": climate_solutions,
        "userAName": userA_name,
        "userBName": userB_name,
    }

    return response


def solution_details(G, climate_solutions_iris, nx):
    """
    Get the full details for each shared climate solution, including id, shared score, description, title, and image (if available).

    Note - shared scores are currently hard-coded as a placeholder until implementation is decided.
    """
    climate_solutions = []

    for iri in climate_solutions_iris:
        for node in G.nodes:
            nx.set_current_node(G.nodes[node])

            if nx.get_node_id() == iri:

                solution = {
                    "solutionId": nx.get_node_id(),
                    "sharedScore": 42.00,
                    "solutionShortDescription": nx.get_short_description(),
                    "solutionTitle": G.nodes[node]["label"],
                    "imageUrl": nx.get_image_url_or_none(),
                }

                climate_solutions.append(solution)

    return climate_solutions


def get_conversation_uuid_using_alignment_scores_uuid(alignment_scores_uuid):
    """
    Fetch the associated conversation uuid from the db using the alignment scores uuid.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    conversation_uuid - (UUID) the unique id for the conversation associated with the alignment scores
    """

    alignment_scores, conversation_uuid = (
        db.session.query(AlignmentScores, UserBJourney.conversation_uuid)
        .join(UserBJourney, UserBJourney.alignment_scores_uuid == alignment_scores_uuid)
        .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
        .one_or_none()
    )

    return conversation_uuid


def log_effect_choice(effect_choice_uuid, effect_iri):
    """
    Adds user b's shared impact selection to the db.

    Parameters
    ==========
    effect_choice_uuid - (UUID) the unique id for the effect choice
    effect_iri - the IRI for the chosen shared impact

    Returns
    ==========
    An error if unsuccessful.
    """

    try:
        effect_choice = EffectChoice()
        effect_choice.effect_choice_uuid = effect_choice_uuid
        effect_choice.effect_choice_1_iri = effect_iri

        db.session.add(effect_choice)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while saving user b's effect choice to the db."
        )


def log_solution_choice(solution_choice_uuid, shared_solutions):
    """
    Adds user b's shared solutions selection to the db.

    Parameters
    ==========
    solution_choice_uuid - (UUID) the unique id for the solution choice
    shared_solutions - a list of dictionaries containing the selected solutions' IRIs, e.g. {"solutionId": "R8WxponQcYpGf2zDnbsuVxG"}

    Returns
    ==========
    An error if unsuccessful.
    """

    try:
        solution_choice = SolutionChoice()
        solution_choice.solution_choice_uuid = solution_choice_uuid
        solution_choice.solution_choice_1_iri = shared_solutions[0]["solutionId"]
        solution_choice.solution_choice_2_iri = shared_solutions[1]["solutionId"]

        db.session.add(solution_choice)
        db.session.commit()
    except:
        raise DatabaseError(
            message="An error occurred while saving user b's solution choice to the db."
        )


def build_shared_impact_details_response(impact_iri):
    """
    Get the detals for a shared impact.
    Includes checks that the IRI is found and of the correct type, e.g. not a solution IRI.
    Parameters
    ==========
    impact_iri - the IRI for the shared impact
    Returns
    ==========
    JSON:
    - the effect title
    - the image url (if available)
    - the long description for the effect
    - the sources for the effect
    - a list of personal values that are related to the effect
    """

    G = current_app.config["G"].copy()
    nx = network_x_utils()
    impact = None

    for node in G.nodes:
        nx.set_current_node(G.nodes[node])

        if nx.get_node_id() == impact_iri:

            if "effect" in G.nodes[node]["all classes"]:
                impact = {
                    "effectTitle": G.nodes[node]["label"],
                    "imageUrl": nx.get_image_url_or_none(),
                    "longDescription": nx.get_description(),
                    "effectSources": nx.get_causal_sources(),
                    "relatedPersonalValues": map_associated_personal_values(
                        G.nodes[node]["personal_values_10"]
                    ),
                }
                break
            else:
                raise InvalidUsageError(message="IRI does not refer to an impact.")

    if not impact:
        raise NotInDatabaseError(message="The shared impact IRI cannot be found.")

    return impact


def build_shared_solution_details_response(solution_iri):
    """
    Gets the details for a shared solution.
    Includes checks that the IRI is found and of the correct type, e.g. not an impact IRI.
    Parameters
    ==========
    solution_iri - the IRI for the shared solution
    Returns
    ==========
    JSON:
    - the solution title
    - the image url (if available)
    - the long description for the solution
    - the sources for the solution
    - the solution type
    """

    G = current_app.config["G"].copy()
    nx = network_x_utils()
    solution = None

    for node in G.nodes:
        nx.set_current_node(G.nodes[node])

        if nx.get_node_id() == solution_iri:

            if "risk solution" in G.nodes[node]["all classes"]:

                solution = {
                    "solutionTitle": G.nodes[node]["label"],
                    "imageUrl": nx.get_image_url_or_none(),
                    "longDescription": nx.get_description(),
                    "solutionSources": nx.get_solution_sources(),
                    "solutionType": nx.check_mitigation_or_adaptation_solution(G),
                }
                break
            else:
                raise InvalidUsageError(message="IRI does not refer to a solution.")

    if not solution:
        raise NotInDatabaseError(message="The shared solution IRI cannot be found.")

    return solution


def build_alignment_summary_response(alignment_scores_uuid):
    """
    Deal with db interaction to get the alignment summary for user b.

    Parameters
    ==========
    alignment_scores_uuid - (UUID) the unique id for the alignment scores

    Returns
    ==========
    JSON:
    - user A's name
    - the top match value
    - the alignment percentage for the top match value
    - the chosen shared impact(s) title
    - the chosen shared solutions' titles
    """

    response = None
    G = current_app.config["G"].copy()
    nx = network_x_utils()

    try:
        (
            top_match_value,
            top_match_percent,
            userA_name,
            user_b_journey,
            conversation,
            effect_choice,
            solution_choice,
        ) = (
            db.session.query(
                AlignmentScores.top_match_value,
                AlignmentScores.top_match_percent,
                Users.first_name,
                UserBJourney,
                Conversations,
                EffectChoice,
                SolutionChoice,
            )
            .join(
                UserBJourney,
                UserBJourney.alignment_scores_uuid
                == AlignmentScores.alignment_scores_uuid,
            )
            .join(
                EffectChoice,
                EffectChoice.effect_choice_uuid == UserBJourney.effect_choice_uuid,
            )
            .join(
                SolutionChoice,
                SolutionChoice.solution_choice_uuid
                == UserBJourney.solution_choice_uuid,
            )
            .join(
                Conversations,
                Conversations.conversation_uuid == UserBJourney.conversation_uuid,
            )
            .join(Users, Users.user_uuid == Conversations.sender_user_uuid)
            .filter(AlignmentScores.alignment_scores_uuid == alignment_scores_uuid)
            .one_or_none()
        )

        chosen_impact_iris = [effect_choice.effect_choice_1_iri]
        chosen_solution_iris = [
            solution_choice.solution_choice_1_iri,
            solution_choice.solution_choice_2_iri,
        ]

        response = {
            "userAName": userA_name,
            "topMatchValue": top_match_value,
            "topMatchPercent": round(top_match_percent),
            "sharedImpacts": [
                nx.get_title_by_iri(iri, G) for iri in chosen_impact_iris
            ],
            "sharedSolutions": [
                nx.get_title_by_iri(iri, G) for iri in chosen_solution_iris
            ],
        }

    except:
        raise DatabaseError(
            message="Something went wrong while retrieving the alignment summary data from the db."
        )

    return response