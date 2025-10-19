(define (domain lunar_rover_domain2)
    (:requirements 
        :strips 
            :typing
    )

    (:types
        rover
        lander
        location
        sample
    )

    (:predicates 
        (at ?r - rover ?l - location )
        (lander-at ?ld - lander ?l - location )
        (connected ?l1 ?l2 - location )

        (assigned ?r - rover ?ld - lander )
        (active ?r - rover )

        (holding-data ?r - rover )
        (data-empty ?r - rover )

        (holding-sample ?r - rover )
        (stored ?ld - lander )

        (data-collected ?l - location)
        (data-transmitted ?r - rover )
    )

    (:action deploy
        :parameters 
            (?r - rover ?ld - lander ?l - location)
        :precondition 
            (and
                (lander-at ?ld ?l)
                (assigned ?r ?ld)
                (not (active ?r))
            )
        :effect 
            (and
                (active ?r)
                (at ?r ?l)
            )
    )

    (:action move
        :parameters 
            (?r - rover ?from ?to - location)
        :precondition 
            (and
                (active ?r)
                (at ?r ?from)
                (connected ?from ?to)
            )
        :effect 
            (and
                (not (at ?r ?from))
                (at ?r ?to)
            )
    )

    (:action take_image
        :parameters 
            (?r - rover ?l - location)
        :precondition 
            (and
                (active ?r)
                (at ?r ?l)
                (data-empty ?r)
            )
        :effect 
            (and
                (holding-data ?r)
                (data-collected ?l)
                (not (data-empty ?r))
            )
    )

    (:action scan 
        :parameters 
            (?r - rover ?l - location)
        :precondition 
            (and 
                (active ?r)
                (at ?r ?l)
                (data-empty ?r)
            )
        :effect 
            (and
                (holding-data ?r)
                (data-collected ?l)
                (not (data-empty ?r))
            )
    )

    (:action transmit_data
        :parameters 
            (?r - rover ?ld - lander ?l - location)
        :precondition 
            (and
                (active ?r)
                (assigned ?r ?ld)
                (lander-at ?ld ?l)
                (at ?r ?l)
                (holding-data ?r)
            )
        :effect 
            (and
                (data-transmitted ?r)
                (not (holding-data ?r))
                (data-empty ?r)
            )
    )

    (:action collect_sample
        :parameters 
            (?r - rover ?l - location ?s - sample)
        :precondition 
            (and 
                (active ?r)
                (at ?r ?l)
                (not (holding-sample ?r))
            )
        :effect 
            (and 
                (holding-sample ?r)
            )
    )

    (:action store_sample
        :parameters 
            (?r - rover ?ld - lander ?l - location ?s - sample)
        :precondition 
            (and
                (assigned ?r ?ld)
                (lander-at ?ld ?l)
                (at ?r ?l)
                (holding-sample ?r)
                (not (stored ?ld))
            )
        :effect 
            (and
                (not (holding-sample ?r))
                (stored ?ld)
            )
    )        
            
)
    

