Feature: Markov app library
    This library forms the basis of the Bluto app,
    we want to make sure everything here works as it should

    Scenario Outline: Generating posts
        Given a list of posts
        When we generate a <number> of new <length> character posts
        Then the <new_number> and <new_length> of posts is correct

        Examples: post Number and Length
            | number    | new_number    | length    | new_length    |
            | 5         | 5             | 50        | 50            |
            | 10        | 10            | 100       | 100           |
            | 20        | 20            | 140       | 140           |
            | 50        | 50            | 200       | 200           |
            | 50        | 50            | 280       | 280           |
