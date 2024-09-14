from web3 import Web3


class BlockchainNode:
    def __init__(self, blockchain: str):
        self.blockchain = blockchain.lower()
        self.node_url = self.get_node_url()

    def get_node_url(self):
        """Возвращает URL адрес узла в зависимости от переданного блокчейна"""
        match self.blockchain:
            case "ethereum":
                # return "wss://ethereum-rpc.publicnode.com" - основная
                return "wss://ethereum-sepolia-rpc.publicnode.com"
            case "arbitrum":
                return "https://arbitrum-sepolia.blockpi.network/v1/rpc/public"
                # https://arb-mainnet-public.unifra.io - основная
            case "optimism":
                return "wss://optimism-rpc.publicnode.com"
            case _:
                raise ValueError("Unsupported blockchain")

    def get_web3_instance(self):
        return Web3(Web3.HTTPProvider(self.node_url))
