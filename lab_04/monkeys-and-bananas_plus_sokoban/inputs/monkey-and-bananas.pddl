(define (domain monkey-and-bananas)
    (:requirements :strips :typing :negative-preconditions)

    (:types
        monkey - object
        crate - object
        bananas - object
        position
    )

    (:predicates
        (at ?o - object ?p - position)
        (nextTo ?p1 - position ?p2 - position)
        (straightTriple ?p1 - position ?p2 - position ?p3 - position)
        (empty ?p - position)
        (movable ?c - crate)
        (up ?m - monkey)
        (grabbed ?b - bananas)
    )

    (:action move
        :parameters (?m - monkey ?pFrom - position ?pTo - position)
        :precondition (and
            (not (up ?m))
            (at ?m ?pFrom)
            (empty ?pTo)
            (nextTo ?pFrom ?pTo)
        )
        :effect (and
            (empty ?pFrom)
            (not (empty ?pTo))
            (not (at ?m ?pFrom))
            (at ?m ?pTo)
        )
    )

    (:action pull
        :parameters (?m - monkey ?c - crate ?mPos - position ?cPos - position ?toPos - position)
        :precondition (and
            (movable ?c)
            (not (up ?m))
            (at ?m ?mPos)
            (at ?c ?cPos)
            (nextTo ?mPos ?cPos)
            (nextTo ?mPos ?toPos)
            (straightTriple ?cPos ?mPos ?toPos)
            (empty ?toPos)
        )
        :effect (and
            (not (at ?m ?mPos))
            (at ?m ?toPos)
            (not (at ?c ?cPos))
            (at ?c ?mPos)
            (empty ?cPos)
            (not (empty ?toPos))
        )
    )

    (:action push
        :parameters (?m - monkey ?c - crate ?mPos - position ?cPos - position ?toPos - position)
        :precondition (and
            (movable ?c)
            (not (up ?m))
            (at ?m ?mPos)
            (at ?c ?cPos)
            (nextTo ?mPos ?cPos)
            (nextTo ?cPos ?toPos)
            (straightTriple ?mPos ?cPos ?toPos)
            (empty ?toPos)
        )
        :effect (and
            (not (at ?m ?mPos))
            (at ?m ?cPos)
            (not (at ?c ?cPos))
            (at ?c ?toPos)
            (empty ?mPos)
            (not (empty ?toPos))
        )
    )

    (:action climb
        :parameters (?m - monkey ?c - crate ?mPos - position ?cPos - position)
        :precondition (and
            (at ?m ?mPos)
            (at ?c ?cPos)
            (nextTo ?mPos ?cPos)
        )
        :effect (and
            (not (movable ?c))
            (empty ?mPos)
            (not (at ?m ?mPos))
            (at ?m ?cPos)
            (up ?m)
        )
    )

    (:action grab
        :parameters (?m - monkey ?b - bananas ?pos - position)
        :precondition (and
            (at ?m ?pos)
            (at ?b ?pos)
            (up ?m)
            (not (grabbed ?b))
        )
        :effect (and
            (grabbed ?b)
        )
    )
)