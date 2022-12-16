import argparse
import logging

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--origin', type=str, required=True, help='Origin video path')
parser.add_argument('--destin', type=str, required=True, help='Proceeded video path')
parser.add_argument('--start', type=int, required=True, help='Start frame index')
parser.add_argument('--end', type=int, required=True, help='End frame index')
args = parser.parse_args()
logging.info({
    '--origin': args.origin,
    '--destin': args.destin,
    '--start': args.start,
    '--end': args.end,
})
print(f"{123},{456}")
