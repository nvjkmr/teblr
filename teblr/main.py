import teblr
import helpers

def main():
    teblr.client = helpers.create_client()
    args = helpers.args_parser()
    args.func(args)
