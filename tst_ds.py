from datasets import Datasets

ds = Datasets({"address": "http://localhost:5000"})
print(ds.info("8b88a424-dbd8-4032-8be7-a930a415b9a5"))