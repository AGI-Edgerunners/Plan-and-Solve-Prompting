import time

import openai


def decoder_for_gpt3(args, input, max_length, apikey):
    # openai.api_key = apikey
    engine = args.engine
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    temperature = 0.7 if args.SC and max_length != 32 else 0.0
    n = 10 if args.SC and max_length != 32 else 1
    stop = ["\n\n"] if max_length == 32 else None

    response = openai.Completion.create(
        engine=engine,
        prompt=input,
        max_tokens=max_length,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        n=n,
        stop=stop,
        api_key=apikey
    )
    if max_length == 32 or not args.SC:
        return response["choices"][0]['text']
    elif max_length != 32 and args.SC:
        text = response["choices"]
        tem_rational = []
        for i in range(len(text)):
            tem_rational.append(text[i]['text'])
        return tem_rational
    elif args.engine == 'code-davinci-002':
        raise NotImplementedError('implement the code when running gpt3 engine: {}'.format(args.engine))
    else:
        raise NotImplementedError('implement the code when running gpt3 engine: {}'.format(args.engine))


def basic_runner(args, inputs, max_length, apikey, max_retry=3):
    retry = 0
    get_result = False
    pred = [] if args.SC else ''
    error_msg = ''
    while not get_result:
        try:
            pred = decoder_for_gpt3(args, inputs, max_length, apikey)
            get_result = True
        except openai.error.RateLimitError as e:
            if e.user_message == 'You exceeded your current quota, please check your plan and billing details.':
                raise e
            elif retry < max_retry:
                time.sleep(args.api_time_interval)
                retry += 1
            else:
                error_msg = e.user_message
                break
        except Exception as e:
            raise e
    return get_result, pred, error_msg
