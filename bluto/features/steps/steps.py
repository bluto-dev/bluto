import behave
import markov as mk

from pathlib import Path


# Given
@given("a list of posts")
def step_impl(context):
    with Path.open("features/test_posts.txt") as f:
        content = f.readlines()
        posts = [x.strip() for x in content]
    context.post_list = posts


# When
@when("we generate a {number:d} of new {length:d} character posts")
def step_impl(context, number, length):
    context.new_post_list = mk.make_markov_sentences(context.post_list, length, number)
    assert not (None in context.new_post_list)


# Then
@then("the {new_number:d} and {new_length:d} of posts is correct")
def step_impl(context, new_number, new_length):
    assert len(context.new_post_list) == new_number
    assert len(max(context.new_post_list, key=len)) <= new_length
