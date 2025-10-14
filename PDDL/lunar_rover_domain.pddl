(define (domain lunar_rover_domain)
    (:requirements :strips :typing)

    ;; =============================
    ;; TYPES
    ;; =============================
    (:types
        rover
        lander
        location
        sample
        data           ;; represents image or scan data
    )

    ;; =============================
    ;; PREDICATES
    ;; =============================
    (:predicates
        ;; --- Position and connectivity ---
        (at ?r - rover ?l - location)                ;; Rover is at a location
        (lander-at ?ld - lander ?l - location)       ;; Lander is fixed at a location
        (connected ?l1 ?l2 - location)               ;; Two locations are connected

        ;; --- Ownership ---
        (belongs-to ?r - rover ?ld - lander)         ;; Rover belongs to a lander
        (deployed ?r - rover)                        ;; Rover has been deployed

        ;; --- Rover status ---
        (has-sample ?r - rover)                      ;; Rover currently carrying a sample
        (has-data ?r - rover)                        ;; Rover carrying one piece of data
        (empty ?r - rover)                           ;; Rover has free memory (no data)

        ;; --- Lander storage ---
        (lander-has-sample ?ld - lander)             ;; Lander has stored a sample

        ;; --- Data and mission state ---
        (image-taken ?l - location)                  ;; Image taken at this location
        (scan-taken ?l - location)                   ;; Scan done at this location
        (data-transmitted ?r - rover)                ;; Rover has transmitted its data
    )

    ;; =============================
    ;; ACTIONS
    ;; =============================

    ;; --- 1. Deploy Rover ---
    (:action deploy
        :parameters (?r - rover ?ld - lander ?l - location)
        :precondition (and
            (lander-at ?ld ?l)
            (belongs-to ?r ?ld)
            (not (deployed ?r))
        )
        :effect (and
            (deployed ?r)
            (at ?r ?l)
        )
    )

    ;; --- 2. Move between connected locations ---
    (:action move
        :parameters (?r - rover ?from ?to - location)
        :precondition (and
            (deployed ?r)
            (at ?r ?from)
            (connected ?from ?to)
        )
        :effect (and
            (not (at ?r ?from))
            (at ?r ?to)
        )
    )

    ;; --- 3. Take Image ---
    (:action take-image
        :parameters (?r - rover ?l - location)
        :precondition (and
            (deployed ?r)
            (at ?r ?l)
            (empty ?r)
        )
        :effect (and
            (not (empty ?r))
            (has-data ?r)
            (image-taken ?l)
        )
    )

    ;; --- 4. Perform Subsurface Scan ---
    (:action perform-scan
        :parameters (?r - rover ?l - location)
        :precondition (and
            (deployed ?r)
            (at ?r ?l)
            (empty ?r)
        )
        :effect (and
            (not (empty ?r))
            (has-data ?r)
            (scan-taken ?l)
        )
    )

    ;; --- 5. Transmit Data to Lander ---
    (:action transmit-data
        :parameters (?r - rover ?ld - lander ?l - location)
        :precondition (and
            (deployed ?r)
            (belongs-to ?r ?ld)
            (lander-at ?ld ?l)
            (at ?r ?l)
            (has-data ?r)
        )
        :effect (and
            (data-transmitted ?r)
            (not (has-data ?r))
            (empty ?r)
        )
    )

    ;; --- 6. Collect Sample ---
    (:action collect-sample
        :parameters (?r - rover ?l - location ?s - sample)
        :precondition (and
            (deployed ?r)
            (at ?r ?l)
            (not (has-sample ?r))
        )
        :effect (and
            (has-sample ?r)
        )
    )

    ;; --- 7. Store Sample in Lander ---
    (:action store-sample
        :parameters (?r - rover ?ld - lander ?l - location ?s - sample)
        :precondition (and
            (belongs-to ?r ?ld)
            (lander-at ?ld ?l)
            (at ?r ?l)
            (has-sample ?r)
            (not (lander-has-sample ?ld))
        )
        :effect (and
            (not (has-sample ?r))
            (lander-has-sample ?ld)
        )
    )
)
