import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("-m", "--message")
def say_hello(message: str):
    print("Message:", message)


if __name__ == "__main__":
    cli()
