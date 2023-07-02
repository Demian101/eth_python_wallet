import click
import sys 
sys.path.append("..") 
from configuration import Configuration


@click.command()
def list_tokens():
    """List all added tokens."""
    configuration = Configuration().load_configuration()

    tokens = configuration.contracts
    
    click.echo('ETH')
    for token in tokens:
        contract_address = configuration.contracts[token]
        click.echo('%s, address: %s' % (token, contract_address))

if __name__ == '__main__':
    list_tokens()