import behave
import markov as mk

# Given
@given('a list of tweets')
def step_impl(context):
    with open("features/test_tweets.txt", "r") as f:
        content = f.readlines()
        tweets = [x.strip() for x in content]
    context.tweet_list = tweets

# When
@when('we generate a {number:d} of new {length:d} character tweets')
def step_impl(context, number, length):
    data = mk.make_markov_model(context.tweet_list)
    context.new_tweet_list = mk.generate(data, length, number)
    assert (not(None in context.new_tweet_list))

# Then
@then('the {new_number:d} and {new_length:d} of tweets is correct')
def step_impl(context, new_number, new_length):
    assert (len(context.new_tweet_list) == new_number)
    assert (len(max(context.new_tweet_list, key=len)) <= new_length)

