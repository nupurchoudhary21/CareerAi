from transformers import pipeline

MODEL_NAME = "ihk/skillner"

extractor = pipeline(
    "token-classification",
    model=MODEL_NAME,
    aggregation_strategy="simple"
)

text = """
leslie hindman auctioneer is looking for a full stack ruby rail software developer.
solid knowledge experience ruby rail vue react angular sql rspec git.
"""

results = extractor(text)

print("\nEXTRACTED SKILLS:\n")

for result in results:
    print(
        f"{result['word']} -> "
        f"{result['entity_group']} -> "
        f"{result['score']:.3f}"
    )