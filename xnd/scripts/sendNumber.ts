import { toNano } from 'ton-core';
import { Counter } from '../wrappers/Counter';
import { NetworkProvider } from '@ton-community/blueprint';
import { OpenedContract } from '@ton/core/dist/contract/openContract';

interface CounterContract extends OpenedContract<Counter> {
    sendNumber: (sender: any, amount: any, value: bigint) => Promise<void>;
}

export async function run(provider: NetworkProvider) {
    const counter = provider.open(Counter.createFromAddress(provider.sender().address));

    await counter.sendNumber(provider.sender(), toNano('0.01'), 123n);
}