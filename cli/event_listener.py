import click
import sys 
sys.path.append("..") 
from contract import ( Contract, )
from infura import ( Infura, )
from configuration import ( Configuration, )
import asyncio
from pprint import  pprint


def handle_event(event):
    """定义函数来处理事件并打印到控制台"""
    pprint(event)
    print("Contract address: ", event.address)
    print('event.event', event.event)
    print("transactionHash: ", event.transactionHash.hex())


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    """
    异步定义函数循环
    1. 这个循环设置一个事件过滤器, 寻找新的 event
    2. 这个循环在轮询间隔运行
    """
    while True:
        for event_ in event_filter.get_new_entries():
            handle_event(event_)
        await asyncio.sleep(poll_interval)



@click.command()
@click.option('-c', '--contract_address', default='', prompt='Contract address',
              help='Contract address.')
def event_listener(contract_address):
    """
      为最新的区块（latest block）创建一个过滤器，并监听合约的 Transfer 事件是否被触发
      每隔 2s 运行一次 event_filter 函数去监听最新区块里的合约事件
    """
    configuration = Configuration().load_configuration()
    w3 = Infura().get_web3()
    contract_address = w3.toChecksumAddress(contract_address)
    contract = Contract(configuration, contract_address)
    # print('contract.contract', contract.contract)
    # 监听合约里的 mint 函数里 emit 的 Transfer event：
    event_filter = contract.contract.events.Transfer.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        print("[Listening] Transfer event of {} ...".format(contract_address))
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()



if __name__ == "__main__":
    event_listener()