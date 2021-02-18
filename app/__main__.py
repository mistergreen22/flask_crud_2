from argparse import ArgumentParser

from app import app


def main():
    parser = ArgumentParser(prog='python -m app')
    parser.add_argument('-p', '--port', dest='port', type=int, default=5000)

    args = parser.parse_args()
    app.run(port=args.port)


if __name__ == '__main__':
    main()
