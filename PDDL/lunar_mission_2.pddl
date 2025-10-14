(define (problem lunar_mission_2)
    (:domain lunar_rover_domain)

    (:objects
        rover1 rover2 - rover
        lander1 lander2 - lander
        wp1 wp2 wp3 wp4 wp5 wp6 - location
        sample1 sample2 - sample
        data1 data2 - data
    )

    (:init
        ;; --- Lander and rover setup ---
        (lander-at lander1 wp2)
        (lander-at lander2 wp5)

        (belongs-to rover1 lander1)
        (belongs-to rover2 lander2)

        ;; Rover1 starts deployed at wp2, rover2 undeployed
        (deployed rover1)
        (at rover1 wp2)
        (not (deployed rover2))
        (at rover2 wp5)

        ;; --- Connectivity map (from Figure 3) ---
        (connected wp1 wp2)
        (connected wp2 wp1)
        (connected wp2 wp3)
        (connected wp3 wp2)
        (connected wp3 wp4)
        (connected wp4 wp3)
        (connected wp4 wp5)
        (connected wp5 wp4)
        (connected wp5 wp6)
        (connected wp6 wp5)

        ;; --- Rover memory empty ---
        (empty rover1)
        (empty rover2)
    )

    (:goal
        (and
            (image-taken wp3)
            (scan-taken wp4)
            (image-taken wp2)
            (scan-taken wp6)
            (lander-has-sample lander1)
            (lander-has-sample lander2)
        )
    )
)

