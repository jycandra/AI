(define (problem lunar_mission_1)
    (:domain lunar_rover_domain)

    (:objects
        rover1 - rover
        lander1 - lander
        wp1 wp2 wp3 wp4 wp5 - location
        sample1 - sample
        data1 - data
    )

    (:init
        ;; Lander setup
        (lander-at lander1 wp2)
        (belongs-to rover1 lander1)
        (not (deployed rover1))

        ;; Connectivity map (from Figure 2)
        (connected wp1 wp2)
        (connected wp2 wp1)
        (connected wp2 wp3)
        (connected wp3 wp2)
        (connected wp3 wp4)
        (connected wp4 wp3)
        (connected wp4 wp5)
        (connected wp5 wp4)

        ;; Rover starts at lander location, memory empty
        (at rover1 wp2)
        (empty rover1)
    )

    (:goal
        (and
            (image-taken wp5)
            (scan-taken wp3)
            (lander-has-sample lander1)
        )
    )
)
