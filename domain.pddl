(define (domain grid)

    (:requirements :strips)


    (:predicates
        (at ?l)
        (adj ?l1 ?l2)
    )

    (:action move
        :parameters (?l1 ?l2)
        :precondition (and (at ?l1) (adj ?l1 ?l2))
        :effect (and (at ?l2) (not (at ?l1)))
    )
    
)
