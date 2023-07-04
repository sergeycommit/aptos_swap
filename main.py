import json
import time
from time import sleep
import random

import requests
from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from aptos_sdk.transactions import TransactionArgument, TransactionPayload, TypeTag, EntryFunction, Serializer, \
    StructTag, RawTransaction, SignedTransaction
from aptos_sdk.authenticator import Authenticator, Ed25519Authenticator
from loguru import logger

from tokens import token_address

GAS_LIMIT = 1000
GAS_PRICE = 100

PANCAKESWAP_ADRESS = '0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa'

NODE_URL = "https://fullnode.mainnet.aptoslabs.com/v1"
REST_CLIENT = RestClient(NODE_URL)

def get_price(token_from, token_to):
    response = requests.get(
        f'https://min-api.cryptocompare.com/data/price?fsym={token_from}&tsyms={token_to}').text

    return json.loads(response)[token_to]

def swap_cake(privat_key: str, amount: int, slippage: int, token_from: float, token_to: float) -> None:
        try:
            current_account = Account.load_key(key=privat_key)

        except ValueError:
            logger.error(f'{privat_key} | Невалидный Private Key')
            return

        while True:
            token_from, token_to = token_from.upper(), token_to.upper()
            try:
                account_balance = int(REST_CLIENT.account_balance(account_address=str(current_account.address())))
                gas_price = 54100

                amount_to = int(amount * get_price(token_from, token_to) * slippage)

                if account_balance <= amount + gas_price:
                    logger.info(f'{privat_key} | Маленький баланс: {account_balance / 100000000}')
                    return

                transaction_arguments = [
                        TransactionArgument(amount, Serializer.u64),
                        TransactionArgument(amount_to, Serializer.u64),
                    ]

                payload = EntryFunction.natural(
                        "0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::router::swap_exact_input",
                        "swap_exact_input",
                        [TypeTag(StructTag.from_str(token_address[token_from])),
                         TypeTag(StructTag.from_str(token_address[token_to]))],
                        transaction_arguments,
                    )

                raw_transaction = RawTransaction(
                            current_account.address(),
                            REST_CLIENT.account_sequence_number(current_account.address()),
                            TransactionPayload(payload),
                            GAS_LIMIT,
                            GAS_PRICE,
                            int(time.time()) + 600,
                            chain_id=1,
                        )
                signature = current_account.sign(raw_transaction.keyed())
                authenticator = Authenticator(
                            Ed25519Authenticator(current_account.public_key(), signature)
                        )

                tx_hash = REST_CLIENT.submit_bcs_transaction(SignedTransaction(raw_transaction, authenticator))

                logger.success(f'{privat_key} | https://tracemove.io/transaction/{tx_hash}')

            except Exception as error:
                logger.error(f'{privat_key} | {error}')

                if 'INSUFFICIENT_BALANCE_FOR_TRANSACTION_FEE' in str(error):
                    if account_balance:
                        logger.error(f'{privat_key} | Маленький баланс: {account_balance / 100000000}')

                    else:
                        logger.error(f'{privat_key} | Маленький баланс')

                    return

                elif 'SEQUENCE_NUMBER_TOO_OLD' or '"Transaction already in mempool with a different payload"' in str(error):
                    sleep(1)
                    continue

                elif '{"message":"' in str(error):
                    return

            else:
                return


if __name__ == '__main__':
    token_from = input('Введите токен для обмена: APT, WETH, USDT, USDC, CAKE, BLT: ')
    token_to = input('Введите токен для получения: APT, WETH, USDT, USDC, CAKE, BLT: ')

    random_ = int(input('Введите 1 если диапазон количества токенов, 0 если определенное количество: '))

    if random_:
        from_ = int(float(input('Введите от скольки монет отправить: ')) * 100000000)
        to_ = int(float(input('Введите до скольки монет отправить: ')) * 100000000)
    else:
        amount = int(float(input('Введите сколько монет отправить: ')) * 100000000)

    slippage = 1 - int(input('Введите slippage от 0 до 10: '))/100

    with open('private_keys.txt', 'r', encoding='utf-8-sig') as file:
            private_keys = [row.strip() for row in file]

    logger.info(f'Успешно загружено {len(private_keys)} wallet\'s')

    token_from = token_from.lower()
    token_to = token_to.lower()

    for key in private_keys:
        if random_:
            amount = random.randint(from_, to_)
        swap_cake(key, amount, slippage, token_from, token_to)
        time.sleep(random.randint(5, 20))   ### Рандом задержки времени между кошельками

    logger.info('DONE')