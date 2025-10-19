(define (domain lunar_rover_domain)
    (:requirements :strips :typing)

    
    (:types
        rover
        lander
        location
        sample
    )

    ;; PREDICATES
    ;; =============================
    (:predicates
        ;; --- Position and connectivity ---
        (at ?r - rover ?l - location)               ;; Rover is at a location
        (lander-at ?ld - lander ?l - location)      ;; Lander is fixed at a location
        (connected ?l1 ?l2 - location)              ;; Two locations are connected

        ;; --- Ownership and deployment ---
        (assigned ?r - rover ?ld - lander)          ;; Rover belongs to a lander
        (active ?r - rover)                         ;; Rover has been deployed and is active

        ;; --- Rover memory and data ---
        (holding-data ?r - rover)                   ;; Rover currently holds data (image or scan)
        (data-empty ?r - rover)                     ;; Rover memory is empty (no data)

        ;; --- Sample collection ---
        (holding-sample ?r - rover)                 ;; Rover currently carries a sample
        (stored ?ld - lander)                       ;; Lander has stored a sample

        ;; --- Mission progress ---
        (data-collected ?l - location)              ;; Image or scan has been taken at location
        (data-transmitted ?r - rover)               ;; Rover has transmitted data to lander
    )

    ;; =============================
    ;; ACTIONS
    ;; =============================

    ;; --- 1. Deploy Rover ---
    (:action deploy
        :parameters (?r - rover ?ld - lander ?l - location)
        :precondition (and
            (lander-at ?ld ?l)
            (assigned ?r ?ld)
            (not (active ?r))
        )
        :effect (and
            (active ?r)
            (at ?r ?l)
        )
    )

    ;; --- 2. Move between connected locations ---
    (:action move
        :parameters (?r - rover ?from ?to - location)
        :precondition (and
            (active ?r)
            (at ?r ?from)
            (connected ?from ?to)
        )
        :effect (and
            (not (at ?r ?from))
            (at ?r ?to)
        )
    )

    ;; --- 3. Take Image (or Scan) ---
    (:action collect-data
        :parameters (?r - rover ?l - location)
        :precondition (and
            (active ?r)
            (at ?r ?l)
            (data-empty ?r)
        )
        :effect (and
            (not (data-empty ?r))
            (holding-data ?r)
            (data-collected ?l)
        )
    )

    ;; --- 4. Transmit Data to Lander ---
    (:action transmit-data
        :parameters (?r - rover ?ld - lander ?l - location)
        :precondition (and
            (active ?r)
            (assigned ?r ?ld)
            (lander-at ?ld ?l)
            (at ?r ?l)
            (holding-data ?r)
        )
        :effect (and
            (data-transmitted ?r)
            (not (holding-data ?r))
            (data-empty ?r)
        )
    )

    ;; --- 5. Collect Sample ---
    (:action collect-sample
        :parameters (?r - rover ?l - location ?s - sample)
        :precondition (and
            (active ?r)
            (at ?r ?l)
            (not (holding-sample ?r))
        )
        :effect (and
            (holding-sample ?r)
        )
    )

    ;; --- 6. Store Sample in Lander ---
    (:action store-sample
        :parameters (?r - rover ?ld - lander ?l - location ?s - sample)
        :precondition (and
            (assigned ?r ?ld)
            (lander-at ?ld ?l)
            (at ?r ?l)
            (holding-sample ?r)
            (not (stored ?ld))
        )
        :effect (and
            (not (holding-sample ?r))
            (stored ?ld)
        )
    )
)

