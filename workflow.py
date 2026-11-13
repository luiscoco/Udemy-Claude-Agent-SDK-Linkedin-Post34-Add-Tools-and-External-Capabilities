"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

def lookup(arguments):
    if arguments['sku'] != 'BOOK-02':
        raise ValueError('Unknown SKU')
    return {'sku': 'BOOK-02', 'units': 7, 'source': 'local inventory fixture'}


async def run(agent, data):
    observed = lookup({'sku': data['sku']})
    options = in_process_tool('stock', 'Look up exact SKU stock.', {'sku': str}, lookup) if agent.live else None
    findings = await agent.ask('inventory_researcher', 'Use stock to obtain the inventory observation.', {'sku': data['sku']}, observed, sdk=options)
    answer = await agent.ask('writer', 'Explain only this checked observation. Do not invent a delivery date.', findings, 'BOOK-02 has 7 units in the fixture. Delivery availability is unknown.')
    return {'observation': observed, 'findings': findings, 'answer': answer}
